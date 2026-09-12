"""Módulo 07 — Gabarito comentado."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

HASH_GENESIS = "0" * 64


def calcular_hash(dados: dict, hash_anterior: str) -> str:
    texto = json.dumps(dados, sort_keys=True) + hash_anterior
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


class LivroDeAuditoria:
    def __init__(self) -> None:
        self.registros: list[dict] = []

    def registrar(self, ator: str, acao: str, dados: dict) -> dict:
        hash_anterior = self.registros[-1]["hash_atual"] if self.registros else HASH_GENESIS

        corpo = {
            "ator": ator,
            "acao": acao,
            "dados": dados,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        hash_atual = calcular_hash(corpo, hash_anterior)

        registro = {**corpo, "hash_anterior": hash_anterior, "hash_atual": hash_atual}
        self.registros.append(registro)
        return registro

    def verificar_integridade(self) -> bool:
        hash_esperado_anterior = HASH_GENESIS

        for registro in self.registros:
            if registro["hash_anterior"] != hash_esperado_anterior:
                return False

            corpo = {
                "ator": registro["ator"],
                "acao": registro["acao"],
                "dados": registro["dados"],
                "timestamp": registro["timestamp"],
            }
            hash_recalculado = calcular_hash(corpo, registro["hash_anterior"])
            if hash_recalculado != registro["hash_atual"]:
                return False

            hash_esperado_anterior = registro["hash_atual"]

        return True


if __name__ == "__main__":
    livro = LivroDeAuditoria()
    livro.registrar("soraya", "ingestao_legado", {"linhas_processadas": 5000})
    livro.registrar("soraya", "deteccao_anomalia", {"transacoes_suspeitas": 100})
    livro.registrar("victor", "aprovacao_relatorio", {"aprovado": True})

    print("Integridade antes da adulteração:", livro.verificar_integridade())

    livro.registros[1]["dados"]["transacoes_suspeitas"] = 1

    print("Integridade depois da adulteração:", livro.verificar_integridade())
