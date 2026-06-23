from database.conexao import ConexaoBD
from models.categoria import CategoriaEconomica, CategoriaExecutiva


class RepositorioCategoria:
    def __init__(self):
        self._conn = ConexaoBD().conectar()

    def inserir(self, categoria):
        tipo = type(categoria).__name__
        franquia = getattr(categoria, 'franquia_km_diaria', None)
        seguro = int(getattr(categoria, 'seguro_incluso', False))
        cursor = self._conn.cursor()
        cursor.execute(
            "INSERT INTO categoria (nome, diaria, tipo, franquia_km_diaria, seguro_incluso) VALUES (?, ?, ?, ?, ?)",
            (categoria.nome, categoria.diaria, tipo, franquia, seguro)
        )
        self._conn.commit()
        categoria.id = cursor.lastrowid
        return categoria

    def buscar(self, id):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM categoria WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._montar(row) if row else None

    def listar(self):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM categoria")
        return [self._montar(row) for row in cursor.fetchall()]

    def atualizar(self, categoria):
        tipo = type(categoria).__name__
        franquia = getattr(categoria, 'franquia_km_diaria', None)
        seguro = int(getattr(categoria, 'seguro_incluso', False))
        self._conn.execute(
            "UPDATE categoria SET nome=?, diaria=?, tipo=?, franquia_km_diaria=?, seguro_incluso=? WHERE id=?",
            (categoria.nome, categoria.diaria, tipo, franquia, seguro, categoria.id)
        )
        self._conn.commit()

    def excluir(self, id):
        # Verifica se há veículos usando esta categoria
        cursor = self._conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM veiculo WHERE categoria_id = ?", (id,))
        count = cursor.fetchone()[0]
        if count > 0:
            raise Exception("Não é possível remover uma categoria associada a veículos ativos.")
        self._conn.execute("DELETE FROM categoria WHERE id = ?", (id,))
        self._conn.commit()

    def _montar(self, row):
        id, nome, diaria, tipo, franquia, seguro = row
        if tipo == "CategoriaEconomica":
            return CategoriaEconomica(id=id, nome=nome, diaria=diaria, franquia_km_diaria=franquia or 100)
        elif tipo == "CategoriaExecutiva":
            return CategoriaExecutiva(id=id, nome=nome, diaria=diaria, seguro_incluso=bool(seguro))
        return None
