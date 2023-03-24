def pegar_area_usuario():
    area = int(input("Qual a área a ser pintada (m²): "))
    return area

def calcular_litros_precisamos(area):
    litros = area / 6
    return litros
    
def calcular_latas(litros):
    latas = litros / 18
    if int(latas) != latas:
        latas = int(latas) + 1
    return latas

def calcular_preco(latas):
    preco = latas * 80
    return preco
    

area = pegar_area_usuario()
litros = calcular_litros_precisamos(area)
latas = calcular_latas(litros)
preco = calcular_preco(latas)


print("Quantidade de latas ", latas)
print("Preço: ", preco)