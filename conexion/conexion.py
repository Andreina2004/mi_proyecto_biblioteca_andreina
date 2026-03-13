import mysql.connector

def get_conn():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="biblioteca_db"
    )
    return conn