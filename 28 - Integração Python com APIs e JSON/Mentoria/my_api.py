import requests

link = "https://api.thiarly.repl.co/luca"

requisicao = requests.get(link)

print(requisicao.json())


print('\n')

from flask import Flask

app = Flask(__name__) # -> cria o site

@app.route("/") # -> diz em qual link da função vai rodar
def hello_world(): # -> função
    return {"Atendimento": "Geral"} # -> texto que será exibido


@app.route("/thiarly") # -> diz em qual link da função vai rodar
def thiarly (): # -> função
    return {"Chama": "Vaqueja"} # -> texto que será exibido


@app.route("/luca") # -> diz em qual link da função vai rodar
def luca (): # -> função
    return {"Brinquedo": "Batman", "Cor": "Preto"} # -> texto que será exibido

app.run() # -> executa o site
