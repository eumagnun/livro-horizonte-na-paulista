"""
Módulo 06 — Refatoração com Clean Code

Reescreva, de forma limpa, a mesma lógica de
`codigo_legado/faturamento_legado.py`. Leia o README.md antes de começar.

A entrada continua sendo uma lista de tuplas:
    (amount: float, transaction_type: str, network_node: str, adjustment_code: str)
"""

from __future__ import annotations

CODIGOS_DE_AJUSTE_SUSPEITOS = {"9A", "4F"}


def eh_ajuste_suspeito(codigo_ajuste: str) -> bool:
    """Devolve True se o código de ajuste é um dos códigos suspeitos."""
    # TODO: implemente
    raise NotImplementedError("Implemente eh_ajuste_suspeito")


def calcular_valor_efetivo(valor: float, tipo_transacao: str) -> float:
    """Devolve o valor "efetivo" da transação para fins de soma:
    - se for um ESTORNO, o valor efetivo é sempre negativo;
    - para qualquer outro tipo, o valor efetivo é sempre positivo.
    (Isto é: usamos o valor absoluto, com o sinal certo para cada caso.)
    """
    # TODO: implemente
    raise NotImplementedError("Implemente calcular_valor_efetivo")


def somar_ajustes_suspeitos_por_no(transacoes: list[tuple]) -> dict[str, float]:
    """Recebe uma lista de tuplas (amount, transaction_type, network_node,
    adjustment_code) e devolve um dicionário {network_node: soma}, somando
    apenas as transações cujo adjustment_code é suspeito.
    """
    # TODO: use eh_ajuste_suspeito e calcular_valor_efetivo para montar o
    #       dicionário de resultado, um nó de rede por chave.
    raise NotImplementedError("Implemente somar_ajustes_suspeitos_por_no")


if __name__ == "__main__":
    exemplo = [
        (1000.0, "PAGAMENTO", "SANTOS-PORT-07", "9A"),
        (-500.0, "ESTORNO", "SANTOS-PORT-07", "9A"),
        (200.0, "FATURA", "SP-CORE-01", "00"),
    ]
    print(somar_ajustes_suspeitos_por_no(exemplo))
