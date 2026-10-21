from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, db_connection, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "Hello_World"
ALGORITHM = "HS256"
EXPIRE_TIME_IN_MINUTES = 30

def create_token(data: dict):
    encoded_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_TIME_IN_MINUTES)
    encoded_data.update({"exp": expire})
    encoded_jwt = jwt.encode(encoded_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("user_id")
        if id is None: 
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(db_connection.get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Could not validate credentials ", headers={"WWW-Authentication":"Bearer"})

    token = verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user
