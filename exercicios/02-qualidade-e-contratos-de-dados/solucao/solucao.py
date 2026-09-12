"""Módulo 02 — Gabarito comentado."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

CAMINHO_TRANSACOES_BRUTAS = Path(__file__).parent / "../../dados/transacoes_brutas.csv"

TIPOS_VALIDOS = {"FATURA", "AJUSTE", "ESTORNO", "PAGAMENTO"}


def normalizar_data(valor: str) -> str:
    if "/" in valor:
        dia, mes, ano = valor.split("/")
        return f"{ano}-{mes}-{dia}"
    return valor


def normalizar_valor(valor) -> float:
    if isinstance(valor, str) and "," in valor:
        valor = valor.replace(",", ".")
    return float(valor)


def normalizar_tipo_transacao(valor: str) -> str:
    return valor.strip().upper()


def limpar_transacoes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["transaction_date"] = df["transaction_date"].apply(normalizar_data)
    df["amount"] = df["amount"].apply(normalizar_valor)
    df["transaction_type"] = df["transaction_type"].apply(normalizar_tipo_transacao)

    df = df.dropna(subset=["customer_id"])
    df = df.drop_duplicates(subset=["transaction_id"], keep="first")
    return df.reset_index(drop=True)


def validar_contrato(df: pd.DataFrame) -> dict:
    regex_iso = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    return {
        "sem_customer_id_nulo": bool(df["customer_id"].isna().sum() == 0),
        "sem_transaction_id_duplicado": bool(df["transaction_id"].duplicated().sum() == 0),
        "tipos_de_transacao_validos": bool(df["transaction_type"].isin(TIPOS_VALIDOS).all()),
        "valores_sao_numericos": df["amount"].dtype == float,
        "datas_no_formato_iso": bool(df["transaction_date"].apply(lambda d: bool(regex_iso.match(d))).all()),
    }


if __name__ == "__main__":
    bruto = pd.read_csv(CAMINHO_TRANSACOES_BRUTAS, dtype=str)
    limpo = limpar_transacoes(bruto)
    contrato = validar_contrato(limpo)

    print(f"Linhas antes da limpeza: {len(bruto)}")
    print(f"Linhas depois da limpeza: {len(limpo)}")
    print("=== Contrato de Dados ===")
    for regra, resultado in contrato.items():
        print(f"{regra}: {resultado}")
