from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    publish: bool = True

class BaseUser(BaseModel):
    name: str
    email: EmailStr
    

class PostCreate(PostBase):
    pass

class CreateUser(BaseUser):
    password: str

class UpdatePost(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int

    user: UserResponse

    class Config:
        orm_model = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

class UserResponse(BaseUser):
    id: int
    created_at: datetime

    class Config: 
        orm_model = True


class UserLogin(BaseModel):
    email : EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str 

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) 