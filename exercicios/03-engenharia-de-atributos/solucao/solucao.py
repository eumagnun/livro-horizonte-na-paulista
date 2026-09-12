"""Módulo 03 — Gabarito comentado."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

CAMINHO_TRANSACOES_LIMPAS = Path(__file__).parent / "../../dados/transacoes_limpas.csv"
CAMINHO_TABELA_RISCO = Path(__file__).parent / "../../dados/tabela_risco_pais.csv"


def enriquecer_com_risco_pais(df: pd.DataFrame, tabela_risco: pd.DataFrame) -> pd.DataFrame:
    return df.merge(tabela_risco, on="country", how="left")


def adicionar_flag_cross_border(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["cross_border"] = df["country"] != "BR"
    return df


def adicionar_zscore_por_cliente(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    media = df.groupby("customer_id")["amount"].transform("mean")
    desvio = df.groupby("customer_id")["amount"].transform("std").fillna(1.0)
    df["amount_zscore_cliente"] = (df["amount"] - media) / desvio
    return df


def construir_features(df: pd.DataFrame, tabela_risco: pd.DataFrame) -> pd.DataFrame:
    df = enriquecer_com_risco_pais(df, tabela_risco)
    df = adicionar_flag_cross_border(df)
    df = adicionar_zscore_por_cliente(df)
    return df


if __name__ == "__main__":
    transacoes = pd.read_csv(CAMINHO_TRANSACOES_LIMPAS)
    risco = pd.read_csv(CAMINHO_TABELA_RISCO)

    enriquecidas = construir_features(transacoes, risco)

    suspeitas = enriquecidas[
        (enriquecidas["amount_zscore_cliente"].abs() > 3) & (enriquecidas["is_tax_haven"])
    ]

    print(f"Total de transações: {len(enriquecidas)}")
    print(f"Transações com z-score > 3 em paraísos fiscais: {len(suspeitas)}")
    print(suspeitas[["transaction_id", "customer_id", "amount", "country_name"]].head(10))
