from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional 
from random import randrange

app = FastAPI()

def find_post(id):
    for post in my_memory:
            if id == post["id"]:
                return post

def find_post_index(id):
    for i, p in enumerate(my_memory):
        if p["id"] == id: 
            return i


class Post(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    publish: Optional[bool] = None
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
    print("Request Successful")
    return {"data": my_memory} 

@app.get('/posts/latest')
def get_latest():
    post =my_memory[ len(my_memory) - 1 ] 
    return {"data": post}

@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id: {id} does not exist"}
    return {"data": post}

@app.post('/posts', status_code= status.HTTP_201_CREATED)
def create_post(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict["id"] = randrange(1, 1000000000000000)
    my_memory.append(post_dict)
    return {"data": post_dict}

@app.delete('/posts/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {id} does not exist")
    my_memory.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Post Found")
    post = post.model_dump()
    post["id"] = id
    my_memory[index] = post
    print("post updated")
    return {"detail": post}

@app.patch('/posts/{id}')
def partial_update_post(id: int, post: Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post = post.model_dump(exclude_unset=True)
    my_memory[index].update(post)
    print("Updated successfully")
    return {"detail": my_memory[index]}