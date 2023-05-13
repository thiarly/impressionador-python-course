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
    pass


# ### Refatorando um código para POO

# In[13]:


get_ipython().system('pip install pyautogui')


# In[ ]:


import pyautogui
import pyperclip
import time

# abrindo o chrome
pyautogui.PAUSE = 1
pyautogui.press("win")
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

# In[ ]:




