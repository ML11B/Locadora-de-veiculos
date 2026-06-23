from models.contrato import Contrato


class Veiculo:
    def __init__(self, id=None, modelo="", placa="", categoria=None):
        self._id = id
        self._modelo = modelo
        self._placa = placa
        self._categoria = categoria

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def modelo(self):
        return self._modelo

    @property
    def placa(self):
        return self._placa

    @property
    def categoria(self):
        return self._categoria

    def associar_categoria(self, categoria):
        self._categoria = categoria

    def realizar_locacao(self, dias, km_rodados):
        if dias <= 0:
            raise ValueError("A duração da locação deve ser maior que zero.")
        if self._categoria is None:
            raise ValueError("O veículo não possui uma categoria associada.")

        valor = self._categoria.calcular_valor(dias, km_rodados)
        contrato = Contrato(
            veiculo=self,
            dias=dias,
            km_rodados=km_rodados,
            valor_total=valor
        )
        return contrato

    def __str__(self):
        return f"Veiculo({self._modelo}, {self._placa})"
