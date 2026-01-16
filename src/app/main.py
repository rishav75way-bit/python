from fastapi import FastAPI
from sqlmodel import SQLModel
from src.app.db.session import engine
import src.app.models.user

from src.app.api.routes.health import router as health_router
from src.app.api.routes.auth import router as auth_router
from src.app.api.routes.users import router as users_router

app = FastAPI(title="python-practice")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
