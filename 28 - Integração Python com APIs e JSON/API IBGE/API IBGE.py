import requests

link = "https://servicodados.ibge.gov.br/api/v3/agregados/7392/periodos/2014/variaveis/10484?localidades=N1[all]"

requisicao = requests.get(link)
informacoes = requisicao.json()

# import pprint

# pprint.pprint(informacoes[0]['resultados'][0]['series'])

item_busca = informacoes[0]['variavel'] # variavel
resultados = informacoes[0]['resultados'][0]['series'] # series

print(item_busca)
print(resultados)