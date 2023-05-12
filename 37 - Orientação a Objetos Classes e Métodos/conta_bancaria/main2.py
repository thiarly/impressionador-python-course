
agencia_canudos = agencia(7534942639, 244524240409, 43214)
agencia_canudos.verificar_caixa()

agencia_canudos.emprestar_dinheiro(1200, 440393840389, 0.10)
print(agencia_canudos.caixa)
print(agencia_canudos.emprestimos)

agencia_canudos.adicionar_cliente('Luca', 33333333555, 30000)
print(agencia_canudos.clientes)