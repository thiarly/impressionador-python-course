'''
O custo da lata é 80/18 = 4,44 R$/L
O custo do galão é 25/3,6 = 6,94 R$/L
A lata é mais econômica, então todas as latas inteiras que pudermos usar devemos comprar em latas. Se ficar faltando alguma coisa para completar devemos avaliar se é melhor comprar latas ou galões. Exemplo:
Se queremos comprar 90 litros. 5 latas dão exatamente 90 litros. Então devemos comprar tudo em latas.
Se queremos comprar 95 litros. 5 latas dão exatamente 90 litros. Então devemos comprar pelo menos 5 latas e avaliar o que falta, se estes últimos 5 litros valem mais apenas em latas ou galões.
Para os 5 litros faltantes precisamos de 2 galões que custam 50 reais no total. Ou de uma lata que custa 80 reais no total. Portanto, neste caso vale mais a pena usar 2 galões.
Se queremos comprar 107 litros. 5 latas dão exatamente 90 litros. Então devemos comprar pelo menos 5 latas e avaliar o que falta, se estes últimos 5 litros valem mais apenas em latas ou galões.
Para os 17 litros faltantes precisamos de 5 galões que custam 125 reais no total. Ou de uma lata que custa 80 reais no total. Portanto, neste caso vale mais a pena usar uma lata.
3 galões custam 75 reais, 4 galões custam 100 reais. Então, se for possível completar com até 3 galões escolhe-se galões. Qualquer quantidade maior que 3 galões, usa-se latas.
Podemos ir ao exercício:'''


# calcular o menor preço possível de latas e galoes para pintar uma parede

# descobrir a área a ser pintada (pegar um input do usuário)
galoes = 0
latas = 0
area = float(input('Digite a área a ser pintada: M quadrado M²: '))

# calcular quantos litros vamos precisar (area / 6)
litros = area / 6

# calcular quantas latas e galoes vamos precisar
        # calcular quantas latas inteiras vamos precisar
latas = int(litros / 18)

        # calcular quanto vai sobrar de litros de tinta
litros_faltam = litros % 18

        # se sobrar tinta:
            # quantos galoes vamos precisar para essa sobra    

if litros_faltam > 0:
    if litros_faltam % 3.6 > 0:
        galoes = int(litros_faltam / 3.6) + 1
    else:
        galoes = litros_faltam / 3.6

preco_latas = latas * 80
      
    # calcular o preço
        # qtde_latas_inteiras * 80
precos_galoes = galoes * 25
if precos_galoes > 80:
    latas += 1
    preco_latas = latas * 80
    galoes = 0
    precos_galoes = 0


preco_final = preco_latas + precos_galoes
print('Latas:', latas)
print('Galões:', galoes)
print('Preço Final:', preco_final)


        # se qtde_galoes * 25 > 80:
            # preço anterior + 80
        # caso contrario
            # preco anterior + qtde_galoes * 25



