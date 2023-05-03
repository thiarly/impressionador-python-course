class tv():

#atributo
    def __init__(self):
        self.cor = "preta"
        self.ligada = False
        self.tamanho = 55
        self.canal = "Amazon Prime"
        self.volume = 10

 #metodo
    def mudar_canal(self):
        self.canal = "grobo"      

#metodo
    def mudar_canal1(self, novo_canal):
        self.canal = novo_canal 
        print('Canal alterado para {}'.format(novo_canal))



tv_quintal = tv()
tv_cozinha = tv()

tv_quintal.mudar_canal1("HBO")
tv_cozinha.mudar_canal1("youtube")
print(tv_quintal.canal)
print(tv_cozinha.canal)

print('\n')



tv_sala = tv()
tv_quarto = tv()

#mudando metodo tv_sala para mudar canal
tv_sala.mudar_canal()

print(tv_sala.canal)
print(tv_quarto.canal)


print('\n')
print(tv_quarto.cor, tv_quarto.ligada, tv_quarto.tamanho, tv_quarto.canal, tv_quarto.volume)

 
