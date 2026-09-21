from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class PushMessage:
    user_id: int
    title: str
    body: str
    event: str
    created_at: datetime

def make_push(user_id: int, title: str, body: str, event: str) -> PushMessage:
    return PushMessage(user_id, title, body, event, datetime.now(timezone.utc))
