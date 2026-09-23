from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    name: str
    section: int

my_list = []

@app.post('/posts')
def demo_post(post: Post):
    print(post)
    return {"detail": post}