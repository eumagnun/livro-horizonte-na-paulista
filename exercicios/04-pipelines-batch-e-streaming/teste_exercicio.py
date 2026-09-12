"""Testes automáticos do Módulo 04. Rode com: pytest -v (a partir de exercicios/)"""

import pytest

from exercicio import (
    ProcessadorDeEventos,
    carregar_eventos,
    processar_em_lote,
    processar_stream,
)


@pytest.fixture(scope="module")
def eventos():
    return carregar_eventos()


def test_carregar_eventos_le_arquivo_jsonl(eventos):
    assert len(eventos) == 300
    assert "adjustment_code" in eventos[0]


def test_processar_em_lote_encontra_suspeitos(eventos):
    suspeitos = processar_em_lote(eventos)
    assert len(suspeitos) == 10
    assert all(e["adjustment_code"] in {"9A", "4F"} for e in suspeitos)


def test_processador_de_eventos_ignora_evento_normal():
    processador = ProcessadorDeEventos()
    evento_normal = {"transaction_id": "TXN1", "amount": 100.0, "adjustment_code": "00"}
    resultado = processador.processar_evento(evento_normal)
    assert resultado is None
    assert processador.total_processado == 1
    assert processador.alertas == []


def test_processador_de_eventos_detecta_evento_suspeito():
    processador = ProcessadorDeEventos()
    processador.processar_evento({"transaction_id": "TXN1", "amount": 100.0, "adjustment_code": "00"})
    alerta = processador.processar_evento(
        {"transaction_id": "TXN2", "amount": 250000.0, "adjustment_code": "9A"}
    )
    assert alerta is not None
    assert alerta["posicao"] == 2
    assert alerta["transaction_id"] == "TXN2"
    assert len(processador.alertas) == 1


def test_processar_stream_encontra_os_mesmos_suspeitos_que_o_lote(eventos):
    suspeitos_batch = {e["transaction_id"] for e in processar_em_lote(eventos)}
    alertas_stream = processar_stream(eventos)
    suspeitos_stream = {a["transaction_id"] for a in alertas_stream}

    assert suspeitos_stream == suspeitos_batch
    # As posições devem estar em ordem crescente (detectadas ao longo do tempo)
    posicoes = [a["posicao"] for a in alertas_stream]
    assert posicoes == sorted(posicoes)
