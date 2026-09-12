"""Módulo 08 — Gabarito comentado."""

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
    return permissao in PERMISSOES_POR_PAPEL.get(papel, set())


def gerar_hash_senha(senha: str, salt: bytes | None = None) -> tuple[str, str]:
    if salt is None:
        salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, 100_000)
    return hash_bytes.hex(), salt.hex()


def verificar_senha(senha: str, hash_armazenado: str, salt_armazenado: str) -> bool:
    salt = bytes.fromhex(salt_armazenado)
    hash_calculado, _ = gerar_hash_senha(senha, salt)
    return hash_calculado == hash_armazenado


class KillSwitch:
    def __init__(self) -> None:
        self.ativo = False
        self.historico: list[dict] = []

    def acionar(self, papel_do_usuario: str, motivo: str) -> dict:
        if not tem_permissao(papel_do_usuario, "acionar_kill_switch"):
            raise PermissionError(
                f"O papel '{papel_do_usuario}' não tem permissão para acionar o kill switch."
            )

        evento = {
            "papel": papel_do_usuario,
            "motivo": motivo,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.ativo = True
        self.historico.append(evento)
        return evento


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
