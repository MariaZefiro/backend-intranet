from flask import Blueprint, jsonify
from db import get_connection, close_connection

list_date_bp = Blueprint('list_date', __name__)

@list_date_bp.route('/events', methods=['GET'])
def get_events():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM datas")
        result = cursor.fetchall()
        
        cursor.close()
        return jsonify(result), 200
    except Exception as e:
        print(f"Erro ao obter eventos: {e}")
        return jsonify({"error": "Erro ao obter eventos"}), 500
    finally:
        close_connection(conn)
