import mysql.connector
from config import db_user, db_pass, db_port, db_ip, db_name

db_config = {
    'user': db_user,
    'password': db_pass,
    'host': db_ip,
    'port': db_port,
    'database': db_name,
    'raise_on_warnings': True,
    'pool_size': 5, 
}

def get_connection():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

def close_connection(conn):
    if conn and conn.is_connected():
        conn.close()
