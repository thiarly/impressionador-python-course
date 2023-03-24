# calcular quantas latas e quantos custa comprar a tinta

# descobrir a area a ser pintada
area = float(input("Qual a área a ser pintada?"))
# descobrir quantos litros de tinta o cliente precisa (area / 6)
litros = area / 6
# quantas latas eu vou precisar para a quantidade de litros
    # calcular quantas latas (litros / 18)
    # se deu um número "quebrado" de latas
        # adiciona 1 lata
    # se não 
        # dê a quantidade de latas      
latas = litros / 18

if int(latas) != latas:
    latas = int(latas) + 1

# calcular o preço das latas (quantidade de latas * R$ 80)
preco = latas * 80

print('Quantidade de latas', latas)
print('Preço:', preco)



