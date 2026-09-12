# Módulo 03 — Engenharia de Atributos e Enriquecimento de Dados

> Capítulo de referência: **03 - Pequenas Vitórias, Grandes Lições**

## Conceitos

- **Engenharia de Atributos (Feature Engineering)**: usar conhecimento de
  domínio para criar novas colunas ("atributos") a partir dos dados brutos,
  de forma que padrões escondidos fiquem visíveis — para um humano ou para
  um modelo de Machine Learning.
- **Enriquecimento de dados**: cruzar uma tabela com outra fonte (uma tabela
  de referência, uma API externa) para agregar contexto que o dado original
  não tinha sozinho.
- **Z-score**: uma forma de medir "o quão fora do normal" um valor está,
  comparado à média e ao desvio-padrão de um grupo. Um z-score de 3, por
  exemplo, significa "3 desvios-padrão acima da média do grupo" — bem
  incomum.

## Cenário de negócio

Você já tem uma base de transações limpa (a saída do Módulo 02). Mas
"limpa" não é a mesma coisa que "útil". Olhando linha a linha, ninguém
enxerga o padrão que Soraya encontrou no livro: transações de ajuste que
cruzam fronteiras fiscais e vão sempre para o mesmo tipo de destino.

Seu trabalho agora é **enriquecer** a base com uma tabela de referência de
risco por país (`../dados/tabela_risco_pais.csv`, um "conhecimento de
domínio" sobre paraísos fiscais) e **criar atributos novos** que tornem
visível o comportamento anômalo de cada cliente.

## O que você vai construir

Em `exercicio.py`, complete:

1. **`enriquecer_com_risco_pais(df, tabela_risco)`** — uma junção
   (`merge`) entre as transações e a tabela de risco por país, trazendo as
   colunas `country_name`, `risk_score` e `is_tax_haven`.

2. **`adicionar_flag_cross_border(df)`** — cria a coluna booleana
   `cross_border`: `True` quando `country != "BR"`.

3. **`adicionar_zscore_por_cliente(df)`** — cria a coluna
   `amount_zscore_cliente`: para cada transação, quantos desvios-padrão
   o valor está distante da média *daquele mesmo cliente* (não da média
   geral!). Fórmula: `(valor - média_do_cliente) / desvio_padrão_do_cliente`.
   Dica: `df.groupby("customer_id")["amount"].transform(...)`.

4. **`construir_features(df, tabela_risco)`** — já implementada, encadeia as
   três funções acima.

## Ponto de partida

A entrada é `../dados/transacoes_limpas.csv` (já limpa, equivalente ao
resultado do Módulo 02 — este módulo é independente, não precisa ter
terminado o anterior). Use
`../dados/transacoes_enriquecidas_gabarito.csv` **apenas para conferir** seu
resultado final, comparando coluna a coluna.

## Como testar

```bash
cd exercicios
pytest 03-engenharia-de-atributos -v
```

## Critério de sucesso

Rode `python exercicio.py` e observe: quais clientes têm transações com
`amount_zscore_cliente` acima de 3 **e** `is_tax_haven == True`? Esse é
exatamente o tipo de lista que Soraya monta antes de levar a descoberta a
Victor.

## Para ir além (ferramentas open source do mundo real)

- [**Feast**](https://feast.dev/) é uma "feature store" open source — um
  catálogo versionado de atributos reutilizáveis entre times de dados.
- [**scikit-learn**](https://scikit-learn.org/) tem transformadores prontos
  (`StandardScaler`, `OneHotEncoder`) para boa parte da engenharia de
  atributos mais comum — vamos usá-lo no Módulo 05.

## Próximo módulo

[`../04-pipelines-batch-e-streaming/`](../04-pipelines-batch-e-streaming/)
