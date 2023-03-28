import xmltodict


# abrir e ler o arquivo:

with open('NFs Finais/DANFEBrota.xml', 'rb') as arquivo:
    documento = xmltodict.parse(arquivo)

#print(documento['nfeProc']['NFe']['infNFe']['dest']['xNome'])

#for item in documento ['nfeProc']['NFe']['infNFe']:
#    print(item)
#print(documento ['nfeProc']['NFe']['infNFe']['emit']['xFant'])

dic_notafiscal = documento ['nfeProc']['NFe']['infNFe']