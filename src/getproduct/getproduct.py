from fastapi import FastAPI
from utils.database import Products
from mangum import Mangum
import lambdawarmer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/api/get-product/{id}')
async def getProduct(id: str):
    new_list = []
    all_products = ""
    try:
        # Retrieve all documents from the collection
        all_products = await Products.find({"user_id": id}).to_list(length=None)

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='User_id not valid')
    for product in all_products:
        product['_id'] = str(product.get('_id'))
        new_list.append(product)

    return new_list

handler = Mangum(app)


def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)

