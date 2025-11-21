"""
Chat1 - Telegram Bot for AI-OS

Connects Telegram users to Agent Gateway API.
Implements full Human-in-the-Loop workflow with approval buttons.

Usage:
    python chat/telegram_bot.py
    
Or via start.py (automatic if TELEGRAM_BOT_TOKEN is set)
"""

import sys
import os
from pathlib import Path

# Fix encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stdin = codecs.getreader('utf-8')(sys.stdin.buffer, 'strict')

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv(project_root / ".env")

# Get token
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ TELEGRAM_BOT_TOKEN not found in .env")
    print("\n💡 Steps:")
    print("   1. Talk to @BotFather on Telegram")
    print("   2. Create bot with /newbot")
    print("   3. Add token to SSOT (.env.local)")
    print("   4. Run: python sync_api_key.py")
    sys.exit(1)

print("=" * 70)
print("Chat1 - Telegram Bot for AI-OS")
print("=" * 70)
print(f"\n🤖 Bot Token: {BOT_TOKEN[:10]}...{BOT_TOKEN[-4:]}")

# Check if library is installed
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application,
        CommandHandler,
        MessageHandler,
        CallbackQueryHandler,
        ContextTypes,
        filters
    )
    print("✅ python-telegram-bot library loaded")
except ImportError:
    print("\n❌ python-telegram-bot not installed")
    print("\n💡 Installing...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "python-telegram-bot", "--break-system-packages"], check=True)
    print("✅ Installed! Restarting bot...")
    
    # Re-import
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application,
        CommandHandler,
        MessageHandler,
        CallbackQueryHandler,
        ContextTypes,
        filters
    )

# Import Agent Gateway
from ai_core.agent_gateway import plan_and_optionally_execute

print("✅ Agent Gateway loaded")

