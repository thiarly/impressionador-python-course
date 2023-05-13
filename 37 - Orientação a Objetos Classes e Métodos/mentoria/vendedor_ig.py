class ComissaoIntergard():
    def __init__(self, nome, setor):
        self.nome = nome
        self.setor = setor
        self.faturamento = 0

    def atualiza_faturamento(self, valor):
        self.faturamento = valor

    def calcular_comissao(self):
        
        if self.setor == "Vendedor":
            comissao = self.faturamento * 0.01
            comissao_formatada = "{:,.2f}".format(comissao)
            comissao_formatada = comissao_formatada.replace(',', '.')
            print('Comissão dos vendedores: R$ {}'.format(comissao_formatada))
        
        elif self.setor == "TI":
            comissao_milhao = 600
            calculo = self.faturamento // 1000000
            comissao = calculo * comissao_milhao
            comissao_formatada = "{:,.2f}".format(comissao)
            comissao_formatada = comissao_formatada.replace(',', '.')
            print('Comissão do setor de TI: R$ {}'.format(comissao_formatada))
        
        elif self.setor == "Assistência":
            comissao_milhao = 500
            calculo = self.faturamento // 1000000
            comissao = calculo * comissao_milhao
            comissao_formatada = "{:,.2f}".format(comissao)
            comissao_formatada = comissao_formatada.replace(',', '.')
            print('Comissão do setor da Assistência: R$ {}'.format(comissao_formatada))


thiarly = ComissaoIntergard('thiarly', 'TI')
thiarly.atualiza_faturamento(1000000)



vendedores = ComissaoIntergard('Todos_Vendedores', 'Vendedor')
vendedores.atualiza_faturamento(1000000)


assistencia = ComissaoIntergard('Todos da Assistência', 'Assistência')
assistencia.atualiza_faturamento(1000000)
print (assistencia.calcular_comissao())