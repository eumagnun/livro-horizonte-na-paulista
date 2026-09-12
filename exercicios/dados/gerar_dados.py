"""
Gerador de dados sintéticos do universo JCN (Joint Communications Network).

Este script recria, de forma fictícia e determinística (mesma seed sempre gera
os mesmos dados), o cenário de negócio do livro "O Horizonte na Paulista":
uma operadora de telecomunicações com um sistema legado de faturamento
("Legacy-Billing-V3") que esconde transações de ajuste suspeitas.

Nenhum dado aqui é real. Tudo é gerado com a biblioteca Faker + numpy.

Como usar:
    cd exercicios/dados
    python gerar_dados.py

Isso (re)cria todos os arquivos usados pelos módulos 01 a 11. Os arquivos já
vêm versionados no repositório, então rodar este script não é obrigatório
para fazer os exercícios — mas é o próprio primeiro exercício do módulo 00
entender e rodar este gerador.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker

SEED = 42
N_TRANSACOES = 5000
PASTA_SAIDA = Path(__file__).parent

random.seed(SEED)
np.random.seed(SEED)
fake = Faker("pt_BR")
Faker.seed(SEED)

TIPOS_TRANSACAO = ["FATURA", "AJUSTE", "ESTORNO", "PAGAMENTO"]
NOS_REDE_NORMAIS = ["SP-CORE-01", "SP-CORE-02", "RJ-CORE-01", "MG-CORE-01", "BA-CORE-01"]
NO_REDE_SUSPEITO = "SANTOS-PORT-07"
PAISES_NORMAIS = ["BR"] * 20  # imensa maioria das transações é nacional
PAISES_SUSPEITOS = ["KY", "LU", "PA"]  # paraísos fiscais clássicos
CODIGOS_AJUSTE_NORMAIS = ["00", "01", "02", "10"]
CODIGOS_AJUSTE_SUSPEITOS = ["9A", "4F"]


def gerar_transacoes_base(n: int) -> pd.DataFrame:
    """Gera a massa de transações 'verdade' (limpa), incluindo ~2% de outliers
    propositais que representam os ajustes fora do padrão do CFO Eduardo Costa.
    """
    ids_clientes = [f"CLI{str(i).zfill(6)}" for i in range(1, 1201)]

    linhas = []
    n_suspeitas = int(n * 0.02)
    indices_suspeitos = set(random.sample(range(n), n_suspeitas))

    data_inicio = pd.Timestamp("2023-01-01")

    for i in range(n):
        suspeita = i in indices_suspeitos
        tipo = random.choice(TIPOS_TRANSACAO)
        data = data_inicio + pd.Timedelta(days=random.randint(0, 364))

        if suspeita:
            valor = round(random.uniform(80_000, 450_000), 2)
            codigo_ajuste = random.choice(CODIGOS_AJUSTE_SUSPEITOS)
            no_rede = NO_REDE_SUSPEITO
            pais = random.choice(PAISES_SUSPEITOS)
            conta_destino = f"OFFSHORE-{fake.iban()[-8:]}"
        else:
            valor = round(random.uniform(20, 3500), 2)
            codigo_ajuste = random.choice(CODIGOS_AJUSTE_NORMAIS)
            no_rede = random.choice(NOS_REDE_NORMAIS)
            pais = random.choice(PAISES_NORMAIS)
            conta_destino = f"BR-{fake.random_number(digits=10, fix_len=True)}"

        # ESTORNO pode legitimamente ser negativo; nos demais tipos, valor
        # negativo é a "bandeira vermelha" que Soraya encontra no capítulo 2.
        if tipo == "ESTORNO" and random.random() < 0.5:
            valor = -valor
        elif suspeita and random.random() < 0.3:
            valor = -valor  # ajuste suspeito negativo, fora do tipo ESTORNO

        linhas.append(
            {
                "transaction_id": f"TXN{str(i + 1).zfill(8)}",
                "customer_id": random.choice(ids_clientes),
                "transaction_date": data,
                "transaction_type": tipo,
                "amount": valor,
                "adjustment_code": codigo_ajuste,
                "network_node": no_rede,
                "country": pais,
                "destination_account": conta_destino,
                "is_suspicious_ground_truth": suspeita,
            }
        )

    return pd.DataFrame(linhas)


def para_texto_largura_fixa(df: pd.DataFrame) -> list[str]:
    """Converte o DataFrame para o formato de arquivo de largura fixa que o
    mainframe COBOL da JCN produziria (sem separadores, campos com tamanho
    fixo em caracteres).
    """
    linhas = []
    for _, row in df.iterrows():
        valor_centavos = int(round(row["amount"] * 100))
        sinal = "-" if valor_centavos < 0 else "+"
        campo_valor = f"{sinal}{abs(valor_centavos):013d}"  # 14 chars

        linha = (
            row["transaction_id"].ljust(11)
            + row["customer_id"].ljust(10)
            + row["transaction_date"].strftime("%Y%m%d")
            + row["transaction_type"].ljust(10)
            + campo_valor
            + row["adjustment_code"].ljust(4)
            + row["network_node"].ljust(15)
            + row["country"].ljust(3)
        )
        linhas.append(linha)
    return linhas


def gravar_arquivo_legado_ebcdic(df: pd.DataFrame, caminho: Path) -> None:
    """Grava o arquivo de largura fixa codificado em EBCDIC (cp037), o mesmo
    codec usado por mainframes IBM reais. É o arquivo bruto do módulo 01.
    """
    linhas = para_texto_largura_fixa(df)
    conteudo = "\n".join(linhas) + "\n"
    caminho.write_bytes(conteudo.encode("cp037"))


def gravar_layout(caminho: Path) -> None:
    layout = """\
