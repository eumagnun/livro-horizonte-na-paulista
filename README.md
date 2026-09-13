# O Horizonte na Paulista — Exercícios Práticos

Este repositório contém uma trilha de **exercícios práticos, gratuitos e
open source**, construída em cima dos conceitos técnicos e éticos do livro
**"O Horizonte na Paulista | Depurando o Sistema"**. O texto do livro em si
não faz parte deste repositório.

<p align="center">
  <img src="https://livro-horizonte-na-paulista.web.app/assets/capa.jpg" width="240" alt="Capa do livro O Horizonte na Paulista">
</p>

<p align="center">
  🌐 <a href="https://livro-horizonte-na-paulista.web.app/"><strong>Landing page do livro</strong></a>
  (código-fonte em
  <a href="https://github.com/eumagnun/livro-horizonte-na-paulista-lp">livro-horizonte-na-paulista-lp</a>)
</p>

## Sobre o livro

O livro acompanha Soraya Oliveira, uma engenheira de software que troca uma
carreira sênior por um cargo de trainee em Ciência de Dados na JCN (Joint
Communications Network), uma operadora de telecomunicações fictícia na
Avenida Paulista. No que deveria ser um projeto rotineiro de "arqueologia
digital" — ingerir um sistema legado de faturamento — ela encontra padrões
que não deveriam existir, e a história se transforma em uma investigação de
governança corporativa, ética em dados e fraude financeira.

Você não precisa ter lido o livro para fazer os exercícios — cada módulo
explica o trecho da história que o inspirou e o conceito técnico por trás
dele.

📱 **Versão digital (Kindle):** [amazon.com.br/dp/B0GHQH5H15](https://www.amazon.com.br/dp/B0GHQH5H15)

📖 **Versão impressa:** em breve, via [loja.uiclap.com/titulo/ua202447](https://loja.uiclap.com/titulo/ua202447)

## Sobre os exercícios (pasta `exercicios/`)

O livro é ficção, mas quase todo capítulo se apoia em um conceito técnico
real: sistemas legados, qualidade de dados, engenharia de atributos,
pipelines batch vs. streaming, detecção de fraude com Machine Learning,
governança e cadeia de custódia, segurança, privacidade (LGPD) e
observabilidade.

A pasta [`exercicios/`](exercicios/) transforma cada um desses conceitos em
um **exercício de programação prático**, ambientado no mesmo universo
fictício da JCN — com dados sintéticos, cenários de negócio e testes
automatizados que confirmam se você resolveu certo.

### Para quem é

Para quem já sabe programar em Python no nível básico (variáveis, funções,
laços) e quer aprender, na prática, conceitos reais de **Engenharia de
Dados, Ciência de Dados, Governança e Segurança** — sem precisar saber nada
disso de antemão. Cada módulo explica o conceito do zero antes de pedir
qualquer código.

### Foco 100% open source

Nenhuma ferramenta usada aqui exige licença paga, cadastro em nuvem ou
cartão de crédito. Tudo roda localmente com Python e bibliotecas de código
aberto (pandas, scikit-learn, numpy, Faker, pytest — todas com licenças
livres tipo BSD/MIT). Cada módulo também aponta, na seção "Para ir além",
ferramentas open source usadas de verdade pela indústria para o mesmo
problema (Apache Kafka, Apache Spark, Great Expectations, Evidently AI,
Hyperledger, OpenDP, entre outras).

### Estrutura

```
exercicios/
├── requirements.txt
├── dados/                                    <- dados sintéticos do universo JCN
│   └── gerar_dados.py                         (gerador reprodutível, seed fixa)
├── 00-preparando-o-ambiente/                 <- setup do zero
├── 01-arqueologia-de-dados-legados/          <- ingestão de sistema legado (EBCDIC, largura fixa)
├── 02-qualidade-e-contratos-de-dados/        <- limpeza e validação de dados
├── 03-engenharia-de-atributos/               <- feature engineering e enriquecimento
├── 04-pipelines-batch-e-streaming/           <- processamento em lote vs. em tempo real
├── 05-deteccao-de-anomalias-e-fraude/        <- Machine Learning não supervisionado
├── 06-clean-code-e-git/                      <- refatoração e fluxo de Git/Code Review
├── 07-governanca-e-auditoria/                <- cadeia de custódia e logs imutáveis
├── 08-seguranca-kill-switch-e-acesso/        <- controle de acesso e "kill switch"
├── 09-etica-privacidade-lgpd/                <- anonimização e privacidade diferencial
├── 10-observabilidade-e-monitoramento/       <- monitoramento vs. observabilidade, data drift
└── 11-projeto-final-investigacao-jcn/        <- projeto de síntese, integra tudo
```

Cada módulo (exceto o 00 e o 11) segue o mesmo formato:

```
NN-nome-do-modulo/
├── README.md          <- conceito + cenário de negócio + o que fazer
├── exercicio.py         <- esqueleto com TODOs para você preencher
├── teste_exercicio.py   <- testes automáticos (pytest)
└── solucao/
    └── solucao.py         <- gabarito comentado (só olhe depois de tentar!)
```

### Como começar

```bash
cd exercicios
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd dados && python gerar_dados.py && cd ..

pytest 01-arqueologia-de-dados-legados -v
```

Instruções detalhadas, passo a passo, estão em
[`exercicios/00-preparando-o-ambiente/README.md`](exercicios/00-preparando-o-ambiente/README.md).

### Trilha recomendada

Os módulos foram desenhados para serem feitos em ordem — cada um usa um
dado de entrada independente (não é necessário ter completado o anterior
para começar o seguinte), mas o fio narrativo e a complexidade crescem na
sequência 01 → 11, culminando no projeto final, que integra tudo em uma
investigação de fraude completa, do arquivo bruto ao relatório.

## Licença

Os exercícios e o código deste repositório podem ser usados livremente para
fins de estudo. Os direitos do texto do livro pertencem ao autor.
