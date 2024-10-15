import os
from flask import Blueprint, jsonify, request
from db import get_connection, close_connection

delete_carousel_bp = Blueprint('delete_carousel', __name__)

@delete_carousel_bp.route('/delete_carousel/<int:id>', methods=['DELETE'])
def delete_carousel(id):
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT image_url FROM carrossel WHERE id = %s", (id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Carrossel com este ID não encontrado"}), 404

        image_url = result[0]
        
        query = "DELETE FROM carrossel WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()

        # Exclui a imagem física
        image_path = os.path.join(image_url)  
        if os.path.exists(image_path):
            os.remove(image_path)
        else:
            print(f"Imagem {image_url} não encontrada em {image_path}.")

        return jsonify({"message": "Imagem do carrossel removida com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao deletar carrossel: {e}")
        return jsonify({"error": "Erro ao deletar carrossel"}), 500
    finally:
        close_connection(conn)
