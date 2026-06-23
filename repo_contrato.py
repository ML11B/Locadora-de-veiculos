from database.conexao import ConexaoBD
from models.contrato import Contrato


class RepositorioContrato:
    def __init__(self):
        self._conn = ConexaoBD().conectar()

    def inserir(self, contrato):
        cursor = self._conn.cursor()
        cursor.execute(
            "INSERT INTO contrato (veiculo_id, dias, km_rodados, valor_total, data) VALUES (?, ?, ?, ?, ?)",
            (contrato.veiculo.id, contrato.dias, contrato.km_rodados, contrato.valor_total, contrato.data)
        )
        self._conn.commit()
        contrato.id = cursor.lastrowid
        return contrato

    def buscar(self, id):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM contrato WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._montar(row) if row else None

    def listar(self):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM contrato")
        return [self._montar(row) for row in cursor.fetchall()]

    def _montar(self, row):
        from database.repo_veiculo import RepositorioVeiculo
        id, veiculo_id, dias, km_rodados, valor_total, data = row
        veiculo = RepositorioVeiculo().buscar(veiculo_id)
        return Contrato(id=id, veiculo=veiculo, dias=dias, km_rodados=km_rodados,
                        valor_total=valor_total, data=data)
