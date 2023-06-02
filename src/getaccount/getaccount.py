from fastapi import FastAPI, Response, status, HTTPException
from bson.objectid import ObjectId
from utils.database import User
from mangum import Mangum
import lambdawarmer
from utils.accessToken import create_access_token, create_refresh_token, decode_token

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/api/get-account/{id}')
async def getAccount(id: str):

    try:
        user = await User.find_one({"_id": ObjectId(id)})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        # Remove sensitive information from the user object
        new_dict = dict(user)
        new_dict["_id"] = id
        new_dict.pop("password", None)
        new_dict.pop("token", None)
        return new_dict

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid id')



handler = Mangum(app)


def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)

