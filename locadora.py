from database.repo_veiculo import RepositorioVeiculo


class Locadora:
    def __init__(self, nome="Locadora"):
        self._nome = nome
        self._repo = RepositorioVeiculo()

    @property
    def nome(self):
        return self._nome

    def adicionar_veiculo(self, veiculo):
        self._repo.inserir(veiculo)

    def listar_veiculos(self):
        return self._repo.listar()

    def __str__(self):
        return f"Locadora({self._nome})"
