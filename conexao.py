import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "locadora.db")


class ConexaoBD:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._conn = None
        return cls._instancia

    def conectar(self):
        try:
            if self._conn is None:
                self._conn = sqlite3.connect(DB_PATH)
                self._conn.execute("PRAGMA foreign_keys = ON")
                self._criar_tabelas()
            return self._conn
        except sqlite3.Error as e:
            raise ConnectionError(f"Falha na conexão com o banco de dados: {e}")

    def _criar_tabelas(self):
        cursor = self._conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS categoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                diaria REAL NOT NULL,
                tipo TEXT NOT NULL,
                franquia_km_diaria INTEGER,
                seguro_incluso INTEGER
            );

            CREATE TABLE IF NOT EXISTS veiculo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                modelo TEXT NOT NULL,
                placa TEXT NOT NULL UNIQUE,
                categoria_id INTEGER,
                FOREIGN KEY (categoria_id) REFERENCES categoria(id)
            );

            CREATE TABLE IF NOT EXISTS contrato (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                veiculo_id INTEGER NOT NULL,
                dias INTEGER NOT NULL,
                km_rodados INTEGER NOT NULL,
                valor_total REAL NOT NULL,
                data TEXT NOT NULL,
                FOREIGN KEY (veiculo_id) REFERENCES veiculo(id)
            );
        """)
        self._conn.commit()

    def fechar(self):
        if self._conn:
            self._conn.close()
            self._conn = None
            ConexaoBD._instancia = None
