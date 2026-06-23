from datetime import date


class Contrato:
    def __init__(self, id=None, veiculo=None, dias=0, km_rodados=0, valor_total=0.0, data=None):
        self._id = id
        self._veiculo = veiculo
        self._dias = dias
        self._km_rodados = km_rodados
        self._valor_total = valor_total
        self._data = data or date.today().isoformat()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def veiculo(self):
        return self._veiculo

    @property
    def dias(self):
        return self._dias

    @property
    def km_rodados(self):
        return self._km_rodados

    @property
    def valor_total(self):
        return self._valor_total

    @property
    def data(self):
        return self._data

    def exibir_resumo(self):
        return (
            f"=== CONTRATO #{self._id or 'N/A'} ===\n"
            f"Data:        {self._data}\n"
            f"Veículo:     {self._veiculo}\n"
            f"Categoria:   {self._veiculo.categoria if self._veiculo else 'N/A'}\n"
            f"Dias:        {self._dias}\n"
            f"KM rodados:  {self._km_rodados}\n"
            f"Valor total: R$ {self._valor_total:.2f}\n"
        )

    def __str__(self):
        return f"Contrato(id={self._id}, valor=R${self._valor_total:.2f})"
