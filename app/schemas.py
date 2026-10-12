from pydantic import BaseModel

class BasePost(BaseModel):
    title: str
    content: str
    publish: bool = True

class CreatePost(BasePost):
    pass

class UpdatePost(BasePost):
    pass

class PostResponse(BaseModel):
    title: str
    content: str
    publish: str
