from fastapi import FastAPI, Response, Depends, APIRouter, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db_connection import get_db
from .. import schemas, models, oauth2

router = APIRouter(
    prefix="/posts",
    tags = ["Posts"]
)


# @router.get("/", response_model=List[schemas.PostResponse]) , response_model=List[schemas.PostOut]
@router.get("/", response_model=List[schemas.PostOut])

def get_posts(db: Session= Depends(get_db), limit: int = 5, skip: int = 0, search: Optional[str] = ""):

    posts = (
        db.query(models.Post, func.count(models.Voting.user_id).label("votes"))
        .join(models.Voting, models.Post.id == models.Voting.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts



@router.get('/latest', response_model=schemas.PostResponse)
def get_latest(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"The post does not exist"})
    return post

@router.get('/{id}', response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")
    return post

@router.post('/', status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(new_post: schemas.PostBase, db : Session =  Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id = current_user.id, **new_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete('/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    if current_user.id != post.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not autrhorized for deleting this post")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int,npost: schemas.PostBase, db: Session=Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
        
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
            )
    if current_user.id != post.user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not autrhorized for deleting this post")
    
    post_query.update(npost.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()



@router.patch('/{id}', response_model=schemas.PostResponse)
def partial_update_post(id: int, post: schemas.PostBase):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post = post.model_dump(exclude_unset=True)
    my_memory[index].update(post)
    print("Updated successfully")
    return {"detail": my_memory[index]}
