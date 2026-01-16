from sqlmodel import Session, select
from src.app.models.user import User

def get_by_email(session, email):
    return session.exec(select(User).where(User.email == email)).first()

def get_by_id(session, user_id):
    return session.get(User, user_id)

def list_users(session):
    return session.exec(select(User)).all()

def create_user(session, name, email, hashed_password):
    user = User(name=name, email=email, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update_user(session, user, name):
    if name:
        user.name = name
    session.commit()
    session.refresh(user)
    return user

def delete_user(session, user):
    session.delete(user)
    session.commit()
