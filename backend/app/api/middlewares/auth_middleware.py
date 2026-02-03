# from fastapi import Header, HTTPException, status, Depends
# from typing import Optional
# from app.core import auth_utils
# from app.core.db import get_session
# from app.models.user import User
# from sqlmodel import Session, select


# def session_validator(x_session_id: Optional[str] = Header(None)):
#     """
#     Dependency to validate the session ID from the X-Session-ID header.
#     """
#     if not x_session_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Session ID missing",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     session = auth_utils.get_session(x_session_id)
#     if not session:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired session",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return session

# def get_current_user(session_data: auth_utils.Session = Depends(session_validator), db_session: Session = Depends(get_session)) -> User:
#     """
#     Dependency to retrieve the current authenticated user.
#     """
#     user = db_session.exec(select(User).where(User.id == session_data.user_id)).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     if not user.is_active:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
#     return user




from fastapi import HTTPException, status, Depends, Request
from app.core import auth_utils
from app.core.db import get_session
from app.models.user import User
from sqlmodel import Session, select


# ✅ COOKIE BASED SESSION VALIDATOR
def session_validator(request: Request):
    """
    Validate session using cookie instead of header
    """

    session_id = request.cookies.get("access_token")

    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session cookie missing",
        )

    session = auth_utils.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )

    return session


# ✅ CURRENT USER GETTER
def get_current_user(
    session_data: auth_utils.Session = Depends(session_validator),
    db_session: Session = Depends(get_session),
) -> User:

    user = db_session.exec(
        select(User).where(User.id == session_data.user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return user
