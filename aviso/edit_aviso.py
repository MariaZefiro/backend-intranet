from flask import Blueprint, request, jsonify
from db import get_connection, close_connection
import bleach

edit_avisos_bp = Blueprint('edit_avisos', __name__)

@edit_avisos_bp.route('/save-avisos', methods=['POST'])
def save_avisos():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    try:
        avisos = request.get_json()

        if not isinstance(avisos, list):
            return jsonify({"error": "Dados inválidos"}), 400

        cursor = conn.cursor()

        for aviso in avisos:
            aviso_id = aviso.get('id')
            titulo = aviso.get('titulo', '')

            if not aviso_id:
                return jsonify({"error": "ID do aviso ausente"}), 400

            # Sanitização usando bleach
            titulo_clean = bleach.clean(titulo, tags=[], strip=True)

            sql = "UPDATE avisos SET titulo = %s WHERE id = %s"
            cursor.execute(sql, (titulo_clean, aviso_id))

        conn.commit()
        cursor.close()
        return jsonify({"message": "Avisos salvos com sucesso"}), 200

    except Exception as e:
        print(f"Erro ao salvar avisos: {e}")
        conn.rollback()
        return jsonify({"error": "Erro ao salvar avisos"}), 500
    finally:
        close_connection(conn)
