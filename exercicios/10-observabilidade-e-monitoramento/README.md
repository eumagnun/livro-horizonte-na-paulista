# Módulo 10 — Observabilidade e Monitoramento de Sistemas de IA

> "O relatório de Observabilidade está 98% concluído... A Observabilidade
> (Observability) em IA é um degrau acima do monitoramento simples. Enquanto
> o monitoramento diz que o sistema está 'online' ou 'offline', a
> observabilidade nos permite entender o estado interno do modelo através
> dos dados que ele [processa]." — Capítulo 15, *O Horizonte na Paulista*

## Conceitos

- **Monitoramento**: responde perguntas simples e binárias — "o serviço
  está no ar?", "quantos erros aconteceram na última hora?". Necessário,
  mas insuficiente.
- **Observabilidade**: vai além — permite entender **por que** um sistema
  está se comportando de determinado jeito, olhando para o que está
  acontecendo *dentro* dele, especialmente em sistemas de IA, onde o
  "comportamento" é estatístico, não binário.
- **Data drift / Model drift**: quando os dados que um modelo recebe hoje
  têm uma distribuição estatística diferente dos dados com que ele foi
  treinado. Um modelo pode continuar "no ar" (monitoramento OK) e, ainda
  assim, estar dando previsões cada vez piores porque o mundo mudou
  (observabilidade ruim, sem essa métrica, ninguém percebe).
- **PSI (Population Stability Index)**: uma métrica padrão de mercado para
  quantificar o quanto uma distribuição numérica "andou" em relação a uma
  distribuição de referência. Convenção usada na indústria:
  - `PSI < 0.10` → sem drift significativo;
  - `0.10 ≤ PSI < 0.25` → drift moderado, vale investigar;
  - `PSI ≥ 0.25` → drift severo, o modelo provavelmente precisa ser
    retreinado.

## Cenário de negócio

O Nexus (a IA da JCN) foi treinado com o comportamento de gasto dos
clientes de um período de referência. Antes de confiar cegamente nas
previsões dele para sempre, a equipe de Soraya precisa de um jeito
sistemático de perguntar: **"os dados de hoje ainda parecem com os dados
com que o modelo aprendeu?"**

## O que você vai construir

Em `exercicio.py`, complete:

1. **`calcular_taxa_erro(logs)`** — a métrica clássica de *monitoramento*:
   recebe uma lista de dicionários de log (cada um com uma chave
   `"status"`, valendo `"SUCCESS"` ou `"ERROR"`) e devolve o percentual
   (0 a 100) de execuções que falharam.

2. **`calcular_psi(referencia, atual, n_bins=10)`** — a métrica de
   *observabilidade*: recebe dois arrays numéricos (`numpy.ndarray`) e
   calcula o Population Stability Index entre eles. Algoritmo:
   1. Divida `referencia` em `n_bins` faixas de mesmo tamanho populacional
      (dica: `numpy.percentile` com pontos igualmente espaçados de 0 a
      100), com a primeira faixa começando em `-inf` e a última terminando
      em `+inf` (para cobrir qualquer valor de `atual` fora do intervalo
      observado em `referencia`).
   2. Conte quantos pontos de `referencia` e de `atual` caem em cada faixa,
      e converta em proporções (percentual do total de cada array).
   3. Para evitar divisão por zero ou `log(0)`, garanta que nenhuma
      proporção seja exatamente `0` (dica: `numpy.clip(proporcao, 1e-6,
      None)`).
   4. PSI = soma, em todas as faixas, de
      `(proporção_atual - proporção_referencia) * ln(proporção_atual / proporção_referencia)`.

3. **`classificar_drift(psi)`** — devolve uma string:
   `"sem drift"`, `"drift moderado"` ou `"drift severo"`, conforme os
   limiares acima.

## Como testar

```bash
cd exercicios
pytest 10-observabilidade-e-monitoramento -v
```

## Critério de sucesso

Rode `python exercicio.py`. Ele compara a distribuição de `amount` do
primeiro trimestre de transações (referência) com a do último trimestre
(atual) na base real da JCN — e, separadamente, com uma distribuição
sinteticamente "deslocada", para você ver os dois extremos: dados estáveis
vs. dados com drift severo.

## Para ir além (ferramentas open source do mundo real)

- [**Evidently AI**](https://www.evidentlyai.com/) é uma biblioteca open
  source dedicada inteiramente a observabilidade de dados e de modelos de
  ML, incluindo cálculo automático de PSI e dashboards.
- [**Prometheus**](https://prometheus.io/) + [**Grafana**](https://grafana.com/)
  formam a dupla open source mais usada do mercado para monitoramento
  clássico (métricas, alertas).
- [**OpenTelemetry**](https://opentelemetry.io/) (já citado no Módulo 07)
  também é a base moderna para observabilidade de sistemas em geral, não só
  de IA.

## Próximo módulo (projeto final)

[`../11-projeto-final-investigacao-jcn/`](../11-projeto-final-investigacao-jcn/)
