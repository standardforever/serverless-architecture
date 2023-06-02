import boto3
from botocore.exceptions import ClientError
from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel
from uuid import uuid4
from typing import List
from dotenv import dotenv_values
import base64
from fastapi.middleware.cors import CORSMiddleware
import os
from mangum import Mangum
import lambdawarmer

config = dotenv_values(".env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust the allowed origins accordingly
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


AWS_BUCKET = os.environ.get("AWS_BUCKET")
S3_FOLDER = os.environ.get("S3_FOLDER")

s3 = boto3.client('s3')

SUPPORTED_FILE_TYPES = [
    'png',
    'jpeg',
    'jpg',
    'svg',
    'gif',
    'webp'
]

KB = 1024
MB = 1024 * KB


class Image(BaseModel):
    filename: str
    contentType: str
    body: str


class ImageList(BaseModel):
    imageList: List[Image]


@app.post("/api/upload-images")
async def upload_images(image_list: ImageList):
    uploaded_files = []

    for image in image_list.imageList:
        # Check the length of the file
        size = len(image.body)

        # Limit the size of the file that can be sent
        if not 0 < size <= 100 * MB:
            raise HTTPException(status_code=400, detail="Supported file size is 0-3 MB")

        # Get the file extension
        file_extension = image.filename.split('.')[-1]

        if file_extension not in SUPPORTED_FILE_TYPES:
            raise HTTPException(status_code=400, detail="File type not accepted")

        key = f"{S3_FOLDER}{uuid4()}.{file_extension}"

        # Decode the base64-encoded image data
        decoded_image = base64.b64decode(image.body)

        # Upload the file to S3
        try:
            s3.put_object(Body=decoded_image, Bucket=AWS_BUCKET, Key=key,
                          ContentType=image.contentType,
                          ContentDisposition='inline')  # Set Content-Disposition header
        except ClientError as e:
            raise HTTPException(status_code=500, detail="Failed to upload file")

        # Construct the S3 object URL
        file_path = f"https://{AWS_BUCKET}.s3.amazonaws.com/{key}"
        uploaded_files.append(file_path)

    return {"uploaded_files": uploaded_files}


handler = Mangum(app)

def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)

