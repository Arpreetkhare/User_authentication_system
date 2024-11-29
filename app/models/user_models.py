from bson import ObjectId
from pydantic import BaseModel, Field, validator,field_validator
from typing import Optional




class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)  # Password length validation
    

    @field_validator('username')
    def username_validator(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Username cannot be empty or just spaces')
        return v
    
   
# Helper function to convert ObjectId to string
   
class UserInResponse(BaseModel):
    id: str
    username: str

    class Config:
        orm_mode = True    

class UserInDB(User):
    hashed_password: str





def objectid_to_str(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, dict):
            return {key: objectid_to_str(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [objectid_to_str(item) for item in obj]
        return obj
