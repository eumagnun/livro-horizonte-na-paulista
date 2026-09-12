"""
Módulo 11 — Gabarito de referência do projeto final.

Este é só UM jeito válido de resolver o projeto (reaproveitando as soluções
dos módulos anteriores via importlib). O README.md deixa claro que
reescrever o código diretamente também é uma solução válida. Não existe um
único "gabarito certo" para um projeto de síntese como este — use isto como
inspiração, não como molde a copiar.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).parent / ".."


def importar_modulo(caminho_relativo: str, nome: str):
    caminho = (RAIZ / caminho_relativo).resolve()
    spec = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def executar_investigacao(papel_do_usuario: str) -> dict:
    mod01 = importar_modulo("../01-arqueologia-de-dados-legados/solucao/solucao.py", "mod01")
    mod02 = importar_modulo("../02-qualidade-e-contratos-de-dados/solucao/solucao.py", "mod02")
    mod03 = importar_modulo("../03-engenharia-de-atributos/solucao/solucao.py", "mod03")
    mod05 = importar_modulo("../05-deteccao-de-anomalias-e-fraude/solucao/solucao.py", "mod05")
    mod07 = importar_modulo("../07-governanca-e-auditoria/solucao/solucao.py", "mod07")
    mod08 = importar_modulo("../08-seguranca-kill-switch-e-acesso/solucao/solucao.py", "mod08")
    mod09 = importar_modulo("../09-etica-privacidade-lgpd/solucao/solucao.py", "mod09")
    mod10 = importar_modulo("../10-observabilidade-e-monitoramento/solucao/solucao.py", "mod10")

    livro = mod07.LivroDeAuditoria()

    # 1. Ingestão
    df = mod01.carregar_arquivo_legado()
    perfil = mod01.perfilar_dados(df)
    livro.registrar("investigacao_jcn", "ingestao_legado", {"total_linhas": perfil["total_linhas"]})

    # 2. Qualidade de dados: convertemos para o formato "bruto" (strings)
    # que a função de limpeza do Módulo 02 espera, para reaproveitá-la.
    df_como_bruto = df.copy()
    df_como_bruto["transaction_date"] = df_como_bruto["transaction_date"].dt.strftime("%Y-%m-%d")
    df_como_bruto["amount"] = df_como_bruto["amount"].astype(str)
    df_limpo = mod02.limpar_transacoes(df_como_bruto)
    contrato = mod02.validar_contrato(df_limpo)
    livro.registrar("investigacao_jcn", "validacao_contrato", contrato)

    # 3. Engenharia de atributos
    tabela_risco = pd.read_csv(RAIZ / "../dados/tabela_risco_pais.csv")
    df_features = mod03.construir_features(df_limpo, tabela_risco)
    livro.registrar("investigacao_jcn", "engenharia_atributos", {"colunas": list(df_features.columns)})

    # 4. Detecção de anomalias
    X = mod05.preparar_matriz_features(df_features)
    modelo = mod05.treinar_detector(X)
    df_resultado = mod05.detectar_anomalias(df_features, modelo)
    n_suspeitas = int(df_resultado["is_anomaly_predicted"].sum())
    livro.registrar("investigacao_jcn", "deteccao_anomalias", {"transacoes_sinalizadas": n_suspeitas})

    # 6. Controle de acesso (checamos ANTES de montar o relatório sensível)
    if not mod08.tem_permissao(papel_do_usuario, "ver_transacoes_suspeitas"):
        raise PermissionError(f"Papel '{papel_do_usuario}' não pode ver transações suspeitas.")

    suspeitas = df_resultado[df_resultado["is_anomaly_predicted"]].copy()

    # 7. Privacidade: pseudonimiza customer_id antes de expor no relatório
    salt = "investigacao-jcn-2023"
    suspeitas["customer_id_pseudonimizado"] = suspeitas["customer_id"].apply(
        lambda cid: mod09.pseudonimizar_id(cid, salt)[:12]
    )
    top_10 = suspeitas.sort_values("amount_zscore_cliente", ascending=False).head(10)
    top_10_relatorio = top_10[["customer_id_pseudonimizado", "amount", "amount_zscore_cliente", "country"]]

    # 8. Observabilidade: drift entre Q1 e Q4 das transações suspeitas
    suspeitas["transaction_date"] = pd.to_datetime(suspeitas["transaction_date"])
    q1 = suspeitas[suspeitas["transaction_date"].dt.quarter == 1]["amount"].to_numpy()
    q4 = suspeitas[suspeitas["transaction_date"].dt.quarter == 4]["amount"].to_numpy()
    if len(q1) >= 2 and len(q4) >= 2:
        psi = mod10.calcular_psi(q1, q4, n_bins=4)
        drift = mod10.classificar_drift(psi)
    else:
        psi, drift = None, "amostra insuficiente para medir drift"
    livro.registrar("investigacao_jcn", "checagem_observabilidade", {"psi": psi, "classificacao": drift})

    relatorio = {
        "total_transacoes": len(df_resultado),
        "total_sinalizadas": n_suspeitas,
        "contrato_de_dados_aprovado": all(contrato.values()),
        "top_10_clientes_suspeitos": top_10_relatorio,
        "drift_psi": psi,
        "drift_classificacao": drift,
        "log_auditoria_integro": livro.verificar_integridade(),
    }
    return relatorio


if __name__ == "__main__":
    relatorio = executar_investigacao(papel_do_usuario="auditor")

    print("=== Relatório da Investigação JCN ===")
    print(f"Total de transações analisadas: {relatorio['total_transacoes']}")
    print(f"Transações sinalizadas como suspeitas: {relatorio['total_sinalizadas']}")
    print(f"Contrato de dados aprovado: {relatorio['contrato_de_dados_aprovado']}")
    print(f"Drift (PSI): {relatorio['drift_psi']} -> {relatorio['drift_classificacao']}")
    print(f"Log de auditoria íntegro: {relatorio['log_auditoria_integro']}")
    print("\nTop 10 clientes suspeitos (pseudonimizados):")
    print(relatorio["top_10_clientes_suspeitos"].to_string(index=False))
