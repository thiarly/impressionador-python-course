import pandas as pd
import win32com.client as win32

# Importar a base de dados
tabela = pd.read_excel('Vendas.xlsx')

# visualizar a base de dados
pd.set_option('display.max_columns', None)
print('=' * 60)
print('Tabela de Analise')
print('=' * 60)
print(tabela)
print('\n')


# faturamento por loja
faturamento = tabela[["ID Loja", 'Valor Final']].groupby('ID Loja').sum()
print('=' * 60)
print(f'Faturamento Total das Lojas:')
print('=' * 60)
print(faturamento)
print('\n')


# quantidade de produtos vendidos por loja
quantidade = tabela[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
print('=' * 60)
print(f'Quantidade total por loja')
print('=' * 60)
print(quantidade)
print('\n')


# ticket medio por produto em cada loja
ticket_medio = (faturamento['Valor Final'] / quantidade['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0: 'Ticket Medio'})
print('*' * 60)
print(f'Ticket Medio por Loja')
print('*' * 60)
print(ticket_medio)
print('\n')

# enviar um e-mail com relatorio

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'thiarly.cavalcante@gmail.com'
mail.Subject = 'Relatório de Vendas por Loja'
mail.HTMLBody = f'''
<p>Prezados,</p>

<p>Segue o Relatório de Vendas por cada Loja.</p>

<p>Faturamento:</p>
{faturamento.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})}

<p>Quantidade Vendida:</p>
{quantidade.to_html()}

<p>Ticket Médio dos Produtos em cada Loja:</p>
{ticket_medio.to_html(formatters={'Ticket Médio': 'R${:,.2f}'.format})}

<p>Qualquer dúvida estou à disposição.</p>

<p>Att.,</p>
<p>Lira</p>
'''

mail.Send()

print('Email Enviado')