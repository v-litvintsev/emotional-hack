from fastapi import APIRouter,WebSocket,WebSocketDisconnect,Body,Depends
from .ws import ConnectionManager
from fastapi.responses import HTMLResponse
from .database import *
from .models import *
from fastapi.encoders import jsonable_encoder



manager = ConnectionManager()
router = APIRouter()

# @router.get('/chat')
# async def get():
#     return HTMLResponse(html)

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
async def add_user_data(user:UserSchema = Body(...),Data =Depends(Database)):
    user = jsonable_encoder(user)
    new_user = await Data.add_user(user)
    return ResponseModel(new_user,'User added successfully.')



@router.get("/", response_description="Students retrieved")
async def get_students(Data =Depends(Database)):
    users = await Data.retrieve_users()
    if users:
        return ResponseModel(users,'Users data retrieved successfully')
    return ResponseModel(users,'Empty list returned')


@router.get("/{id}", response_description="Student data retrieved")
async def get_student_data(id:str,Data =Depends(Database)):
    user = await Data.retrieve_user(id)
    if user:
        return ResponseModel(user, 'User data retrieved successfully')
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")



@router.delete('/{id}', response_description="User data deleted from the database")
async def delete_user_data(id:str,Data =Depends(Database)):
    deleted_user = await Data.delete_user(id)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id), "User deleted successfully"
        )
    return ResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )
