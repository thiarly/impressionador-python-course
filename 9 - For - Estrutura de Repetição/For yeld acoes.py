acoes = ["JHSF3", "BBDC4", "EGIE3"]
cotacao = [6.0, 22.50, 41.20]
dpa = [0.25, 0.89, 3.20]
meta_yeld = 6

for i in range(len(acoes)):
    acao = acoes[i]
    #print(acoes[i]) 
    y1 = (cotacao[i], (dpa[i] / cotacao[i]) * 100)

    print('{} valor da cotação {} e yeld de {:.3}%'.format(acoes[i], cotacao[i], (dpa[i] / cotacao[i]) * 100))

        
    
    
    