#!/usr/bin/env python
# coding: utf-8

# ### Criando classes

# In[1]:


class MinhaClasse():
    pass


# In[2]:


class MinhaClasse():
    def metodo():
        pass


# In[4]:


class MinhaClasse():
    atributo = "valor"
    def metodo():
        pass


# In[ ]:


class MinhaClasse():
    def __init__(self):
        self.atributo = "valor"
    def metodo(self):
        pass


# ### Exemplo simples

# In[8]:


class Vendedor():
    def __init__(self, nome):
        self.nome = nome
        self.vendas = 0
        self.bonus = 0
    def vendeu(self, quantidade):
        self.vendas = quantidade
    def calcular_bonus(self, meta):
        if self.vendas > meta:
            self.bonus = self.vendas * 0.01
        else:
            self.bonus = 0


# In[10]:


vendedor1 = Vendedor("Lira")
print(vendedor1.nome, vendedor1.vendas, vendedor1.bonus)


# In[11]:


vendedor1.vendeu(1000)
vendedor1.calcular_bonus(500)
print(vendedor1.nome, vendedor1.vendas, vendedor1.bonus)


# ### Refatorando um código para POO

# In[13]:

#
#get_ipython().system('pip install pyautogui')


# In[ ]:


import pyautogui
import pyperclip
import time

# abrindo o chrome
pyautogui.PAUSE = 1
pyautogui.hotkey('option', 'space')
pyautogui.write("chrome")
pyautogui.press("enter")

# entrando no site da hashtag
link = "https://www.hashtagtreinamentos.com/blog"
pyperclip.copy(link)
pyautogui.hotkey("ctrl", "v")
pyautogui.press("enter")

# aguardar
time.sleep(3)

# clicando no campo de busca
pyautogui.click(x=1508, y=585)

# pesquisando campo de busca
texto = "classe"
pyperclip.copy(texto)
pyautogui.hotkey("ctrl", "v")
pyautogui.press("enter")

# aguardar
time.sleep(3)

# clicar na imagem
pyautogui.click(x=749, y=699)

# aguardar
time.sleep(3)

# extrair o link
pyautogui.click(x=390, y=789, button="right")
pyautogui.press("up")
pyautogui.press("up")
pyautogui.press("enter")

# printar o texto copiado
texto = pyperclip.paste()
print(texto)


# In[24]:


# pegando a posicao de um elemento
for i in range(5):
    print(f"pegando posicao em {5 - i} segundos")
    time.sleep(1)
    
print(pyautogui.position())


# ### Refatorando com classe

# In[43]:


import time
import pyautogui
import pyperclip

class Controlador():
    def __init__(self):
        pyautogui.PAUSE = 1
    def abrir_programa(self, nome_programa):
        pyautogui.press("win")
        pyautogui.write(nome_programa)
        pyautogui.press("enter")
    def escrever(self, texto):
        pyperclip.copy(texto)
        pyautogui.hotkey("ctrl", "v")
    def escrever_e_enter(self, texto):
        self.escrever(texto)
        pyautogui.press("enter")
    def entrar_site(self, site, espera=3):
        self.escrever_e_enter(site)
        self.aguardar(espera)
    def aguardar(self, tempo=3):
        time.sleep(tempo)
    def clicar(self, pos_x, pos_y, botao="left"):
        pyautogui.click(pos_x, pos_y, button=botao)
    def pegar_posicao(self):
        for i in range(5):
            print(f"pegando posicao em {5 - i} segundos")
            time.sleep(1)
        print(pyautogui.position())
    def extrair_link(self, pos_x, pos_y, posicao_link_menu=2):
        self.clicar(pos_x, pos_y, botao="right")
        for i in range(posicao_link_menu):
            pyautogui.press("up")
        pyautogui.press("enter")
        texto = pyperclip.paste()
        print(texto)


# In[44]:


controlador = Controlador()
controlador.abrir_programa("chrome")
controlador.entrar_site("https://www.hashtagtreinamentos.com/blog")
controlador.clicar(1469, 589)
controlador.escrever_e_enter("classe")
controlador.aguardar()
controlador.clicar(749, 699)
controlador.aguardar()
controlador.extrair_link(390, 789)


# In[39]:


controlador.pegar_posicao()


# In[ ]:




