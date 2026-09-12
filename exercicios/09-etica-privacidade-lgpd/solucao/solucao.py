"""Módulo 09 — Gabarito comentado."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

CAMINHO_TRANSACOES_ENRIQUECIDAS = Path(__file__).parent / "../../dados/transacoes_enriquecidas_gabarito.csv"


def pseudonimizar_id(identificador: str, salt: str) -> str:
    texto = identificador + salt
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def adicionar_ruido_laplace(
    valor_real: float,
    sensibilidade: float,
    epsilon: float,
    rng: np.random.Generator | None = None,
) -> float:
    if rng is None:
        rng = np.random.default_rng()
    escala = sensibilidade / epsilon
    ruido = rng.laplace(loc=0, scale=escala)
    return valor_real + ruido


def contagem_privada(
    serie_booleana: pd.Series,
    epsilon: float,
    rng: np.random.Generator | None = None,
) -> float:
    contagem_real = serie_booleana.sum()
    return adicionar_ruido_laplace(contagem_real, sensibilidade=1, epsilon=epsilon, rng=rng)


if __name__ == "__main__":
    df = pd.read_csv(CAMINHO_TRANSACOES_ENRIQUECIDAS)

    contagem_real = int(df["cross_border"].sum())
    print(f"Contagem real de transações cross-border: {contagem_real}")

    rng = np.random.default_rng(42)
    for epsilon in [0.1, 1.0, 10.0]:
        contagem_ruidosa = contagem_privada(df["cross_border"], epsilon=epsilon, rng=rng)
        print(f"epsilon={epsilon:>5}: contagem privatizada = {contagem_ruidosa:.1f}")

    print("\n=== Pseudonimização ===")
    salt = "jcn-2023-salt-secreto"
    for customer_id in df["customer_id"].head(3):
        print(f"{customer_id} -> {pseudonimizar_id(customer_id, salt)}")
