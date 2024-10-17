from flask import Blueprint, request, jsonify
from db import get_connection, close_connection

edit_post_bp = Blueprint('edit_posts', __name__)

@edit_post_bp.route('/edit_posts', methods=['POST'])
def edit_posts():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    try:
        # Recebe os dados do post
        data = request.get_json()

        # Valida se 'posts' está presente e é uma lista
        posts = data.get('posts', [])
        if not isinstance(posts, list):
            return jsonify({"error": "Dados inválidos"}), 400

        cursor = conn.cursor()

        for post in posts:
            post_id = post.get('id')
            curtidas = post.get('curtidas')

            # Verifica se 'id' está presente e 'curtidas' é um número válido
            if not post_id or not isinstance(curtidas, int):
                return jsonify({"error": "ID ou curtidas inválidos"}), 400

            # Atualiza o número de curtidas
            sql = "UPDATE posts SET curtidas = %s WHERE id = %s"
            cursor.execute(sql, (curtidas, post_id))

        conn.commit()
        cursor.close()
        return jsonify({"message": "Posts salvos com sucesso"}), 200

    except Exception as e:
        print(f"Erro ao salvar posts: {e}")
        conn.rollback()
        return jsonify({"error": "Erro ao salvar posts"}), 500
    finally:
        close_connection(conn)
