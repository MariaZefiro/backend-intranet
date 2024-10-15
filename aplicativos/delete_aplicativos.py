import os
from flask import Blueprint, jsonify, request
from db import get_connection, close_connection

delete_icon_bp = Blueprint('delete_icon', __name__)

@delete_icon_bp.route('/delete_icon/<int:id>', methods=['DELETE'])
def delete_icon(id):
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try: 
        cursor = conn.cursor()
        
        cursor.execute("SELECT icone_url FROM aplicativos WHERE id = %s", (id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Ícone com este ID não encontrado"}), 404

        icone_url = result[0]
        
        query = "DELETE FROM aplicativos WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()

        # Exclui a imagem física
        image_path = os.path.join(icone_url)  # Ajuste o caminho conforme necessário
        if os.path.exists(image_path):
            os.remove(image_path)
        else:
            print(f"Imagem {icone_url} não encontrada em {image_path}.")

        return jsonify({"message": "Ícone removido com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao deletar ícone: {e}")
        return jsonify({"error": "Erro ao deletar ícone"}), 500
    finally:
        close_connection(conn)
