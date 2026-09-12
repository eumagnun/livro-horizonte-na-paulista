"""Testes automáticos do Módulo 05. Rode com: pytest -v (a partir de exercicios/)"""

import pandas as pd
import pytest

from exercicio import (
    CAMINHO_TRANSACOES_ENRIQUECIDAS,
    avaliar_deteccao,
    detectar_anomalias,
    preparar_matriz_features,
    treinar_detector,
)


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(CAMINHO_TRANSACOES_ENRIQUECIDAS)


def test_preparar_matriz_features_colunas_e_tipos(df):
    X = preparar_matriz_features(df)
    assert list(X.columns) == ["amount", "risk_score", "amount_zscore_cliente", "cross_border"]
    assert X["cross_border"].isin([0, 1]).all()
    assert len(X) == len(df)


def test_treinar_detector_devolve_modelo_treinado(df):
    X = preparar_matriz_features(df)
    modelo = treinar_detector(X)
    previsoes = modelo.predict(X)
    assert set(previsoes).issubset({-1, 1})


def test_detectar_anomalias_adiciona_coluna(df):
    X = preparar_matriz_features(df)
    modelo = treinar_detector(X)
    resultado = detectar_anomalias(df, modelo)
    assert "is_anomaly_predicted" in resultado.columns
    assert resultado["is_anomaly_predicted"].dtype == bool
    # Com contaminação de 2%, esperamos algo perto de 2% de linhas marcadas.
    proporcao = resultado["is_anomaly_predicted"].mean()
    assert 0.01 < proporcao < 0.04


def test_deteccao_encontra_a_maioria_das_fraudes_reais(df):
    X = preparar_matriz_features(df)
    modelo = treinar_detector(X)
    resultado = detectar_anomalias(df, modelo)
    metricas = avaliar_deteccao(resultado)

    assert set(metricas.keys()) == {"precisao", "recall", "f1"}
    assert metricas["recall"] > 0.8
    assert metricas["precisao"] > 0.8
