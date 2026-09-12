"""Testes automáticos do Módulo 07. Rode com: pytest -v (a partir de exercicios/)"""

from exercicio import HASH_GENESIS, LivroDeAuditoria, calcular_hash


def test_calcular_hash_e_deterministico():
    h1 = calcular_hash({"a": 1}, HASH_GENESIS)
    h2 = calcular_hash({"a": 1}, HASH_GENESIS)
    assert h1 == h2
    assert len(h1) == 64  # sha256 em hexadecimal


def test_calcular_hash_muda_se_dados_mudam():
    h1 = calcular_hash({"a": 1}, HASH_GENESIS)
    h2 = calcular_hash({"a": 2}, HASH_GENESIS)
    assert h1 != h2


def test_registrar_encadeia_com_hash_anterior():
    livro = LivroDeAuditoria()
    r1 = livro.registrar("soraya", "acao1", {"x": 1})
    r2 = livro.registrar("soraya", "acao2", {"x": 2})

    assert r1["hash_anterior"] == HASH_GENESIS
    assert r2["hash_anterior"] == r1["hash_atual"]
    assert r1["hash_atual"] != r2["hash_atual"]


def test_verificar_integridade_livro_vazio_e_integro():
    livro = LivroDeAuditoria()
    assert livro.verificar_integridade() is True


def test_verificar_integridade_livro_normal_e_integro():
    livro = LivroDeAuditoria()
    livro.registrar("soraya", "ingestao", {"linhas": 100})
    livro.registrar("victor", "aprovacao", {"ok": True})
    assert livro.verificar_integridade() is True


def test_verificar_integridade_detecta_adulteracao():
    livro = LivroDeAuditoria()
    livro.registrar("soraya", "ingestao", {"linhas": 100})
    livro.registrar("victor", "aprovacao", {"ok": True})
    livro.registrar("eduardo", "aprovacao_final", {"ok": True})

    assert livro.verificar_integridade() is True

    # Adulteração: editar um registro do meio diretamente.
    livro.registros[1]["dados"]["ok"] = False

    assert livro.verificar_integridade() is False
