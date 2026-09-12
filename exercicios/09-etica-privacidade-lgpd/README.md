# Módulo 09 — Ética, Privacidade e Anonimização de Dados

> "Soraya falava sobre implementar Differential Privacy (Privacidade
> Diferencial) para proteger os dados dos clientes." — Capítulo 15, *O
> Horizonte na Paulista*

## Conceitos

- **LGPD (Lei Geral de Proteção de Dados)**: a lei brasileira que regula o
  tratamento de dados pessoais. Dois de seus princípios centrais são
  **minimização** (só colete/mantenha o dado pessoal estritamente
  necessário) e **finalidade** (use o dado só para o que foi declarado).
- **Pseudonimização**: substituir um identificador direto (como
  `customer_id`) por um valor derivado (um hash) que não permite voltar ao
  dado original sem uma informação extra (o *salt*). Diferente de
  **anonimização de verdade**, a pseudonimização ainda pode, em teoria, ser
  revertida por quem tem a chave/salt — por isso a LGPD trata os dois
  conceitos de forma diferente.
- **Privacidade Diferencial (Differential Privacy)**: uma técnica
  matemática que adiciona ruído estatístico controlado a uma resposta
  agregada (uma contagem, uma média), de forma que dá para saber
  tendências gerais sem conseguir isolar informações sobre uma pessoa
  específica. Quanto menor o parâmetro `epsilon`, mais ruído (mais
  privacidade, menos precisão) — é sempre uma troca (trade-off).

## Cenário de negócio

A área jurídica da JCN pede que qualquer relatório agregado sobre clientes
(por exemplo, "quantos clientes têm transações internacionais?") não exponha
informações que permitam identificar indivíduos, mesmo que o relatório
final seja só um número. Você vai implementar duas técnicas de proteção que
aparecem no clímax do livro.

## O que você vai construir

Em `exercicio.py`, complete:

1. **`pseudonimizar_id(identificador, salt)`** — devolve um hash SHA-256
   (hexadecimal) de `identificador + salt`. O mesmo `identificador` com o
   mesmo `salt` deve sempre gerar o mesmo resultado; com um salt diferente,
   o resultado muda completamente.

2. **`adicionar_ruido_laplace(valor_real, sensibilidade, epsilon, rng=None)`**
   — implementa o **Mecanismo de Laplace**, a forma mais clássica de
   Privacidade Diferencial: soma a `valor_real` um ruído aleatório sorteado
   de uma distribuição de Laplace com escala `sensibilidade / epsilon`.
   Dica: `rng.laplace(loc=0, scale=sensibilidade/epsilon)` (use
   `numpy.random.default_rng()` se `rng` não for informado).

3. **`contagem_privada(serie_booleana, epsilon, rng=None)`** — conta quantos
   valores `True` existem em uma série booleana do pandas e devolve essa
   contagem com ruído de Laplace aplicado (sensibilidade = 1, porque
   adicionar ou remover uma pessoa muda uma contagem em no máximo 1).

## Como testar

```bash
cd exercicios
pytest 09-etica-privacidade-lgpd -v
```

## Critério de sucesso

Rode `python exercicio.py`. Ele compara a contagem real de transações
`cross_border` com versões "privatizadas" em três níveis de `epsilon`
(muita privacidade, privacidade média, pouca privacidade) — observe como o
ruído diminui à medida que `epsilon` aumenta.

## Discussão

- Por que pseudonimização (Módulo 08 já mostrou o hashing) **não** é o
  mesmo que anonimização de verdade?
- Se dois relatórios "privados" forem publicados toda semana sobre o mesmo
  grupo de clientes, alguém determinado consegue, com estatística, reduzir
  a incerteza e reidentificar pessoas? (Essa é uma preocupação real,
  chamada de *ataque de correlação* — um dos motivos pelos quais
  Privacidade Diferencial usa um "orçamento de privacidade" acumulado ao
  longo do tempo, não só por consulta.)

## Para ir além (ferramentas open source do mundo real)

- [**OpenDP**](https://opendp.org/) e [**Google Differential Privacy**](https://github.com/google/differential-privacy)
  são bibliotecas open source que implementam Privacidade Diferencial de
  forma robusta e auditada — não use uma implementação artesanal como esta
  em produção.
- [**Microsoft Presidio**](https://microsoft.github.io/presidio/) detecta e
  anonimiza automaticamente dados pessoais (PII) em texto e dados
  estruturados.

## Próximo módulo

[`../10-observabilidade-e-monitoramento/`](../10-observabilidade-e-monitoramento/)
