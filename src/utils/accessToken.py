from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
# from dotenv import dotenv_values

# os.environ.get = dotenv_values(".env")


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = os.environ.get("ALGORITHM")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.environ.get('JWT_REFRESH_SECRET_KEY')



def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.JWTError:
        return None