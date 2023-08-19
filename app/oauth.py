from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .errors import credentials_exception as credentials_err

oauth2scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "70ffe8d2a70b1b8883b3c2847a2b32bd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
    except JWTError: 
        raise credentials_exception
    else:
        return id

def get_current_user(token: str = Depends(oauth2scheme)):
    return verify_access_token(token, credentials_err)
