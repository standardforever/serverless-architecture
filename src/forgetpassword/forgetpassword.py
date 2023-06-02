from fastapi import FastAPI, Response, status, HTTPException
from bson.objectid import ObjectId
from mangum import Mangum

from utils.database import User
from schemas.userSchema import ForgetPassword
import uuid
from utils.email import send_email



BASE_URL = os.environ.get("BASE_URL")


app = FastAPI()


@app.post('/api/forget-password')
async def resetPassword(payload: ForgetPassword):
    """ FOrget Password
    """
    # Check if the user exist
    db_user = await User.find_one({'email': payload.email.lower()})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    token = str(uuid.uuid4())

    await User.update_one(
            {"_id": ObjectId(db_user.get("_id"))}, {"$set": {"resetPassword": token}}
        )
    link = "{}/forget-password-verify/{}/{}".format(BASE_URL,db_user.get("_id"), token)
    body = "<h1> Click this link to verify your email</h1> <a href='{}'> Verify email here</a>".format(link)
    await send_email(payload.email, "Reset Password", body)
    return {"status": "ok", "message": "check your inbox"}


handler = Mangum(app)

def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)

