"""
Módulo 07 — Governança de Dados e Cadeia de Custódia

Complete as funções e métodos marcados com TODO. Leia o README.md antes de
começar.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

HASH_GENESIS = "0" * 64


def calcular_hash(dados: dict, hash_anterior: str) -> str:
    """Devolve um hash SHA-256 (hexadecimal) combinando `dados` (de forma
    determinística) com `hash_anterior`.
    """
    # TODO: texto = json.dumps(dados, sort_keys=True) + hash_anterior
    # TODO: devolva hashlib.sha256(texto.encode("utf-8")).hexdigest()
    raise NotImplementedError("Implemente calcular_hash")


class LivroDeAuditoria:
    """Um log de auditoria "append-only" (só cresce, nunca edita o passado),
    com os registros encadeados por hash -- a mesma ideia central de uma
    blockchain, em miniatura.
    """

    def __init__(self) -> None:
        self.registros: list[dict] = []

    def registrar(self, ator: str, acao: str, dados: dict) -> dict:
        """Cria e adiciona um novo registro de auditoria, encadeado ao
        anterior, e devolve o registro criado.
        """
        # TODO: hash_anterior = o hash_atual do último registro em
        #       self.registros, ou HASH_GENESIS se a lista estiver vazia
        # TODO: monte o dicionário `corpo` com "ator", "acao", "dados" e
        #       "timestamp" (dica: datetime.now(timezone.utc).isoformat())
        # TODO: hash_atual = calcular_hash(corpo, hash_anterior)
        # TODO: registro = {**corpo, "hash_anterior": hash_anterior, "hash_atual": hash_atual}
        # TODO: adicione `registro` a self.registros e devolva-o
        raise NotImplementedError("Implemente LivroDeAuditoria.registrar")

    def verificar_integridade(self) -> bool:
        """Devolve True se a cadeia inteira de registros é íntegra: cada
        hash_anterior bate com o hash_atual do registro anterior, e cada
        hash_atual recalculado bate com o valor guardado.
        """
        # TODO: percorra self.registros com um índice
        # TODO: para cada registro, descubra o hash_anterior esperado
        #       (HASH_GENESIS para o primeiro, ou o hash_atual do anterior)
        # TODO: compare com o registro["hash_anterior"] guardado
        # TODO: recalcule o hash a partir de {"ator", "acao", "dados", "timestamp"}
        #       do próprio registro e o hash_anterior guardado, e compare com
        #       registro["hash_atual"]
        # TODO: se qualquer uma dessas comparações falhar, devolva False
        # TODO: se percorrer tudo sem falhas, devolva True
        raise NotImplementedError("Implemente LivroDeAuditoria.verificar_integridade")


if __name__ == "__main__":
    livro = LivroDeAuditoria()
    livro.registrar("soraya", "ingestao_legado", {"linhas_processadas": 5000})
    livro.registrar("soraya", "deteccao_anomalia", {"transacoes_suspeitas": 100})
    livro.registrar("victor", "aprovacao_relatorio", {"aprovado": True})

    print("Integridade antes da adulteração:", livro.verificar_integridade())

    # Simula uma adulteração: alguém edita os dados de um registro do meio
    # diretamente, sem passar pelo método `registrar`.
    livro.registros[1]["dados"]["transacoes_suspeitas"] = 1

    print("Integridade depois da adulteração:", livro.verificar_integridade())
