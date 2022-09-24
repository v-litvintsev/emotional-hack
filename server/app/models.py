from pydantic import BaseModel, EmailStr, Field
from typing import List,Optional

class UserSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    messages: Optional[List]

    class Config:
        schema_extra = {
            "example": {
                "username": "Vlad Zuev",
                "email": "zuevvlad55@gmail.com",
                "messages": ['1','2'],
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