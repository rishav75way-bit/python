from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from src.app.db.session import get_session
from src.app.schemas.user import UserCreate, UserUpdate, UserOut
from src.app.services.user_service import list_users, create_user, get_by_id, update_user, delete_user, get_by_email
from src.app.core.security import hash_password
from src.app.api.routes.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=list[UserOut])
def users(session: Session = Depends(get_session), _=Depends(get_current_user)):
    return list_users(session)

@router.post("", response_model=UserOut)
def create(payload: UserCreate, session: Session = Depends(get_session), _=Depends(get_current_user)):
    if get_by_email(session, payload.email):
        raise HTTPException(status_code=400)
    return create_user(session, payload.name, payload.email, hash_password(payload.password))

@router.get("/{user_id}", response_model=UserOut)
def get(user_id: int, session: Session = Depends(get_session), _=Depends(get_current_user)):
    user = get_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404)
    return user

@router.patch("/{user_id}", response_model=UserOut)
def patch(user_id: int, payload: UserUpdate, session: Session = Depends(get_session), _=Depends(get_current_user)):
    user = get_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404)
    return update_user(session, user, payload.name)

@router.delete("/{user_id}")
def delete(user_id: int, session: Session = Depends(get_session), _=Depends(get_current_user)):
    user = get_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404)
    delete_user(session, user)
    return {"deleted": True}
