

# import os
# from fastapi import APIRouter, HTTPException, status, Depends, Response
# from pydantic import BaseModel
# from typing import Annotated

# from sqlmodel import Session, select
# from app.core.db import get_session
# from app.models.user import User
# from app.core.security import verify_password
# from app.core.auth_utils import create_session

# router = APIRouter()

# class UserLogin(BaseModel):
#     email: str
#     password: str

# @router.post("/login")
# async def login_for_access_token(
#     user_login: UserLogin,
#     response: Response,  # ✅ Add Response here
#     db: Annotated[Session, Depends(get_session)]
# ):
#     user = db.exec(select(User).where(User.email == user_login.email)).first()

#     if not user or not user.is_active or not verify_password(user_login.password, user.password_hash):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     # Create a session
#     session_obj = create_session(user_id=user.id)
    
#     is_secure = os.getenv("COOKIE_SECURE", "False").lower() == "true"
#     same_site = os.getenv("COOKIE_SAMESITE", "lax")

#     # # ✅ Set cookie
#     response.set_cookie(
#         key="access_token",
#         value=session_obj.session_id,
#         httponly=True,
#         samesite=same_site,
#         secure=is_secure,          # production mein true
#         max_age=60 * 60 * 24 * 7,  # 7 days
#         path="/" # localhost ke liye
#     )






import os
from fastapi import APIRouter, HTTPException, status, Depends, Response
from pydantic import BaseModel
from typing import Annotated

from sqlmodel import Session, select
from app.core.db import get_session
from app.models.user import User
from app.core.security import verify_password
from app.core.auth_utils import create_session

router = APIRouter()

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login_for_access_token(
    user_login: UserLogin,
    response: Response,
    db: Annotated[Session, Depends(get_session)]
):
    user = db.exec(select(User).where(User.email == user_login.email)).first()

    if not user or not user.is_active or not verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create a session
    session_obj = create_session(user_id=user.id)
    
    # Production-safe cookie flags (cross-origin ke liye must)
    # Railway pe env var set kar sakte ho: COOKIE_SECURE=true, COOKIE_SAMESITE=None
    is_secure = os.getenv("COOKIE_SECURE", "True").lower() == "true"  # Default True for prod
    same_site = os.getenv("COOKIE_SAMESITE", "None")  # Default 'None' for cross-origin

    response.set_cookie(
        key="access_token",
        value=session_obj.session_id,
        httponly=True,
        samesite=same_site,          # 'None' for cross-site (Vercel → Railway)
        secure=is_secure,            # True for HTTPS (production must)
        max_age=60 * 60 * 24 * 7,    # 7 days
        path="/"
    )

    return {"message": "Login successful"}  # Optional response body