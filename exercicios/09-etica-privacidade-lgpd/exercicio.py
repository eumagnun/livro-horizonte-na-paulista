"""
Módulo 09 — Ética, Privacidade e Anonimização de Dados

Complete as funções marcadas com TODO. Leia o README.md antes de começar.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

CAMINHO_TRANSACOES_ENRIQUECIDAS = Path(__file__).parent / "../dados/transacoes_enriquecidas_gabarito.csv"


def pseudonimizar_id(identificador: str, salt: str) -> str:
    """Devolve o hash SHA-256 (hexadecimal) de `identificador + salt`."""
    # TODO: texto = identificador + salt
    # TODO: devolva hashlib.sha256(texto.encode("utf-8")).hexdigest()
    raise NotImplementedError("Implemente pseudonimizar_id")


def adicionar_ruido_laplace(
    valor_real: float,
    sensibilidade: float,
    epsilon: float,
    rng: np.random.Generator | None = None,
) -> float:
    """Implementa o Mecanismo de Laplace de Privacidade Diferencial: soma a
    `valor_real` um ruído aleatório de uma distribuição de Laplace com
    escala `sensibilidade / epsilon`.
    """
    # TODO: if rng is None: rng = np.random.default_rng()
    # TODO: escala = sensibilidade / epsilon
    # TODO: ruido = rng.laplace(loc=0, scale=escala)
    # TODO: devolva valor_real + ruido
    raise NotImplementedError("Implemente adicionar_ruido_laplace")


def contagem_privada(
    serie_booleana: pd.Series,
    epsilon: float,
    rng: np.random.Generator | None = None,
) -> float:
    """Conta quantos valores True existem em `serie_booleana` e devolve essa
    contagem com ruído de Laplace (sensibilidade=1).
    """
    # TODO: contagem_real = serie_booleana.sum()
    # TODO: devolva adicionar_ruido_laplace(contagem_real, sensibilidade=1, epsilon=epsilon, rng=rng)
    raise NotImplementedError("Implemente contagem_privada")


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
