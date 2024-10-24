from flask import Flask, send_from_directory
from flask_cors import CORS
from config import app_ip
import os

app = Flask(__name__)
CORS(app)

app.secret_key = "sJG3u3Cx6hMa1wbW"

# Registrar Blueprints após a criação do app
from data.list_date import list_date_bp
from data.edit_date import edit_date_bp
from carousel.list_carousel import list_carousel_bp
from carousel.add_carousel import add_carousel_bp
from carousel.delete_carousel import delete_carousel_bp
from aviso.edit_aviso import edit_avisos_bp
from aviso.list_aviso import list_avisos_bp
from acesso_rapido.list_acesso import list_acesso_rapido_bp
from acesso_rapido.edit_acesso import edit_acesso_rapido_bp
from aviso.add_aviso import add_avisos_bp
from aviso.delete_aviso import delete_aviso_bp
from aplicativos.list_aplicativos import aplicativos_bp
from aplicativos.add_aplicativos import add_icon_bp
from aplicativos.delete_aplicativos import delete_icon_bp
from users.list_users import list_users_bp
from users.get_user import get_users_bp
from posts.add_post import add_post_bp
from posts.list_post import list_post_bp
from posts.list_post import check_like_status
from posts.edit_post import edit_post_bp
from posts.delete_post import delete_post_bp

from login import login_bp

app.register_blueprint(list_date_bp, url_prefix='/api')
app.register_blueprint(edit_date_bp, url_prefix='/api')
app.register_blueprint(add_carousel_bp, url_prefix='/api')
app.register_blueprint(list_carousel_bp, url_prefix='/api')
app.register_blueprint(delete_carousel_bp, url_prefix='/api')
app.register_blueprint(edit_avisos_bp, url_prefix='/api')
app.register_blueprint(list_avisos_bp, url_prefix='/api')
app.register_blueprint(list_acesso_rapido_bp, url_prefix='/api')
app.register_blueprint(edit_acesso_rapido_bp, url_prefix='/api')
app.register_blueprint(add_avisos_bp, url_prefix='/api')
app.register_blueprint(delete_aviso_bp, url_prefix='/api')
app.register_blueprint(aplicativos_bp, url_prefix='/api')
app.register_blueprint(add_icon_bp, url_prefix='/api')
app.register_blueprint(delete_icon_bp, url_prefix='/api')
app.register_blueprint(list_users_bp, url_prefix='/api')
app.register_blueprint(add_post_bp, url_prefix='/api')
app.register_blueprint(list_post_bp, url_prefix='/api')
app.register_blueprint(edit_post_bp, url_prefix='/api')
app.register_blueprint(delete_post_bp, url_prefix='/api')
app.register_blueprint(get_users_bp, url_prefix='/api')

app.register_blueprint(login_bp, url_prefix='/api')

# Rota para servir arquivos de imagem
@app.route('/uploads/<path:filename>')
def upload_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'uploads'), filename)

if __name__ == '__main__':
    app.run(host=app_ip, debug=True)
