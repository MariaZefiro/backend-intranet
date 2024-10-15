from flask import Blueprint, jsonify
from db import get_connection, close_connection

aplicativos_bp = Blueprint('aplicativos', __name__)

@aplicativos_bp.route('/aplicativos', methods=['GET'])
def get_aplicativos():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM aplicativos")  
        result = cursor.fetchall()
        cursor.close()
        return jsonify(result), 200
    except Exception as e:
        print(f"Erro ao obter aplicativos: {e}")
        return jsonify({"error": "Erro ao obter aplicativos"}), 500
    finally:
        close_connection(conn)
