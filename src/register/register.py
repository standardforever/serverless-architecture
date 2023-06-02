from datetime import datetime, timedelta
from bson.objectid import ObjectId
from fastapi import FastAPI, Response, status, HTTPException
import os
from mangum import Mangum
import asyncio

from utils.database import User
from serializers.userSerializer import userEntity, userResponseEntity
from schemas.userSchema import UserResponse, CreateUserSchema
from utils.password_hash import hash_password
from utils.accessToken import create_access_token, create_refresh_token
from utils.email import send_email
import uuid
from fastapi.middleware.cors import CORSMiddleware

import lambdawarmer


from dotenv import dotenv_values



BASE_URL = os.environ.get("BASE_URL")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/api/register', status_code=status.HTTP_201_CREATED)#, response_model=UserResponse)
async def create_user(payload: CreateUserSchema):
    """ Register User
    """
    # User = database.get_user_collection()
    # Check if user already exist
    
    user = await User.find_one({'email': payload.email.lower()})
 
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')

    # Compare password and passwordConfirm
    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
    

    payload.password = hash_password(payload.password)

    del payload.passwordConfirm

    # add to database
    payload.token = str(uuid.uuid4())
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = await User.insert_one(payload.dict())
    user_id = str(result.inserted_id)
    
    link = "{}/verify-email/{}/{}".format(BASE_URL, user_id, payload.token)
    body = "<h1> Click this link to verify your email</h1> <a href='{}'> Verify email here</a>".format(link)
    await send_email(payload.email, "Verify email", body)
    # return {"status": "ok", "message": "check your inbox"}
    
    return {
            "status": "success",
            "user_id": user_id,
        "tokens": {"access_token": create_access_token(payload.email),
        "refresh_token": create_refresh_token(payload.email),} 
    }


handler = Mangum(app)


def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)
