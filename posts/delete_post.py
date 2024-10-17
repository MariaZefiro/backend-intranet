import os
from flask import Blueprint, request, jsonify
from db import get_connection, close_connection

delete_post_bp = Blueprint('delete_posts', __name__)

@delete_post_bp.route('/delete_post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()

        # Inicia uma transação
        conn.start_transaction()

        # 1. Buscar todas as imagens associadas ao post
        query_images = """
            SELECT imagens.imagem_url, imagens.id 
            FROM imagens_posts 
            JOIN imagens ON imagens_posts.image_id = imagens.id 
            WHERE imagens_posts.post_id = %s
        """
        cursor.execute(query_images, (post_id,))
        images = cursor.fetchall()

        # 2. Excluir as associações em imagens_posts
        query_delete_imagens_posts = "DELETE FROM imagens_posts WHERE post_id = %s"
        cursor.execute(query_delete_imagens_posts, (post_id,))

        # 3. Para cada imagem, verificar se está associada a outros posts
        for image in images:
            image_path, image_id = image

            # Verifica se a imagem está associada a outros posts
            query_check_associations = "SELECT COUNT(*) FROM imagens_posts WHERE image_id = %s"
            cursor.execute(query_check_associations, (image_id,))
            count = cursor.fetchone()[0]

            if count == 0:
                # A imagem não está mais associada a nenhum post
                if os.path.exists(image_path):
                    os.remove(image_path)
                else:
                    print(f"Imagem não encontrada no caminho: {image_path}")

                # Excluir a imagem da tabela imagens
                query_delete_image = "DELETE FROM imagens WHERE id = %s"
                cursor.execute(query_delete_image, (image_id,))

        # 4. Excluir o post
        query_delete_post = "DELETE FROM posts WHERE id = %s"
        cursor.execute(query_delete_post, (post_id,))

        # Confirmar a transação
        conn.commit()
        return jsonify({"message": "Post excluído com sucesso"}), 200

    except Exception as e:
        # Reverter a transação em caso de erro
        conn.rollback()
        print(f"Erro ao excluir post: {e}")
        return jsonify({"error": "Erro ao excluir post"}), 500
    finally:
        close_connection(conn)
