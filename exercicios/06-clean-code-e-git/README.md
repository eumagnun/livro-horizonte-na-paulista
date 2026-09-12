# Módulo 06 — Clean Code e Git

> "Para um engenheiro de dados sênior como ele, ler o código de Soraya era
> como ouvir uma sinfonia. Era limpo, modular, seguindo os princípios de
> Clean Code." — Capítulo 3

Este módulo tem duas partes independentes: **refatoração de código** (com
testes automáticos) e **prática de Git** (um checklist guiado, sem
correção automática — é uma habilidade de terminal, não de código).

---

## Parte 1 — Refatoração com Clean Code

### Conceitos

- **Clean Code**: código que se lê como prosa — nomes que dizem o que a
  coisa é, funções pequenas que fazem uma coisa só, sem "mágica" escondida.
- **Refatoração**: mudar a estrutura interna do código **sem mudar o que
  ele faz**. A forma mais segura de fazer isso é ter testes que comprovem
  que o comportamento não mudou antes e depois.
- **Teste de caracterização (characterization test)**: um teste que
  documenta o comportamento atual de um código (mesmo que feio), para que
  você possa refatorá-lo com confiança.

### Cenário de negócio

`codigo_legado/faturamento_legado.py` contém uma função `proc()` que
alguém da equipe do Eduardo Costa escreveu anos atrás. Ela calcula o total
de ajustes suspeitos (`9A`/`4F`) por nó de rede, tratando estornos como
valores sempre negativos. **Funciona**, mas ninguém mais consegue entender
ou dar manutenção nela com segurança — exatamente o tipo de código que
esconde os "remendos" do capítulo 1.

### O que você vai construir

Em `exercicio.py`, escreva uma versão **limpa** que produza **exatamente o
mesmo resultado** que `codigo_legado/faturamento_legado.py`, para qualquer
lista de transações de entrada. Sugestões de como aplicar Clean Code aqui:

- nomes descritivos em vez de `x`, `d`, `v`, `n`, `t`, `c`;
- uma função para decidir "isso é um código de ajuste suspeito?"
  (`eh_ajuste_suspeito`);
- uma função para calcular "qual o valor efetivo desta transação no total?"
  (`calcular_valor_efetivo`);
- uma função principal `somar_ajustes_suspeitos_por_no` que orquestra as
  duas anteriores;
- **type hints** e um **docstring curto** explicando a regra de negócio.

Não precisa (e não deve) mudar a *assinatura* de entrada — a função
principal ainda recebe uma lista de tuplas `(amount, transaction_type,
network_node, adjustment_code)`.

### Como testar

```bash
cd exercicios
pytest 06-clean-code-e-git -v
```

Os testes rodam a **mesma entrada** nas duas versões (a legada e a sua) e
comparam a saída. Se o resultado for idêntico, sua refatoração é segura.

---

## Parte 2 — Prática de Git (checklist guiado)

Esta parte não tem correção automática — é para você praticar no terminal.
Rode os comandos numa pasta de testes separada (fora deste repositório, ou
em um repositório novo).

1. **Crie um repositório novo e faça o primeiro commit:**
   ```bash
   mkdir pratica-git && cd pratica-git
   git init
   echo "# Projeto Nexus" > README.md
   git add README.md
   git commit -m "docs: adiciona README inicial do projeto Nexus"
   ```

2. **Crie uma branch para uma nova funcionalidade** (nunca trabalhe direto
   na branch principal em um time):
   ```bash
   git checkout -b feature/pipeline-ingestao
   ```

3. **Faça uma mudança e um commit pequeno e descritivo:**
   ```bash
   echo "def ingerir(): pass" > pipeline.py
   git add pipeline.py
   git commit -m "feat: adiciona esqueleto da função de ingestão"
   ```

4. **Veja o histórico:**
   ```bash
   git log --oneline
   ```

5. **Simule um Pull Request**: volte para a branch principal e faça o
   merge:
   ```bash
   git checkout main   # ou "master", dependendo da sua configuração
   git merge feature/pipeline-ingestao
   ```

6. **Checklist de Code Review** — releia seu próprio `pipeline.py` como se
   fosse revisar o código de outra pessoa (é exatamente o que Victor faz
   com o código de Soraya no capítulo 3). Pergunte-se:
   - [ ] O nome da função/variável diz o que ela faz?
   - [ ] Essa função faz uma coisa só?
   - [ ] Existe algum número ou texto "mágico" sem explicação?
   - [ ] Um colega entenderia isso sem eu precisar explicar ao vivo?
   - [ ] A mensagem de commit explica o *porquê*, não só o *o quê*?

## Critério de sucesso

- Todos os testes de `teste_exercicio.py` passam (Parte 1).
- Você completou o checklist de Git e conseguiu ver seu commit no
  `git log` (Parte 2).

## Para ir além (ferramentas open source do mundo real)

- [**Git**](https://git-scm.com/) em si já é open source (licença GPLv2).
- [**pre-commit**](https://pre-commit.com/) automatiza checagens de
  qualidade (formatação, lint) antes de cada commit.
- [**Ruff**](https://docs.astral.sh/ruff/) e [**Black**](https://black.readthedocs.io/)
  são formatadores/linters open source populares em Python.
- Plataformas como o **GitHub** (usado neste próprio repositório) trazem o
  fluxo de Pull Request e Code Review para times reais.

## Próximo módulo

[`../07-governanca-e-auditoria/`](../07-governanca-e-auditoria/)
