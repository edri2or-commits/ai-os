"""AI-OS – OLL-Audit Layer
Version: 0.1
Date: 24 November 2025
Author: AI-OS Build Commander (גיטהאב)

תיאור:
שכבת ה-Audit המרכזית של מערכת ה-Orchestration-Lite (OLL).
רכיב זה מנהל לוג מערכת מאוחד בפורמט JSONL, כדי לאפשר מעקב אחרי כל פעולה, אישור ואירוע במערכת.
"""

import asyncio
import json
import datetime
from pathlib import Path
from typing import Dict, Any


class OLLAudit:
    def __init__(self, log_dir: str = "logs", log_file: str = "OLL_AUDIT.jsonl"):
        self.log_path = Path(log_dir)
        self.log_path.mkdir(parents=True, exist_ok=True)
        self.file_path = self.log_path / log_file
        self.lock = asyncio.Lock()

    async def record(self, event_type: str, details: Dict[str, Any]):
        async with self.lock:
            entry = {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "event_type": event_type,
                "details": details
            }
            async with await asyncio.to_thread(open, self.file_path, "a", encoding="utf-8") as f:
                await asyncio.to_thread(f.write, json.dumps(entry, ensure_ascii=False) + "\n")
            print(f"[OLL-AUDIT] {event_type}: {details}")

    async def read_all(self):
        if not self.file_path.exists():
            return []
        async with self.lock:
            content = await asyncio.to_thread(self.file_path.read_text, encoding="utf-8")
            return [json.loads(line) for line in content.splitlines() if line.strip()]


# דוגמת שימוש
async def example_usage():
    audit = OLLAudit()
    await audit.record("TEST_EVENT", {"info": "נבדק בהצלחה"})
    entries = await audit.read_all()
    print(f"נמצאו {len(entries)} רשומות בלוג.")


if __name__ == "__main__":
    asyncio.run(example_usage())
