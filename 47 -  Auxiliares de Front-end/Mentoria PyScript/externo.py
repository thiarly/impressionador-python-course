import pandas as pd
import matplotlib.pyplot as plt

from pyodide.http import open_url
link = open_url("https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv")
tabela = pd.read_csv(link)
pyscript.write("tabela_paises",tabela)

contagem = tabela["Region"].value_counts()
fig, eixo = plt.subplots()
contagem.plot(ax=eixo)
pyscript.write("grafico_qtde", fig)
