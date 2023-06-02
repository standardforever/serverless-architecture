from fastapi import FastAPI, Response, status, HTTPException
from utils.database import Products
import boto3
from dotenv import dotenv_values
from mangum import Mangum
import lambdawarmer
from utils.accessToken import decode_token
from pydantic import BaseModel
from typing import List
from bson.objectid import ObjectId

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

class PayloadSchema(BaseModel):
    product_id: str
    image: List[str]

@app.post('/api/delete-image')
async def deleteImage(payload: PayloadSchema):
    products = ""
    try:
        products = await Products.find_one({"_id": ObjectId(payload.product_id)})
        if products == None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Product not found')
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Product not found')
    product_image = products.get("images")
    
    try:
        count = 0
        for image in product_image:
            value = list(image.values())[3]
            if value in payload.image:
                object_key = '/'.join(value.split('/')[3:])
                response = s3.delete_object(Bucket=AWS_BUCKET, Key=object_key)
                del product_image[count]
            count += 1  
    except:
        raise HTTPException(status_code=500, detail="Unable to delete Object")

    await Products.update_one({"_id": ObjectId(payload.product_id)}, {"$set": {"images": product_image}})
    return {"message": "Object deleted successfully"}


handler = Mangum(app)


def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)

