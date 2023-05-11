from datetime import datetime
import pytz
from random import randint


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
        self.nome = nome
        self.cpf = cpf
        self._saldo = 0
        self._limite = 0
        self.agencia = agencia
        self.conta = conta
        self._transacoes = []
        self.cartoes = []


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

    @staticmethod
    def _data_hora():
        fuso_BR = pytz.timezone('Brazil/East')
        horario_BR = datetime.now(fuso_BR)
        return horario_BR
    

    def __init__(self, titular, conta_corrente):
        self.numero = randint(1000000000000000, 9999999999999999)
        self.titular = titular
        self.validade = ('{}/{}').format(CartaoCredito._data_hora().month, CartaoCredito._data_hora().year + 5)
        self.cod_seguranca = '{}{}{}'.format(randint(0, 9), randint(0, 9), randint(0, 9))
        self.limite = 1000
        self.conta_corrente = conta_corrente
        conta_corrente.cartoes.append(self)
        self._senha = '12345'


    @property
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self, valor):
        if len(valor) == 4 and valor.isnumeric():
            self._senha = print('Senha alterada, nova senha: {}'.format(valor))

        else:
            print('Nova senha inválida! {}'.format(valor))



