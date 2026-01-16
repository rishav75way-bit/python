from src.app.services.user_service import get_by_email, create_user
from src.app.core.security import hash_password, verify_password, create_access_token

def register(session, name, email, password):
    if get_by_email(session, email):
        return None
    return create_user(session, name, email, hash_password(password))

def login(session, email, password):
    user = get_by_email(session, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return create_access_token(user.email)
