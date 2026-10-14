from pydantic import BaseModel, EmailStr
from datetime import datetime

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

    class Config:
        orm_model = True

class UserResponse(BaseUser):
    created_at: datetime

    class Config: 
        orm_model = True
