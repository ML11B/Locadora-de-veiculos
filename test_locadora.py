import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.categoria import CategoriaEconomica, CategoriaExecutiva
from models.veiculo import Veiculo
from models.contrato import Contrato


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def cat_economica():
    return CategoriaEconomica(id=1, nome="Econômica", diaria=80.0, franquia_km_diaria=100)

@pytest.fixture
def cat_executiva():
    return CategoriaExecutiva(id=2, nome="Executiva", diaria=200.0, seguro_incluso=True)

@pytest.fixture
def veiculo_economico(cat_economica):
    v = Veiculo(id=1, modelo="Fiat Mobi", placa="AAA-0001")
    v.associar_categoria(cat_economica)
    return v

@pytest.fixture
def veiculo_sem_categoria():
    return Veiculo(id=2, modelo="Fiat Mobi", placa="BBB-0002")


# ── Testes CategoriaEconomica ─────────────────────────────────────────────────

def test_economica_dentro_da_franquia(cat_economica):
    """5 dias, 400 km (franquia = 500 km) → sem excedente"""
    valor = cat_economica.calcular_valor(dias=5, km_rodados=400)
    assert valor == 80.0 * 5  # 400.00

def test_economica_fora_da_franquia(cat_economica):
    """5 dias, 600 km (franquia = 500 km) → 100 km excedentes × R$0,50"""
    valor = cat_economica.calcular_valor(dias=5, km_rodados=600)
    esperado = (80.0 * 5) + (100 * 0.50)  # 400 + 50 = 450.00
    assert valor == esperado


# ── Testes CategoriaExecutiva ─────────────────────────────────────────────────

def test_executiva_locacao_curta(cat_executiva):
    """3 dias → sem desconto"""
    valor = cat_executiva.calcular_valor(dias=3, km_rodados=200)
    assert valor == 200.0 * 3  # 600.00

def test_executiva_longa_duracao_com_desconto(cat_executiva):
    """10 dias → 10% de desconto"""
    valor = cat_executiva.calcular_valor(dias=10, km_rodados=500)
    esperado = round(200.0 * 10 * 0.90, 2)  # 1800.00
    assert valor == esperado


# ── Testes de exceção ─────────────────────────────────────────────────────────

def test_locacao_duracao_invalida(veiculo_economico):
    """Duração zero deve lançar ValueError"""
    with pytest.raises(ValueError, match="maior que zero"):
        veiculo_economico.realizar_locacao(dias=0, km_rodados=100)

def test_locacao_duracao_negativa(veiculo_economico):
    """Duração negativa deve lançar ValueError"""
    with pytest.raises(ValueError):
        veiculo_economico.realizar_locacao(dias=-1, km_rodados=100)

def test_locacao_sem_categoria(veiculo_sem_categoria):
    """Veículo sem categoria deve lançar ValueError"""
    with pytest.raises(ValueError, match="categoria"):
        veiculo_sem_categoria.realizar_locacao(dias=3, km_rodados=200)


# ── Teste do contrato gerado ──────────────────────────────────────────────────

def test_contrato_gerado_corretamente(veiculo_economico):
    contrato = veiculo_economico.realizar_locacao(dias=3, km_rodados=250)
    assert isinstance(contrato, Contrato)
    assert contrato.dias == 3
    assert contrato.km_rodados == 250
    assert contrato.valor_total == 80.0 * 3  # dentro da franquia
