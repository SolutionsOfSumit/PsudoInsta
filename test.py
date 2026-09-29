from fastapi import FastAPI, status 
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

status.HTTP_200_OK