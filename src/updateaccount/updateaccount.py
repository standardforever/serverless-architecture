from datetime import datetime, timedelta
from bson.objectid import ObjectId
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel, EmailStr, constr
from mangum import Mangum

from utils.database import User
from utils.password_hash import hash_password
from utils.accessToken import create_access_token, create_refresh_token
import uuid
from fastapi.middleware.cors import CORSMiddleware
import pymongo
import lambdawarmer
import os


BASE_URL = os.environ.get("BASE_URL")

app = FastAPI()




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class UpdateUserSchema(BaseModel):
    password: constr(min_length=4) = None
    passwordConfirm: str = None
    first_name: str = None
    last_name: str = None
    company_name:str = None
    credit: str = None
    profile_image: str = None

    class Config:
        orm_mode = True


@app.put('/api/update-account/{id}')
async def updateAccount(id: str, payload: UpdateUserSchema):
    """ Update User
    """
    # Check if the user exit

    try:
        user = await User.find_one({'_id': ObjectId(id)})
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="account doesn't exist")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="account doesn't exist")

    new_object = {}
    

    # Compare password and passwordConfirm
    if payload.password != None or payload.password != None:
        if payload.password != payload.passwordConfirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
        new_object["password"] = hash_password(payload.password)
        del payload.passwordConfirm
        del payload.password

    payload_dict = payload.dict()
    for key, value in payload_dict.items():
        if value != None:
            new_object[key] = value
    result = {}
    if len(new_object) > 0:
        new_object["updated_at"] = datetime.utcnow()
        result = await User.update_one({"_id": ObjectId(id)}, {"$set": new_object})
    new_user = await User.find_one({'_id': ObjectId(id)})
    new_user["_id"] = id
    del new_user["password"]
    del new_user["token"]
    del new_user["resetPassword"]
    return new_user


handler = Mangum(app)

def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)

