from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional 
from random import randrange

app = FastAPI()

def find_post(id):
    for post in my_memory:
            if int(id) == post["id"]:
                return post

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None

my_memory = [
    {
        "title": "Title of post 1",
        "content": "Contents of post 1",
        "id": 1
    },
    {
        "title": "Title of post 2",
        "content": "Content of post 2",
        "id": 2
    }
]
@app.get("/posts")
def root():
    return {"data": my_memory} 

@app.get('/posts/latest')
def get_latest():
    post =my_memory[ len(my_memory) - 1 ] 
    return {"data": post}

@app.get('/posts/{id}')
def get_post(id):
    post = find_post(id)
    return {"data": post}

@app.post('/posts')
def create_post(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict["id"] = randrange(1, 1000000000000000)
    my_memory.append(post_dict)
    return {"data": post_dict}