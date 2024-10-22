from flask import Blueprint, request, jsonify
from db import get_connection, close_connection

edit_post_bp = Blueprint('edit_posts', __name__)

@edit_post_bp.route('/edit_posts', methods=['POST'])
def edit_posts():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    try:
        data = request.get_json()
        post_id = data.get('id')
        usuario_id = data.get('usuario_id')  # O usuário logado
        action = data.get('action')  # 'like' ou 'unlike'
        
        if not post_id or not usuario_id or action not in ['like', 'unlike']:
            return jsonify({"error": "Dados inválidos"}), 400
        
        cursor = conn.cursor()

        # Verificar se o usuário já curtiu o post
        cursor.execute("SELECT * FROM curtidas WHERE post_id = %s AND usuario_id = %s", (post_id, usuario_id))
        curtida_existente = cursor.fetchone()

        if action == 'like':
            # Se o usuário ainda não curtiu, adicionar curtida
            if not curtida_existente:
                cursor.execute("INSERT INTO curtidas (post_id, usuario_id) VALUES (%s, %s)", (post_id, usuario_id))
                cursor.execute("UPDATE posts SET curtidas = curtidas + 1 WHERE id = %s", (post_id,))
        elif action == 'unlike':
            # Se já curtiu, remover curtida
            if curtida_existente:
                cursor.execute("DELETE FROM curtidas WHERE post_id = %s AND usuario_id = %s", (post_id, usuario_id))
                cursor.execute("UPDATE posts SET curtidas = curtidas - 1 WHERE id = %s", (post_id,))

        conn.commit()
        cursor.close()

        return jsonify({"message": "Ação realizada com sucesso"}), 200

    except Exception as e:
        print(f"Erro ao atualizar curtidas: {e}")
        conn.rollback()
        return jsonify({"error": "Erro ao atualizar curtidas"}), 500
    finally:
        close_connection(conn)
