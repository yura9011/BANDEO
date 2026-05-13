from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date

class UserBase(SQLModel):
    role: str  # "MUSICO" o "BANDA"
    display_name: str

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    edit_token: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    profile: "Profile" = Relationship(back_populates="user")
    posts: List["Post"] = Relationship(back_populates="user")
    events: List["Event"] = Relationship(back_populates="user")

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    bio: Optional[str] = None
    instruments: str
    genres: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    youtube_links: Optional[str] = None
    spotify_link: Optional[str] = None
    instagram_link: Optional[str] = None
    user: User = Relationship(back_populates="profile")

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user: User = Relationship(back_populates="posts")

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date: date                          # día del evento
    time: Optional[str] = None          # "21:00"
    venue: str                          # nombre del lugar
    address: Optional[str] = None       # dirección
    city: str
    price: Optional[str] = None         # "Gratis", "$2000", etc.
    details: Optional[str] = None       # info extra
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user: User = Relationship(back_populates="events")
