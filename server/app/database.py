from motor import motor_asyncio
from bson.objectid import ObjectId




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
            "email": user["email"],
            'messages': user['messages'],
        }

    async def add_user(self, user_data: dict) -> dict:
        user = await self.user_collection.insert_one(user_data)
        new_user = await self.user_collection.find_one({'_id': user.inserted_id})

        return self.user_helper(new_user)

    async def retrieve_users(self):
        users = []

        async for user in self.user_collection.find():
            users.append(self.user_helper(user))

        return users

    async def retrieve_user(self,id: str) -> dict:
        user = await self.user_collection.find_one({'_id': ObjectId(id)})
        if user:
            return self.user_helper(user)

    async def delete_user(self,id: str):
        user = await self.user_collection.find_one({'_id': ObjectId(id)})
        if user:
            await self.user_collection.delete_one({'_id': ObjectId(id)})
            return True


