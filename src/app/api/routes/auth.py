from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from src.app.db.session import get_session
from src.app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from src.app.services.auth_service import register, login
from src.app.core.security import decode_token
from src.app.services.user_service import get_by_email

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

@router.post("/register")
def register_api(data: RegisterRequest, session: Session = Depends(get_session)):
    user = register(session, data.name, data.email, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Email exists")
    return {"message": "registered"}

@router.post("/login", response_model=TokenResponse)
def login_api(data: LoginRequest, session: Session = Depends(get_session)):
    token = login(session, data.email, data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token}

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
):
    data = decode_token(creds.credentials)
    user = get_by_email(session, data["sub"])
    if not user:
        raise HTTPException(status_code=401)
    return user
