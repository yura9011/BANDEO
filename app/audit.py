import json
from datetime import date, datetime
from typing import Any, Optional

from sqlmodel import Session

from app.models.user import AuditLog, Event, Post, Profile, User

SENSITIVE_FIELDS = {"edit_token"}

def _json_ready(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    return value

def _model_data(record: Any) -> dict[str, Any]:
    if hasattr(record, "model_dump"):
        data = record.model_dump()
    else:
        data = record.dict()
    return {key: _json_ready(value) for key, value in data.items() if key not in SENSITIVE_FIELDS}

def snapshot_user_profile(user: User, profile: Optional[Profile]) -> dict[str, Any]:
    return {
        "user": _model_data(user),
        "profile": _model_data(profile) if profile else None,
    }

def snapshot_user_full(session: Session, user: User) -> dict[str, Any]:
    profile = session.exec(select_profile(user.id)).first()
    posts = session.exec(select_posts(user.id)).all()
    events = session.exec(select_events(user.id)).all()
    return {
        "user": _model_data(user),
        "profile": _model_data(profile) if profile else None,
        "posts": [_model_data(post) for post in posts],
        "events": [_model_data(event) for event in events],
    }

def snapshot_entity(session: Session, entity_type: str, record: Any) -> Optional[dict[str, Any]]:
    if record is None:
        return None
    if entity_type == "user":
        return snapshot_user_full(session, record)
    return _model_data(record)

def add_audit_log(
    session: Session,
    *,
    action: str,
    entity_type: str,
    entity_id: Optional[int],
    actor_type: str,
    actor_user_id: Optional[int] = None,
    before: Any = None,
    after: Any = None,
) -> None:
    session.add(AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        actor_type=actor_type,
        actor_user_id=actor_user_id,
        before_data=_dump_snapshot(before),
        after_data=_dump_snapshot(after),
    ))

def audit_display_rows(logs: list[AuditLog]) -> list[dict[str, Any]]:
    rows = []
    for log in logs:
        rows.append({
            "log": log,
            "before_pretty": _pretty_snapshot(log.before_data),
            "after_pretty": _pretty_snapshot(log.after_data),
        })
    return rows

def _dump_snapshot(value: Any) -> Optional[str]:
    if value is None:
        return None
    return json.dumps(_json_ready(value), ensure_ascii=False, sort_keys=True)

def _pretty_snapshot(value: Optional[str]) -> str:
    if not value:
        return ""
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return value
    return json.dumps(parsed, ensure_ascii=False, indent=2, sort_keys=True)

def select_profile(user_id: int):
    from sqlmodel import select
    return select(Profile).where(Profile.user_id == user_id)

def select_posts(user_id: int):
    from sqlmodel import select
    return select(Post).where(Post.user_id == user_id)

def select_events(user_id: int):
    from sqlmodel import select
    return select(Event).where(Event.user_id == user_id)
