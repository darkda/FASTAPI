from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .import database, schemas, models
from .config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme =  OAuth2PasswordBearer(tokenUrl= 'login')

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)


    return encode_jwt

def verify_access_token(access_token: str, credential_exception):
    try:
        


        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

        id:str = payload.get("user_id")

        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)


    except JWTError:
        raise credential_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f" could not validate credentials", headers={"www-Authenticate": "Bearer"})
    token = verify_access_token(token, credential_exception)
    user  = db.query(models.User).filter(models.User.id == token.id).first()





    return user