class ContaCorrente():
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.saldo = 0
        self.limite = 0

    def consultar_saldo(self):
        print('O seu saldo atual é de R$ {:,.2f}'.format(self.saldo))

    def depositar(self, valor):
        self.saldo += valor
        print('Deposito realizado {}'.format(valor))

    def _limite_conta(self):
        self.limite = -1000
        return self.limite
    
    def sacar_dinheiro(self, valor):
        if self.saldo - valor < self._limite_conta():
            print("Você não tem saldo suficiente para sacar esse valor.")
            self.consultar_saldo()
        else:
            self.saldo -= valor
            print('Saque realizado {}'.format(valor))

    def consultar_limite_chequeespecial(self):
        print('Seu limite de Cheque Especial é de {}'.format(self._limite_conta()))



# Programa
conta_thiarly = ContaCorrente("Thiarly", "044.000.111-22")
conta_thiarly.consultar_saldo()


# Depositando valor
conta_thiarly.depositar(100000)
conta_thiarly.consultar_saldo()

# Sacando valor
print('-' *60)
conta_thiarly.sacar_dinheiro(111111)
print('-' *60)


print('\n')
print('-' *60)
conta_thiarly.consultar_saldo()
print('-' *60)
conta_thiarly.consultar_limite_chequeespecial()

