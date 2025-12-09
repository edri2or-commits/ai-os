"""
H3 Telegram Approval Bot - Backend Service
HEADLESS_MIGRATION_ROADMAP aligned implementation

Watches: truth-layer/drift/approvals/pending/ for new CRs
Sends: Telegram notifications with inline buttons
Processes: User approvals/rejections
Writes: Approval files for Executor
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
import yaml

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv(project_root / ".env")

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
import aiosqlite

# ============================================================================
# Configuration
# ============================================================================

APPROVALS_DIR = project_root / "truth-layer" / "drift" / "approvals"
PENDING_DIR = APPROVALS_DIR / "pending"
APPROVED_DIR = APPROVALS_DIR / "approved"
REJECTED_DIR = APPROVALS_DIR / "rejected"

# Create directories
for d in [PENDING_DIR, APPROVED_DIR, REJECTED_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Telegram config
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))

if not TOKEN or not CHAT_ID:
    print("❌ Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env")
    sys.exit(1)

print(f"✅ Telegram configured: {TOKEN[:10]}...{TOKEN[-4:]}")
print(f"✅ Chat ID: {CHAT_ID}")

# SQLite database
DB_PATH = project_root / "services" / "approval-bot" / "approvals.db"

# ============================================================================
# Database
# ============================================================================

async def init_db():
    """Initialize SQLite database"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS approvals (
                cr_id TEXT PRIMARY KEY,
                type TEXT,
                risk TEXT,
                proposal TEXT,
                status TEXT,
                created_at TEXT,
                updated_at TEXT,
                telegram_message_id INTEGER
            )
        """)
        await db.commit()
    print("✅ Database initialized")

# ============================================================================
# File Watcher
# ============================================================================

class CRWatcher(FileSystemEventHandler):
    """Watches pending/ directory for new CRs"""
    
    def __init__(self, loop):
        self.loop = loop
        super().__init__()
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        if not event.src_path.endswith('.yaml') and not event.src_path.endswith('.yml'):
            return
        
        cr_file = Path(event.src_path)
        print(f"\n📄 New CR detected: {cr_file.name}")
        
        # Schedule async task
        asyncio.run_coroutine_threadsafe(
            send_approval_request(cr_file),
            self.loop
        )

# ============================================================================
# Telegram Integration
# ============================================================================

async def send_approval_request(cr_file: Path):
    """Send CR to Telegram with approval buttons"""
    
    try:
        # Read CR
        with open(cr_file, 'r', encoding='utf-8') as f:
            cr_data = yaml.safe_load(f)
        
        if not cr_data:
            print(f"⚠️ Empty CR file: {cr_file.name}")
            return
        
        cr_id = cr_file.stem  # e.g., "CR_2025-12-06_001"
        
        # Store in SQLite
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                INSERT OR REPLACE INTO approvals 
                (cr_id, type, risk, proposal, status, created_at)
                VALUES (?, ?, ?, ?, 'PENDING', ?)
            """, (
                cr_id,
                cr_data.get('type', 'UNKNOWN'),
                cr_data.get('risk', 'medium'),
                json.dumps(cr_data.get('proposal', [])),
                datetime.utcnow().isoformat()
            ))
            await db.commit()
        
        # Build Telegram message
        proposal_list = cr_data.get('proposal', [])
        if isinstance(proposal_list, list) and len(proposal_list) > 0:
            proposal_summary = "\n".join([
                f"- {item.get('op', 'unknown')}: {item.get('description', 'N/A')}"
                for item in proposal_list[:3]
            ])
            if len(proposal_list) > 3:
                proposal_summary += f"\n... +{len(proposal_list) - 3} more"
        else:
            proposal_summary = json.dumps(proposal_list, indent=2)[:300]
        
        message = f"""🔔 <b>Change Request Approval</b>

<b>ID:</b> <code>{cr_id}</code>
<b>Type:</b> {cr_data.get('type', 'UNKNOWN')}
<b>Risk:</b> {cr_data.get('risk', 'medium')}

<b>Proposal:</b>
{proposal_summary}
"""
        
        # Inline keyboard
        keyboard = [
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve:{cr_id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject:{cr_id}")
            ],
            [InlineKeyboardButton("📄 View Full", callback_data=f"diff:{cr_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send
        bot = Bot(token=TOKEN)
        msg = await bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        
        # Save message ID
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE approvals SET telegram_message_id = ? WHERE cr_id = ?",
                (msg.message_id, cr_id)
            )
            await db.commit()
        
        print(f"✅ Sent to Telegram: {cr_id}")
    
    except Exception as e:
        print(f"❌ Error sending approval request: {e}")
        import traceback
        traceback.print_exc()

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    if not query.data or ':' not in query.data:
        await query.edit_message_text("❌ Invalid callback data")
        return
    
    action, cr_id = query.data.split(":", 1)
    
    print(f"\n🔘 Callback: {action} for {cr_id}")
    
    if action == "approve":
        # Update DB
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE approvals SET status = 'APPROVED', updated_at = ? WHERE cr_id = ?",
                (datetime.utcnow().isoformat(), cr_id)
            )
            await db.commit()
        
        # Write approval file (triggers Executor)
        approval_file = APPROVED_DIR / f"{cr_id}_APPROVED.json"
        approval_file.write_text(json.dumps({
            "status": "approved",
            "timestamp": datetime.utcnow().isoformat(),
            "approved_by": f"telegram_user_{update.effective_user.id}"
        }, indent=2), encoding='utf-8')
        
        print(f"✅ Approval written: {approval_file}")
        
        # Update Telegram message
        await query.edit_message_text(
            text=query.message.text + "\n\n✅ **Approved!** Executor will process this CR.",
            parse_mode='Markdown'
        )
    
    elif action == "reject":
        # Update DB
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE approvals SET status = 'REJECTED', updated_at = ? WHERE cr_id = ?",
                (datetime.utcnow().isoformat(), cr_id)
            )
            await db.commit()
        
        # Write rejection file
        rejection_file = REJECTED_DIR / f"{cr_id}_REJECTED.json"
        rejection_file.write_text(json.dumps({
            "status": "rejected",
            "timestamp": datetime.utcnow().isoformat(),
            "rejected_by": f"telegram_user_{update.effective_user.id}"
        }, indent=2), encoding='utf-8')
        
        print(f"❌ Rejection written: {rejection_file}")
        
        # Update Telegram message
        await query.edit_message_text(
            text=query.message.text + "\n\n❌ **Rejected**",
            parse_mode='Markdown'
        )
    
    elif action == "diff":
        # Fetch full proposal from DB
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT proposal FROM approvals WHERE cr_id = ?",
                (cr_id,)
            ) as cursor:
                row = await cursor.fetchone()
        
        if row:
            proposal = json.loads(row[0])
            diff_text = "**Full Proposal:**\n```json\n" + json.dumps(proposal, indent=2)[:4000] + "\n```"
            await context.bot.send_message(
                chat_id=CHAT_ID,
                text=diff_text,
                parse_mode='Markdown'
            )
        else:
            await context.bot.send_message(
                chat_id=CHAT_ID,
                text=f"❌ CR not found: {cr_id}"
            )

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "🤖 **AI Life OS Approval Bot**\n\n"
        "I'll send you Change Requests for approval.\n"
        "Click the buttons to approve or reject.\n\n"
        f"Your Chat ID: `{update.effective_chat.id}`",
        parse_mode='Markdown'
    )

# ============================================================================
# Main
# ============================================================================

async def main():
    """Start the approval bot"""
    
    print("=" * 70)
    print("H3 Telegram Approval Bot - Starting")
    print("=" * 70)
    print()
    
    # Initialize database
    await init_db()
    
    # Start file watcher
    loop = asyncio.get_event_loop()
    event_handler = CRWatcher(loop)
    observer = Observer()
    observer.schedule(event_handler, str(PENDING_DIR), recursive=False)
    observer.start()
    print(f"👁️ Watching: {PENDING_DIR}")
    
    # Start Telegram bot
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    print("\n" + "=" * 70)
    print("✅ Approval Bot Running!")
    print("=" * 70)
    print(f"\n📁 Watching: {PENDING_DIR}")
    print(f"📱 Telegram: @YourBot (Chat ID: {CHAT_ID})")
    print(f"💾 Database: {DB_PATH}")
    print("\n⏸️  Press CTRL+C to stop")
    print("=" * 70)
    print()
    
    # Run bot (blocking)
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping...")
        observer.stop()
        observer.join()
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        print("✅ Stopped")

if __name__ == "__main__":
    asyncio.run(main())
