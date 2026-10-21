from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import db_connection, schemas, models, utils, oauth2

router = APIRouter(
    prefix="/login",
    tags = ["auth"]
)

@router.post("/", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_connection.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the email id {user_credentials.email} does not exist")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    token = oauth2.create_token(data = {"user_id": user.id})


    return {
        "access_token": token,
        "token_type": "bearer"
        }