import os
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from db import get_connection, close_connection

add_carousel_bp = Blueprint('add_carousel', __name__)

# Configurações para o upload de arquivos
UPLOAD_FOLDER = 'uploads/carousel'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@add_carousel_bp.route('/carousel', methods=['POST'])
def add_carousel():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Tipo de arquivo não permitido. Apenas imagens são aceitas."}), 400

    try:
        # Salva o arquivo na pasta uploads/carousel
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Cria o diretório se não existir
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Adiciona o caminho da imagem ao banco de dados
        cursor = conn.cursor()
        query = "INSERT INTO carrossel (image_url) VALUES (%s)"
        cursor.execute(query, (file_path,))  # Corrigido para ser uma tupla
        conn.commit()

        return jsonify({"message": "Imagem adicionada ao carrossel com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao adicionar ao carrossel: {e}")
        return jsonify({"error": "Erro ao adicionar ao carrossel"}), 500
    finally:
        close_connection(conn)
