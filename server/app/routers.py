from fastapi import APIRouter,WebSocket,WebSocketDisconnect,Body,Depends
from .ws import ConnectionManager
from .database import *
from .models import *
from fastapi.encoders import jsonable_encoder
import json
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel


class Emotion():

    def emotion_message(message: str):
        FastTextSocialNetworkModel.MODEL_PATH = 'app/models/fasttext-social-network-model.bin'
        tokenizer = RegexTokenizer()
        model = FastTextSocialNetworkModel(tokenizer=tokenizer)

        msg = [message]
        results = model.predict(msg, k=2)
        res = results[0]
        for key, value in res.items():
            return key

manager = ConnectionManager()
router = APIRouter()
Data = Database()

@router.websocket('/ws',)
async def websocket_endpoint(websocket:WebSocket):
    await manager.connect(websocket)
    try:
        while True:

            message = await websocket.receive_text()
            parsed_message = json.loads(message)

            if parsed_message['type'] == 'message':

                parsed_message['emotion'] = Emotion.emotion_message(parsed_message['text'])
                msg = await Data.add_message(parsed_message)
                parsed_message['_id'] = str(parsed_message['_id'])

            await manager.broadcast(json.dumps(parsed_message))

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.post("/messages", response_description="Upload message")
async def add_message(message: MessageSchema = Body(...), Data =Depends(Database)):
    message = jsonable_encoder(message)
    message = await Data.add_message(message)
    if message:
        return ResponseModel(message, 'Messages data retrieved successfully')
    return ErrorResponseModel("An error occurred.", 404, "Messages don't exist.")

@router.get("/messages", response_description= "Get message" )
async def get_message(Data = Depends(Database)):
    messages =  await Data.get_all_message()

    return ResponseModel(messages,"Messages data retrieved successfully")

