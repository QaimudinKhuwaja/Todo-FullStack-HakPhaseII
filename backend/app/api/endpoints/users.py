from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.security import get_password_hash
from app.core.db import get_session
from app.models.user import User, UserCreate, UserOut

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_create: UserCreate, session: Session = Depends(get_session)):
    hashed_password = get_password_hash(user_create.password)
    user = User(email=user_create.email, password_hash=hashed_password)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user