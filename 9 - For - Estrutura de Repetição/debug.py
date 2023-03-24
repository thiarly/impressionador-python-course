estoque = [[8, 10, 5, 9], 
           [3, 7, 9, 22],
           [23, 15, 8, 9],
           [4, 90, 5, 12],
           ]

filiais = ['canudos', 'juazeiro', 'cajazeiras', 'souza']

meta = 10
fabrica_abaixo_nivel = []


for i, lista in enumerate(estoque):
    # Quero saber se dentro da lista tem algum ITEM abaixo do valor minímo. 
    for qtde in (lista):
        if qtde < meta:
            if filiais[i] in fabrica_abaixo_nivel:
                pass
            else:
                fabrica_abaixo_nivel.append(filiais[i])
            print(fabrica_abaixo_nivel, qtde)
                





            
            