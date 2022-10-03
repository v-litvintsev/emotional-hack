from motor import motor_asyncio

class Database():
    def __init__(self):
        self.client = motor_asyncio.AsyncIOMotorClient("mongodb://mongodb:27017/")
        self.database = self.client.users
        self.user_collection = self.database.get_collection('users_collection')


    @staticmethod
    def message_helper(message) -> dict:
        return {
            'id': str(message['_id']),
            'text':  message['text'],
            'emotion': message['emotion'],
            'sender': message['sender'],

        }
    async def get_messages(self,username:str):
        user = await self.user_collection.find_one({'username':username})
        if user:
            return self.message_helper(user)

    async def add_message(self,message_data: dict) -> dict:

        message = await self.user_collection.insert_one(message_data)
        new_message = await self.user_collection.find_one({'_id': message.inserted_id})

        return self.message_helper(new_message)

    async def get_all_message(self):
        messages = [self.message_helper(message) async for message in self.user_collection.find()]

        return messages







