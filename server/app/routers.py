from fastapi import APIRouter,WebSocket,WebSocketDisconnect,Body
from .ws import ConnectionManager
from fastapi.responses import HTMLResponse
from .database import *
from .models import *
from fastapi.encoders import jsonable_encoder



manager = ConnectionManager()
router = APIRouter()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""











@router.get('/chat')
async def get():
    return HTMLResponse(html)

@router.websocket('/ws/{client_id}')
async def websocket_endpoint(websocket:WebSocket,client_id:int):
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {message}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")



@router.post('/', response_description='User data added into the database')
async def add_user_data(user:UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user,'User added successfully.')



@router.get("/", response_description="Students retrieved")
async def get_students():
    users = await retrieve_users()
    if users:
        return ResponseModel(users,'Users data retrieved successfully')
    return ResponseModel(users,'Empty list returned')


@router.get("/{id}", response_description="Student data retrieved")
async def get_student_data(id):
    user = await retrieve_user(id)
    if user:
        return ResponseModel(user, 'User data retrieved successfully')
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")



@router.delete('/{id}', response_description="User data deleted from the database")
async def delete_user_data(id:str):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id), "User deleted successfully"
        )
    return ResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )
