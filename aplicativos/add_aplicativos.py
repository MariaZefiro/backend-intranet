import os
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from db import get_connection, close_connection

add_icon_bp = Blueprint('add_icon', __name__)

# Configurações para o upload de arquivos
UPLOAD_FOLDER = 'uploads/icons'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@add_icon_bp.route('/add_icon', methods=['POST'])
def add_icon():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Falha na conexão com o banco de dados"}), 500

    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    
    # Obtenha o nome e o link dos ícones do corpo da requisição
    nome = request.form.get('nome')
    link = request.form.get('link')

    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Tipo de arquivo não permitido. Apenas imagens são aceitas."}), 400

    try:
        # Salva o arquivo na pasta uploads/icons
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Cria o diretório se não existir
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Adiciona o caminho da imagem ao banco de dados
        cursor = conn.cursor()
        query = "INSERT INTO aplicativos (nome, icone_url, link) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, file_path, link))  # Corrigido para incluir todos os parâmetros
        conn.commit()

        return jsonify({"message": "Imagem adicionada aos aplicativos com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao adicionar ao aplicativo: {e}")
        return jsonify({"error": "Erro ao adicionar aplicativo"}), 500
    finally:
        close_connection(conn)
