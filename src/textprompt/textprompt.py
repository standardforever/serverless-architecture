from fastapi import FastAPI, Response, status, HTTPException
import random
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
import lambdawarmer


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/api/text-prompts')
async def textPrompts():
    num = random.randint(0, 4)
    random_value = [ "text1", "text2", "text3", "text4", "text5"]
    return({"text-prompts": random_value[num]})


handler = Mangum(app)

def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)

