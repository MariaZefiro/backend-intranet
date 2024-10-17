from main import ad_server, app, indice  
from flask import request, jsonify 
from ldap3 import Server, Connection, SIMPLE, ALL  
import jwt  # Importa JWT para geração de token JWT

# Função para gerar token JWT
def generate_token(user_id, username):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Define tempo de expiração do token
    token = jwt.encode({'user_id': str(user_id), 'username': username, 'exp': expiration}, app.secret_key, algorithm='HS256')  # Codifica o token com informações do usuário e chave secreta do app
    return token

# Função para autenticar no Active Directory
def authenticate_in_ad(username, password):
    try:
        server = Server(ad_server, use_ssl=False, get_info=ALL)  # Conecta ao servidor AD
        conn = Connection(server, user=f'{username}@intranet.leste', password=password, authentication=SIMPLE, auto_bind=True)  # Faz a conexão com credenciais fornecidas
        if conn.bind():  
            conn.search(search_base='DC=intranet,DC=leste', search_filter=f'(sAMAccountName={username})', attributes=['displayName'])  # Realiza busca pelo displayName do usuário
            if len(conn.entries) > 0:
                display_name = conn.entries[0].displayName.value  # Obtém o displayName do usuário encontrado
                conn.unbind()  
                return display_name 
            else:
                conn.unbind()  
                return None 
        else:
            conn.unbind()  
            return None 
    except Exception as e:
        print(f'Erro ao autenticar no AD: {str(e)}')  
        return None  

# Endpoint para autenticação de login
@app.route('/api/login2', methods=['PUT'])
def login():
    data = request.get_json()  
    username = data.get('username')  
    password = data.get('password') 

    display_name = authenticate_in_ad(username, password)  # Chama função para autenticar no Active Directory

    if display_name:  # Se autenticação no AD for bem-sucedida
        # CONECTA NO BACNO E INSERE O USUARIO NA TABELA usuarios 
    else:
        # Retorna mensagem de erro em formato JSON com código de status HTTP 401 se autenticação no AD falhou
        return jsonify({'error': 'Usuário e/ou senha inválidos'}), 401
