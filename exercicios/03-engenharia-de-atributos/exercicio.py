"""
Módulo 03 — Engenharia de Atributos e Enriquecimento de Dados

Complete as funções marcadas com TODO. Leia o README.md antes de começar.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

CAMINHO_TRANSACOES_LIMPAS = Path(__file__).parent / "../dados/transacoes_limpas.csv"
CAMINHO_TABELA_RISCO = Path(__file__).parent / "../dados/tabela_risco_pais.csv"


def enriquecer_com_risco_pais(df: pd.DataFrame, tabela_risco: pd.DataFrame) -> pd.DataFrame:
    """Junta `df` com `tabela_risco` pela coluna `country`, trazendo as
    colunas country_name, risk_score e is_tax_haven para dentro de `df`.
    """
    # TODO: use pd.merge (ou df.merge) com how="left" na coluna "country"
    raise NotImplementedError("Implemente enriquecer_com_risco_pais")


def adicionar_flag_cross_border(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona a coluna booleana `cross_border`: True quando country != 'BR'."""
    # TODO: df["cross_border"] = ...
    raise NotImplementedError("Implemente adicionar_flag_cross_border")


def adicionar_zscore_por_cliente(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona a coluna `amount_zscore_cliente`: quantos desvios-padrão o
    valor da transação está da média DAQUELE MESMO cliente.

    Fórmula: (amount - média_do_cliente) / desvio_padrão_do_cliente

    Dica: df.groupby("customer_id")["amount"].transform("mean") devolve uma
    série do mesmo tamanho de df, já alinhada linha a linha.
    """
    # TODO: calcule a média por cliente com groupby(...).transform("mean")
    # TODO: calcule o desvio-padrão por cliente com groupby(...).transform("std")
    # TODO: cuidado: clientes com uma única transação têm desvio-padrão NaN;
    #       trate esse caso substituindo NaN por 1.0 (dica: .fillna(1.0))
    raise NotImplementedError("Implemente adicionar_zscore_por_cliente")


def construir_features(df: pd.DataFrame, tabela_risco: pd.DataFrame) -> pd.DataFrame:
    """Já implementada: encadeia as três funções acima."""
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
