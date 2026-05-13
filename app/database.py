import os
from urllib.parse import urlparse, parse_qs
from sqlmodel import create_engine, SQLModel, Session
from app.models.user import User, Profile, Post, Event

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bandeo.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    parsed = urlparse(DATABASE_URL)
    qs = parse_qs(parsed.query)
    sslmode = qs.pop("sslmode", [None])[0]

    clean_url = f"postgresql+psycopg2://{parsed.netloc}{parsed.path}"
    if qs:
        clean_url += "?" + "&".join(f"{k}={v[0]}" for k, v in qs.items())

    connect_args = {}
    if sslmode:
        connect_args["sslmode"] = sslmode

    engine = create_engine(clean_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
