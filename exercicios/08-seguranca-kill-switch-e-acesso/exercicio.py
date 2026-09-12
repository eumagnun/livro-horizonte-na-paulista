"""
Módulo 08 — Segurança: Controle de Acesso e Kill Switch

Complete as funções e métodos marcados com TODO. Leia o README.md antes de
começar.
"""

from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone

PERMISSOES_POR_PAPEL: dict[str, set[str]] = {
    "engenheiro_dados": {"ver_transacoes_normais"},
    "auditor": {"ver_transacoes_normais", "ver_transacoes_suspeitas"},
    "cfo": {"ver_transacoes_normais", "ver_transacoes_suspeitas", "acionar_kill_switch"},
}


def tem_permissao(papel: str, permissao: str) -> bool:
    """Devolve True se o `papel` tem a `permissao`, consultando
    PERMISSOES_POR_PAPEL.
    """
    # TODO: implemente
    raise NotImplementedError("Implemente tem_permissao")


def gerar_hash_senha(senha: str, salt: bytes | None = None) -> tuple[str, str]:
    """Gera um hash de senha com salt usando PBKDF2-HMAC-SHA256.

    Se `salt` não for informado, gere um novo salt aleatório de 16 bytes
    (dica: os.urandom(16)).

    Devolva uma tupla (hash_hexadecimal, salt_hexadecimal).
    """
    # TODO: if salt is None: salt = os.urandom(16)
    # TODO: hash_bytes = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, 100_000)
    # TODO: devolva (hash_bytes.hex(), salt.hex())
    raise NotImplementedError("Implemente gerar_hash_senha")


def verificar_senha(senha: str, hash_armazenado: str, salt_armazenado: str) -> bool:
    """Recalcula o hash de `senha` usando o mesmo salt armazenado e compara
    com o hash armazenado.
    """
    # TODO: salt = bytes.fromhex(salt_armazenado)
    # TODO: hash_calculado, _ = gerar_hash_senha(senha, salt)
    # TODO: devolva hash_calculado == hash_armazenado
    raise NotImplementedError("Implemente verificar_senha")


class KillSwitch:
    """Um interruptor de emergência que só papéis autorizados podem acionar,
    e que registra cada tentativa de acionamento bem-sucedida.
    """

    def __init__(self) -> None:
        self.ativo = False
        self.historico: list[dict] = []

    def acionar(self, papel_do_usuario: str, motivo: str) -> dict:
        """Se `papel_do_usuario` tiver a permissão "acionar_kill_switch",
        marca self.ativo = True, registra um dicionário de evento (com
        "papel", "motivo" e "timestamp") em self.historico e devolve esse
        dicionário. Caso contrário, levanta PermissionError com uma mensagem
        clara.
        """
        # TODO: use tem_permissao para checar a permissão
        # TODO: se não tiver, levante PermissionError(...)
        # TODO: se tiver, monte o evento, marque self.ativo = True,
        #       adicione a self.historico e devolva o evento
        raise NotImplementedError("Implemente KillSwitch.acionar")


if __name__ == "__main__":
    kill_switch = KillSwitch()

    try:
        evento = kill_switch.acionar("cfo", "Suspeita de vazamento de dados confirmada")
        print(f"Kill switch acionado por {evento['papel']}: {evento['motivo']}")
    except PermissionError as erro:
        print(f"Falha ao acionar: {erro}")

    try:
        kill_switch.acionar("engenheiro_dados", "Só queria testar")
    except PermissionError as erro:
        print(f"Falha ao acionar (esperado): {erro}")

    hash_hex, salt_hex = gerar_hash_senha("senha-super-secreta")
    print("Senha correta valida?", verificar_senha("senha-super-secreta", hash_hex, salt_hex))
    print("Senha errada valida?", verificar_senha("chute-qualquer", hash_hex, salt_hex))
