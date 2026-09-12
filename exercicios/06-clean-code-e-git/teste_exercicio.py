"""Testes automáticos do Módulo 06. Rode com: pytest -v (a partir de exercicios/)"""

import random

import pytest

from codigo_legado.faturamento_legado import proc
from exercicio import (
    calcular_valor_efetivo,
    eh_ajuste_suspeito,
    somar_ajustes_suspeitos_por_no,
)


def test_eh_ajuste_suspeito():
    assert eh_ajuste_suspeito("9A") is True
    assert eh_ajuste_suspeito("4F") is True
    assert eh_ajuste_suspeito("00") is False


def test_calcular_valor_efetivo_estorno_e_sempre_negativo():
    assert calcular_valor_efetivo(500.0, "ESTORNO") == -500.0
    assert calcular_valor_efetivo(-500.0, "ESTORNO") == -500.0


def test_calcular_valor_efetivo_outros_tipos_e_sempre_positivo():
    assert calcular_valor_efetivo(500.0, "PAGAMENTO") == 500.0
    assert calcular_valor_efetivo(-500.0, "FATURA") == 500.0


def _gerar_transacoes_aleatorias(n: int, seed: int) -> list[tuple]:
    rng = random.Random(seed)
    tipos = ["FATURA", "AJUSTE", "ESTORNO", "PAGAMENTO"]
    codigos = ["00", "01", "9A", "4F", "10"]
    nos = ["SANTOS-PORT-07", "SP-CORE-01", "RJ-CORE-01"]

    transacoes = []
    for _ in range(n):
        valor = rng.uniform(-5000, 5000)
        tipo = rng.choice(tipos)
        no = rng.choice(nos)
        codigo = rng.choice(codigos)
        transacoes.append((valor, tipo, no, codigo))
    return transacoes


def test_refatoracao_produz_mesmo_resultado_que_codigo_legado():
    transacoes = _gerar_transacoes_aleatorias(n=200, seed=7)

    resultado_legado = proc(transacoes)
    resultado_novo = somar_ajustes_suspeitos_por_no(transacoes)

    assert resultado_novo.keys() == resultado_legado.keys()
    for chave in resultado_legado:
        assert resultado_novo[chave] == pytest.approx(resultado_legado[chave])


def test_refatoracao_lida_com_lista_vazia():
    assert somar_ajustes_suspeitos_por_no([]) == proc([])
