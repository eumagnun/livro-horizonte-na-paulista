# Módulo 04 — Pipelines de Dados: Batch vs. Streaming

> "De seis horas por lote para quarenta e cinco minutos de fluxo contínuo."
> — Soraya, Capítulo 3

## Conceitos

- **Processamento em lote (Batch)**: acumular dados por um período (uma
  hora, um dia) e processar tudo de uma vez. Simples, mas introduz atraso —
  um problema só é detectado no próximo lote.
- **Processamento em fluxo (Streaming) / Arquitetura Orientada a Eventos**:
  processar cada evento assim que ele chega, mantendo um estado que vai
  sendo atualizado incrementalmente. Mais complexo, mas permite reagir em
  tempo real.
- **Latência de detecção**: o tempo entre "o problema aconteceu" e "alguém
  percebeu o problema". É a métrica que muda drasticamente entre as duas
  abordagens.

## Cenário de negócio

No livro, o sistema legado da JCN processa faturamento em lotes de seis em
seis horas. Uma transação suspeita (código `9A` ou `4F`, valor alto, no nó
de rede `SANTOS-PORT-07`) fica invisível até o fim do lote. Soraya reescreve
essa pipeline para processar cada evento assim que ele chega — e, com isso,
o alerta vira imediato.

`../dados/eventos_stream.jsonl` é um recorte de 300 transações, uma por
linha (formato JSON Lines), ordenadas por tempo — exatamente como elas
chegariam em um sistema real de eventos.

## O que você vai construir

Em `exercicio.py`, complete:

1. **`processar_em_lote(eventos)`** — recebe a lista **inteira** de eventos
   de uma vez (só depois que tudo já chegou) e devolve a lista de
   transações suspeitas encontradas (código de ajuste `9A` ou `4F`). Isso
   simula a abordagem antiga: só sabemos depois que o lote inteiro terminou.

2. **`ProcessadorDeEventos`** — uma classe que representa a nova abordagem
   orientada a eventos. Ela mantém um estado interno (`self.total_processado`
   e `self.alertas`) e expõe:
   - **`processar_evento(evento)`**: analisa **um único evento** no momento
     em que ele chega. Se for suspeito, registra um alerta imediatamente
     (com o índice/posição em que foi detectado) e devolve o dicionário do
     alerta; caso contrário, devolve `None`.

3. **`processar_stream(eventos)`** — usa `ProcessadorDeEventos` para
   alimentar os eventos um a um (como um `for`, nunca todos de uma vez) e
   devolve a lista de alertas, na ordem em que foram detectados.

## Como testar

```bash
cd exercicios
pytest 04-pipelines-batch-e-streaming -v
```

## Critério de sucesso

Rode `python exercicio.py`. Ele deve imprimir a mesma lista de transações
suspeitas nas duas abordagens — a diferença não é *o quê* é encontrado, mas
**quando**. No modo streaming, o programa mostra em que posição da fila
cada alerta foi detectado, comprovando que não foi preciso esperar o fim do
lote.

## Para ir além (ferramentas open source do mundo real)

- [**Apache Kafka**](https://kafka.apache.org/) é o "cano" de eventos mais
  usado do mercado para streaming em produção.
- [**Apache Spark Structured Streaming**](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
  (mencionado no livro como "Spark Streaming") faz, em escala industrial, o
  mesmo que a classe `ProcessadorDeEventos` faz aqui em miniatura.
- [**Apache Flink**](https://flink.apache.org/) é outra alternativa open
  source focada especificamente em processamento de fluxo de baixa latência.

## Próximo módulo

[`../05-deteccao-de-anomalias-e-fraude/`](../05-deteccao-de-anomalias-e-fraude/)
