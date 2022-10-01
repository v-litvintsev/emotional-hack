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
                ws.send(JSON.stringify({type:'message', text: input.value, sender: username,emotion: 'none'}))
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
                id = str(datetime.now())

                model_message = MessageSchema(
                    id = id,
                    text = parsed_message['text'],
                    emotion = parsed_message['emotion'],
                    sender = parsed_message['sender']
                )

                user = await Data.add_message(model_message.sender, model_message)

            await manager.broadcast(json.dumps(message))

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.post('/', response_description='User data added into the database')
async def add_user_data(user:UserSchema = Body(...),Data =Depends(Database)):
    user = jsonable_encoder(user)
    new_user = await Data.add_user(user)
    return ResponseModel(new_user,'User added successfully.')



@router.get("/", response_description="Users retrieved")
async def get_students(Data =Depends(Database)):
    users = await Data.retrieve_users()
    if users:
        return ResponseModel(users,'Users data retrieved successfully')
    return ResponseModel(users,'Empty list returned')


@router.get("/{username}", response_description="User data retrieved")
async def get_user_data(username:str, Data =Depends(Database)):
    user = await Data.retrieve_user(username)
    if user:
        return ResponseModel(user, 'User data retrieved successfully')
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")



@router.delete('/{username}', response_description="User data deleted from the database")
async def delete_user_data(id:str, Data =Depends(Database)):
    deleted_user = await Data.delete_user(id)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id), "User deleted successfully"
        )
    return ResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )



@router.get("/messages/{username}", response_description="Messages username")
async def send_message(username:str, Data =Depends(Database)):
    user = await Data.get_messages(username)
    if user:
        return ResponseModel(user, 'Messages data retrieved successfully')
    return ErrorResponseModel("An error occurred.", 404, "Messages don't exist.")
