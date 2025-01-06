from pydantic import BaseModel, Field, EmailStr, ConfigDict

class UserData(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserFullData(UserData):
    username: str = Field(..., min_length=4)
    confirmed_password: str