from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class Notification:
    user_id: int
    title: str
    body: str
    event: str
    created_at: datetime

def build_notification(user_id, title, body, event):
    return Notification(user_id, title, body, event, datetime.now(timezone.utc))
