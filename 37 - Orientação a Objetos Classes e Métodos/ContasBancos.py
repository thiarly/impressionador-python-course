from datetime import datetime
import pytz
import time



class ContaCorrente():
    """
    Atributos:
        nome (str): Nome do Cliente
        cpf (str): CPF do cliente. Deve ser inserido com pontos e traços
        agencia: Agência do responsável pela conta corrente
        conta: Número da conta corrente do cliente
        saldo: Saldo disponível na conta do cliente
        limite: Limite de Cheque especial daquele cliente
        transações: Histórico de transações do Cliente
    """

    @staticmethod
    def _data_hora():
        fuso_BR = pytz.timezone('Brazil/East')
        horario_BR = datetime.now(fuso_BR)
        return horario_BR.strftime('%d/%m/%Y %H:%M:%S')
    
    def __init__(self, nome, cpf, agencia, conta):
        self.nome = nome
        self.cpf = cpf
        self.saldo = 0
        self.limite = 0
        self.agencia = agencia
        self.conta = conta
        self.transacoes = []


    def consultar_saldo(self):
        print('O seu saldo atual é de R$ {:,.2f}'.format(self.saldo))

    def depositar(self, valor):
        self.saldo += valor
        print('Deposito realizado {}'.format(valor))
        self.transacoes.append((valor, self.saldo, ContaCorrente._data_hora()))

    def _limite_conta(self):
        self.limite = -1000
        return self.limite
    
    def sacar_dinheiro(self, valor):
        if self.saldo - valor < self._limite_conta():
            print("Você não tem saldo suficiente para sacar esse valor.")
            self.consultar_saldo()
        else:
            self.saldo -= valor
            self.transacoes.append((valor, self.saldo, ContaCorrente._data_hora()))

    def consultar_limite_chequeespecial(self):
        print('Seu limite de Cheque Especial é de {}'.format(self._limite_conta()))

    def consultar_historico_transações(self):
        print("Histórico de transações:")
        print("Valor, Saldo, Data e Hora")
        for transacao in self.transacoes:
            print(transacao)
            

    def transferir (self, valor, conta_destino):
        self.saldo -= valor
        self.transacoes.append((valor, self.saldo, ContaCorrente._data_hora()))

        conta_destino.saldo += valor
        conta_destino.transacoes.append((valor, conta_destino.saldo, ContaCorrente._data_hora()))


# Programa
conta_thiarly = ContaCorrente("Thiarly", "044.000.111-22", 8324, 156697)
conta_thiarly.consultar_saldo()

# depositando um dinheiro na conta
conta_thiarly.depositar(1000)
conta_thiarly.consultar_saldo()


# # sacando um dinheiro na conta
# conta_thiarly.sacar_dinheiro(1100)
# print("saldo final:")
# conta_thiarly.consultar_limite_chequeespecial()

print('--'*30)
conta_thiarly.consultar_historico_transações()
print('--'*30)

conta_luca = ContaCorrente('Luca', '022.333.344-43', 8434, 244234)
conta_thiarly.transferir(500, conta_luca)

# conta_thiarly.consultar_saldo()
conta_luca.consultar_saldo()

conta_thiarly.consultar_historico_transações()
conta_luca.consultar_historico_transações()


help(ContaCorrente)