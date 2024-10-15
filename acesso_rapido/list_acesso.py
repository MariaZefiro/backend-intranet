from flask import Blueprint, request, jsonify
from db import get_connection, close_connection
import bleach

list_acesso_rapido_bp = Blueprint('list_acesso_rapido', __name__)

@list_acesso_rapido_bp.route('/acesso_rapido', methods=['GET'])
def get_acesso_rapido():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM acesso_rapido")
        columns = [col[0] for col in cursor.description]
        acessos = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(acessos), 200
    except Exception as e:
        print(f"Erro ao buscar acesso rápido: {e}")
        return jsonify({"error": "Erro ao buscar acesso rápido"}), 500
    finally:
        close_connection(conn)