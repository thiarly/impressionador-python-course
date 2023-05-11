from ContasBancos import ContaCorrente, CartaoCredito
from Agencia import AgenciaComum, AgenciaVirtual, AgenciaPremium


# # Programa
# conta_thiarly = ContaCorrente("Thiarly", "044.000.111-22", 8324, 156697)


# cartao_thiarly = CartaoCredito('Thiarly', conta_thiarly)

# print(cartao_thiarly.conta_corrente.conta )

# print(conta_thiarly.cartoes[0].numero)
# print(cartao_thiarly.validade)
# print(cartao_thiarly.cod_seguranca)

# cartao_thiarly.senha = '3111'


# print(conta_thiarly.__dict__)


agencia_premium_cajazeiras = AgenciaPremium(8344332211, 7763535357272653)
print(agencia_premium_cajazeiras.caixa)
print(agencia_premium_cajazeiras.clientes)