from fastapi import Header, HTTPException, status
from typing import Optional
from backend.app.core import auth_utils

def session_validator(x_session_id: Optional[str] = Header(None)):
    """
    Dependency to validate the session ID from the X-Session-ID header.
    """
    if not x_session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session ID missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    session = auth_utils.get_session(x_session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return session
