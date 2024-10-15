from flask import Blueprint, request, jsonify
from db import get_connection, close_connection
import bleach

edit_date_bp = Blueprint('edit_date', __name__)

@edit_date_bp.route('/save-events', methods=['POST'])
def save_events():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500
    try:
        events = request.get_json()

        if not isinstance(events, list):
            return jsonify({"error": "Dados inválidos"}), 400

        cursor = conn.cursor()

        for event in events:
            event_id = event.get('id')
            nome_data = event.get('nome_data', '')
            data = event.get('data', '')

            if not event_id:
                return jsonify({"error": "ID do evento ausente"}), 400

            # Sanitização usando bleach
            nome_data_clean = bleach.clean(nome_data, tags=['br'], strip=True)
            data_clean = bleach.clean(data, tags=[], strip=True)

            sql = "UPDATE datas SET nome_data = %s, data = %s WHERE id = %s"
            cursor.execute(sql, (nome_data_clean, data_clean, event_id))

        conn.commit()
        cursor.close()
        return jsonify({"message": "Eventos salvos com sucesso"}), 200

    except Exception as e:
        print(f"Erro ao salvar eventos: {e}")
        conn.rollback()
        return jsonify({"error": "Erro ao salvar eventos"}), 500
    finally:
        close_connection(conn)
