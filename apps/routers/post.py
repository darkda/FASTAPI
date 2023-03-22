# from ..import models
from ..database import engine, get_db
import sqlalchemy.orm 
from sqlalchemy.orm import Session
from typing import List, Optional

from fastapi import Body, FastAPI, Response, status, HTTPException, Depends,APIRouter
# from httpx import post
# from pydantic import BaseModel
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
# import time
from ..import models , schemas, oauth2


router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)






# @router.get("/sqlalchemy")

# def test_posts(db: Session = Depends(get_db)):

#    posts = db.query(models.Post).all()

#    return {"data": posts}




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
     

    #  new_created_post  = models.Post(title = post.title, name = post.name, published = post.published)
     new_created_post  = models.Post(owner_id=current_user.id, **post.dict())
    #  new_created_post.owner_id = current_user.id

     db.add(new_created_post)
     db.commit()
     db.refresh(new_created_post)

     print(current_user.email)
    #  cursor.execute(""" INSERT INTO "POSTS" (title, name, published ) VALUES (%s, %s, %s) RETURNING *  """, (new_post.title, new_post.name, new_post.published))
    #  new_created_post = cursor.fetchone()
    #  new_created_post
    #  conn.commit()

     return new_created_post

@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM "POSTS" """)
    # posts  = cursor.fetchall()
    
#    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
   posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

   return posts
    #print(new_post.name)
    #print(new_post.published)
    #print(new_post.rating)
    # Post_dict = new_post.dict()
    # Post_dict['id'] = randrange(0, 10000000000)
    # my_posts.routerend(Post_dict)
   # print(new_post.dict)
    # return {"Message": "data created"}

   
    #return {"new post" : f"title {payload['title']} name: {payload['name']}"}
#title string, name string


# def find_post(id):
#     for p in my_posts:
#         cursor.execute("""  SELECT * FROM "POSTS" WHERE id = %s  """, (str(id)))
#         found_post = cursor.fetchone()

    
    
#     return { "data": found_post }  


#         if p["id"] == id:
#             return p
        
# def find_index_post(id):

#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

        

# @router.get("/posts/latest")
# async def get_latestPost():
#     post = my_posts[len(my_posts)-1]
#     return {"latest post": post}


@router.get("/{id}", response_model=schemas.Post)

async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   
   posts = db.query(models.Post).filter(models.Post.id == id).first()

#    print(id)
#    print(type(id))
#    post = find_post(id)
   if not posts:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    #    response.status_code = status.HTTP_404_NOT_FOUND
    #    return {"message": f"post with id: {id} was not found"}

   return  posts
    

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id : int , db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    # post = find_post(id)
    # if not post:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    
    # cursor.execute("""  DELETE FROM "POSTS" WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_delete_query = db.query(models.Post).filter(models.Post.id == id)
    post_delete = post_delete_query.first()


    if post_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    
    if post_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"not authorised to perform action")

    post_delete_query.delete(synchronize_session=False)

    db.commit()

    
    return{'message': 'post deleted'}


@router.put("/{id}")
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""  UPDATE "POSTS" SET title = %s, name = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.name, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()





    # index = find_index_post(id)
    if updated_post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"not authorised to perform action")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    # updated_post_query.update({'title': 'this is the updated title', 'name': 'this is the updated name', 'published': True},synchronize_session=False)
    updated_post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    db.refresh(updated_post)

    return updated_post