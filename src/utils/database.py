import motor.motor_asyncio
import os
# from dotenv import dotenv_values
# config = dotenv_values(".env")

MONGO_DETAILS = os.environ.get("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

db = client["authentication"]

User = db["User"]
Products = db["Products"]





# class Database:
#     def __init__(self):
#         self.client = None
#         self.db = None

#     async def connect(self):
#         if self.client is None:
#             self.client = AsyncIOMotorClient(MONGO_DETAILS, maxPoolSize=10)  # Adjust the maxPoolSize as needed
#             self.db = self.client["authentication"]

#     def get_user_collection(self):
#         return self.db["User"]


# defined the connection details, and created a client via AsyncIOMotorClient.

# # User.create_index([("email", pymongo.ASCENDING)], unique=True)
