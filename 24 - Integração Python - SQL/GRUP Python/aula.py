import mysql.connector

conexao = mysql.connector.connect(
    host='192.168.0.18',
    user='lost',
    password='@Children0',
    database='bdyoutube',
)

cursor = conexao.cursor()


# CRUD

# CREATE
# nome_produto = "pirulito"
# valor = 2.50

# comando = f'INSERT INTO vendas (nome_produto, valor) VALUES ("{nome_produto}", {valor})'
# cursor.execute(comando)
# conexao.commit() # edita o banco de dados

# READ
# comando = f'SELECT * FROM vendas'
# cursor.execute(comando)
# resultado = cursor.fetchall() # ler o banco de dados
# print(resultado)

# UPDATE
# nome_produto = "pirulito"
# valor = 1

# comando = f'UPDATE vendas SET valor = {valor} WHERE nome_produto = "{nome_produto}"'
# cursor.execute(comando)
# conexao.commit() # edita o banco de dados


# DELETE
nome_produto = "pirulito"

comando = f'DELETE FROM vendas WHERE nome_produto = "{nome_produto}"'
cursor.execute(comando)
conexao.commit() # edita o banco de dados


cursor.close()
conexao.close()