from fastapi import FastAPI, Response, status, HTTPException
import random
from mangum import Mangum
import lambdawarmer
from pydantic import BaseModel
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PayloadSchema(BaseModel):
    """ Payload schema
    """
    payload: Dict

@app.post('/api/generate-image')
async def generateImage(payload: PayloadSchema):
    print(payload)

    return ({"image_1": "https://ipop-images.s3.amazonaws.com/pictures/images.jpeg",
            "image_2": "https://ipop-images.s3.amazonaws.com/pictures/images4.jpeg",
            "image_3": "https://ipop-images.s3.amazonaws.com/pictures/images5.jpeg",
            "image_4": "https://ipop-images.s3.amazonaws.com/pictures/index1.jpeg",
            "image_5": "https://ipop-images.s3.amazonaws.com/pictures/index6.jpeg",
            "image_6": "https://ipop-images.s3.amazonaws.com/pictures/index7.jpeg",
            "image_7": "https://ipop-images.s3.amazonaws.com/pictures/index8.jpeg",
            "image_8": "https://ipop-images.s3.amazonaws.com/pictures/index9.jpeg",
            "image_9": "https://ipop-images.s3.amazonaws.com/pictures/index.jpeg",
            "image_0": "https://ipop-images.s3.amazonaws.com/pictures/index.jpeg",})


handler = Mangum(app)


def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)

