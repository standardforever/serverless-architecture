from datetime import datetime, timedelta
from fastapi import FastAPI, Response, status, HTTPException
from bson.objectid import ObjectId
from mangum import Mangum

from utils.database import Products, User
from schemas.productSchema import ProductSchema
import uuid

import lambdawarmer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/api/create-product', status_code=status.HTTP_201_CREATED)
async def createProduct(payload: ProductSchema):
    """ Create PRoduct
    """
    try:
        user = await User.find_one({"_id": ObjectId(payload.user_id)})
        if  user == None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='User_id not valid')
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='User_id not valid')

    # add to database
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = await Products.insert_one(payload.dict())

    # Return the created product with the result ID
    created_product = payload.dict()
    created_product['_id'] = str(result.inserted_id)
    return created_product



handler = Mangum(app)


def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)

