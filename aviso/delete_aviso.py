import os
from flask import Blueprint, jsonify, request
from db import get_connection, close_connection

delete_aviso_bp = Blueprint('delete_aviso', __name__)

@delete_aviso_bp.route('/delete_aviso/<int:id>', methods=['DELETE'])
def delete_carousel(id):
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT titulo FROM avisos WHERE id = %s", (id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Aviso com este ID não encontrado"}), 404

        image_url = result[0]
        
        query = "DELETE FROM avisos WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()


        return jsonify({"message": "Imagem do carrossel removida com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao deletar carrossel: {e}")
        return jsonify({"error": "Erro ao deletar carrossel"}), 500
    finally:
        close_connection(conn)
