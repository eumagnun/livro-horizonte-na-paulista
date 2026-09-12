"""Módulo 05 — Gabarito comentado."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import f1_score, precision_score, recall_score

CAMINHO_TRANSACOES_ENRIQUECIDAS = Path(__file__).parent / "../../dados/transacoes_enriquecidas_gabarito.csv"

COLUNAS_FEATURES = ["amount", "risk_score", "amount_zscore_cliente", "cross_border"]


def preparar_matriz_features(df: pd.DataFrame) -> pd.DataFrame:
    X = df[COLUNAS_FEATURES].copy()
    X["cross_border"] = X["cross_border"].astype(int)
    return X


def treinar_detector(X: pd.DataFrame, contaminacao: float = 0.02) -> IsolationForest:
    modelo = IsolationForest(contamination=contaminacao, random_state=42)
    modelo.fit(X)
    return modelo


def detectar_anomalias(df: pd.DataFrame, modelo: IsolationForest) -> pd.DataFrame:
    X = preparar_matriz_features(df)
    previsoes = modelo.predict(X)
    df = df.copy()
    df["is_anomaly_predicted"] = previsoes == -1
    return df


def avaliar_deteccao(df: pd.DataFrame) -> dict:
    y_verdadeiro = df["is_suspicious_ground_truth"]
    y_previsto = df["is_anomaly_predicted"]
    return {
        "precisao": precision_score(y_verdadeiro, y_previsto),
        "recall": recall_score(y_verdadeiro, y_previsto),
        "f1": f1_score(y_verdadeiro, y_previsto),
    }


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
