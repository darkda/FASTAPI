from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime





class UserLogin (BaseModel):
    email: str
    password: str
class PostBase(BaseModel):
    
    title: str
    name: str
    published: bool =  True
    
class UserOut (BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

class Post(PostBase):
    id: int = None
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True



class PostCreate(PostBase):
    pass
    # post: Post

class UserCreate (BaseModel):
    email: EmailStr
    password: str
    




class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData (BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostOut(BaseModel):
    Post : Post
    votes: int

    class Config:
        orm_mode = True
    

