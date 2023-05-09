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
        _limite: Limite de Cheque especial daquele cliente
        transações: Histórico de transações do Cliente
    """

    @staticmethod
    def _data_hora():
        fuso_BR = pytz.timezone('Brazil/East')
        horario_BR = datetime.now(fuso_BR)
        return horario_BR.strftime('%d/%m/%Y %H:%M:%S')
    
    def __init__(self, nome, cpf, agencia, conta):
        self._nome = nome
        self._cpf = cpf
        self._saldo = 0
        self._limite = 0
        self._agencia = agencia
        self._conta = conta
        self._transacoes = []
        self._cartoes = []


    def consultar_saldo(self):
        print('O seu saldo atual é de R$ {:,.2f}'.format(self._saldo))

    def depositar(self, valor):
        self._saldo += valor
        print('Deposito realizado {}'.format(valor))
        self._transacoes.append((valor, self._saldo, ContaCorrente._data_hora()))

    def _limite_conta(self):
        self._limite = -1000
        return self._limite
    
    def sacar_dinheiro(self, valor):
        if self._saldo - valor < self._limite_conta():
            print("Você não tem _saldo suficiente para sacar esse valor.")
            self.consultar_saldo()
        else:
            self._saldo -= valor
            self._transacoes.append((valor, self._saldo, ContaCorrente._data_hora()))

    def consultar_limite_chequeespecial(self):
        print('Seu _limite de Cheque Especial é de {}'.format(self._limite_conta()))

    def consultar_historico_transações(self):
        print("Histórico de transações:")
        print("Valor, Saldo, Data e Hora")
        for transacao in self._transacoes:
            print(transacao)
            

    def transferir (self, valor, conta_destino):
        self._saldo -= valor
        self._transacoes.append((valor, self._saldo, ContaCorrente._data_hora()))

        conta_destino._saldo += valor
        conta_destino._transacoes.append((valor, conta_destino._saldo, ContaCorrente._data_hora()))


class CartaoCredito:
    def __init__(self, titular, conta_corrente):
        self.numero = None
        self.titular = titular
        self.validade = None
        self.cod_seguranca = None
        self.limite = None
        self.conta_corrente = conta_corrente
        conta_corrente._cartoes.append(self)

# Programa
conta_thiarly = ContaCorrente("Thiarly", "044.000.111-22", 8324, 156697)


cartao_thiarly = CartaoCredito('Thiarly', conta_thiarly)

print(cartao_thiarly.conta_corrente._conta )