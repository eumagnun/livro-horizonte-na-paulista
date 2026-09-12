"""Testes automáticos do Módulo 08. Rode com: pytest -v (a partir de exercicios/)"""

import pytest

from exercicio import KillSwitch, gerar_hash_senha, tem_permissao, verificar_senha


def test_tem_permissao_cfo_pode_acionar_kill_switch():
    assert tem_permissao("cfo", "acionar_kill_switch") is True


def test_tem_permissao_engenheiro_nao_pode_acionar_kill_switch():
    assert tem_permissao("engenheiro_dados", "acionar_kill_switch") is False


def test_tem_permissao_engenheiro_ve_transacoes_normais():
    assert tem_permissao("engenheiro_dados", "ver_transacoes_normais") is True


def test_tem_permissao_papel_desconhecido():
    assert tem_permissao("estagiario", "ver_transacoes_normais") is False


def test_gerar_hash_senha_e_verificar_senha_correta():
    hash_hex, salt_hex = gerar_hash_senha("minha-senha-123")
    assert verificar_senha("minha-senha-123", hash_hex, salt_hex) is True


def test_verificar_senha_incorreta_falha():
    hash_hex, salt_hex = gerar_hash_senha("minha-senha-123")
    assert verificar_senha("senha-errada", hash_hex, salt_hex) is False


def test_gerar_hash_senha_usa_salt_diferente_a_cada_chamada():
    _, salt1 = gerar_hash_senha("mesma-senha")
    _, salt2 = gerar_hash_senha("mesma-senha")
    assert salt1 != salt2


def test_kill_switch_aciona_com_papel_autorizado():
    ks = KillSwitch()
    evento = ks.acionar("cfo", "teste")
    assert ks.ativo is True
    assert len(ks.historico) == 1
    assert evento["papel"] == "cfo"
    assert evento["motivo"] == "teste"


def test_kill_switch_recusa_papel_nao_autorizado():
    ks = KillSwitch()
    with pytest.raises(PermissionError):
        ks.acionar("engenheiro_dados", "não deveria funcionar")
    assert ks.ativo is False
    assert ks.historico == []
