
link_cep = 'https://cep.awesomeapi.com.br/json/09760180'
requisicao_cep = requests.get(link_cep)
print(requisicao_cep.json())