import bcrypt
import mysql.connector

#PREENCHER QUANDO PRECISAR
conn = mysql.connector.connect(
    host='',
    user='',
    password='',
    database=''
)

cursor = conn.cursor()

cursor.execute("SELECT id, nome_usuario, senha_hash FROM usuarios")
usuarios = cursor.fetchall()

for usuario in usuarios:
    user_id = usuario[0]
    nome_usuario = usuario[1]
    senha = usuario[2] 

    # Hash a senha com bcrypt
    hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Atualizar o banco de dados com a nova senha hasheada
    cursor.execute("UPDATE usuarios SET senha_hash = %s WHERE id = %s", (hashed_password, user_id))

conn.commit()

cursor.close()
conn.close()