"""
Módulo 05 — Detecção de Anomalias e Fraude com Machine Learning

Complete as funções marcadas com TODO. Leia o README.md antes de começar.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import f1_score, precision_score, recall_score

CAMINHO_TRANSACOES_ENRIQUECIDAS = Path(__file__).parent / "../dados/transacoes_enriquecidas_gabarito.csv"

COLUNAS_FEATURES = ["amount", "risk_score", "amount_zscore_cliente", "cross_border"]


def preparar_matriz_features(df: pd.DataFrame) -> pd.DataFrame:
    """Devolve um DataFrame só com as colunas em COLUNAS_FEATURES, nessa
    ordem, prontas para entrar no modelo. A coluna `cross_border` (booleana)
    deve virar 0/1.
    """
    # TODO: monte X = df[COLUNAS_FEATURES].copy()
    # TODO: converta X["cross_border"] para inteiro (0/1)
    raise NotImplementedError("Implemente preparar_matriz_features")


def treinar_detector(X: pd.DataFrame, contaminacao: float = 0.02) -> IsolationForest:
    """Cria e treina um IsolationForest com o parâmetro `contamination` e
    random_state=42, e devolve o modelo já treinado (fit).
    """
    # TODO: crie o modelo: IsolationForest(contamination=contaminacao, random_state=42)
    # TODO: treine com modelo.fit(X)
    # TODO: devolva o modelo
    raise NotImplementedError("Implemente treinar_detector")


def detectar_anomalias(df: pd.DataFrame, modelo: IsolationForest) -> pd.DataFrame:
    """Usa o modelo já treinado para prever anomalias sobre `df` e devolve
    uma cópia de `df` com a nova coluna booleana `is_anomaly_predicted`
    (o IsolationForest devolve -1 para anomalia e 1 para normal).
    """
    # TODO: X = preparar_matriz_features(df)
    # TODO: previsoes = modelo.predict(X)
    # TODO: df = df.copy(); df["is_anomaly_predicted"] = previsoes == -1
    raise NotImplementedError("Implemente detectar_anomalias")


def avaliar_deteccao(df: pd.DataFrame) -> dict:
    """Compara df['is_anomaly_predicted'] com df['is_suspicious_ground_truth']
    e devolve {"precisao": ..., "recall": ..., "f1": ...}.
    """
    # TODO: use precision_score, recall_score, f1_score do sklearn.metrics,
    #       passando (y_verdadeiro, y_previsto)
    raise NotImplementedError("Implemente avaliar_deteccao")


if __name__ == "__main__":
    df = pd.read_csv(CAMINHO_TRANSACOES_ENRIQUECIDAS)

    X = preparar_matriz_features(df)
    modelo = treinar_detector(X)
    df = detectar_anomalias(df, modelo)
    metricas = avaliar_deteccao(df)

    print(f"Transações analisadas: {len(df)}")
    print(f"Anomalias previstas pelo modelo: {df['is_anomaly_predicted'].sum()}")
    print(f"Suspeitas de fato (ground truth): {df['is_suspicious_ground_truth'].sum()}")
    print("=== Métricas ===")
    for nome, valor in metricas.items():
        print(f"{nome}: {valor:.2%}")
