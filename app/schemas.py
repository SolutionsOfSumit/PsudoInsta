from pydantic import BaseModel
from datetime import datetime

class BasePost(BaseModel):
    title: str
    content: str
    publish: bool = True


class CreatePost(BasePost):
    pass

class UpdatePost(BasePost):
    pass

class PostResponse(BasePost):
    id: int
    created_at: datetime

    class Config:
        orm_model = True
