import os
from urllib.parse import urlparse
from sqlmodel import create_engine, SQLModel, Session
from app.models.user import User, Profile, Post, Event

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./bandeo.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    parsed = urlparse(DATABASE_URL)
    # Eliminar TODOS los query params (sslmode, channel_binding, etc.)
    # y forzar psycopg2 como dialecto explícito
    clean_url = f"postgresql+psycopg2://{parsed.netloc}{parsed.path}"
    # sslmode=require es el único param que psycopg2.connect() acepta via connect_args
    engine = create_engine(clean_url, connect_args={"sslmode": "require"})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
