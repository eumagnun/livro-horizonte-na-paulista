"""Módulo 04 — Gabarito comentado."""

from __future__ import annotations

import json
from pathlib import Path

CAMINHO_EVENTOS = Path(__file__).parent / "../../dados/eventos_stream.jsonl"

CODIGOS_SUSPEITOS = {"9A", "4F"}


def carregar_eventos(caminho: Path = CAMINHO_EVENTOS) -> list[dict]:
    with caminho.open(encoding="utf-8") as f:
        return [json.loads(linha) for linha in f]


def processar_em_lote(eventos: list[dict]) -> list[dict]:
    return [evento for evento in eventos if evento["adjustment_code"] in CODIGOS_SUSPEITOS]


class ProcessadorDeEventos:
    def __init__(self) -> None:
        self.total_processado = 0
        self.alertas: list[dict] = []

    def processar_evento(self, evento: dict) -> dict | None:
        self.total_processado += 1

        if evento["adjustment_code"] in CODIGOS_SUSPEITOS:
            alerta = {
                "posicao": self.total_processado,
                "transaction_id": evento["transaction_id"],
                "amount": evento["amount"],
            }
            self.alertas.append(alerta)
            return alerta

        return None


def processar_stream(eventos: list[dict]) -> list[dict]:
    processador = ProcessadorDeEventos()
    for evento in eventos:
        processador.processar_evento(evento)
    return processador.alertas


if __name__ == "__main__":
    eventos = carregar_eventos()

    print("=== Modo Batch (só sabemos no final) ===")
    suspeitos_batch = processar_em_lote(eventos)
    print(f"{len(suspeitos_batch)} transações suspeitas encontradas, só após ler os {len(eventos)} eventos.")

    print("\n=== Modo Streaming (sabemos evento a evento) ===")
    alertas = processar_stream(eventos)
    for alerta in alertas:
        print(f"Alerta na posição {alerta['posicao']}/{len(eventos)}: {alerta['transaction_id']} (R$ {alerta['amount']:.2f})")
