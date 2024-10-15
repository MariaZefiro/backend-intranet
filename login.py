from flask import Flask, request, jsonify, Blueprint
import bcrypt
from db import get_connection, close_connection

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        data = request.json

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Usuário e senha são obrigatórios"}), 400  

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE BINARY nome_usuario = %s", (username,))
        user = cursor.fetchone()

        if user:
            # Verifica a senha informada
            if bcrypt.checkpw(password.encode('utf-8'), user['senha_hash'].encode('utf-8')):
                return jsonify({"success": True, "message": "Login realizado com sucesso", "isAdmin": True}), 200
            else:
                return jsonify({"success": False, "message": "Usuário ou senha incorretos"}), 401
        else:
            return jsonify({"success": False, "message": "Usuário ou senha incorretos"}), 401
            
    except Exception as e:
        print(f"Erro durante o login: {e}") 
        conn.rollback()
        return jsonify({"error": "Ocorreu um erro durante o login"}), 500
    
    finally:
        close_connection(conn)
