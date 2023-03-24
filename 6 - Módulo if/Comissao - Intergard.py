#Criar um programar que calcule a comissão dos funcionários da INTERGARD DO BRASIL
#Vendedores, TI, Assistência Técnica, e Gerência

# Vendedor = 1% sobre o Faturamento
# TI = R$ 600,00  sobre casa milhão de Faturamento
# Assistência Técnica = 500 sobre casa milhão de Faturamento
# Gerência = 1000,00 sobre cada milhão de Faturamento


faturamento = float(input('Digite o faturamento do mês: '))

#comissão funcionários
vendendor = 0.01
ti = 600
assistencia = 500
gerencia = 1000

#meta de comissão
meta = 1000000

#VENDEDORES
if faturamento >= meta:
    bonus = 0.01 * faturamento
else:
    bonus = 0
print(f'O bônus dos VENDEDORES esse mês é de R$ {bonus}')

#TI
if faturamento >= meta:
    if faturamento >= meta:
        bonus = ti
    if faturamento >= (meta * 2):
        bonus = ti * 2
    if faturamento >= (meta * 3):
         bonus = ti * 3
    if faturamento >= (meta * 4):
        bonus = ti * 4
    if faturamento >= (meta * 5):
         bonus = ti * 5
else:
    bonus = 0

print(f'O bônus da TI esse mês é de R$ {bonus}')


#ASSISTÊNCIA
if faturamento >= meta:
    if faturamento >= meta:
        bonus = assistencia
    if faturamento >= (meta * 2):
        bonus = assistencia * 2
    if faturamento >= (meta * 3):
         bonus = assistencia * 3
    if faturamento >= (meta * 4):
        bonus = assistencia * 4
    if faturamento >= (meta * 5):
         bonus = assistencia * 5
else:
    bonus = 0

print(f'O bônus da ASSISTÊNCIA esse mês é de R$ {bonus}')

#GERÊNCIA
if faturamento >= meta:
    if faturamento >= meta:
        bonus = gerencia
    if faturamento >= (meta * 2):
        bonus = gerencia * 2
    if faturamento >= (meta * 3):
         bonus = gerencia * 3
    if faturamento >= (meta * 4):
        bonus = gerencia * 4
    if faturamento >= (meta * 5):
         bonus = gerencia * 5
else:
    bonus = 0

print(f'O bônus da GERÊNCIA esse mês é de R$ {bonus}')