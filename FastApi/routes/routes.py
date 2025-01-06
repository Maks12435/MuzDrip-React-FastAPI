from services.services import DBCheck, email_exist, user_exist, InsertUser
from services.music import get_genres, get_music
from fastapi import APIRouter, HTTPException
from models import UserData, UserFullData

auth_router = APIRouter()

@auth_router.post("/login")
def loginUser(creds: UserData):
    user = DBCheck(creds)
    if user:
        return {"data": "successful"}
    raise HTTPException(status_code=403, detail="Invalid email or password were typed")

@auth_router.post("/register")
def registerUser(creds: UserFullData):
    try:
        if email_exist(creds.email):
            raise HTTPException(status_code=400, detail='Email is already exists')
        if user_exist(creds.username):
            raise HTTPException(status_code=400, detail='This username is already exists')
        if creds.password != creds.confirmed_password:
            raise HTTPException(status_code=400, detail='Passwords do not match')
        InsertUser(creds)
        return {"message": "User registered successfully"}
    
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@auth_router.get('/genres')
def genres():
    try:  
        return get_genres()
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@auth_router.get('/music_data')
def songs():
    try:
        return get_music()
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
