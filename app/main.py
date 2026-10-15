from fastapi import FastAPI, Body, Response, status, HTTPException, Depends 
from pydantic import BaseModel
from typing import Optional, List 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .db_connection import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
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


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session= Depends(get_db)):
    posts = db.query(models.Post).all()
    print("Fetch successful")
    return posts

@app.get('/posts/latest', response_model=schemas.PostResponse)
def get_latest():
    post =my_memory[ len(my_memory) - 1 ] 
    return post

@app.get('/posts/{id}', response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")
    return post

@app.post('/posts', status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(new_post: schemas.PostBase, db : Session =  Depends(get_db)):
    new_post = models.Post(**new_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.delete('/posts/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, response_model=schemas.PostResponse)

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT, response_model=schemas.PostResponse)

@app.put('/posts/{id}', response_model=schemas.PostResponse)
def update_post(id: int,npost: schemas.PostBase, db: Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
        
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
            )

    post_query.update(npost.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()



@app.patch('/posts/{id}', response_model=schemas.PostResponse)
def partial_update_post(id: int, post: schemas.PostBase):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post = post.model_dump(exclude_unset=True)
    my_memory[index].update(post)
    print("Updated successfully")
    return {"detail": my_memory[index]}

# STARTING USERERES FROM HERE
@app.get("/users", response_model=List[schemas.BaseUser])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    print("Fetch Successful")
    return users

@app.post("/users", response_model=schemas.UserResponse)
def get_user(new_user: schemas.CreateUser, db: Session = Depends(get_db)):

    hashed_password = pwd_context.hash(new_user.password)
    new_user.password = hashed_password
    user = models.User(**new_user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

