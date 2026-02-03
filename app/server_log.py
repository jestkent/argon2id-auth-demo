from collections import deque
from datetime import datetime, timezone

# Keep last 50 events in memory (demo only)
EVENTS = deque(maxlen=50)

def add_event(event: dict) -> None:
    event["ts"] = datetime.now(timezone.utc).isoformat()
    EVENTS.appendleft(event)

def get_events():
    return list(EVENTS)
