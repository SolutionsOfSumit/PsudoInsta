from jose import JWSError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "Hello_World"
ALGORITHM = "HS256"
EXPIRE_TIME_IN_MINUTES = 30

def create_token(data: dict):
    encoded_data = data.copy()
    expire = datetime.now() + timedelta(minutes=EXPIRE_TIME_IN_MINUTES)
    encoded_data.update({"exp": expire})
    encoded_jwt = jwt.encode(encoded_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt