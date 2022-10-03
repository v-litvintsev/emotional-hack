from pydantic import BaseModel, Field
from typing import  Optional


class MessageSchema(BaseModel):
    text: str = Field(...)
    emotion: Optional[str]
    sender: str

    class Config:
        schema_extra = {
            "example": {
                "text": "hello",
                "emotion": "hapiness",
                "sender": "vladek"
            }
        }

def ResponseModel(data, message):
    return {
        'data': [data],
        'code': 200,
        'message': message
    }


def ErrorResponseModel(error, code, message):
    return {'error': error, 'code': code, 'message': message}
