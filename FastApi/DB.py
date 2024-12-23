import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        dbname="MuzDripUsers",
        user="postgres",
        password="1243",
        host="localhost",
        port="5432"
    )
    return conn