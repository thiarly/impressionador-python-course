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


# programa

agencia_canudos = agencia(7534942639, 244524240409, 43214)
agencia_canudos.verificar_caixa()

agencia_canudos.emprestar_dinheiro(1200, 440393840389, 0.10)
print(agencia_canudos.caixa)
print(agencia_canudos.emprestimos)

agencia_canudos.adicionar_cliente('Luca', 33333333555, 30000)
print(agencia_canudos.clientes)