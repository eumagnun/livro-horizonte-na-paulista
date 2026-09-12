"""Testes automáticos do Módulo 01. Rode com: pytest -v (a partir de exercicios/)"""

import math
from pathlib import Path

import pytest

from exercicio import (
    CAMINHO_ARQUIVO_LEGADO,
    carregar_arquivo_legado,
    decodificar_arquivo,
    parsear_linha,
    perfilar_dados,
)

PRIMEIRA_LINHA_ESPERADA = (
    "TXN00000001CLI000284 20231027ESTORNO   +000000015109510  RJ-CORE-01     BR "
)


def test_decodificar_arquivo_retorna_linhas_de_texto():
    linhas = decodificar_arquivo(CAMINHO_ARQUIVO_LEGADO)
    assert isinstance(linhas, list)
    assert len(linhas) == 5000
    assert linhas[0] == PRIMEIRA_LINHA_ESPERADA


def test_parsear_linha_extrai_campos_corretos():
    campos = parsear_linha(PRIMEIRA_LINHA_ESPERADA)
    assert campos["transaction_id"] == "TXN00000001"
    assert campos["customer_id"] == "CLI000284"
    assert campos["transaction_date"] == "2023-10-27"
    assert campos["transaction_type"] == "ESTORNO"
    assert math.isclose(campos["amount"], 1510.95, rel_tol=1e-6)
    assert campos["adjustment_code"] == "10"
    assert campos["network_node"] == "RJ-CORE-01"
    assert campos["country"] == "BR"


def test_parsear_linha_trata_valor_negativo():
    linha_negativa = (
        "TXN99999999CLI999999 20230101AJUSTE    -000001234560000  SP-CORE-01     BR "
    )
    campos = parsear_linha(linha_negativa)
    assert math.isclose(campos["amount"], -123456.00, rel_tol=1e-6)


def test_carregar_arquivo_legado_monta_dataframe_valido():
    df = carregar_arquivo_legado()
    assert len(df) == 5000
    colunas_esperadas = {
        "transaction_id",
        "customer_id",
        "transaction_date",
        "transaction_type",
        "amount",
        "adjustment_code",
        "network_node",
        "country",
    }
    assert colunas_esperadas.issubset(set(df.columns))
    assert df["amount"].dtype == float


def test_perfilar_dados_retorna_estatisticas_esperadas():
    df = carregar_arquivo_legado()
    relatorio = perfilar_dados(df)

    assert relatorio["total_linhas"] == 5000
    assert relatorio["valor_minimo"] < 0
    assert relatorio["valor_maximo"] > 0
    # Sabemos, por construção dos dados, que existe uma fração de transações
    # com valor negativo fora de ESTORNO -- o "sinal vermelho" do capítulo 2.
    assert 0 < relatorio["pct_valores_negativos_fora_estorno"] < 5
    assert isinstance(relatorio["nulos_por_coluna"], dict)
