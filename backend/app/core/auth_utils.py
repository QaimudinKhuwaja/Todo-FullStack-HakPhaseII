from datetime import datetime, timedelta
from typing import Dict, NamedTuple, Optional
import uuid

class Session(NamedTuple):
    session_id: str
    user_id: int
    created_at: datetime
    expires_at: datetime

# In-memory store for sessions
# In a real application, this would be a database or a distributed cache like Redis
_sessions: Dict[str, Session] = {}

SESSION_EXPIRY_SECONDS = 1800  # 30 minutes

def create_session(user_id: int) -> Session:
    """
    Creates a new session for the given user ID.
    """
    session_id = str(uuid.uuid4())
    now = datetime.utcnow()
    expires_at = now + timedelta(seconds=SESSION_EXPIRY_SECONDS)
    session = Session(
        session_id=session_id,
        user_id=user_id,
        created_at=now,
        expires_at=expires_at
    )
    _sessions[session_id] = session
    return session

def get_session(session_id: str) -> Optional[Session]:
    """
    Retrieves a session by its ID.
    Returns None if the session does not exist or has expired.
    """
    session = _sessions.get(session_id)
    if session and session.expires_at > datetime.utcnow():
        # Session is valid, refresh its expiry
        now = datetime.utcnow()
        new_expires_at = now + timedelta(seconds=SESSION_EXPIRY_SECONDS)
        updated_session = session._replace(expires_at=new_expires_at)
        _sessions[session_id] = updated_session
        return updated_session
    # If session expired or doesn't exist, remove it from store (optional cleanup)
    if session_id in _sessions:
        del _sessions[session_id]
    return None

def delete_session(session_id: str) -> None:
    """
    Deletes a session by its ID.
    """
    if session_id in _sessions:
        del _sessions[session_id]