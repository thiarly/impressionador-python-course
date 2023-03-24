nota1 = float(input('Digite a 1º nota:'))
nota2 = float(input('Digite a 2º nota:'))

media = (nota1 + nota2) / 2

if media < 10:
    

    if media <= 4:
        conceito = "E"
    elif media <= 6:
        conceito = "D"
    elif media <= 7.5:
        conceito = "C"
    elif media <= 9:
        conceito = "B"
    elif media <= 10:
        conceito = "A"

    print (f'Conceito = {conceito}, valor da média {media}')


else:
    print('Redigite sua nota, valor inválido.')

