# Módulo 02 — Qualidade de Dados e "Contratos de Dados"

> "Garbage in, garbage out. Se a entrada é lixo, a saída é só lixo bem
> documentado." — Soraya, Capítulo 1

## Conceitos

- **Garbage In, Garbage Out (GIGO)**: nenhum modelo de IA ou relatório
  financeiro é melhor do que os dados que o alimentam.
- **Limpeza de dados (data cleaning)**: padronizar formatos, remover
  duplicatas, tratar valores ausentes — antes de qualquer análise.
- **Contrato de dados (data contract)**: um conjunto de regras explícitas e
  verificáveis que um conjunto de dados deve cumprir (ex.: "esta coluna nunca
  é nula", "este valor é sempre um dos 4 tipos válidos"). Em vez de descobrir
  problemas de qualidade só quando o relatório sai errado, o contrato os
  detecta automaticamente, cedo.

## Cenário de negócio

O arquivo `../dados/transacoes_brutas.csv` é uma exportação real (simulada)
do time de integração: a mesma informação do Módulo 01, mas *sem* passar
pelo seu parser cuidadoso — cheia dos defeitos típicos de um pipeline que
junta fontes diferentes:

- transações duplicadas (reprocessamento de lote);
- `customer_id` vazio em algumas linhas;
- datas em dois formatos diferentes (`2023-09-23` e `04/03/2023`);
- valores monetários ora com ponto, ora com vírgula decimal (`1522.04` vs
  `"1522,04"`);
- `transaction_type` ora maiúsculo, ora minúsculo (`FATURA` vs `fatura`).

Antes desses dados alimentarem o Nexus (a IA do Conselho) ou qualquer
relatório de auditoria, seu trabalho é **limpar** e, principalmente,
**validar** — de um jeito que qualquer pessoa da equipe possa rodar de novo
sempre que uma nova exportação chegar.

## O que você vai construir

Em `exercicio.py`, complete:

1. **`normalizar_data(valor)`** — aceita uma data em `"YYYY-MM-DD"` ou
   `"DD/MM/YYYY"` e sempre devolve `"YYYY-MM-DD"`.
2. **`normalizar_valor(valor)`** — aceita um valor monetário como string com
   ponto ou vírgula decimal (ex.: `"1522.04"` ou `"1522,04"`) e devolve um
   `float`.
3. **`normalizar_tipo_transacao(valor)`** — devolve o tipo sempre em
   maiúsculas.
4. **`limpar_transacoes(df)`** — aplica as três normalizações acima, remove
   transações duplicadas (mesmo `transaction_id`) e descarta linhas sem
   `customer_id` (não dá para investigar uma transação sem saber de quem
   ela é).
5. **`validar_contrato(df)`** — recebe um DataFrame **já limpo** e devolve um
   dicionário `{nome_da_regra: bool}` dizendo se cada regra do contrato de
   dados foi cumprida:
   - `"sem_customer_id_nulo"`
   - `"sem_transaction_id_duplicado"`
   - `"tipos_de_transacao_validos"` (só `FATURA`, `AJUSTE`, `ESTORNO`,
     `PAGAMENTO`)
   - `"valores_sao_numericos"`
   - `"datas_no_formato_iso"` (regex `^\d{4}-\d{2}-\d{2}$`)

## Como testar

```bash
cd exercicios
pytest 02-qualidade-e-contratos-de-dados -v
```

## Critério de sucesso

- Todos os testes passam.
- Rodando `python exercicio.py`, o contrato de dados é validado e imprime
  `True` para todas as regras — a mesma garantia que Victor exige antes de
  qualquer dado tocar o Nexus.

## Para ir além (ferramentas open source do mundo real)

- [**Great Expectations**](https://greatexpectations.io/) e
  [**Pandera**](https://pandera.readthedocs.io/) formalizam exatamente essa
  ideia de "contrato de dados" como código versionável, com relatórios em
  HTML.
- [**dbt**](https://www.getdbt.com/) (edição open source) tem testes de dados
  embutidos no próprio pipeline de transformação SQL.

## Próximo módulo

[`../03-engenharia-de-atributos/`](../03-engenharia-de-atributos/)
