from datetime import datetime
import pytz
import time



class ContaCorrente():

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


# Programa
conta_thiarly = ContaCorrente("Thiarly", "044.000.111-22", 8324, 156697)
conta_thiarly.consultar_saldo()

# depositando um dinheiro na conta
conta_thiarly.depositar(1000)
conta_thiarly.consultar_saldo()

time.sleep(5)

# sacando um dinheiro na conta
conta_thiarly.sacar_dinheiro(1100)
print("saldo final:")
conta_thiarly.consultar_limite_chequeespecial()

print('--'*30)
conta_thiarly.consultar_historico_transações()