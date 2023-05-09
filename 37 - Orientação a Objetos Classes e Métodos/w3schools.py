class pessoa:
    def __init__ (self, name, age):
        self.name = name
        self.age = age


    def criandopessoal(self):
        print('Hello my name is' + self.name)




user1 = pessoa('thiarly', 32)


print(user1.name, user1.age)