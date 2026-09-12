"""
Módulo 01 — Arqueologia de Dados: Ingestão de Sistemas Legados

Complete as funções marcadas com TODO. Leia o README.md deste módulo antes
de começar — ele explica o cenário de negócio e o layout do arquivo.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

CAMINHO_ARQUIVO_LEGADO = Path(__file__).parent / "../dados/legado_faturamento.ebcdic.txt"


def decodificar_arquivo(caminho: Path) -> list[str]:
    """Lê o arquivo binário em `caminho` e devolve uma lista de linhas de
    texto, já decodificadas de EBCDIC (codec 'cp037') para strings normais
    do Python. Remova quebras de linha do final de cada string.
    """
    # TODO: leia os bytes do arquivo com caminho.read_bytes()
    # TODO: decodifique os bytes usando o codec "cp037"
    # TODO: separe o texto em linhas (dica: str.splitlines())
    raise NotImplementedError("Implemente decodificar_arquivo")


def parsear_linha(linha: str) -> dict:
    """Recebe uma linha de texto já decodificada e devolve um dicionário com
    os campos extraídos, de acordo com o layout em '../dados/layout_legado.txt'.

    Chaves esperadas no dicionário de saída:
        transaction_id, customer_id, transaction_date (str "YYYY-MM-DD"),
        transaction_type, amount (float, em reais), adjustment_code,
        network_node, country
    """
    # TODO: use fatiamento de string (slicing) para extrair cada campo,
    # usando as posições documentadas em layout_legado.txt.
    # Lembre-se de:
    #   - usar .strip() para remover espaços de preenchimento (padding)
    #   - converter o campo de data de "YYYYMMDD" para "YYYY-MM-DD"
    #   - converter o campo amount (sinal + 13 dígitos em centavos) para
    #     um float em reais, ex: "+0000000151095" -> 1510.95
    raise NotImplementedError("Implemente parsear_linha")


def carregar_arquivo_legado(caminho: Path = CAMINHO_ARQUIVO_LEGADO) -> pd.DataFrame:
    """Já implementada: usa as duas funções acima para montar o DataFrame."""
    linhas = decodificar_arquivo(caminho)
    registros = [parsear_linha(linha) for linha in linhas if linha.strip()]
    df = pd.DataFrame(registros)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["amount"] = df["amount"].astype(float)
    return df


def perfilar_dados(df: pd.DataFrame) -> dict:
    """Devolve um dicionário com estatísticas de perfilamento do DataFrame.

    Chaves esperadas:
        total_linhas (int)
        nulos_por_coluna (dict[str, int])
        valor_minimo (float)
        valor_maximo (float)
        pct_valores_negativos_fora_estorno (float, entre 0 e 100)
    """
    # TODO: total_linhas = número de linhas do DataFrame
    # TODO: nulos_por_coluna = contagem de nulos por coluna (dica: df.isna().sum())
    # TODO: valor_minimo / valor_maximo = menor/maior valor da coluna "amount"
    # TODO: pct_valores_negativos_fora_estorno =
    #       (linhas com amount < 0 E transaction_type != "ESTORNO") / total * 100
    raise NotImplementedError("Implemente perfilar_dados")


if __name__ == "__main__":
    df = carregar_arquivo_legado()
    relatorio = perfilar_dados(df)

    print("=== Relatório de Perfilamento — Legacy-Billing-V3 ===")
    for chave, valor in relatorio.items():
        print(f"{chave}: {valor}")
