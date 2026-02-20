from __future__ import annotations
from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional


class UserCreate (BaseModel):

    name: str
    email: EmailStr
    password: constr(min_length=8, max_length=72)  # plain text from user, will be hashed

class UserUpdate(BaseModel):

    name: str | None = None
    email: EmailStr | None = None
    password: constr(min_length=8, max_length=72) | None = None  # optional update



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

class PostResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    user_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str