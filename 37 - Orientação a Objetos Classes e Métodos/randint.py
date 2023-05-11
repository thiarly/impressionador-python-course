import random

num_cartao = []

for i in range(0, 12):
   num_cartao.append(random.randint(0, 9))

print(num_cartao)


test = random.randint(1000000000000000, 9999999999999999)
print(test)
print (len(str(test)))