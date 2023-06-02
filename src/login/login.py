
from fastapi import FastAPI, Response, status, HTTPException
from mangum import Mangum
from serializers.userSerializer import userEntity
from utils.database import User
from schemas.userSchema import LoginUserSchema
from utils.password_hash import verify_password
from utils.accessToken import create_access_token, create_refresh_token
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/api/login')
async def login(payload: LoginUserSchema, response: Response):
    """ Login User
    """
#     # Check if user already exist
    db_user = await User.find_one({'email': payload.email.lower()})

    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    # convert it database response to json
    user = userEntity(db_user)

    if db_user.get('verified') != True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    # Check if the password is valid
    if not verify_password(payload.password, user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    return {
        "user_id": user.get("id"),
        "status": "success",
        "tokens": {"access_token": create_access_token(user["email"]),
        "refresh_token": create_refresh_token(user['email']),} 
    }


handler = Mangum(app)

def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)
