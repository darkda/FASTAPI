
# from ..import models
from ..database import engine, get_db
import sqlalchemy.orm 
from sqlalchemy.orm import Session
from typing import Optional, List

from fastapi import Body, FastAPI, Response, status, HTTPException, Depends,APIRouter
# from httpx import post
# from pydantic import BaseModel
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
# import time
from ..import models , schemas, utils


router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_users (user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pass = utils.hashpwd(user.password)
    user.password = hashed_pass
    new_created_user  = models.User(**user.dict())
    db.add(new_created_user)
    db.commit()
    db.refresh(new_created_user)



    return new_created_user


@router.get("/{id}",status_code=status.HTTP_200_OK,  response_model=schemas.UserOut)

def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} does not exist")

    return user
   
    