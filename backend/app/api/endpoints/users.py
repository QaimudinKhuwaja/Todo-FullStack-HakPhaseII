from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.security import get_password_hash
from app.core.db import get_session
from app.models.user import User, UserCreate, UserOut

router = APIRouter()

@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_create: UserCreate, session: Session = Depends(get_session)):
    # Step 1: Check if email already exists
    existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please use a different email or login."
        )
    
    # Step 2: If not exists, proceed to register
    hashed_password = get_password_hash(user_create.password)
    user = User(email=user_create.email, password_hash=hashed_password)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user



