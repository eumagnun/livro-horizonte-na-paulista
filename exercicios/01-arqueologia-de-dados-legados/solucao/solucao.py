"""
Módulo 01 — Gabarito comentado.

Só olhe este arquivo depois de tentar resolver `exercicio.py` por conta
própria. O valor do exercício está no processo, não na resposta pronta.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

CAMINHO_ARQUIVO_LEGADO = Path(__file__).parent / "../../dados/legado_faturamento.ebcdic.txt"


def decodificar_arquivo(caminho: Path) -> list[str]:
    bytes_brutos = caminho.read_bytes()
    texto = bytes_brutos.decode("cp037")
    return texto.splitlines()


def parsear_linha(linha: str) -> dict:
    transaction_id = linha[0:11].strip()
    customer_id = linha[11:21].strip()
    data_bruta = linha[21:29].strip()  # "YYYYMMDD"
    transaction_type = linha[29:39].strip()
    amount_bruto = linha[39:53].strip()  # sinal + 13 dígitos, em centavos
    adjustment_code = linha[53:57].strip()
    network_node = linha[57:72].strip()
    country = linha[72:75].strip()

    data_formatada = f"{data_bruta[0:4]}-{data_bruta[4:6]}-{data_bruta[6:8]}"

    sinal = -1 if amount_bruto[0] == "-" else 1
    centavos = int(amount_bruto[1:])
    amount = sinal * centavos / 100

    return {
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "transaction_date": data_formatada,
        "transaction_type": transaction_type,
        "amount": amount,
        "adjustment_code": adjustment_code,
        "network_node": network_node,
        "country": country,
    }


def carregar_arquivo_legado(caminho: Path = CAMINHO_ARQUIVO_LEGADO) -> pd.DataFrame:
    linhas = decodificar_arquivo(caminho)
    registros = [parsear_linha(linha) for linha in linhas if linha.strip()]
    df = pd.DataFrame(registros)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["amount"] = df["amount"].astype(float)
    return df


def perfilar_dados(df: pd.DataFrame) -> dict:
    total_linhas = len(df)
    nulos_por_coluna = df.isna().sum().to_dict()
    valor_minimo = float(df["amount"].min())
    valor_maximo = float(df["amount"].max())

    negativos_fora_estorno = df[(df["amount"] < 0) & (df["transaction_type"] != "ESTORNO")]
    pct = (len(negativos_fora_estorno) / total_linhas) * 100

    return {
        "total_linhas": total_linhas,
        "nulos_por_coluna": nulos_por_coluna,
        "valor_minimo": valor_minimo,
        "valor_maximo": valor_maximo,
        "pct_valores_negativos_fora_estorno": pct,
    }


if __name__ == "__main__":
    df = carregar_arquivo_legado()
    relatorio = perfilar_dados(df)

    print("=== Relatório de Perfilamento — Legacy-Billing-V3 ===")
    for chave, valor in relatorio.items():
        print(f"{chave}: {valor}")
