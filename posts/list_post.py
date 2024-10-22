from flask import Blueprint, jsonify, request
from db import get_connection, close_connection

list_post_bp = Blueprint('list_post', __name__)

@list_post_bp.route('/list_post', methods=['GET'])
def get_posts():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        query = """
            SELECT p.id, p.nome_usuario, p.data_hora, p.conteudo, p.curtidas, u.url_foto, i.imagem_url
            FROM posts p
            JOIN usuarios u ON p.nome_usuario = u.nome_usuario
            LEFT JOIN imagens_posts ip ON p.id = ip.post_id
            LEFT JOIN imagens i ON ip.image_id = i.id
            ORDER BY p.data_hora DESC
        """
        cursor.execute(query)
        posts = cursor.fetchall()

        post_list = {}
        for post in posts:
            post_id = post[0]
            if post_id not in post_list:
                post_list[post_id] = {
                    'id': post[0],
                    'author': post[1],
                    'date': post[2],
                    'content': post[3],
                    'curtidas': post[4],
                    'avatar': post[5],
                    'postImages': []  # Lista para armazenar as imagens do post
                }
            # Adiciona a imagem à lista de imagens do post
            if post[5]:
                post_list[post_id]['postImages'].append(post[6])

        # Converte o dicionário em uma lista
        post_list = list(post_list.values())
        
        return jsonify(post_list), 200
    except Exception as e:
        print(f"Erro ao buscar posts: {e}")
        return jsonify({"error": "Erro ao buscar posts"}), 500
    finally:
        close_connection(conn)


@list_post_bp.route('/check_like_status', methods=['GET'])
def check_like_status():
    post_id = request.args.get('post_id')  
    usuario_id = request.args.get('usuario_id')  

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        query = """
            SELECT COUNT(*) > 0
            FROM curtidas
            WHERE post_id = %s AND usuario_id = %s
        """
        cursor.execute(query, (post_id, usuario_id))
        has_liked = cursor.fetchone()[0]  # Retorna True ou False

        return jsonify({"hasLiked": has_liked}), 200
    except Exception as e:
        print(f"Erro ao verificar o status de curtida: {e}")
        return jsonify({"error": "Erro ao verificar o status de curtida"}), 500
    finally:
        close_connection(conn)


