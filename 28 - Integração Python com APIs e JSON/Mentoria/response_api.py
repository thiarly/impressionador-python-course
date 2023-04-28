import requests

link = "https://api.thiarly.repl.co/vendas/produtos/Drone"

requisicao = requests.get(link)

print(requisicao.json())
