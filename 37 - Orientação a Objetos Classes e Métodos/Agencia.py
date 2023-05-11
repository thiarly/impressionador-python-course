from random import randint

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
    
    def __init__(self, site, telefone, cnpj):
        self.site = site
        super().__init__(telefone, cnpj, 1000)
        self.caixa = 1000000
        self.caixa_paypal = 0


    def depositar_paypal(self, valor):
        self.caixa -= valor
        self.caixa_paypal += valor
        


    def sacar_paypal(self, valor):
        self.caixa_paypal -= valor
        self.caixa += valor
    

class AgenciaComum(agencia):
     def __init__(self, telefone, cnpj):
        super().__init__(telefone, cnpj, numero=randint(1001, 9999))
        self.caixa = 2000000


class AgenciaPremium(agencia):
    def __init__(self, telefone, cnpj):
        super().__init__(telefone, cnpj, numero=randint(1001, 9999))
        self.caixa = 5000000

    def adicionar_cliente(self, nome, cpf, patrimonio):
        if patrimonio > 1000000:
            super().adicionar_cliente(nome, cpf, patrimonio)
            print('Cliente adicionado com sucesso!')        
        else:
            print('O Cliente não tem patrimônio mínimo necessário para conta premium!')


if __name__ == '__main__':

    agencia_canudos_virtual = AgenciaVirtual('www.canudos_virtual.com.br', 41044104, 11111111111)
    print('Agencia: {} Caixa: R$ {} Site: {}'.format(agencia_canudos_virtual.numero, agencia_canudos_virtual.caixa, agencia_canudos_virtual.site)) 
    print('\n')

    agencia_canudos_comum = AgenciaComum(3434343, 33333388888)
    print('Agencia: {} Caixa R$ {}'.format(agencia_canudos_comum.numero, agencia_canudos_comum.caixa)) 
    print('\n')

    agencia_canudos_premium = AgenciaPremium(2434343, 23333388888)
    print('Agencia: {} Caixa R$ {}'.format(agencia_canudos_premium.numero, agencia_canudos_premium.caixa)) 


    print(agencia_canudos_virtual.caixa)
    print()
    agencia_canudos_virtual.depositar_paypal(200)
    print(agencia_canudos_virtual.caixa)
    print(agencia_canudos_virtual.caixa_paypal)


    agencia_canudos_premium.adicionar_cliente('Clara', 22222222, 11111000)
    print(agencia_canudos_premium.clientes)


