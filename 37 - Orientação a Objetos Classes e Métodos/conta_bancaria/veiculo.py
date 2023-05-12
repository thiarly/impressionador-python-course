class Carro:
    
    #atributos
    def __init__(self, marca, modelo, cor, ano):
        self.marca = marca
        self.modelo = modelo
        self.cor = cor
        self.ano = ano
        self.velocidade = 0
       

    #metodos
    def acelerar(self):
        self.velocidade += 10

    def frear(self):
        self.velocidade -= 10

    def obter_velocidade(self):
        return self.velocidade
    
    #programa


carro1 = Carro("Fiat", "Toro", "preto", 2023)

#Acessando atributos do objeto
print(carro1.marca, carro1.modelo, carro1.cor, carro1.ano)

#Acessando métodos do objeto

for i in range (5):
    carro1.acelerar()

for i in range(1):
    carro1.frear()

if carro1.obter_velocidade() > 30:
    print('Carro na velocidade permitida {}km/h'.format(carro1.obter_velocidade()))

else:
    print('Carro abaixo da velocidade permitida {}km/h'.format(carro1.obter_velocidade()))



print('\n')

velocidade = []

for i in range(10):
    carro1.acelerar()
    velocidade.append(carro1.velocidade)

print(velocidade[-1])
