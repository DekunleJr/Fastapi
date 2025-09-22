from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from typing import Literal

class Post(BaseModel):
    title: str
    content: str
    published: bool = True




class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ReturnPost(BaseModel):
    id: int
    user_id: int
    title: str  
    content: str
    published: bool
    created_at: datetime
    owner: UserOut
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]