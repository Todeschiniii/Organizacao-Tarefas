class Pessoa:
    def __init__(self, nome, idade):
        self.__nome = nome
        self.__idade = idade

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


p = Pessoa("Ana", 25)
print(p.nome)   # Ana
print(p.idade)  # 25

p.nome = "João"
p.idade = 30
print(p.nome)   # João
print(p.idade)  # 30