# Store pending plans per user
pending_plans = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message"""
    await update.message.reply_text(
        "👋 שלום! אני Chat1 - העוזר החכם של AI-OS.\n\n"
        "📝 **איך אני עובד:**\n"
        "1. תכתוב לי מה אתה רוצה לעשות (בשפה טבעית)\n"
        "2. אני אכין תוכנית מפורטת\n"
        "3. תאשר את התוכנית\n"
        "4. אני אבצע הכל אוטומטית!\n\n"
        "💡 **דוגמאות:**\n"
        "• צור קובץ README חדש\n"
        "• עדכן את התיעוד\n"
        "• הוסף בדיקת בריאות למערכת\n\n"
        "🔒 **בטיחות:** כל פעולה דורשת את האישור שלך!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages (intents)"""
    user_intent = update.message.text
    user_id = update.effective_user.id
    
    print(f"\n📨 Intent from user {user_id}: {user_intent[:50]}...")
    
    # Send processing message
    processing_msg = await update.message.reply_text(
        "⏳ **מעבד את הכוונה שלך...**\n"
        "🧠 GPT Planner בעבודה..."
    )
    
    try:
        # Call Agent Gateway (plan only, no execution)
        result = plan_and_optionally_execute(
            intent=user_intent,
            auto_execute=False,  # Always plan first!
            dry_run=False
        )
        
        status = result.get('status')
        
        if status == 'success':
            plan = result.get('plan', {})
            summary = plan.get('summary', '')
            steps = plan.get('steps', [])
            actions = plan.get('actions_for_claude', [])
            
            # Format response
            response = f"✅ **תוכנית מוכנה!**\n\n"
            response += f"📋 **סיכום:**\n{summary}\n\n"
            
            if steps:
                response += f"🔢 **שלבים ({len(steps)}):**\n"
                for i, step in enumerate(steps[:5], 1):  # Limit to 5 steps
                    response += f"{i}. {step}\n"
                if len(steps) > 5:
                    response += f"... ועוד {len(steps) - 5} שלבים\n"
                response += "\n"
            
            if actions:
                response += f"⚙️ **פעולות ({len(actions)}):**\n"
                for i, action in enumerate(actions[:3], 1):  # Limit to 3 actions
                    action_type = action.get('type', 'unknown')
                    action_desc = action.get('description', '')
                    response += f"{i}. {action_type}: {action_desc[:40]}...\n"
                if len(actions) > 3:
                    response += f"... ועוד {len(actions) - 3} פעולות\n"
            
            # Store plan for execution
            pending_plans[user_id] = {
                'intent': user_intent,
                'result': result
            }
            
            # Create approval buttons
            keyboard = [
                [
                    InlineKeyboardButton("✅ הרץ תוכנית זו", callback_data=f"execute_{user_id}"),
                    InlineKeyboardButton("❌ בטל", callback_data=f"cancel_{user_id}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Delete processing message
            await processing_msg.delete()
            
            # Send plan with buttons
            await update.message.reply_text(
                response,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            print(f"✅ Plan sent to user {user_id}, awaiting approval")
        
        elif status == 'planning_failed':
            error_msg = result.get('error', 'Unknown error')
            
            await processing_msg.edit_text(
                f"❌ **תכנון נכשל**\n\n"
                f"שגיאה: {error_msg}\n\n"
                f"💡 נסה לנסח את הכוונה בצורה ברורה יותר."
            )
            
            print(f"❌ Planning failed for user {user_id}: {error_msg}")
        
        else:
            await processing_msg.edit_text(
                f"⚠️ **סטטוס לא צפוי**: {status}\n\n"
                f"נסה שוב מאוחר יותר."
            )
            
            print(f"⚠️ Unexpected status for user {user_id}: {status}")
    
    except Exception as e:
        await processing_msg.edit_text(
            f"❌ **שגיאה**\n\n"
            f"משהו השתבש: {str(e)}\n\n"
            f"פנה לאדמין אם הבעיה חוזרת."
        )
        
        print(f"❌ Error for user {user_id}: {e}")
        import traceback
        traceback.print_exc()

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = update.effective_user.id
    
    if data.startswith('execute_'):
        # Execute approved plan
        print(f"\n✅ User {user_id} approved execution")
        
        if user_id not in pending_plans:
            await query.edit_message_text(
                "❌ **התוכנית לא נמצאה**\n\n"
                "אולי עבר יותר מדי זמן. נסה שוב."
            )
            return
        
        pending = pending_plans[user_id]
        intent = pending['intent']
        
        await query.edit_message_text(
            "⚙️ **מבצע תוכנית...**\n"
            "זה עשוי לקחת כמה שניות.\n\n"
            "📊 עדכונים בהמשך..."
        )
        
        try:
            # Execute!
            result = plan_and_optionally_execute(
                intent=intent,
                auto_execute=True,  # Execute now!
                dry_run=False
            )
            
            execution = result.get('execution', {})
            summary = execution.get('summary', {})
            
            executed = summary.get('executed', 0)
            pending_count = summary.get('pending', 0)
            errors = summary.get('errors', 0)
            
            # Format result
            response = f"✅ **ביצוע הושלם!**\n\n"
            response += f"📊 **סיכום:**\n"
            response += f"• בוצעו: {executed} פעולות\n"
            
            if pending_count > 0:
                response += f"• ממתינות: {pending_count} פעולות\n"
            
            if errors > 0:
                response += f"• ❌ שגיאות: {errors}\n"
            
            # Check for git operations
            actions_taken = execution.get('actions_taken', [])
            git_commits = [a for a in actions_taken if a.get('type') == 'git.commit']
            
            if git_commits:
                response += f"\n🔄 **Git:**\n"
                for commit in git_commits[:2]:
                    message = commit.get('params', {}).get('message', '')
                    response += f"• {message}\n"
            
            response += f"\n✅ **סיימתי!**"
            
            await query.edit_message_text(response)
            
            # Clear pending plan
            del pending_plans[user_id]
            
            print(f"✅ Execution complete for user {user_id}")
        
        except Exception as e:
            await query.edit_message_text(
                f"❌ **ביצוע נכשל**\n\n"
                f"שגיאה: {str(e)}\n\n"
                f"פנה לאדמין."
            )
            
            print(f"❌ Execution error for user {user_id}: {e}")
    
    elif data.startswith('cancel_'):
        # Cancel plan
        print(f"\n❌ User {user_id} cancelled plan")
        
        if user_id in pending_plans:
            del pending_plans[user_id]
        
        await query.edit_message_text(
            "❌ **תוכנית בוטלה**\n\n"
            "שלח כוונה חדשה מתי שתרצה!"
        )

def main():
    """Start the bot"""
    print("\n🚀 Starting bot...")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    print("✅ Bot handlers registered")
    print("\n" + "=" * 70)
    print("🤖 Chat1 is running!")
    print("=" * 70)
    print("\n💡 Send /start to your bot on Telegram to begin")
    print("⏸️  Press CTRL+C to stop")
    print("\n" + "=" * 70)
    print()
    
    # Start polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
