import os
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from db import get_connection, close_connection
from datetime import datetime

add_post_bp = Blueprint('add_post', __name__)

UPLOAD_FOLDER = 'uploads/posts'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_unique_filename(directory, filename):
    name, extension = os.path.splitext(filename)  # Separa o nome e a extensão do arquivo
    counter = 1
    new_filename = filename

    # Verifica se o arquivo já existe, se sim, incrementa o contador
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{name}({counter}){extension}"
        counter += 1
    
    return new_filename

@add_post_bp.route('/add_post', methods=['POST'])
def add_post():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    nome = request.form.get('nome')
    data_hora_formato = datetime.now()
    data_hora = data_hora_formato.strftime('%d/%m/%Y %H:%M')
    conteudo = request.form.get('conteudo')

    files = request.files.getlist('file')  # Captura todos os arquivos enviados

    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        cursor = conn.cursor()

        query_post = "INSERT INTO posts (nome_usuario, data_hora, conteudo) VALUES (%s, %s, %s) RETURNING id"
        cursor.execute(query_post, (nome, data_hora, conteudo))
        post_id = cursor.fetchone()[0]

        # Processa os arquivos se existirem
        for file in files:
            if file.filename == '':
                continue

            if not allowed_file(file.filename):
                return jsonify({"error": "Tipo de arquivo não permitido. Apenas imagens são aceitas."}), 400

            filename = secure_filename(file.filename)
            unique_filename = get_unique_filename(UPLOAD_FOLDER, filename)
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(file_path)

            query_image = "INSERT INTO imagens (imagem_url) VALUES (%s) RETURNING id"
            cursor.execute(query_image, (file_path,))
            image_id = cursor.fetchone()[0]

            query_image_post = "INSERT INTO imagens_posts (post_id, image_id) VALUES (%s, %s)"
            cursor.execute(query_image_post, (post_id, image_id))

        conn.commit()
        return jsonify({"message": "Post adicionado com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao adicionar post: {e}")
        return jsonify({"error": "Erro ao adicionar post"}), 500
    finally:
        close_connection(conn)
