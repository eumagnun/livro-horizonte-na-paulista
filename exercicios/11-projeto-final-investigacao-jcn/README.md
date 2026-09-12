# Módulo 11 — Projeto Final: A Investigação JCN

> "A 'arqueologia digital' acabara de revelar o primeiro fragmento de uma
> conspiração que tinha o nome do homem mais poderoso das finanças da
> empresa impresso em cada bit." — Capítulo 2

Chegou a hora de fazer, do início ao fim, o que Soraya faz ao longo do
livro inteiro: pegar um sistema legado sujo e transformá-lo em uma
investigação de fraude completa, documentada e defensável.

Este módulo **não tem gabarito com TODOs linha a linha** como os
anteriores — é um projeto de síntese. Você vai reaproveitar (copiando ou
reimportando) o que já construiu nos Módulos 01 a 10.

## O que o projeto final precisa entregar

Um script (`investigacao_jcn.py`, você escreve do zero nesta pasta) que
executa, em sequência, uma investigação completa:

1. **Ingestão** (Módulo 01) — carregue e decodifique o arquivo legado
   `../dados/legado_faturamento.ebcdic.txt`.
2. **Qualidade de dados** (Módulo 02) — valide o resultado contra um
   contrato de dados. Se alguma regra falhar, o relatório final deve
   deixar isso claro (não é aceitável um relatório de fraude construído
   sobre dados não confiáveis).
3. **Engenharia de atributos** (Módulo 03) — enriqueça com a tabela de
   risco por país, `cross_border` e `amount_zscore_cliente`.
4. **Detecção de anomalias** (Módulo 05) — treine um `IsolationForest` e
   sinalize as transações suspeitas.
5. **Governança** (Módulo 07) — registre cada uma das etapas acima em um
   `LivroDeAuditoria`, com o ator `"investigacao_jcn"`.
6. **Controle de acesso** (Módulo 08) — a função que imprime o relatório
   final só deve rodar se for chamada com um papel que tenha a permissão
   `"ver_transacoes_suspeitas"` (levante `PermissionError` caso contrário).
7. **Privacidade** (Módulo 09) — no relatório, pseudonimize os
   `customer_id` antes de exibi-los (nunca exponha o identificador direto
   num relatório que pode circular).
8. **Observabilidade** (Módulo 10) — calcule o PSI entre o primeiro e o
   último trimestre da coluna `amount` das transações sinalizadas como
   suspeitas, e inclua a classificação de drift no relatório.

O relatório final impresso (ou salvo em um arquivo `.txt`/`.json`, à sua
escolha) deve conter, no mínimo:
- total de transações analisadas e quantas foram sinalizadas;
- se o contrato de dados passou ou não;
- os 10 clientes (pseudonimizados) com maior `amount_zscore_cliente` entre
  as transações suspeitas;
- o resultado da checagem de drift;
- confirmação de que o log de auditoria da investigação está íntegro
  (`verificar_integridade()`).

## Como organizar seu código

Você tem duas opções, ambas válidas:

- **Reescrever** as funções relevantes diretamente neste arquivo (mais
  simples, menos DRY);
- **Importar** suas soluções dos módulos anteriores. Como os nomes das
  pastas começam com número e têm hífen, você não pode fazer `import`
  direto — use `importlib.util`:

  ```python
  import importlib.util
  from pathlib import Path

  def importar_modulo(caminho_arquivo: str, nome: str):
      spec = importlib.util.spec_from_file_location(nome, caminho_arquivo)
      modulo = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(modulo)
      return modulo

  mod01 = importar_modulo("../01-arqueologia-de-dados-legados/exercicio.py", "mod01")
  df = mod01.carregar_arquivo_legado()
  ```

## Rubrica de avaliação (autoavaliação)

- [ ] O script roda do início ao fim sem erros com `python investigacao_jcn.py`.
- [ ] Os 8 passos da lista acima estão todos presentes e na ordem certa.
- [ ] Nenhum `customer_id` original aparece no relatório final.
- [ ] O relatório deixa claro tanto o *resultado* (quantas fraudes) quanto a
  *confiabilidade* do processo (contrato de dados, integridade do log,
  drift) — não é só uma lista de números, é uma peça de evidência.
- [ ] Rodar o script duas vezes seguidas gera o mesmo resultado
      (determinismo — cuidado com `random_state` e seeds).

## Reflexão final

Você percorreu o mesmo arco técnico que Soraya percorre no livro:
arqueologia de dados → qualidade → features → detecção → governança →
segurança → privacidade → observabilidade. No livro, essa jornada técnica
também é uma jornada ética — o dado, sozinho, nunca decide o que fazer com
a verdade que revela. Isso continua sendo trabalho humano.

## Para ir além

- Publique seu pipeline como um projeto no GitHub, com testes automatizados
  (`pytest`) e um `README.md` explicando as decisões técnicas — é
  literalmente o portfólio de um Engenheiro de Dados júnior/pleno.
- Tente reescrever a ingestão do Módulo 01 usando
  [**PySpark**](https://spark.apache.org/) em vez de pandas puro, e compare
  o tempo de execução com uma base de dados bem maior (gere mais linhas em
  `../dados/gerar_dados.py`, mudando `N_TRANSACOES`).
