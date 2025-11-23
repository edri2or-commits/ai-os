"""AI-OS – Orchestration-Lite Layer (OLL-Core)
Version: 0.1 (Prototype)
Date: 24 November 2025
Author: AI-OS Build Commander (גיטהאב)

תיאור:
זהו אבטיפוס ראשוני של Event Bus אסינכרוני המשמש כליבה של שכבת OLL.
מטרתו לאפשר זרימת אירועים פשוטה ובטוחה בין סוכנים, תהליכים וכלים במערכת.
"""

import asyncio
import datetime
from typing import Callable, Dict, List, Any


class OLLCore:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Any], Any]]] = {}
        self.audit_log: List[Dict[str, Any]] = []
        self.lock = asyncio.Lock()

    async def subscribe(self, event_type: str, handler: Callable[[Any], Any]):
        async with self.lock:
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            self.subscribers[event_type].append(handler)
            await self._log("SUBSCRIBE", {"event_type": event_type, "handler": handler.__name__})

    async def publish(self, event_type: str, data: Any):
        handlers = self.subscribers.get(event_type, [])
        if not handlers:
            await self._log("NO_HANDLERS", {"event_type": event_type, "data": data})
            return

        for handler in handlers:
            try:
                await handler(data)
                await self._log("EVENT_DISPATCHED", {"event_type": event_type, "handler": handler.__name__})
            except Exception as e:
                await self._log("ERROR", {"event_type": event_type, "handler": handler.__name__, "error": str(e)})

    async def _log(self, action: str, details: Dict[str, Any]):
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "action": action,
            "details": details
        }
        self.audit_log.append(entry)
        print(f"[OLL-AUDIT] {action}: {details}")

    async def get_audit_log(self) -> List[Dict[str, Any]]:
        return self.audit_log


# דוגמת שימוש
async def example():
    oll = OLLCore()

    async def on_plan_generated(event_data):
        print(f"[HANDLER] קיבלתי אירוע: {event_data}")

    await oll.subscribe("plan_generated", on_plan_generated)
    await oll.publish("plan_generated", {"plan_id": "123", "agent": "GPT_GitHub_Agent"})


if __name__ == "__main__":
    asyncio.run(example())
