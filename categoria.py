from abc import ABC, abstractmethod


class Categoria(ABC):
    def __init__(self, id=None, nome="", diaria=0.0):
        self._id = id
        self._nome = nome
        self._diaria = diaria

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def nome(self):
        return self._nome

    @property
    def diaria(self):
        return self._diaria

    @abstractmethod
    def calcular_valor(self, dias, km_rodados):
        pass

    def __str__(self):
        return f"Categoria({self._nome})"


class CategoriaEconomica(Categoria):
    """
    Franquia de KM diária incluída. KM excedente cobrado à parte.
    Acréscimo: R$ 0,50 por km excedente.
    """
    def __init__(self, id=None, nome="", diaria=0.0, franquia_km_diaria=100):
        super().__init__(id, nome, diaria)
        self._franquia_km_diaria = franquia_km_diaria

    @property
    def franquia_km_diaria(self):
        return self._franquia_km_diaria

    def calcular_valor(self, dias, km_rodados):
        valor_base = self._diaria * dias
        franquia_total = self._franquia_km_diaria * dias
        km_excedente = max(0, km_rodados - franquia_total)
        acrescimo = km_excedente * 0.50
        return round(valor_base + acrescimo, 2)

    def __str__(self):
        return f"CategoriaEconomica({self._nome}, franquia={self._franquia_km_diaria}km/dia)"


class CategoriaExecutiva(Categoria):
    """
    Seguro já incluído na diária.
    Desconto progressivo: locações acima de 7 dias recebem 10% de desconto.
    """
    def __init__(self, id=None, nome="", diaria=0.0, seguro_incluso=True):
        super().__init__(id, nome, diaria)
        self._seguro_incluso = seguro_incluso

    @property
    def seguro_incluso(self):
        return self._seguro_incluso

    def calcular_valor(self, dias, km_rodados):
        valor_base = self._diaria * dias
        if dias > 7:
            valor_base *= 0.90  # 10% de desconto
        return round(valor_base, 2)

    def __str__(self):
        return f"CategoriaExecutiva({self._nome}, seguro={self._seguro_incluso})"
