from flask import Blueprint, request, jsonify
from ldap3 import Server, Connection, SIMPLE, ALL  
import jwt  # Importa JWT para geração de token JWT
import bcrypt
import datetime
from config import ad_server
from db import get_connection, close_connection

login_bp = Blueprint('login_bp', __name__)


def authenticate_in_db(username, nome_completo, conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users_ad WHERE BINARY usuario = %s AND nome_completo = %s", (username, nome_completo))
    user = cursor.fetchone()

    if user:
        return user  # Retorna o usuário caso a autenticação seja bem-sucedida
    
    return None  # Retorna None se a autenticação falhar

def authenticate_in_db2(username, nome_completo, conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE BINARY nome_usuario = %s", (username,))
    user = cursor.fetchone()

    if user:
        # Verifica a senha informada
        if bcrypt.checkpw(nome_completo.encode('utf-8'), user['senha_hash'].encode('utf-8')):
            return user  # Retorna o usuário caso a autenticação seja bem-sucedida
    return None  # Retorna None se a autenticação falhar

# Endpoint unificado para autenticação de login
@login_bp.route('/login', methods=['POST'])
def login():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        data = request.json

        username = data.get('username')
        nome_completo = data.get('nome_completo')

        if not username or not nome_completo:
            return jsonify({"error": "Usuário e senha são obrigatórios"}), 400  

        user = authenticate_in_db(username, nome_completo, conn)
        if user:  # Se a autenticação na tabela `usuarios` for bem-sucedida
            return jsonify({
                "success": True,
                "message": "Login realizado com sucesso",
                "id": user['id'], 
                "nome_completo": user['nome_completo'],  
            }), 200
        else:
            user = authenticate_in_db2(username, nome_completo, conn)
            if user:  # Se a autenticação na tabela `usuarios` for bem-sucedida
                return jsonify({
                    "success": True,
                    "message": "Login realizado com sucesso",
                    "id": user['id'], 
                    "nome_completo": user['nome_usuario'],  
                }), 200
            else:
                return jsonify({"error": "Usuário ou senha incorretos"}), 401  # Adicionando retorno de erro apropriado
    except Exception as e:
        conn.rollback()
        print(f"Erro durante o login: {e}") 
        return jsonify({"error": "Ocorreu um erro durante o login"}), 500
    
    finally:
        close_connection(conn)
