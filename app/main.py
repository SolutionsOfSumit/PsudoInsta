from fastapi import FastAPI, Body, Response, status, HTTPException, Depends 
from pydantic import BaseModel
from typing import Optional, List 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .db_connection import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .routers import post, user

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


app.include_router(post.router)
app.include_router(user.router)