from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional 

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Sumit is a monster"} 

@app.get('/posts')
def get_post():
    return { "data": "Your posts will be visible here"}

@app.post('/posts')
def create_post(new_post: Post):
    print(new_post)
    print(new_post.model_dump())
    return {"data": "Operation successful"}