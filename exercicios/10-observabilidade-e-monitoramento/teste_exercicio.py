"""Testes automáticos do Módulo 10. Rode com: pytest -v (a partir de exercicios/)"""

import numpy as np

from exercicio import calcular_psi, calcular_taxa_erro, classificar_drift


def test_calcular_taxa_erro():
    logs = [{"status": "SUCCESS"}] * 90 + [{"status": "ERROR"}] * 10
    assert calcular_taxa_erro(logs) == 10.0


def test_calcular_taxa_erro_sem_erros():
    logs = [{"status": "SUCCESS"}] * 20
    assert calcular_taxa_erro(logs) == 0.0


def test_calcular_psi_distribuicoes_identicas_e_proximo_de_zero():
    rng = np.random.default_rng(1)
    referencia = rng.normal(100, 10, size=2000)
    atual = referencia.copy()
    psi = calcular_psi(referencia, atual)
    assert psi < 0.01


def test_calcular_psi_distribuicoes_muito_diferentes_e_alto():
    rng = np.random.default_rng(1)
    referencia = rng.normal(100, 10, size=2000)
    atual = rng.normal(500, 10, size=2000)
    psi = calcular_psi(referencia, atual)
    assert psi > 1.0


def test_classificar_drift_limiares():
    assert classificar_drift(0.05) == "sem drift"
    assert classificar_drift(0.15) == "drift moderado"
    assert classificar_drift(0.30) == "drift severo"
