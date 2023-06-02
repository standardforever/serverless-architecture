from fastapi import FastAPI, Response, status, HTTPException
from utils.database import Products
from bson.objectid import ObjectId
import boto3
from dotenv import dotenv_values
from mangum import Mangum
import lambdawarmer
from utils.accessToken import decode_token
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

AWS_BUCKET = os.environ.get("AWS_BUCKET")


s3 = boto3.client('s3')

class TokenSchema(BaseModel):
    jwt_token: str

@app.delete('/api/delete-product/{id}')
# async def deleteProduct(id: str, jwt_token: TokenSchema):
async def deleteProduct(id: str):
    # Check if the product exit
    # try:
    #     if decode_token(jwt_token.jwt_token) == None:
    #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                                 detail='token not valid')
    # except:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                                 detail='token not valid')

    product = await Products.find_one({'_id': ObjectId(id)})
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Product not found')
    images = product.get("images")
    try:
        # for image in images:
        #     object_key = '/'.join(image.split('/')[3:])
        #     # Delete the object
        #     response = s3.delete_object(Bucket=AWS_BUCKET, Key=object_key)

        await Products.delete_one({"_id": ObjectId(id)})
        return {"message": "Object deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Unable to delete Object")



handler = Mangum(app)


def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)
