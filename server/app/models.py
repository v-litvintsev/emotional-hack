from pydantic import BaseModel, EmailStr, Field
from typing import List,Optional


class MessageSchema(BaseModel):
    text: str = Field(...)
    checked: bool = False
    emotional: Optional[str]
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
    email: EmailStr = Field(...)
    messages: Optional[List[MessageSchema]]

    class Config:
        schema_extra = {
            "example": {
                "username": "Vlad Zuev",
                "email": "zuevvlad55@gmail.com",
                "messages": [{"text": "message",
                              "checked": False,
                              "emotional": "happiness",
                              "sender": "Vlad"
                              }],
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