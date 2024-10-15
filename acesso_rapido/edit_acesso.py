from flask import Blueprint, request, jsonify
from db import get_connection, close_connection
import bleach

edit_acesso_rapido_bp = Blueprint('edit_acesso_rapido', __name__)

@edit_acesso_rapido_bp.route('/save-acesso', methods=['POST'])
def save_acesso_rapido():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    try:
        acessos = request.get_json()

        if not isinstance(acessos, list):
            return jsonify({"error": "Dados inválidos"}), 400

        cursor = conn.cursor()

        for acesso in acessos:
            acesso_id = acesso.get('id')
            nome = acesso.get('nome', '')

            if not acesso_id:
                return jsonify({"error": "ID do acesso rápido ausente"}), 400

            # Sanitização usando bleach
            nome_clean = bleach.clean(nome, tags=[], strip=True)

            sql = "UPDATE acesso_rapido SET nome = %s WHERE id = %s"
            cursor.execute(sql, (nome_clean, acesso_id))

        conn.commit()
        cursor.close()
        return jsonify({"message": "Acessos Rápidos salvos com sucesso"}), 200

    except Exception as e:
        print(f"Erro ao salvar acessos rápidos: {e}")
        conn.rollback()
        return jsonify({"error": "Erro ao salvar acessos rápidos"}), 500
    finally:
        close_connection(conn)
