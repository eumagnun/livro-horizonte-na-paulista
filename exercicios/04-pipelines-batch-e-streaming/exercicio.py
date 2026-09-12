"""
Módulo 04 — Pipelines de Dados: Batch vs. Streaming

Complete as funções e a classe marcadas com TODO. Leia o README.md antes de
começar.
"""

from __future__ import annotations

import json
from pathlib import Path

CAMINHO_EVENTOS = Path(__file__).parent / "../dados/eventos_stream.jsonl"

CODIGOS_SUSPEITOS = {"9A", "4F"}


def carregar_eventos(caminho: Path = CAMINHO_EVENTOS) -> list[dict]:
    """Já implementada: lê o arquivo JSON Lines e devolve uma lista de dicts."""
    with caminho.open(encoding="utf-8") as f:
        return [json.loads(linha) for linha in f]


def processar_em_lote(eventos: list[dict]) -> list[dict]:
    """Recebe a lista INTEIRA de eventos de uma vez e devolve apenas os que
    têm adjustment_code em CODIGOS_SUSPEITOS. Simula a abordagem batch: só
    conseguimos essa lista depois que TODOS os eventos já chegaram.
    """
    # TODO: use uma list comprehension (ou um for) para filtrar os eventos
    #       cujo campo "adjustment_code" está em CODIGOS_SUSPEITOS
    raise NotImplementedError("Implemente processar_em_lote")


class ProcessadorDeEventos:
    """Representa uma pipeline orientada a eventos: cada evento é analisado
    assim que chega, um de cada vez, sem esperar os demais.
    """

    def __init__(self) -> None:
        self.total_processado = 0
        self.alertas: list[dict] = []

    def processar_evento(self, evento: dict) -> dict | None:
        """Analisa UM evento. Se for suspeito, cria um dicionário de alerta
        com as chaves `posicao` (quantos eventos já foram processados,
        contando este), `transaction_id` e `amount`; adiciona esse alerta em
        `self.alertas` e devolve o alerta. Se não for suspeito, devolve None.

        Não esqueça de incrementar `self.total_processado` a cada chamada,
        suspeito ou não.
        """
        # TODO: incremente self.total_processado
        # TODO: verifique se evento["adjustment_code"] está em CODIGOS_SUSPEITOS
        # TODO: se sim, monte o dicionário de alerta, adicione a self.alertas
        #       e devolva-o. Se não, devolva None.
        raise NotImplementedError("Implemente ProcessadorDeEventos.processar_evento")


def processar_stream(eventos: list[dict]) -> list[dict]:
    """Alimenta um ProcessadorDeEventos um evento de cada vez (nunca a lista
    inteira) e devolve a lista de alertas gerados, na ordem em que
    apareceram.
    """
    # TODO: crie um ProcessadorDeEventos
    # TODO: percorra `eventos` um a um chamando processar_evento
    # TODO: devolva processador.alertas
    raise NotImplementedError("Implemente processar_stream")


if __name__ == "__main__":
    eventos = carregar_eventos()

    print("=== Modo Batch (só sabemos no final) ===")
    suspeitos_batch = processar_em_lote(eventos)
    print(f"{len(suspeitos_batch)} transações suspeitas encontradas, só após ler os {len(eventos)} eventos.")

    print("\n=== Modo Streaming (sabemos evento a evento) ===")
    alertas = processar_stream(eventos)
    for alerta in alertas:
        print(f"Alerta na posição {alerta['posicao']}/{len(eventos)}: {alerta['transaction_id']} (R$ {alerta['amount']:.2f})")
