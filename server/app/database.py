from motor import motor_asyncio
from bson.objectid import ObjectId
from .models  import MessageSchema



#MONGO_DETAILS = "mongodb://mongodb:27017/"  # for docker-compose
# MONGO_DETAILS = 'mongodb://localhost:27017'
class Database():
    def __init__(self):
        self.client = motor_asyncio.AsyncIOMotorClient("mongodb://mongodb:27017/")
        self.database = self.client.users
        self.user_collection = self.database.get_collection('users_collection')
    @staticmethod
    def user_helper(user) -> dict:
        return {
            'id': str(user['_id']),
            'username': user['username'],
           # 'messages': user['messages'],
        }


    @staticmethod
    def message_helper(user) -> dict:
        return {
            'messages': user['messages'],
        }

    async def add_user(self, user_dict: dict) -> dict:
        user_data = {
            'username':user_dict['username'],
            'messages' : []
        }
        user = await self.user_collection.insert_one(user_data)
        new_user = await self.user_collection.find_one({'_id': user.inserted_id})

        return self.user_helper(new_user)

    async def retrieve_users(self):
        users = []

        async for user in self.user_collection.find():
            users.append(self.user_helper(user))

        return users

    async def retrieve_user(self,username: str) -> dict:
        user = await self.user_collection.find_one({'username': username})
        if user:
            return self.user_helper(user)

    async def delete_user(self,id: str):
        user = await self.user_collection.find_one({'_id': ObjectId(id)})
        if user:
            await self.user_collection.delete_one({'_id': ObjectId(id)})
            return True



    async def get_messages(self,username:str):
        user = await self.user_collection.find_one({'username':username})
        if user:
            return self.message_helper(user)

    async def add_message(self,username:str,message:MessageSchema):
        user = await self.user_collection.find_one({"username": username})
        if user:
            updated_user = await self.user_collection.update_one(
                {"username": username}, {"$push": { "messages": {
                    "_id": ObjectId(),
                    "text": message.text,
                    "checked": message.checked,
                    "emotional": message.emotion,
                    "sender": message.sender,

                }

                }}
            )
            if updated_user:
                return True
            return False






