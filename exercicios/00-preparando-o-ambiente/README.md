# Módulo 00 — Preparando o Ambiente

> "Ela abriu o terminal e respirou fundo. O cursor piscava, esperando."
> — Capítulo 1, *O Gigante de Vidro e Aço*

Antes de entrar nas "profundezas obsoletas" da JCN como a Soraya, você precisa
montar sua estação de trabalho. Diferente da JCN — que depende de um mainframe
proprietário de 40 anos — aqui usamos **só ferramentas open source**, de graça,
sem cadastro em nenhum serviço.

## O que você vai precisar

- **Python 3.10 ou mais recente** ([python.org](https://www.python.org/), MIT-like license / PSF License)
- **Git** (para o módulo 06, mas já instale agora)
- Um editor de código (VS Code, PyCharm Community, Vim... o que preferir)

Tudo o que vamos usar depois (pandas, scikit-learn, matplotlib, Faker, pytest)
é software livre, mantido por comunidades abertas, sem custo de licença.

## Passo a passo

1. Confirme sua versão do Python:

   ```bash
   python3 --version
   ```

2. Crie um ambiente virtual **dentro da pasta `exercicios/`** (isso isola as
   bibliotecas deste projeto do resto do seu computador — é a mesma prática
   de isolamento que Victor exige nos pipelines da JCN):

   ```bash
   cd exercicios
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Gere a massa de dados sintética do universo JCN (isso já vem pronto no
   repositório, mas rodar você mesmo é o primeiro exercício de verdade):

   ```bash
   cd dados
   python gerar_dados.py
   ```

   Você deve ver algo como:

   ```
   Dados gerados em: .../exercicios/dados
   Total de transações: 5000 (100 suspeitas)
   ```

5. Rode a suíte de testes de exemplo para confirmar que está tudo funcionando:

   ```bash
   cd ..
   pytest 01-arqueologia-de-dados-legados -q
   ```

   Vai dar **falha** — e está certo! Os testes só passam depois que você
   resolver o exercício. Se aparecer um erro de "módulo não encontrado" em
   vez de um teste falhando, revise o passo 3.

## Como cada módulo está organizado

```
NN-nome-do-modulo/
├── README.md          <- conceito + cenário de negócio + o que fazer
├── exercicio.py        <- esqueleto com TODOs para você preencher
├── teste_exercicio.py  <- testes automáticos (rode com `pytest`)
└── solucao/
    └── solucao.py       <- gabarito comentado — só olhe depois de tentar!
```

Recomendação: **tente por conta própria antes de abrir a `solucao/`**. O
valor do exercício está na luta com o problema, não na resposta pronta.

## Próximo passo

Vá para [`../01-arqueologia-de-dados-legados/`](../01-arqueologia-de-dados-legados/).
