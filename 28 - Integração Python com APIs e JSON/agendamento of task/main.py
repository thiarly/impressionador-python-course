import requests
from datetime import datetime

requisicao = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL")

requisicao_dic = requisicao.json()
cotacao_dolar = requisicao_dic["USDBRL"]["bid"]
cotacao_euro = requisicao_dic["EURBRL"]["bid"]
cotacao_btc = requisicao_dic["BTCBRL"]["bid"]

print(f"Cotação Atualizada. {datetime.now()}\nDólar: R${cotacao_dolar}\nEuro: R${cotacao_euro}\nBTC: R${cotacao_btc}")


# google cloud
# aws
# azure
# heroku

# https://dashboard.heroku.com/apps/lscriptpython247/deploy/heroku-git

# If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

# $ heroku login
# Clone the repository

# Use Git to clone lscriptpython247's source code to your local machine.

# $ heroku git:clone -a lscriptpython247 
# $ cd lscriptpython247
# Deploy your changes

# Make some changes to the code you just cloned and deploy them to Heroku using Git.

# $ git add .
# $ git commit -am "make it better"
# $ git push heroku master