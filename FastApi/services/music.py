from utils.DB import get_db_connection
from psycopg2.extras import RealDictCursor

def get_genres():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = 'SELECT * FROM genres'
    cursor.execute(query)
    user_data=cursor.fetchall()
    cursor.close()
    conn.close()
    return user_data

def get_music():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = 'SELECT songs.*, genres.name FROM songs INNER JOIN genres ON songs.genre_id = genres.id'
    cursor.execute(query)
    user_data=cursor.fetchall()
    cursor.close()
    conn.close()
    return user_data


