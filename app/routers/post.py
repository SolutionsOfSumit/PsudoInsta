from fastapi import FastAPI, Response, Depends, APIRouter, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from ..db_connection import get_db
from .. import schemas, models

router = APIRouter()


@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session= Depends(get_db)):
    posts = db.query(models.Post).all()
    print("Fetch successful")
    return posts

@router.get('/posts/latest', response_model=schemas.PostResponse)
def get_latest(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"The post does not exist"})
    return post

@router.get('/posts/{id}', response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")
    return post

@router.post('/posts', status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(new_post: schemas.PostBase, db : Session =  Depends(get_db)):
    new_post = models.Post(**new_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete('/posts/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, response_model=schemas.PostResponse)

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT, response_model=schemas.PostResponse)

@router.put('/posts/{id}', response_model=schemas.PostResponse)
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



@router.patch('/posts/{id}', response_model=schemas.PostResponse)
def partial_update_post(id: int, post: schemas.PostBase):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post = post.model_dump(exclude_unset=True)
    my_memory[index].update(post)
    print("Updated successfully")
    return {"detail": my_memory[index]}

# STARTING USERERES FROM HERE
@router.get("/users", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    print("Fetch Successful")
    return users

@router.post("/users", response_model=schemas.UserResponse)
def get_user(new_user: schemas.CreateUser, db: Session = Depends(get_db)):

    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password
    user = models.User(**new_user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

