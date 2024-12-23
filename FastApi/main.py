from fastapi import FastAPI, HTTPException
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from DB import get_db_connection
from psycopg2.extras import RealDictCursor
from bcrypt import hashpw, gensalt, checkpw

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class UserData(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserFullData(UserData):
    username: str = Field(..., min_length=4)
    confirmed_password: str

def hash_password(password: str) -> str:
    return hashpw(password.encode('utf-8'), gensalt()).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def DBCheck(user: UserData):
    conn = get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)
    query="SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (user.email,))
    user_data=cursor.fetchone()
    cursor.close()
    conn.close()
    if user_data and verify_password(user.password, user_data['password']):
        return user_data
    return None

def InsertUser(user: UserFullData):
    try:
        conn = get_db_connection()
        cursor=conn.cursor(cursor_factory=RealDictCursor)
        query="INSERT INTO users(username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (user.username, user.email, hash_password(user.password)))
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if conn:
            cursor.close()
            conn.close()

def email_exist(email: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    return user_data is not None

def user_exist(username: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    return user_data is not None

@app.post("/login")
def loginUser(creds: UserData):
    user = DBCheck(creds)
    if user:
        return {"data": "successful"}
    raise HTTPException(status_code=403, detail="Invalid email or password were typed")

@app.post("/register")
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
        raise HTTPException(status_code=422, detail=str(e));

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)