# Importando as bibliotecas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import os
import time

# Para manter o navegador aberto
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Caminho do driver ChromeDriver
nav = webdriver.Chrome(executable_path='/Users/thiarly/opt/anaconda3/chromedriver', options=chrome_options)
nav.maximize_window()

# importar/visualizar a base de dados
tabela_produtos = pd.read_excel("/Users/thiarly/Library/CloudStorage/GoogleDrive-thiarly.cavalcante@gmail.com/My Drive/PROJECTS/Impressionador-Python-Course/35 - Automação Web - Aplicação de Mercado ao Trabalho/Projeto 2 - Google Shopping e Buscape/buscas.xlsx")
print(tabela_produtos)

# Variáveis
produto = 'iphone 12 64 gb'
lista_produto = produto.split(" ")
print(lista_produto)
print(produto)
print('\n')

# DEFINIÇÃO DA FUNÇÃO DE BUSCA DO GOOGLE SHOPPING

def verificar_tem_termos_banidos(lista_termos_banidos, nome):
    tem_termos_banidos = False
    for palavra in lista_termos_banidos:
        if palavra in nome:
            tem_termos_banidos = True
    return tem_termos_banidos


def verificar_tem_todos_termos_produto(lista_termos_nome_produto, nome):
    tem_todos_termos_produtos = True
    for palavra in lista_termos_nome_produto:
        if palavra not in nome:
            tem_todos_termos_produtos = False
    return tem_todos_termos_produtos



def busca_google_shopping(nav, produto, termos_banidos, preco_minimo, preco_maximo):
   
    #Tratamento
    produto = produto.lower()
    termos_banidos = termos_banidos.lower()
    lista_termos_nome_produto = produto.split(" ")
    lista_termos_banidos = termos_banidos.split(" ")
    lista_ofertas = []
    preco_minimo = float(preco_minimo)
    preco_maximo = float(preco_maximo)
    
    #Entra no google e fazer a busca
    nav.get("https://www.google.com/")
    nav.find_element('xpath', '//*[@id="APjFqb"]').send_keys(produto, Keys.ENTER)

    #Entrar na aba shopping:
    elementos = nav.find_elements("class name", "hdtb-mitem")

    for elemento in elementos:
        if "Shopping" in elemento.text: 
            elemento.click()
            break

    #Pegar informações do produto
    lista_resultados = nav.find_elements("class name", "i0X6df")

    for resultado in lista_resultados:
        nome = resultado.find_element("class name", "tAxDx").text
        nome = nome.lower()

        # analisar se ele não tem nenhum termo banido
        tem_termos_banidos = verificar_tem_termos_banidos(lista_termos_banidos, nome)
               
        # analisar se ele tem TODOS os termos do nome do produto
        tem_todos_termos_produtos = (lista_termos_nome_produto, nome)

        # Selecionar só os elementos que tem_termos_banidos = False e ao mesmo tempo tem_todos_termos_produtos = True
        #if tem_termos_banidos == False and tem_todos_termos_produtos == True:
        
        try:
            if not tem_termos_banidos and tem_todos_termos_produtos:
                preco = resultado.find_element("class name", "a8Pemb").text
                preco = preco.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
                preco = float(preco)
                # Verificar se o preço está dentro do preço minimo e máximo
                if preco_minimo <= preco <= preco_maximo:
                    #Lógica para pegar o link, através do parâmetro "href", não foi possível Dessa a variavel elemento_referencia recebe a ("class name", "bONr3b"), que é childre do linkE pegar o "href" atraves do parent "("xpath", "..")"
                    elemento_referencia = resultado.find_element("class name", "bONr3b")
                    elemento_pai = elemento_referencia.find_element("xpath", "..")
                    link = elemento_pai.get_attribute('href')
                    #print(preco, nome, link)
                    lista_ofertas.append((nome, preco, link))
        except ValueError:
            pass
    
    return lista_ofertas


###########################################################################################################################################################
# DEFINIÇÃO DA FUNÇÃO BUSCA DO BUSCAPE

