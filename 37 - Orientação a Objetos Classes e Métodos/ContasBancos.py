class ContaCorrente():
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.saldo = 0



# Programa


conta_thiarly = ContaCorrente("Thiarly", "044.000.111-22")

print(conta_thiarly.nome)
print(conta_thiarly.cpf)
print(conta_thiarly.saldo)


