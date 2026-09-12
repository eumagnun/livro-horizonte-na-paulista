# Módulo 05 — Detecção de Anomalias e Fraude com Machine Learning

> Capítulos de referência: **02 - Mergulho nas Profundezas Obsoletas** e
> **04 - O Peso da Expectativa**

## Conceitos

- **Aprendizado não supervisionado**: técnicas de Machine Learning que
  encontram padrões nos dados **sem** precisar de exemplos previamente
  rotulados como "certo" ou "errado" — essencial em fraude, porque
  raramente temos uma lista completa de fraudes já confirmadas.
- **Isolation Forest**: um algoritmo que detecta outliers com uma ideia
  simples e elegante: pontos anômalos são mais fáceis de "isolar" do resto
  dos dados com poucas divisões aleatórias, porque estão longe da massa
  principal.
- **Outlier / anomalia**: um ponto que se comporta de forma muito diferente
  da maioria. Pode ser erro de medição — ou pode ser o início de uma
  investigação, como Soraya descobre no livro.
- **Precisão e Recall**: duas formas de avaliar um detector. Precisão
  responde "dos alertas que eu levantei, quantos eram fraude de verdade?".
  Recall responde "de todas as fraudes que existiam, quantas eu consegui
  achar?". Nenhum modelo real maximiza as duas ao mesmo tempo — é sempre uma
  escolha de negócio.

## Cenário de negócio

Você já tem a base enriquecida (Módulo 03). Agora é hora de treinar um
modelo que sinalize automaticamente as transações suspeitas — em vez de
depender de alguém notar um gráfico de dispersão manualmente, como Soraya
fez na madrugada do capítulo 2.

Usaremos `../dados/transacoes_enriquecidas_gabarito.csv`. Esse arquivo tem
uma coluna extra, `is_suspicious_ground_truth`, que **na vida real você
nunca teria** — aqui ela existe só para você conseguir medir se seu modelo
está funcionando. **Nunca use essa coluna como característica (feature) de
entrada do modelo** — isso seria "colar a resposta", um erro conhecido como
*data leakage* (vazamento de dados).

## O que você vai construir

Em `exercicio.py`, complete:

1. **`preparar_matriz_features(df)`** — seleciona as colunas numéricas que o
   modelo vai usar: `amount`, `risk_score`, `amount_zscore_cliente` e
   `cross_border` (convertida para `0`/`1`). Devolve um DataFrame só com
   essas colunas, nessa ordem.

2. **`treinar_detector(X, contaminacao=0.02)`** — cria e treina um
   `sklearn.ensemble.IsolationForest` com `contamination=contaminacao` e
   `random_state=42` (fixamos a semente para o resultado ser sempre igual).

3. **`detectar_anomalias(df, modelo)`** — usa `modelo.predict(...)` sobre a
   matriz de features e adiciona a coluna booleana `is_anomaly_predicted`
   (o `IsolationForest` devolve `-1` para anomalia e `1` para normal).

4. **`avaliar_deteccao(df)`** — compara `is_anomaly_predicted` com
   `is_suspicious_ground_truth` e devolve um dicionário com `precisao`,
   `recall` e `f1` (dica: `sklearn.metrics.precision_score`,
   `recall_score`, `f1_score`).

## Como testar

```bash
cd exercicios
pytest 05-deteccao-de-anomalias-e-fraude -v
```

## Critério de sucesso

Rode `python exercicio.py`. O relatório final deve mostrar recall
razoavelmente alto (o modelo encontra a maior parte das transações
suspeitas de verdade) — mesmo sem nunca ter "visto" a resposta certa
durante o treino.

## Para ir além (ferramentas open source do mundo real)

- [**scikit-learn**](https://scikit-learn.org/) tem dezenas de outros
  detectores de anomalia (`LocalOutlierFactor`, `OneClassSVM`, `DBSCAN`).
- [**PyOD**](https://pyod.readthedocs.io/) é uma biblioteca open source
  dedicada inteiramente a detecção de outliers, com mais de 40 algoritmos.
- Em produção, esse tipo de score costuma alimentar um **caso de uso de
  Anti-Fraude / AML (Anti-Money Laundering)** — a mesma área que, no livro,
  levaria a descoberta de Soraya à CVM.

## Próximo módulo

[`../06-clean-code-e-git/`](../06-clean-code-e-git/)
