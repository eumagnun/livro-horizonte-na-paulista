"""Módulo 06 — Gabarito comentado."""

from __future__ import annotations

CODIGOS_DE_AJUSTE_SUSPEITOS = {"9A", "4F"}


def eh_ajuste_suspeito(codigo_ajuste: str) -> bool:
    return codigo_ajuste in CODIGOS_DE_AJUSTE_SUSPEITOS


def calcular_valor_efetivo(valor: float, tipo_transacao: str) -> float:
    if tipo_transacao == "ESTORNO":
        return -abs(valor)
    return abs(valor)


def somar_ajustes_suspeitos_por_no(transacoes: list[tuple]) -> dict[str, float]:
    total_por_no: dict[str, float] = {}

    for valor, tipo_transacao, no_rede, codigo_ajuste in transacoes:
        if not eh_ajuste_suspeito(codigo_ajuste):
            continue

        valor_efetivo = calcular_valor_efetivo(valor, tipo_transacao)
        total_por_no[no_rede] = total_por_no.get(no_rede, 0) + valor_efetivo

    return total_por_no


if __name__ == "__main__":
    exemplo = [
        (1000.0, "PAGAMENTO", "SANTOS-PORT-07", "9A"),
        (-500.0, "ESTORNO", "SANTOS-PORT-07", "9A"),
        (200.0, "FATURA", "SP-CORE-01", "00"),
    ]
    print(somar_ajustes_suspeitos_por_no(exemplo))
