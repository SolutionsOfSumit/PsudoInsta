from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas

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
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id : str = payload.get("user_id")
        if id is None: 
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data
