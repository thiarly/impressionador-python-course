# Criar o projeto no Firebase

# Link documento REST API Firebase
# https://firebase.google.com/docs/reference/rest/database

# Criar o Database (atenção às regras de segurança)
# Estrutura de árvore

# Interação com o Database (REST API)
import requests
import json

link = "seu_link_aqui"

# Criar uma venda (POST)
dados = {'cliente': 'alon', 'preco': 150, 'produto': 'teclado'}
requisicao = requests.post(f'{link}/Vendas/.json', data=json.dumps(dados))
print(requisicao)
print(requisicao.text)

# Criar um novo produto (POST)
dados = {'nome': 'teclado', 'preco': 150, 'quantidade': 80}
requisicao = requests.post(f'{link}/Produtos/.json', data=json.dumps(dados))
print(requisicao)
print(requisicao.text)

# Editar a venda (PATCH)
dados = {'cliente': 'lira'}
requisicao = requests.patch(f'{link}/Vendas/-MyJSm_N0S8KhCc3nAku/.json', data=json.dumps(dados))
print(requisicao)
print(requisicao.text)

# Pegar uma venda específico ou todas as vendas (GET)
requisicao = requests.get(f'{link}/Vendas/.json')
print(requisicao)
dic_requisicao = requisicao.json()
id_alon = None
for id_venda in dic_requisicao:
    cliente = dic_requisicao[id_venda]['cliente']
    if cliente == "alon":
        print(id_venda)
        id_alon = id_venda

# Deletar uma venda (DELETE)
requisicao = requests.delete(f'{link}/Vendas/{id_alon}/.json')
print(requisicao)
print(requisicao.text)