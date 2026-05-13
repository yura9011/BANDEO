import os
from sqlmodel import create_engine, SQLModel, Session
from app.models.user import User, Profile, Post, Event

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    # fallback local unicamente
    DATABASE_URL = "sqlite:///./bandeo.db"

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL — asegurar que use el driver correcto
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
