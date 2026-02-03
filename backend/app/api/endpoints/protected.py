from fastapi import APIRouter, Depends
from app.api.middlewares.auth_middleware import session_validator
from app.core.auth_utils import Session

router = APIRouter()

@router.get("/protected")
async def protected_route(session: Session = Depends(session_validator)):
    return {"message": "Access granted", "session_id": session.session_id}