def busca_buscape (nav, produto, termos_banidos, preco_minimo, preco_maximo):
   
    # tratamento
    produto = produto.lower()
    termos_banidos = termos_banidos.lower()
    lista_termos_nome_produto = produto.split(" ")
    lista_termos_banidos = termos_banidos.split(" ")
    lista_ofertas = []
    preco_minimo = float(preco_minimo)
    preco_maximo = float(preco_maximo)
    
    
    #Buscar no Buscape
    nav.get('https://www.buscape.com.br/')
    nav.find_element('xpath', '//*[@id="new-header"]/div[1]/div/div/div[3]/div/div/div[2]/div/div[1]/input').send_keys(produto, Keys.ENTER)
    
    #Pegar os resultados
    while len(nav.find_elements('class name', 'Select_Select__1S7HV')) <1:
        time.sleep(1)
    lista_resultados = nav.find_elements('class name', 'SearchCard_ProductCard_Inner__7JhKb')
    
   
    for resultado in lista_resultados:
        preco = resultado.find_element('class name', 'Text_MobileHeadingS__Zxam2').text
        nome = resultado.find_element('class name', 'SearchCard_ProductCard_Name__ZaO5o').text
        nome = nome.lower()
        link = resultado.get_attribute("href")
    
        # analisar se ele não tem nenhum termo banido
        tem_termos_banidos = verificar_tem_termos_banidos(lista_termos_banidos, nome)
               
        # analisar se ele tem TODOS os termos do nome do produto
        tem_todos_termos_produtos = (lista_termos_nome_produto, nome)
    
    
        #Analisar se o preço está entre o preço minímo e o preço máximo
    try:
        if not tem_termos_banidos and tem_todos_termos_produtos:
            preco = preco.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
            preco = float(preco)
            #Se o preço ta entre preco_minimo e preco_maximo
            if preco_minimo <= preco <= preco_maximo:
                lista_ofertas.append((nome, preco, link))
    except:
        pass
  
          
    #Retornar a lista de ofertas do buscape
    return lista_ofertas

##############################################################################################################################################
# CONSTRUÇÃO DA LISTA DE OFERTAS
tabela_ofertas = pd.DataFrame()

for linha in tabela_produtos.index:
    
    produto = tabela_produtos.loc[linha, "Nome"]
    termos_banidos = tabela_produtos.loc[linha, "Termos banidos"]
    preco_minimo = tabela_produtos.loc[linha, "Preço mínimo"]
    preco_maximo = tabela_produtos.loc[linha, "Preço máximo"]


    lista_ofertas_google_shopping = busca_google_shopping(nav, produto, termos_banidos, preco_minimo, preco_maximo)
    if lista_ofertas_google_shopping:
        tabela_google_shopping = pd.DataFrame(lista_ofertas_google_shopping, columns=['Produto', 'Preço', 'Link'])
        tabela_ofertas = pd.concat([tabela_ofertas, tabela_google_shopping])
    else:
        tabela_google_shopping = None
    
    lista_ofertas_buscape = busca_buscape(nav, produto, termos_banidos, preco_minimo, preco_maximo)
    if lista_ofertas_buscape:
        tabela_buscape = pd.DataFrame(lista_ofertas_buscape, columns=['Produto', 'Preço', 'Link'])
        tabela_ofertas = pd.concat([tabela_ofertas, tabela_buscape])
    else:
        tabela_buscape = None
        
print(tabela_ofertas)


# EXPORTANDO TABELA PARA EXCEL
tabela_ofertas.to_excel('Projeto 2 - Google Shopping e Buscape/PYofertas.xlsx', index=False)


# ENVIANDO A PLANILHA POR EMAIL

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Verificando se existe alguma oferta dentro da tabela de ofertas
if len(tabela_ofertas.index) > 0:
    # Configurações do servidor de email
    servidor_smtp = 'smtp.office365.com'
    porta = 587
    seu_email = 'thiarly.cavalcante@live.com'
    sua_senha = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'

    # Criando o objeto MIMEMultipart para enviar o e-mail
    msg = MIMEMultipart()
    msg['From'] = 'Thiarly Cavalcante <thiarly.cavalcante@live.com>'
    destino = msg['To'] = 'thiarly.cavalcante@gmail.com'
    print(f'E-mail será enviado para: {msg["To"]}')
    msg['Subject'] = 'Produto(s) Encontrado(s) na faixa de preço desejada'

    # Adicionando o conteúdo do e-mail
    texto_html = f"""
    <p>Prezados,</p>
    <p>Encontramos alguns produtos em oferta dentro da faixa de preço desejada. Segue tabela com detalhes</p>
    {tabela_ofertas.to_html(index=False)}
    <p>Qualquer dúvida estou à disposição</p>
    <p>Att.,</p>
    """
    msg.attach(MIMEText(texto_html, 'html'))

    # Enviando o e-mail
    with smtplib.SMTP(servidor_smtp, porta) as server:
        server.starttls()
        server.login(seu_email, sua_senha)
        server.sendmail(seu_email, 'thiarly.cavalcante@gmail.com', msg.as_string())
        print(f'Email enviado com sucesso para: {destino}')


# FINALIZANDO O NAVEGADOR
time.sleep(10)
nav.quit()
