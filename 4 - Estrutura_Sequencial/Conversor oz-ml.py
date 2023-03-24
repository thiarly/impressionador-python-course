#Conversor de Onça Líquida Amaricana para Mililitro.
valor = 29.574
oz = float(input('Informe o valor em OZ: '))
ml = float(input('Informa o valor em ML: '))

conversor_oz = oz * valor
conversor_ml = ml / valor


print(f'O valor de {oz} em OZ equivale a {conversor_oz} ML.')
print(f'O valor de {ml} em ML equivale a {conversor_ml} OZ.')



