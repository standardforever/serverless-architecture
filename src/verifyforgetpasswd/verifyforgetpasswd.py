from fastapi import FastAPI, Response, status, HTTPException
from bson.objectid import ObjectId
from mangum import Mangum

from utils.database import User
from schemas.userSchema import ResetSchema
from utils.password_hash import hash_password


app = FastAPI()


@app.put('/api/forget-password-verify/{id}/{token}')
async def resetPassword(id: str, token: str, payload: ResetSchema):

    """ Reset Password for Forget password
    """
    db_user = await User.find_one({'_id': ObjectId(id)})

    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Credentail')

    if db_user.get("resetPassword") != token or db_user.get("resetPassword") == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Credentails')


    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')

    password = hash_password(payload.password)
    await User.update_one(
            {"_id": ObjectId(id)}, {"$set": {"password": password, "resetPassword": None}}
        )
    # await User.update_one(
    #         {"_id": ObjectId(id)}, {"$set": {"resetPassword": None, "password": hash_password(payload.password)}}
    #     )
    return ({"message": "reset Successfull!!"})


handler = Mangum(app)


def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)

