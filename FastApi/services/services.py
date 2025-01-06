from utils.DB import get_db_connection
from psycopg2.extras import RealDictCursor
from bcrypt import hashpw, gensalt, checkpw
from models import UserData, UserFullData
from fastapi import HTTPException

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