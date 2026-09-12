"""Módulo 10 — Gabarito comentado."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

CAMINHO_TRANSACOES_ENRIQUECIDAS = Path(__file__).parent / "../../dados/transacoes_enriquecidas_gabarito.csv"


def calcular_taxa_erro(logs: list[dict]) -> float:
    total = len(logs)
    erros = sum(1 for log in logs if log["status"] == "ERROR")
    return (erros / total) * 100


def calcular_psi(referencia: np.ndarray, atual: np.ndarray, n_bins: int = 10) -> float:
    pontos_percentil = np.linspace(0, 100, n_bins + 1)
    limites = np.percentile(referencia, pontos_percentil)
    limites[0] = -np.inf
    limites[-1] = np.inf

    contagem_referencia, _ = np.histogram(referencia, bins=limites)
    contagem_atual, _ = np.histogram(atual, bins=limites)

    proporcao_referencia = np.clip(contagem_referencia / len(referencia), 1e-6, None)
    proporcao_atual = np.clip(contagem_atual / len(atual), 1e-6, None)

    psi = np.sum((proporcao_atual - proporcao_referencia) * np.log(proporcao_atual / proporcao_referencia))
    return float(psi)


def classificar_drift(psi: float) -> str:
    if psi < 0.10:
        return "sem drift"
    if psi < 0.25:
        return "drift moderado"
    return "drift severo"


if __name__ == "__main__":
    df = pd.read_csv(CAMINHO_TRANSACOES_ENRIQUECIDAS, parse_dates=["transaction_date"])

    primeiro_trimestre = df[df["transaction_date"].dt.quarter == 1]["amount"].to_numpy()
    ultimo_trimestre = df[df["transaction_date"].dt.quarter == 4]["amount"].to_numpy()

    psi_real = calcular_psi(primeiro_trimestre, ultimo_trimestre)
    print(f"PSI (Q1 vs Q4, dados reais da JCN): {psi_real:.4f} -> {classificar_drift(psi_real)}")

    rng = np.random.default_rng(42)
    distribuicao_deslocada = primeiro_trimestre * 3 + 50_000 + rng.normal(0, 1000, size=len(primeiro_trimestre))
    psi_sintetico = calcular_psi(primeiro_trimestre, distribuicao_deslocada)
    print(f"PSI (Q1 vs distribuição sinteticamente deslocada): {psi_sintetico:.4f} -> {classificar_drift(psi_sintetico)}")

    logs_exemplo = [{"status": "SUCCESS"}] * 97 + [{"status": "ERROR"}] * 3
    print(f"\nTaxa de erro do pipeline (monitoramento clássico): {calcular_taxa_erro(logs_exemplo):.1f}%")
