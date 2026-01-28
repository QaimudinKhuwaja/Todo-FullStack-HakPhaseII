from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Annotated

from sqlmodel import Session, select
from backend.app.core.db import get_session
from backend.app.models.user import User
from backend.app.core.security import verify_password
from backend.app.core.auth_utils import create_session

router = APIRouter()

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login_for_access_token(
    user_login: UserLogin, db: Annotated[Session, Depends(get_session)]
):
    user = db.exec(select(User).where(User.email == user_login.email)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create a session for the authenticated user
    session_obj = create_session(user_id=user.id) # user.id cannot be None here due to database behavior

    return {"user_id": user.id, "session_id": session_obj.session_id}


class SessionInvalidation(BaseModel):
    session_id: str

@router.post("/logout")
async def logout(
    session_data: SessionInvalidation, db: Annotated[Session, Depends(get_session)] # db is not used here but kept for consistency if needed later
):
    auth_utils.delete_session(session_data.session_id)
    return {"message": "Logged out successfully"}
