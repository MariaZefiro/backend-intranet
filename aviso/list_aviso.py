from flask import Blueprint, request, jsonify
from db import get_connection, close_connection
import bleach

list_avisos_bp = Blueprint('list_avisos', __name__)

@list_avisos_bp.route('/list_avisos', methods=['GET'])
def get_avisos():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM avisos")
        columns = [col[0] for col in cursor.description]
        avisos = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(avisos), 200
    except Exception as e:
        print(f"Erro ao buscar avisos: {e}")
        return jsonify({"error": "Erro ao buscar avisos"}), 500
    finally:
        close_connection(conn)
