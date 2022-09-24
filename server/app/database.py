from motor import motor_asyncio
from bson.objectid import ObjectId





#MONGO_DETAILS = "mongodb://mongodb:27017/"  # for docker-compose
MONGO_DETAILS = 'mongodb://localhost:27017'
client = motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.users

user_collection = database.get_collection('users_collection')



# helpers

def user_helper(user) -> dict:
    return {
        'id': str(user['_id']),
        'username': user['username'],
        "email": user["email"],
        'messages': user['messages'],
    }



async def add_user(user_data:dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({'_id':user.inserted_id})

    return user_helper(new_user)


async def retrieve_users():
    users = []

    async for user in user_collection.find():
        users.append(user_helper(user))

    return users


async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({'_id':ObjectId(id)})
    if user:
        return user_helper(user)


async def delete_user(id:str):
    user = await user_collection.find_one({'_id':ObjectId(id)})
    if user:
        await user_collection.delete_one({'_id':ObjectId(id)})
        return True


