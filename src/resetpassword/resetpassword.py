from fastapi import FastAPI, Response, status, HTTPException
from bson.objectid import ObjectId
from mangum import Mangum
import asyncio
from utils.database import User
from schemas.userSchema import ResetSchema
from utils.password_hash import hash_password
from utils.accessToken import decode_token

app = FastAPI()


@app.put('/api/reset-password/{id}')
async def resetPassword(id: str, payload: ResetSchema):
    """ Reset
    """
    try :
        token = decode_token(id)
        email = token.get('sub')
    except:
        return ({"message": "invalid token"})

    db_user = await User.find_one({'email': email})

    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Credentail')

    # if db_user.get("verified") != True:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail='User not verified')

    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')

    password = hash_password(payload.password)

    id = db_user.get("_id")
    await User.update_one(
            {"_id": ObjectId(id)}, {"$set": {"password": password}}
        )


    return ({"reset Successfull!!": "ResetPassword"})


handler = Mangum(app)


def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)

