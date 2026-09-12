# Módulo 07 — Governança de Dados e Cadeia de Custódia

> "Precisamos saber de onde o dado veio, por onde passou e quem o alterou.
> É a 'cadeia de custódia' da informação." — Capítulo 8, *A Teia Invisível*
>
> "Victor planejava a infraestrutura de blockchain para garantir que os
> logs de auditoria fossem imutáveis." — Capítulo 15

## Conceitos

- **Governança de dados**: o conjunto de políticas e processos que
  garantem que os dados de uma empresa são confiáveis, rastreáveis e usados
  de forma responsável.
- **Cadeia de custódia (chain of custody)**: um termo que vem do mundo
  forense/jurídico — um registro contínuo e à prova de adulteração de quem
  tocou uma evidência, quando e o que fez. Em dados, significa saber
  exatamente a origem e o histórico de alterações de um registro.
- **Log de auditoria imutável (append-only)**: um log onde só é possível
  *adicionar* novos registros — nunca editar ou apagar um já existente. É
  assim que sistemas financeiros e de compliance provam que um relatório
  não foi manipulado depois do fato.
- **Encadeamento por hash (hash chaining)**: a mesma ideia central por trás
  de blockchain, sem precisar de toda a infraestrutura de criptomoedas. Cada
  registro guarda o hash (uma "impressão digital" criptográfica) do
  registro anterior. Se alguém alterar qualquer registro do passado, todos
  os hashes seguintes deixam de "bater" — a adulteração fica evidente.

## Cenário de negócio

Depois da descoberta de Soraya, a JCN precisa provar, para a CVM e para a
Polícia Federal, que o log de auditoria das transações suspeitas não foi
manipulado depois dos fatos. Seu trabalho é construir um livro de auditoria
(`LivroDeAuditoria`) onde cada ação fica permanentemente registrada e
matematicamente amarrada à anterior.

## O que você vai construir

Em `exercicio.py`, complete:

1. **`calcular_hash(dados, hash_anterior)`** — recebe um dicionário de dados
   e o hash do registro anterior, e devolve um hash SHA-256 (string
   hexadecimal) que combina os dois. Dica: converta `dados` para uma string
   determinística com `json.dumps(dados, sort_keys=True)`, concatene com
   `hash_anterior`, e passe para `hashlib.sha256(...).hexdigest()`.

2. **`LivroDeAuditoria.registrar(ator, acao, dados)`** — cria um novo
   registro (dicionário) com as chaves `ator`, `acao`, `dados`,
   `hash_anterior` (o hash do último registro, ou `"0" * 64` se for o
   primeiro) e `hash_atual` (calculado com `calcular_hash`), adiciona à
   lista `self.registros` e devolve o registro criado.

3. **`LivroDeAuditoria.verificar_integridade()`** — percorre todos os
   registros e confirma que:
   - o `hash_anterior` de cada registro bate com o `hash_atual` do registro
     anterior (ou com o hash gênesis, no primeiro);
   - o `hash_atual` de cada registro, recalculado agora a partir de seus
     dados, ainda bate com o valor guardado (ou seja, ninguém editou os
     dados por fora do fluxo normal).

   Devolve `True` se a cadeia inteira é íntegra, `False` caso contrário.

## Como testar

```bash
cd exercicios
pytest 07-governanca-e-auditoria -v
```

## Critério de sucesso

Rode `python exercicio.py`. Ele registra três eventos, confirma que a
cadeia é íntegra e, em seguida, **simula uma adulteração** (edita um
registro do meio diretamente, por fora do método `registrar`) — e mostra
que `verificar_integridade()` passa a detectar o problema.

## Para ir além (ferramentas open source do mundo real)

- [**Hyperledger Fabric**](https://www.hyperledger.org/projects/fabric) é
  uma infraestrutura de blockchain open source pensada para casos de uso
  corporativos/de auditoria (não para criptomoedas).
- [**OpenTelemetry**](https://opentelemetry.io/) padroniza logs, métricas e
  rastros (traces) de forma aberta — a base de qualquer trilha de
  auditoria em sistemas modernos.
- Em bancos de dados como o **PostgreSQL**, extensões de *audit logging*
  fazem algo parecido com o que construímos aqui, de forma automática.

## Próximo módulo

[`../08-seguranca-kill-switch-e-acesso/`](../08-seguranca-kill-switch-e-acesso/)
