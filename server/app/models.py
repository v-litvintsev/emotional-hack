from pydantic import BaseModel, EmailStr, Field
from typing import List,Optional

class UserSchema(BaseModel):
    username: str = Field(...)
    messages: Optional[List]



