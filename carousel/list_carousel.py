from flask import Blueprint, jsonify
from db import get_connection, close_connection
import os

list_carousel_bp = Blueprint('list_carousel', __name__)

@list_carousel_bp.route('/carousel', methods=['GET'])
def get_carousel():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM carrossel")
        result = cursor.fetchall()
        cursor.close()
        return jsonify(result), 200
    except Exception as e:
        print(f"Erro ao obter carrossel: {e}")
        return jsonify({"error": "Erro ao obter carrossel"}), 500
    finally:
        close_connection(conn)
