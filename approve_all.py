from app.database import engine
from sqlmodel import Session, select
from app.models.user import User, Post, Event

with Session(engine) as s:
    for u in s.exec(select(User)).all():
        u.status = "approved"
        s.add(u)
    for p in s.exec(select(Post)).all():
        p.status = "approved"
        s.add(p)
    for e in s.exec(select(Event)).all():
        e.status = "approved"
        s.add(e)
    s.commit()
    print("ok")
