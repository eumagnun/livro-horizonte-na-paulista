"""Testes automáticos do Módulo 03. Rode com: pytest -v (a partir de exercicios/)"""

import pandas as pd
import pytest

from exercicio import (
    CAMINHO_TABELA_RISCO,
    CAMINHO_TRANSACOES_LIMPAS,
    adicionar_flag_cross_border,
    adicionar_zscore_por_cliente,
    construir_features,
    enriquecer_com_risco_pais,
)


@pytest.fixture(scope="module")
def transacoes():
    return pd.read_csv(CAMINHO_TRANSACOES_LIMPAS)


@pytest.fixture(scope="module")
def tabela_risco():
    return pd.read_csv(CAMINHO_TABELA_RISCO)


def test_enriquecer_com_risco_pais_traz_colunas_novas(transacoes, tabela_risco):
    resultado = enriquecer_com_risco_pais(transacoes, tabela_risco)
    assert {"country_name", "risk_score", "is_tax_haven"}.issubset(resultado.columns)
    assert len(resultado) == len(transacoes)

    linha_br = resultado[resultado["country"] == "BR"].iloc[0]
    assert linha_br["country_name"] == "Brasil"
    assert linha_br["is_tax_haven"] == False  # noqa: E712


def test_adicionar_flag_cross_border(transacoes):
    resultado = adicionar_flag_cross_border(transacoes)
    assert resultado.loc[resultado["country"] == "BR", "cross_border"].eq(False).all()
    assert resultado.loc[resultado["country"] != "BR", "cross_border"].eq(True).all()


def test_adicionar_zscore_por_cliente_media_proxima_de_zero(transacoes):
    resultado = adicionar_zscore_por_cliente(transacoes)
    assert "amount_zscore_cliente" in resultado.columns
    # A média dos z-scores de cada cliente deve ser ~0 (definição de z-score).
    media_por_cliente = resultado.groupby("customer_id")["amount_zscore_cliente"].mean()
    assert media_por_cliente.abs().max() < 1e-6
    assert resultado["amount_zscore_cliente"].isna().sum() == 0


def test_construir_features_identifica_transacoes_de_alto_risco(transacoes, tabela_risco):
    resultado = construir_features(transacoes, tabela_risco)
    suspeitas = resultado[(resultado["amount_zscore_cliente"].abs() > 3) & (resultado["is_tax_haven"])]
    # Sabemos, pela forma como os dados foram gerados, que esse cruzamento
    # deve capturar pelo menos parte das transações suspeitas do capítulo 2.
    assert len(suspeitas) > 0
    assert len(suspeitas) < len(resultado) * 0.1
