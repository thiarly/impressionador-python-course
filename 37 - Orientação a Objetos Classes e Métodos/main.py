from ContasBancos import ContaCorrente, CartaoCredito



# Programa
conta_thiarly = ContaCorrente("Thiarly", "044.000.111-22", 8324, 156697)


cartao_thiarly = CartaoCredito('Thiarly', conta_thiarly)

print(cartao_thiarly.conta_corrente.conta )

print(conta_thiarly.cartoes[0].numero)
print(cartao_thiarly.validade)
print(cartao_thiarly.cod_seguranca)

cartao_thiarly.senha = '3111'


print(conta_thiarly.__dict__)
