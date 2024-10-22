from flask import Blueprint, jsonify, request, session
from db import get_connection, close_connection

get_users_bp = Blueprint('get_users', __name__)

@get_users_bp.route('/usuario', methods=['POST'])
def receber_usuario():
    conn = get_connection()
    cursor = conn.cursor()

    data = request.json
    username = data.get('username')
    nome_completo = data.get('nome_completo')

    if not username or not nome_completo:
        return jsonify({"error": "Faltam dados obrigatórios"}), 400

    try:
        cursor.execute("SELECT * FROM users_ad WHERE usuario = %s", (username,))
        user = cursor.fetchone()

        if user:
            session['username'] = user[0]
            session['nome_completo'] = user[1]
            return jsonify({"message": "Usuário já existe", "usuario": user[0], "nome_completo": user[1]}), 200
        else:
            cursor.execute("INSERT INTO users_ad (usuario, nome_completo) VALUES (%s, %s)", (username, nome_completo))
            conn.commit()

            # Armazenar o novo usuário na sessão
            session['username'] = username
            session['nome_completo'] = nome_completo

            return jsonify({"message": "Usuário adicionado com sucesso", "username": username, "nome_completo": nome_completo}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Erro ao acessar o banco de dados: {e}"}), 500
    finally:
        cursor.close()
        close_connection(conn)