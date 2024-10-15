from flask import Blueprint, request, jsonify
from db import get_connection, close_connection
import bleach

add_avisos_bp = Blueprint('add_avisos', __name__)

@add_avisos_bp.route('/add-aviso', methods=['POST'])
def add_aviso():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    try:
        aviso = request.get_json()
        
        if not isinstance(aviso, dict):
            return jsonify({"error": "Dados inválidos"}), 400

        titulo = aviso.get('titulo', '')

        if not titulo:
            return jsonify({"error": "Título do aviso ausente"}), 400

        # Sanitização usando bleach
        titulo_clean = bleach.clean(titulo, tags=[], strip=True)

        sql = "INSERT INTO avisos (titulo) VALUES (%s)"
        cursor = conn.cursor()
        cursor.execute(sql, (titulo_clean,))
        
        conn.commit()
        cursor.close()
        return jsonify({"message": "Aviso adicionado com sucesso"}), 200

    except Exception as e:
        print(f"Erro ao adicionar aviso: {e}")
        conn.rollback()
        return jsonify({"error": "Erro ao adicionar aviso"}), 500
    finally:
        close_connection(conn)
