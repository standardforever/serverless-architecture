from datetime import datetime, timedelta
from fastapi import FastAPI, Response, status, HTTPException
from bson.objectid import ObjectId
from mangum import Mangum
from pydantic import BaseModel
from typing import List, Dict
from utils.database import Products, User
from fastapi.encoders import jsonable_encoder
# from schemas.productSchema import UpdateSchema
import uuid

import lambdawarmer

app = FastAPI()



class UpdateSchema(BaseModel):
    name: str = None
    product_class: str = None
    description: str = None
    images: List[Dict] = None
    updated_at: datetime = None
    user_id: str = None

    class Config:
        orm_mode = True

@app.put('/api/update-product/{id}')
async def updateProduct(id: str, payload: UpdateSchema):
    """ updatePRoduct
    """
    product = ""
    try:
        product = await Products.find_one({"_id": ObjectId(id)})
        if  product == None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Id not valid')
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='id not valid')
    new_object = {}
    # add to database
    if payload.images != None:
        new_list = payload.images + product.get("images")
        product["images"] = new_list
        new_object["images"] = new_list
    payload_dict = payload.dict()

    for key, value in payload_dict.items():
        if value != None and key != "images":
            product[key] = value
            new_object[key] = value
    result = {}
    if len(new_object) > 0:
        new_object["updated_at"] = datetime.utcnow()
        result = await Products.update_one({"_id": ObjectId(id)}, {"$set": new_object})

    # Convert result to JSON format
    product["_id"] = str(product.get("_id"))

    return product


handler = Mangum(app)

def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)

