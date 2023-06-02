from fastapi import FastAPI, Response, status, HTTPException
from bson.objectid import ObjectId
from mangum import Mangum


from utils.database import User

app = FastAPI()


@app.get("/api/verify-email/{id}/{token}")
async def verify(id: str, token: str):
    """ Verify token for email verification
    """
    # return ({"id": id})
    # check if user exit in database
    try:
        db_user = await User.find_one({"_id": ObjectId(id)})
    except Exception as e:
        return ({"error": str(e)})

    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Credentail')

    # new_user = userResponseEntity(db_user)
   
    if db_user.get("token") != token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Credentails')
                            
    # Check if user is already verified
    if db_user.get("verified") == True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                           detail='User already verified')
 
    # Update the user status
    await User.update_one(
            {"_id": ObjectId(str(db_user.get("_id")))}, {"$set": {"verified": True}}
        )
    return ("Verified Successfull!!")
    

handler = Mangum(app)


def lambda_handler(event, context):
    context.callbackWaitsForEmptyEventLoop = False
    if event.get("source") == "serverless-plugin-warmup":
        return {}
    return handler(event, context)

