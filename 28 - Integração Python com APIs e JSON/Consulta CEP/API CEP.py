import requests
import pandas as pd

cep = '097.601-80'
cep = cep.replace("-", "").replace(".", "").replace(" ", "")



if len(cep) == 8:
    link = f'http://viacep.com.br/ws/{cep}/json/'
    requisicao = requests.get(link)
    print(requisicao.json())

    dic_requisicao = requisicao.json()

    uf = dic_requisicao["uf"]
    cidade = dic_requisicao["localidade"]
    bairro = dic_requisicao["bairro"]

    print(cidade, bairro, uf)
    print('\n')
else:

    print('Cep Inválido, por gentileza confirmar o cep.')
    print('\n')



uf = 'SP'
cidade = 'São Paulo'
endereco = "primeiro"

link = f'http://viacep.com.br/ws/{uf}/{cidade}/{endereco}/json/'
requisicao = requests.get(link)

dic_requisicao = requisicao.json()
print(dic_requisicao)


tabela = pd.DataFrame(dic_requisicao)
print(tabela)