class Pessoa2:
    def __init__(self):
        self.__nome = None
        self.__idade = None

    # Getter e setter de nome
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        self.__nome = value

    # Getter e setter de idade
    @property
    def idade(self):
        return self.__idade

    @idade.setter
    def idade(self, value):
        self.__idade = value


p = Pessoa2()        # Começa com None
print(p.nome)       # None
print(p.idade)      # None

p.nome = "Ana"      # Seta via setter
p.idade = 25

print(p.nome)       # Ana
print(p.idade)      # 25