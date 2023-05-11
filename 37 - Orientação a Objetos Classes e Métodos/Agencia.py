class agencia:

    def __init__(self, telefone, cnpj, numero):
        self.telefone = telefone
        self.cnpj = cnpj
        self.numero = numero
        self.clientes = []
        self.caixa = 2000000
        self.emprestimos = []


    def verificar_caixa(self):
        if self.caixa < 1000000:
            print('Caixa da agência insuficiente R$ {:.2f}'.format(self.caixa))
        
        else:
            print('Caixa da filial está solvente R$ {:.2f}'.format(self.caixa))

    def emprestar_dinheiro(self, valor, cpf, juros):
        if self.caixa > 1000000 and valor < self.caixa:
            self.emprestimos.append((valor, cpf, juros))
            print('Valor emprestados {:.2f}, '.format(valor))
        
        else:
            print('Caixa insuficiente para emprestimo')


    def adicionar_cliente(self, nome, cpf, patrimonio):
        self.clientes.append((nome, cpf, patrimonio))



class AgenciaVirtual(agencia):
    pass

class AgenciaComum(agencia):
    pass

class AgenciaPremium(agencia):
    pass

agencia_canudos_virtual = AgenciaVirtual(1434343, 13333388888, 14242)
agencia_canudos_virtual.caixa = 11000
print('Agencia: {} Caixa R$ {}'.format(agencia_canudos_virtual.numero, agencia_canudos_virtual.caixa)) 
print('\n')


agencia_canudos_premium = AgenciaPremium(2434343, 23333388888, 24242)
agencia_canudos_premium.caixa = 12000
print('Agencia: {} Caixa R$ {}'.format(agencia_canudos_premium.numero, agencia_canudos_premium.caixa)) 
print('\n')


agencia_canudos_comum = AgenciaComum(3434343, 33333388888, 34242)
agencia_canudos_comum.caixa = 14000
print('Agencia: {} Caixa R$ {}'.format(agencia_canudos_comum.numero, agencia_canudos_comum.caixa)) 
print('\n')
