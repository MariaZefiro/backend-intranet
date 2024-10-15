from flask import Blueprint, jsonify, request
from db import get_connection, close_connection

list_users_bp = Blueprint('list_users', __name__)

@list_users_bp.route('/users', methods=['GET'])
def get_users():
    username = request.args.get('username') 
    if not username:
        return jsonify({"error": "Username não fornecido"}), 400

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE nome_usuario = %s", (username,))
        result = cursor.fetchall()
        cursor.close()
        
        if len(result) == 0:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        return jsonify(result), 200
    except Exception as e:
        print(f"Erro ao obter usuário: {e}")
        return jsonify({"error": "Erro ao obter usuário"}), 500
    finally:
        close_connection(conn)
