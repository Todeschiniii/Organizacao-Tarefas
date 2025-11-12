import math

class Retangulo:
    def __init__(self):
        self.__base = None
        self.__altura = None

    @property
    def base(self):
        return self.__base

    @base.setter
    def base(self, value):
        if value <= 0:
            raise ValueError("A base deve ser positiva")
        self.__base = value

    @property
    def altura(self):
        return self.__altura

    @altura.setter
    def altura(self, value):
        if value <= 0:
            raise ValueError("A altura deve ser positiva")
        self.__altura = value

    def calcular_area(self):
        if self.base is None or self.altura is None:
            raise ValueError("Base e altura precisam estar definidas para calcular a área")
        return self.base * self.altura

    def calcular_perimetro(self):
        if self.base is None or self.altura is None:
            raise ValueError("Base e altura precisam estar definidas para calcular o perímetro")
        return 2 * (self.base + self.altura)

    def calcular_diagonal(self):
        if self.base is None or self.altura is None:
            raise ValueError("Base e altura precisam estar definidas para calcular a diagonal")
        return math.sqrt(self.base**2 + self.altura**2)


r = Retangulo()      # cria o retângulo, base e altura começam como None

# Definindo valores
r.base = 5
r.altura = 3

# Acessando valores
print("Base:", r.base)       # Base: 5
print("Altura:", r.altura)   # Altura: 3

# Calculando propriedades
print("Área:", r.calcular_area())             # Área: 15
print("Perímetro:", r.calcular_perimetro())   # Perímetro: 16
print("Diagonal:", r.calcular_diagonal())     # Diagonal: 5.8309518