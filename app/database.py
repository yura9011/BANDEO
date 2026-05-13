import os
import ssl
from urllib.parse import urlparse, parse_qs, urlencode
from sqlmodel import create_engine, SQLModel, Session
from app.models.user import User, Profile, Post, Event

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./bandeo.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    parsed = urlparse(DATABASE_URL)
    qs = parse_qs(parsed.query)
    sslmode = qs.pop("sslmode", [None])[0]

    # Reconstruir URL limpia sin sslmode, forzar pg8000
    clean_url = f"postgresql+pg8000://{parsed.netloc}{parsed.path}"
    if qs:
        clean_url += "?" + urlencode({k: v[0] for k, v in qs.items()})

    connect_args = {}
    if sslmode and sslmode != "disable":
        # pg8000 usa ssl= con un objeto ssl.SSLContext
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        connect_args["ssl_context"] = ssl_ctx

    engine = create_engine(clean_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
