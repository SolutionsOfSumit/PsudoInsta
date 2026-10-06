from fastapi import FastAPI, Body, Response, status, HTTPException, Depends 
from pydantic import BaseModel
from typing import Optional 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .db_connection import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True: 
    try:
        conn = psycopg2.connect("dbname=FastAPI user=postgres password=Sumit@123", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error was:", error)

    
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


def find_post(id):
    for post in my_memory:
            if id == post["id"]:
                return post

def find_post_index(id):
    for i, p in enumerate(my_memory):
        if p["id"] == id: 
            return i


@app.get("/posts")
def get_posts(db: Session= Depends(get_db)):
    posts = db.query(models.Post).all()
    print("Fetch successful")
    return posts

@app.get('/posts/latest')
def get_latest():
    post =my_memory[ len(my_memory) - 1 ] 
    return {"data": post}

@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found")
    return post

@app.post('/posts', status_code= status.HTTP_201_CREATED)
def create_post(new_post: Post):
    cursor.execute("""INSERT INTO posts (title, content, publish) VALUES (%s,%s,%s) RETURNING * """, (new_post.title, new_post.content, new_post.publish))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post 

@app.delete('/posts/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Can't able to find the post")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, publish = %s where id = %s RETURNING *""",(post.title, post.content, post.publish, str(id),))
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Post Found")
    conn.commit()
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

# Test Code
@app.get('/test')
def test_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return {"status": post}