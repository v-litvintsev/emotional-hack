from fastapi import APIRouter,WebSocket,WebSocketDisconnect,Body,Depends
from .ws import ConnectionManager
from fastapi.responses import HTMLResponse
from .database import *
from .models import *
from fastapi.encoders import jsonable_encoder
import json
from datetime import datetime

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your nickname: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var username = "biggvladik"
            document.querySelector("#ws-id").textContent = username;
            var ws = new WebSocket(`ws://localhost:80/ws`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(JSON.stringify({ type:'message', text: input.value, sender: username,emotion: 'none'}))
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

manager = ConnectionManager()
router = APIRouter()
Data = Database()
@router.get('/chat')
async def get():
    return HTMLResponse(html)

@router.websocket('/ws')
async def websocket_endpoint(websocket:WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            parsed_message = json.loads(message)
            if parsed_message['type'] == 'message':

                # model_message = MessageSchema(
                #     text = parsed_message['text'],
                #     emotion = parsed_message['emotion'],
                #     sender = parsed_message['sender']
                # )

                msg = await Data.add_message(parsed_message)

            await manager.broadcast(json.dumps(message))

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
