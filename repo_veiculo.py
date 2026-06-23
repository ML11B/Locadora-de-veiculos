from database.conexao import ConexaoBD
from models.veiculo import Veiculo


class RepositorioVeiculo:
    def __init__(self):
        self._conn = ConexaoBD().conectar()

    def inserir(self, veiculo):
        cat_id = veiculo.categoria.id if veiculo.categoria else None
        cursor = self._conn.cursor()
        cursor.execute(
            "INSERT INTO veiculo (modelo, placa, categoria_id) VALUES (?, ?, ?)",
            (veiculo.modelo, veiculo.placa, cat_id)
        )
        self._conn.commit()
        veiculo.id = cursor.lastrowid
        return veiculo

    def buscar(self, id):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM veiculo WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._montar(row) if row else None

    def listar(self):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM veiculo")
        return [self._montar(row) for row in cursor.fetchall()]

    def atualizar(self, veiculo):
        cat_id = veiculo.categoria.id if veiculo.categoria else None
        self._conn.execute(
            "UPDATE veiculo SET modelo=?, placa=?, categoria_id=? WHERE id=?",
            (veiculo.modelo, veiculo.placa, cat_id, veiculo.id)
        )
        self._conn.commit()

    def excluir(self, id):
        cursor = self._conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM contrato WHERE veiculo_id = ?", (id,))
        count = cursor.fetchone()[0]
        if count > 0:
            raise Exception("Não é possível remover um veículo com histórico de contratos.")
        self._conn.execute("DELETE FROM veiculo WHERE id = ?", (id,))
        self._conn.commit()

    def _montar(self, row):
        from database.repo_categoria import RepositorioCategoria
        id, modelo, placa, cat_id = row
        categoria = RepositorioCategoria().buscar(cat_id) if cat_id else None
        v = Veiculo(id=id, modelo=modelo, placa=placa, categoria=categoria)
        return v
