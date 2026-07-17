from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: EmailStr
    display_name: str
    couple_id: str | None

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class CoupleCreateOut(BaseModel):
    id: str
    invite_code: str

    class Config:
        from_attributes = True


class JoinCoupleIn(BaseModel):
    invite_code: str


class MemoryOut(BaseModel):
    id: str
    r2_object_key: str
    media_type: str
    caption: str | None
    taken_at: datetime | None
    created_at: datetime
    photo_url: str | None = None

    class Config:
        from_attributes = True


class MemoryCreateIn(BaseModel):
    r2_object_key: str
    media_type: str = "image"
    caption: str | None = None
    taken_at: datetime | None = None
    latitude: str | None = None
    longitude: str | None = None
