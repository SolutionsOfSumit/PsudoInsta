from fastapi import HTTPException, Depends, Response, status, FastAPI, APIRouter
from .. import schemas, utils, models
from ..db_connection import get_db
from sqlalchemy.orm import Session 

router = APIRouter(
    prefix="/users",
    tags = ["Users"]
)

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session =  Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.delete("/{id}")
def delete_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)