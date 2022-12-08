from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    name: str
    email: str
    gender: str
    phone: str
    city:str
    timestamp: str

class AuthSchema(BaseModel):
    username: str
    password: str