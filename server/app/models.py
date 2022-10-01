from pydantic import BaseModel, Field
from typing import List,Optional
from bson.objectid import ObjectId


class MessageSchema(BaseModel):
    id: str
    text: str = Field(...)
    checked: bool = False
    emotion: Optional[str]
    sender: str

    class Config:
        schema_extra = {
            "example": {
                "text": "hello",
                "checked": False,
                "emotional": "hapiness",
                "sender": "vladek"
            }
        }


class UserSchema(BaseModel):
    username: str = Field(...)
    messages: Optional[List[MessageSchema]]

    class Config:
        schema_extra = {
            "example": {
                "username": "Vlad Zuev"
                # "messages": [{"text": "message",
                #               "checked": False,
                #               "emotional": "happiness",
                #               "sender": "Vlad"
                #               }],
            }
        }


def ResponseModel(data,message):
    return {
        'data':[data],
        'code':200,
        'message':message
    }


def ErrorResponseModel(error,code,message):
    return {'error':error,'code':code,'message':message}