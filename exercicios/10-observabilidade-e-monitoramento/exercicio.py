"""
Módulo 10 — Observabilidade e Monitoramento de Sistemas de IA

Complete as funções marcadas com TODO. Leia o README.md antes de começar.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

CAMINHO_TRANSACOES_ENRIQUECIDAS = Path(__file__).parent / "../dados/transacoes_enriquecidas_gabarito.csv"


def calcular_taxa_erro(logs: list[dict]) -> float:
    """Devolve o percentual (0 a 100) de logs cujo status é 'ERROR'."""
    # TODO: total = len(logs)
    # TODO: erros = quantos logs têm status == "ERROR"
    # TODO: devolva (erros / total) * 100
    raise NotImplementedError("Implemente calcular_taxa_erro")


def calcular_psi(referencia: np.ndarray, atual: np.ndarray, n_bins: int = 10) -> float:
    """Calcula o Population Stability Index entre as distribuições
    `referencia` e `atual`. Veja o algoritmo passo a passo no README.md.
    """
    # TODO: pontos_percentil = np.linspace(0, 100, n_bins + 1)
    # TODO: limites = np.percentile(referencia, pontos_percentil)
    # TODO: limites[0] = -np.inf; limites[-1] = np.inf
    # TODO: contagem_referencia, _ = np.histogram(referencia, bins=limites)
    # TODO: contagem_atual, _ = np.histogram(atual, bins=limites)
    # TODO: proporcao_referencia = contagem_referencia / len(referencia)
    # TODO: proporcao_atual = contagem_atual / len(atual)
    # TODO: proporcao_referencia = np.clip(proporcao_referencia, 1e-6, None)
    # TODO: proporcao_atual = np.clip(proporcao_atual, 1e-6, None)
    # TODO: psi = np.sum((proporcao_atual - proporcao_referencia) * np.log(proporcao_atual / proporcao_referencia))
    # TODO: devolva float(psi)
    raise NotImplementedError("Implemente calcular_psi")


def classificar_drift(psi: float) -> str:
    """Devolve 'sem drift', 'drift moderado' ou 'drift severo' conforme os
    limiares: <0.10 sem drift; entre 0.10 e 0.25 moderado; >=0.25 severo.
    """
    # TODO: implemente
    raise NotImplementedError("Implemente classificar_drift")


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
