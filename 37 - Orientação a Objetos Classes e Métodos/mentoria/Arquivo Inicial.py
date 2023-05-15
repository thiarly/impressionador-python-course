import pyautogui
import pyperclip
import time

class MeuRobo():

    def __init__(self, tempo_espera):
        self.tempo_espera = tempo_espera
        pyautogui.PAUSE = 1
    def  abrir_programa(self, nome_programa):
        pyautogui.hotkey('option', 'space')
        pyautogui.write(nome_programa)
        pyautogui.press("enter")


robo = MeuRobo(3)
robo.abrir_programa("chrome")