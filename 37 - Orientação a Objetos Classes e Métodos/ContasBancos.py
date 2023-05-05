class ContaCorrente():
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.saldo = 0

    def consultar_saldo(self):
        print('O seu saldo atual é de R$ {:,.2f}'.format(self.saldo))

    def depositar(self, valor):
        self.saldo += valor
        print('Deposito realizado {}'.format(valor))

    def sacar_dinheiro(self, valor):
        self.saldo -= valor
        print('Saque realizado {}'.format(valor))



# Programa
conta_thiarly = ContaCorrente("Thiarly", "044.000.111-22")
conta_thiarly.consultar_saldo()


# Depositando valor
conta_thiarly.depositar(100000)
conta_thiarly.consultar_saldo()

# Sacando valor
conta_thiarly.sacar_dinheiro(2500)
conta_thiarly.consultar_saldo()


# print(conta_thiarly.nome)
# print(conta_thiarly.cpf)
# print(conta_thiarly.saldo)


