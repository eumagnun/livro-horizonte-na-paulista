"""Testes automáticos do Módulo 02. Rode com: pytest -v (a partir de exercicios/)"""

import pandas as pd
import pytest

from exercicio import (
    CAMINHO_TRANSACOES_BRUTAS,
    limpar_transacoes,
    normalizar_data,
    normalizar_tipo_transacao,
    normalizar_valor,
    validar_contrato,
)


def test_normalizar_data_formato_brasileiro():
    assert normalizar_data("04/03/2023") == "2023-03-04"


def test_normalizar_data_formato_iso_inalterado():
    assert normalizar_data("2023-09-23") == "2023-09-23"


def test_normalizar_valor_com_virgula():
    assert normalizar_valor("1522,04") == pytest.approx(1522.04)


def test_normalizar_valor_com_ponto():
    assert normalizar_valor("1522.04") == pytest.approx(1522.04)


def test_normalizar_tipo_transacao():
    assert normalizar_tipo_transacao("fatura") == "FATURA"
    assert normalizar_tipo_transacao("  Ajuste ") == "AJUSTE"


@pytest.fixture(scope="module")
def df_bruto():
    return pd.read_csv(CAMINHO_TRANSACOES_BRUTAS, dtype=str)


@pytest.fixture(scope="module")
def df_limpo(df_bruto):
    return limpar_transacoes(df_bruto)


def test_limpar_transacoes_remove_nulos_e_duplicatas(df_bruto, df_limpo):
    assert df_limpo["customer_id"].isna().sum() == 0
    assert df_limpo["transaction_id"].duplicated().sum() == 0
    assert len(df_limpo) < len(df_bruto)


def test_limpar_transacoes_normaliza_tipos(df_limpo):
    assert df_limpo["amount"].dtype == float
    assert set(df_limpo["transaction_type"].unique()).issubset(
        {"FATURA", "AJUSTE", "ESTORNO", "PAGAMENTO"}
    )
    assert df_limpo["transaction_date"].str.match(r"^\d{4}-\d{2}-\d{2}$").all()


def test_validar_contrato_aprova_dados_limpos(df_limpo):
    contrato = validar_contrato(df_limpo)
    assert all(contrato.values()), f"Regras violadas: {contrato}"


def test_validar_contrato_reprova_dados_sujos(df_bruto):
    # Sem limpeza, o contrato deve reprovar em pelo menos uma regra.
    df_bruto_com_tipo_intacto = df_bruto.copy()
    df_bruto_com_tipo_intacto["amount"] = df_bruto_com_tipo_intacto["amount"].apply(
        lambda v: normalizar_valor(v)
    )
    contrato = validar_contrato(df_bruto_com_tipo_intacto)
    assert not all(contrato.values())