LAYOUT DO ARQUIVO LEGACY-BILLING-V3 (largura fixa, EBCDIC/cp037)
Documento recuperado de um manual de 2008 -- pode estar incompleto.

Legenda: "Posicao" e um intervalo inclusivo (primeiro char = posicao 0).
Em Python, para cortar o campo X que vai da posicao A ate B, use:
    linha[A : B + 1]

Campo                 Posicao (0-indexed)   Tamanho   Observacoes
---------------------------------------------------------------------------
transaction_id         0-10                  11        prefixo "TXN"
customer_id             11-20                 10        prefixo "CLI"
transaction_date        21-28                  8        formato YYYYMMDD
transaction_type        29-38                 10        FATURA/AJUSTE/ESTORNO/PAGAMENTO
amount (centavos)       39-52                 14        sinal (+/-) + 13 digitos, sem separador decimal
adjustment_code         53-56                  4        "remendos" do Eduardo Costa, nem sempre documentados
network_node            57-71                 15        identificador do no de rede de origem
country                 72-74                  3        codigo de pais ISO-2 (com padding)
"""
    caminho.write_text(layout, encoding="utf-8")


def gerar_transacoes_brutas_csv(df: pd.DataFrame, caminho: Path) -> None:
    """Gera uma versão CSV 'suja', a mesma massa de dados mas com defeitos de
    qualidade típicos de integração real: nulos, duplicatas, formatos de data
    inconsistentes e valores com vírgula decimal. Usada no módulo 02.
    """
    sujo = df.copy()
    sujo = sujo.drop(columns=["is_suspicious_ground_truth"])

    # 1. Duplicar ~1% das linhas (erro clássico de reprocessamento de lote)
    duplicadas = sujo.sample(frac=0.01, random_state=SEED)
    sujo = pd.concat([sujo, duplicadas], ignore_index=True)

    # 2. Zerar customer_id em ~0.5% das linhas
    idx_nulos = sujo.sample(frac=0.005, random_state=SEED + 1).index
    sujo.loc[idx_nulos, "customer_id"] = None

    # 3. Formato de data inconsistente em um lote de linhas antigas (DD/MM/AAAA)
    idx_data_br = sujo.sample(frac=0.08, random_state=SEED + 2).index
    sujo["transaction_date"] = sujo["transaction_date"].astype(object)
    sujo.loc[idx_data_br, "transaction_date"] = sujo.loc[idx_data_br, "transaction_date"].apply(
        lambda d: d.strftime("%d/%m/%Y")
    )
    outros = sujo.index.difference(idx_data_br)
    sujo.loc[outros, "transaction_date"] = sujo.loc[outros, "transaction_date"].apply(
        lambda d: d.strftime("%Y-%m-%d")
    )

    # 4. Valor com vírgula decimal (padrão pt-BR) em parte das linhas, como texto
    idx_valor_texto = sujo.sample(frac=0.10, random_state=SEED + 3).index
    sujo["amount"] = sujo["amount"].astype(object)
    sujo.loc[idx_valor_texto, "amount"] = sujo.loc[idx_valor_texto, "amount"].apply(
        lambda v: f"{v:.2f}".replace(".", ",")
    )

    # 5. Inconsistência de caixa em transaction_type
    idx_lower = sujo.sample(frac=0.05, random_state=SEED + 4).index
    sujo.loc[idx_lower, "transaction_type"] = sujo.loc[idx_lower, "transaction_type"].str.lower()

    sujo = sujo.sample(frac=1, random_state=SEED + 5).reset_index(drop=True)  # embaralha
    sujo.to_csv(caminho, index=False)


def gerar_transacoes_limpas(df: pd.DataFrame, caminho: Path) -> None:
    """Gera a versão já limpa (mas ainda NÃO enriquecida) das transações --
    o ponto de partida independente do Módulo 03, para quem quer praticar
    engenharia de atributos sem depender do próprio código do Módulo 02.
    """
    limpa = df.drop(columns=["is_suspicious_ground_truth"]).copy()
    limpa["transaction_date"] = limpa["transaction_date"].dt.strftime("%Y-%m-%d")
    limpa.to_csv(caminho, index=False)


def gerar_tabela_risco_pais(caminho: Path) -> None:
    dados = [
        {"country": "BR", "country_name": "Brasil", "risk_score": 0.05, "is_tax_haven": False},
        {"country": "US", "country_name": "Estados Unidos", "risk_score": 0.15, "is_tax_haven": False},
        {"country": "PT", "country_name": "Portugal", "risk_score": 0.10, "is_tax_haven": False},
        {"country": "DE", "country_name": "Alemanha", "risk_score": 0.08, "is_tax_haven": False},
        {"country": "KY", "country_name": "Ilhas Cayman", "risk_score": 0.95, "is_tax_haven": True},
        {"country": "LU", "country_name": "Luxemburgo", "risk_score": 0.80, "is_tax_haven": True},
        {"country": "PA", "country_name": "Panamá", "risk_score": 0.90, "is_tax_haven": True},
        {"country": "CH", "country_name": "Suíça", "risk_score": 0.55, "is_tax_haven": False},
    ]
    pd.DataFrame(dados).to_csv(caminho, index=False)


def gerar_eventos_stream(df: pd.DataFrame, caminho: Path, n: int = 300) -> None:
    """Gera um recorte de N transações como um arquivo JSON Lines ordenado por
    timestamp, simulando um feed de eventos chegando em tempo real (módulo 04).
    """
    amostra = df.sample(n=n, random_state=SEED).sort_values("transaction_date")
    with caminho.open("w", encoding="utf-8") as f:
        for _, row in amostra.iterrows():
            evento = {
                "event_time": row["transaction_date"].isoformat(),
                "transaction_id": row["transaction_id"],
                "customer_id": row["customer_id"],
                "amount": row["amount"],
                "transaction_type": row["transaction_type"],
                "adjustment_code": row["adjustment_code"],
                "network_node": row["network_node"],
                "country": row["country"],
            }
            f.write(json.dumps(evento, ensure_ascii=False) + "\n")


def gerar_transacoes_enriquecidas(df: pd.DataFrame, risco_path: Path, caminho: Path) -> None:
    """Gera a versão 'gabarito' já limpa e enriquecida, usada como ponto de
    partida dos módulos 05, 07, 08, 09 e 10 (para quem não fez os módulos
    anteriores) e como referência de conferência dos módulos 01-04.
    """
    risco = pd.read_csv(risco_path)
    enriquecida = df.merge(risco, on="country", how="left")
    enriquecida["cross_border"] = enriquecida["country"] != "BR"
    media_por_cliente = enriquecida.groupby("customer_id")["amount"].transform("mean")
    desvio_por_cliente = enriquecida.groupby("customer_id")["amount"].transform("std").fillna(1.0)
    enriquecida["amount_zscore_cliente"] = (enriquecida["amount"] - media_por_cliente) / desvio_por_cliente
    enriquecida.to_csv(caminho, index=False)


def main() -> None:
    df = gerar_transacoes_base(N_TRANSACOES)

    gravar_arquivo_legado_ebcdic(df, PASTA_SAIDA / "legado_faturamento.ebcdic.txt")
    gravar_layout(PASTA_SAIDA / "layout_legado.txt")
    gerar_transacoes_brutas_csv(df, PASTA_SAIDA / "transacoes_brutas.csv")
    gerar_transacoes_limpas(df, PASTA_SAIDA / "transacoes_limpas.csv")
    gerar_tabela_risco_pais(PASTA_SAIDA / "tabela_risco_pais.csv")
    gerar_eventos_stream(df, PASTA_SAIDA / "eventos_stream.jsonl")
    gerar_transacoes_enriquecidas(
        df, PASTA_SAIDA / "tabela_risco_pais.csv", PASTA_SAIDA / "transacoes_enriquecidas_gabarito.csv"
    )

    # Guarda também a verdade fundamental (quais transações são suspeitas de
    # fato) para os testes automatizados do módulo 05 poderem calcular
    # precisão/recall -- isso NÃO deve ser usado como atalho pelos alunos.
    df[["transaction_id", "is_suspicious_ground_truth"]].to_csv(
        PASTA_SAIDA / "_gabarito_suspeitas.csv", index=False
    )

    print(f"Dados gerados em: {PASTA_SAIDA}")
    print(f"Total de transações: {len(df)} ({df['is_suspicious_ground_truth'].sum()} suspeitas)")


if __name__ == "__main__":
    main()
