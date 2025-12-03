"""
SYSTEM_BOOK.md Auto-Sync
========================

Automatically updates SYSTEM_BOOK.md from 01-active-context.md
Triggered by Protocol 1 after every slice

Updates:
1. Section 1: Quick Context Injection -> Current State
2. Section 6: System State (Live) -> Phase Status + Recent Achievement

Research Support:
- Living Documentation (Martraire 2024): "Low effort" = automation
- Documentation as Code (DevOps 2024): CI/CD auto-deployment
- Anthropic + Mintlify (2025): Auto-generation standard

Source: memory-bank/protocols/protocol_1_v2.py
"""

import re
from pathlib import Path
from datetime import datetime

# Paths
ROOT = Path(__file__).parent.parent
ACTIVE_CONTEXT = ROOT / "memory-bank/01-active-context.md"
SYSTEM_BOOK = ROOT / "SYSTEM_BOOK.md"

def extract_progress(active_context_text: str) -> str:
    """Extract progress % from 01-active-context.md"""
    # Match: "**Progress:** ~90% complete"
    match = re.search(r'\*\*Progress:\*\*\s*~?(\d+)%', active_context_text)
    if match:
        return match.group(1)
    return "85"  # Fallback

def extract_phase(active_context_text: str) -> str:
    """Extract phase name from 01-active-context.md"""
    # Match: "**Phase:** Phase 1 – Infrastructure Deployment"
    match = re.search(r'\*\*Phase:\*\*\s*(.+?)🚀', active_context_text)
    if match:
        return match.group(1).strip()
    return "Phase 1 - Infrastructure Deployment"  # Fallback

def extract_recent_achievement(active_context_text: str) -> str:
    """
    Extract title + date from most recent Recent Changes entry
    
    More robust than Just Finished because:
    - Structured format (Date | Title)
    - Single source of truth (Recent Changes = official record)
    - Timestamp makes it clear this is the latest
    - Works with multi-line descriptions
    
    Pattern: "**2025-12-04 | Pre-commit Hook - Zero-Drift Safety Net** ✅"
    Returns: "Pre-commit Hook - Zero-Drift Safety Net (2025-12-04)"
    """
    # Match most recent entry in Recent Changes
    match = re.search(
        r'\*\*(\d{4}-\d{2}-\d{2}) \| (.+?)\*\* ✅', 
        active_context_text
    )
    if match:
        date = match.group(1)
        title = match.group(2).strip()
        return f"{title} ({date})"
    
    # Fallback to Just Finished if Recent Changes not found
    fallback_match = re.search(
        r'\*\*Just Finished:\*\*.*?- ✅ (.+?)(?:\n|$)', 
        active_context_text, 
        re.DOTALL
    )
    if fallback_match:
        return fallback_match.group(1).strip()
    
    return "Recent system updates"  # Ultimate fallback

def update_system_book():
    """Main sync function"""
    
    # 1. Read source data
    active_text = ACTIVE_CONTEXT.read_text(encoding='utf-8')
    system_book_text = SYSTEM_BOOK.read_text(encoding='utf-8')
    
    progress = extract_progress(active_text)
    phase_name = extract_phase(active_text)
    recent_achievement = extract_recent_achievement(active_text)
    
    print(f"[INFO] Extracted from 01-active-context.md:")
    print(f"   Progress: {progress}%")
    print(f"   Phase: {phase_name}")
    print(f"   Recent: {recent_achievement[:60]}...")
    
    # 2. Update Section 1: Quick Context Injection -> Current State
    # Pattern: "- **Phase:** 1 - Infrastructure Deployment (85% complete)"
    system_book_text = re.sub(
        r'(- \*\*Phase:\*\*).+?(\()\d+%(.*?complete\))',
        rf'\1 {phase_name} \g<2>{progress}%\3',
        system_book_text
    )
    
    # 3. Update Section 6: Current Phase Status -> Progress
    # Pattern: "- Progress: ~85% complete"
    system_book_text = re.sub(
        r'(- Progress:)\s*~?\d+%\s*(complete)',
        rf'\1 ~{progress}% \2',
        system_book_text
    )
    
    # 4. Update Section 6: Recent Achievement
    # Pattern: "**Recent Achievement:**" followed by description
    # Replace entire section until next "---"
    achievement_block = f"""**Recent Achievement:**
{recent_achievement}

(Auto-synced from 01-active-context.md via sync_system_book.py)"""
    
    system_book_text = re.sub(
        r'\*\*Recent Achievement:\*\*.*?(?=\n---)',
        achievement_block + '\n',
        system_book_text,
        flags=re.DOTALL
    )
    
    # 5. Write updated file
    SYSTEM_BOOK.write_text(system_book_text, encoding='utf-8')
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[SUCCESS] SYSTEM_BOOK.md updated ({timestamp})")
    print(f"   Phase: {phase_name} ({progress}%)")
    print(f"   Recent: {recent_achievement[:50]}...")

if __name__ == "__main__":
    try:
        update_system_book()
    except Exception as e:
        print(f"[ERROR] Error syncing SYSTEM_BOOK.md: {e}")
        raise
