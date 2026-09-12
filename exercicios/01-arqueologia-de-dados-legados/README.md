# Módulo 01 — Arqueologia de Dados: Ingestão de Sistemas Legados

> Capítulos de referência no livro: **01 - O Gigante de Vidro e Aço** e
> **02 - Mergulho nas Profundezas Obsoletas**

## Conceitos

- **Sistema legado**: software antigo, ainda em produção, que ninguém tem
  coragem (ou orçamento) de substituir.
- **EBCDIC**: uma codificação de caracteres usada por mainframes IBM desde os
  anos 1960 — bem diferente do UTF-8 que usamos hoje. Vamos usá-la de verdade
  neste exercício (Python já sabe lidar com ela através do codec `cp037`).
- **Arquivo de largura fixa (fixed-width)**: formato onde cada campo ocupa um
  número fixo de caracteres, sem separador (vírgula, `;`, `|`...). Muito comum
  em sistemas de mainframe, ainda hoje usado em bancos e operadoras.
- **Data Profiling**: examinar um conjunto de dados novo *antes* de usá-lo —
  quantos nulos existem, quais os valores mínimo/máximo, que padrões
  aparecem — exatamente como um exame de sangue antes de uma cirurgia.

## Cenário de negócio

Você acabou de entrar na JCN (Joint Communications Network) como trainee na
equipe de Engenharia de Dados. Seu primeiro projeto — chamado internamente de
**"Arqueologia Digital"** — é ingerir o extrato do sistema
`Legacy-Billing-V3`, um mainframe COBOL de mais de 15 anos, para dentro do
novo Data Lake da empresa.

O arquivo `../dados/legado_faturamento.ebcdic.txt` é exatamente esse extrato:
um arquivo de largura fixa, codificado em EBCDIC, sem nenhum separador entre
campos. O layout (a "planta baixa" do arquivo) está documentado — de forma
incompleta, como seria de se esperar de um manual de 2008 — em
`../dados/layout_legado.txt`.

Antes de qualquer modelo de IA rodar em cima desses dados (o projeto "Nexus"
do Conselho), alguém precisa: (1) decodificar o arquivo, (2) separar os
campos corretamente, e (3) fazer um perfilamento inicial para saber se dá
para confiar no que está ali.

## O que você vai construir

Abra `exercicio.py` e complete as três funções marcadas com `TODO`:

1. **`decodificar_arquivo(caminho)`** — lê os bytes brutos do arquivo e
   devolve uma lista de strings (uma por linha), já decodificadas de EBCDIC
   para texto normal. Dica: `bytes.decode("cp037")`.

2. **`parsear_linha(linha)`** — recebe uma linha de texto já decodificada e
   devolve um dicionário com os campos extraídos, seguindo o layout em
   `layout_legado.txt`. Preste atenção especial ao campo `amount`: ele vem em
   **centavos**, com um caractere de sinal (`+`/`-`) na frente, e sem ponto
   decimal — você precisa convertê-lo para um número decimal em reais (ex.:
   `"+0000000151095"` → `1510.95`).

3. **`perfilar_dados(df)`** — recebe o DataFrame completo e devolve um
   dicionário de estatísticas:
   - `total_linhas`: quantidade de transações
   - `nulos_por_coluna`: quantos valores nulos existem em cada coluna
   - `valor_minimo` e `valor_maximo`: menor e maior valor de `amount`
   - `pct_valores_negativos_fora_estorno`: percentual de transações com
     `amount` negativo cujo `transaction_type` **não** é `"ESTORNO"` — esse é
     exatamente o sinal de alerta que Soraya encontra no capítulo 2.

A função `carregar_arquivo_legado(caminho)` (já pronta) usa as duas primeiras
funções para montar o DataFrame final — não precisa mexer nela.

## Como testar seu código

```bash
cd exercicios
pytest 01-arqueologia-de-dados-legados -v
```

## Critério de sucesso

- Todos os testes em `teste_exercicio.py` passam.
- Rodando `python exercicio.py` a partir desta pasta, você vê um relatório de
  perfilamento impresso no terminal, terminando com a mesma pergunta que
  Soraya se fez: quantas transações têm valor negativo fora de um estorno?

## Para ir além (ferramentas open source do mundo real)

Em produção, esse tipo de ingestão costuma ser feito com:
- [**Apache NiFi**](https://nifi.apache.org/) ou [**Apache Airflow**](https://airflow.apache.org/) para orquestrar a pipeline;
- [**PySpark**](https://spark.apache.org/) quando o arquivo tem bilhões de linhas em vez de milhares (veja o Módulo 04);
- [**Great Expectations**](https://greatexpectations.io/) para formalizar o perfilamento como "contratos de dados" versionados (veja o Módulo 02).

## Próximo módulo

[`../02-qualidade-e-contratos-de-dados/`](../02-qualidade-e-contratos-de-dados/)
