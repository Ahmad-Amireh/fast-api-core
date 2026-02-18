from __future__ import annotations
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate (BaseModel):

    name: str
    email: EmailStr

class UserUpdate(BaseModel):

    name: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    posts: List[PostResponse] = []
    
    class Config:

        from_attributes = True

class PostCreate(BaseModel):
    title: str
    content: Optional[str] = None
    user_id: int

class PostResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    user_id: int

    class Config:
        from_attributes = True
