"""Testes automáticos do Módulo 09. Rode com: pytest -v (a partir de exercicios/)"""

import numpy as np
import pandas as pd

from exercicio import adicionar_ruido_laplace, contagem_privada, pseudonimizar_id


def test_pseudonimizar_id_e_deterministico():
    h1 = pseudonimizar_id("CLI000123", "salt-a")
    h2 = pseudonimizar_id("CLI000123", "salt-a")
    assert h1 == h2
    assert len(h1) == 64


def test_pseudonimizar_id_muda_com_salt_diferente():
    h1 = pseudonimizar_id("CLI000123", "salt-a")
    h2 = pseudonimizar_id("CLI000123", "salt-b")
    assert h1 != h2


def test_pseudonimizar_id_nao_revela_o_original():
    identificador = "CLI000123"
    hash_resultado = pseudonimizar_id(identificador, "salt-a")
    assert identificador not in hash_resultado


def test_adicionar_ruido_laplace_e_reprodutivel_com_rng_fixo():
    rng1 = np.random.default_rng(123)
    rng2 = np.random.default_rng(123)
    r1 = adicionar_ruido_laplace(100.0, sensibilidade=1, epsilon=1.0, rng=rng1)
    r2 = adicionar_ruido_laplace(100.0, sensibilidade=1, epsilon=1.0, rng=rng2)
    assert r1 == r2


def test_adicionar_ruido_laplace_diminui_com_epsilon_maior():
    # Em média, o ruído absoluto deve ser bem menor com epsilon alto do que
    # com epsilon baixo (mais privacidade = mais ruído = epsilon menor).
    rng = np.random.default_rng(42)
    ruidos_epsilon_baixo = [
        abs(adicionar_ruido_laplace(0.0, sensibilidade=1, epsilon=0.1, rng=rng)) for _ in range(500)
    ]
    ruidos_epsilon_alto = [
        abs(adicionar_ruido_laplace(0.0, sensibilidade=1, epsilon=10.0, rng=rng)) for _ in range(500)
    ]
    assert np.mean(ruidos_epsilon_baixo) > np.mean(ruidos_epsilon_alto)


def test_contagem_privada_fica_proxima_da_contagem_real_com_epsilon_alto():
    rng = np.random.default_rng(0)
    serie = pd.Series([True, True, True, False, False, False, False, False, False, False])
    contagem_real = serie.sum()

    resultados = [contagem_privada(serie, epsilon=50.0, rng=rng) for _ in range(200)]
    media = np.mean(resultados)

    assert abs(media - contagem_real) < 0.5
