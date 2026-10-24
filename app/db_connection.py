from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from sqlalchemy.engine import URL
from pydantic import BaseModel
from .config import settings

password = quote_plus(settings.database_password)

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{password}@localhost:{settings.database_port}/{settings.database_name}'

# SQLALCHEMY_DATABASE_URL =URL.create(
#     drivername="postgresql",
#     username="postgres",
#     password="Sumit@123",     # raw password — SQLAlchemy encodes it internally
#     host="localhost",
#     port=5432,
#     database="FastAPI"
#)


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

class Post(BaseModel):
    title:str
    content:str
    publish: bool = True