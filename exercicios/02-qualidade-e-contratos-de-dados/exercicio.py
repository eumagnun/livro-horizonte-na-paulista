"""
Módulo 02 — Qualidade de Dados e Contratos de Dados

Complete as funções marcadas com TODO. Leia o README.md antes de começar.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

CAMINHO_TRANSACOES_BRUTAS = Path(__file__).parent / "../dados/transacoes_brutas.csv"

TIPOS_VALIDOS = {"FATURA", "AJUSTE", "ESTORNO", "PAGAMENTO"}


def normalizar_data(valor: str) -> str:
    """Recebe uma data em 'YYYY-MM-DD' OU 'DD/MM/YYYY' e devolve sempre em
    'YYYY-MM-DD'.
    """
    # TODO: se `valor` contém "/", é formato DD/MM/YYYY -> reordene as partes
    # TODO: caso contrário, já está em YYYY-MM-DD -> devolva como está
    raise NotImplementedError("Implemente normalizar_data")


def normalizar_valor(valor) -> float:
    """Recebe um valor monetário (string com ponto OU vírgula decimal, ou já
    um número) e devolve sempre um float.
    """
    # TODO: se `valor` for string e contiver vírgula, troque "," por "."
    # TODO: converta o resultado para float
    raise NotImplementedError("Implemente normalizar_valor")


def normalizar_tipo_transacao(valor: str) -> str:
    """Devolve o tipo de transação sempre em maiúsculas, sem espaços nas bordas."""
    # TODO: use .strip().upper()
    raise NotImplementedError("Implemente normalizar_tipo_transacao")


def limpar_transacoes(df: pd.DataFrame) -> pd.DataFrame:
    """Recebe o DataFrame bruto (todas as colunas como string) e devolve um
    DataFrame limpo:
      - transaction_date, amount e transaction_type normalizados
      - linhas com customer_id nulo removidas
      - duplicatas de transaction_id removidas (mantendo a primeira ocorrência)
    """
    # TODO: aplique normalizar_data, normalizar_valor e normalizar_tipo_transacao
    #       às colunas correspondentes (dica: df["coluna"].apply(funcao))
    # TODO: remova linhas onde customer_id é nulo (dica: df.dropna(subset=[...]))
    # TODO: remova duplicatas por transaction_id (dica: df.drop_duplicates(subset=[...]))
    raise NotImplementedError("Implemente limpar_transacoes")


def validar_contrato(df: pd.DataFrame) -> dict:
    """Recebe um DataFrame JÁ LIMPO e devolve um dicionário
    {nome_da_regra: True/False} indicando se cada regra do contrato de dados
    foi cumprida.
    """
    # TODO: "sem_customer_id_nulo" -> não existe nenhum nulo em customer_id
    # TODO: "sem_transaction_id_duplicado" -> não há transaction_id repetido
    # TODO: "tipos_de_transacao_validos" -> todo valor de transaction_type
    #       está em TIPOS_VALIDOS
    # TODO: "valores_sao_numericos" -> a coluna amount é do tipo float
    # TODO: "datas_no_formato_iso" -> todo valor casa com o regex
    #       r"^\d{4}-\d{2}-\d{2}$"
    raise NotImplementedError("Implemente validar_contrato")


if __name__ == "__main__":
    bruto = pd.read_csv(CAMINHO_TRANSACOES_BRUTAS, dtype=str)
    limpo = limpar_transacoes(bruto)
    contrato = validar_contrato(limpo)

    print(f"Linhas antes da limpeza: {len(bruto)}")
    print(f"Linhas depois da limpeza: {len(limpo)}")
    print("=== Contrato de Dados ===")
    for regra, resultado in contrato.items():
        print(f"{regra}: {resultado}")
