# Módulo 08 — Segurança: Controle de Acesso e Kill Switch

> "O Eduardo usou um Kill Switch (Interruptor de Emergência) administrativo
> que ele mantinha no sistema desde os [primeiros anos]... ao acionar o
> Kill Switch de emergência, ele gerou um log de auditoria de nível 0."
> — Capítulo 9
>
> "Vamos dar o que ele quer. Mas com uma Backdoor de Integridade. [...]
> Normalmente é usada por invasores, mas Victor estava propondo uma
> Backdoor Ética." — Capítulo 9

## Conceitos

- **Controle de acesso baseado em papéis (RBAC — Role-Based Access
  Control)**: em vez de dar ou negar permissão pessoa por pessoa, você
  define *papéis* (cargo, função) e o que cada papel pode fazer. É assim
  que sistemas corporativos reais controlam quem vê o quê.
- **Princípio do menor privilégio**: cada papel deve ter *apenas* as
  permissões estritamente necessárias para seu trabalho — nem mais.
- **Kill Switch**: um mecanismo de emergência que desliga ou bloqueia uma
  operação crítica instantaneamente. Poderoso, mas perigoso se qualquer
  pessoa puder acioná-lo sem controle e sem deixar rastro.
- **Hash de senha com salt**: nunca guardamos senhas em texto puro. Um
  "salt" (valor aleatório único por senha) evita que duas senhas iguais
  gerem o mesmo hash, e dificulta ataques de força bruta com tabelas
  pré-computadas (*rainbow tables*).

## Cenário de negócio

A JCN precisa de dois mecanismos de segurança:

1. Um sistema de permissões que garanta que só **CFO** e **Auditor** possam
   ver as "Transações de Classe Especial" (as suspeitas) — um Engenheiro de
   Dados comum só vê o restante. É o mesmo cuidado que Victor tenta impor
   a Soraya ("reporte a mim, e apenas a mim").
2. Um **Kill Switch** que só papéis autorizados podem acionar — e que,
   toda vez que é acionado, registra quem, quando e por quê. Um kill switch
   sem controle de acesso nem auditoria não é uma ferramenta de governança;
   é uma arma nas mãos de quem quiser abusar dela (como o próprio Eduardo
   Costa faz no capítulo 9).

## O que você vai construir

Em `exercicio.py`, complete:

1. **`tem_permissao(papel, permissao)`** — consulta o dicionário
   `PERMISSOES_POR_PAPEL` (já definido) e devolve `True`/`False`.

2. **`gerar_hash_senha(senha, salt=None)`** — gera (ou reaproveita) um
   *salt* aleatório e devolve uma tupla `(hash_hex, salt_hex)` usando
   `hashlib.pbkdf2_hmac`.

3. **`verificar_senha(senha, hash_armazenado, salt_armazenado)`** —
   recalcula o hash com o mesmo salt e compara com o hash armazenado.

4. **`KillSwitch.acionar(papel_do_usuario, motivo)`** — só permite o
   acionamento se `tem_permissao(papel_do_usuario, "acionar_kill_switch")`
   for `True`. Caso contrário, levanta `PermissionError`. Se autorizado,
   registra o evento (papel, motivo, timestamp) no histórico
   `self.historico` e marca `self.ativo = True`.

## Como testar

```bash
cd exercicios
pytest 08-seguranca-kill-switch-e-acesso -v
```

## Discussão (sem código — pense e, se quiser, escreva suas respostas)

O capítulo 9 do livro levanta um dilema real de engenharia: Victor propõe
uma "backdoor ética" — um mecanismo escondido que, sob certas condições,
divulga automaticamente evidências para um órgão regulador.

- Um mecanismo de auditoria automática que age *sem* aprovação humana em
  tempo real é governança ou é vigilantismo?
- Quem deveria ter poder para autorizar a existência desse tipo de
  mecanismo dentro de um sistema de produção?
- Como você tornaria um Kill Switch **auditável** (Módulo 07) e, ao mesmo
  tempo, resistente a abuso por quem tem acesso administrativo legítimo?

Não existe resposta "certa" aqui — é o tipo de decisão que engenheiros e
áreas de compliance discutem juntos, o tempo todo, em empresas reais.

## Critério de sucesso

Todos os testes passam, e rodando `python exercicio.py` você vê o Kill
Switch sendo acionado com sucesso por um papel autorizado e recusado (com
uma mensagem de erro clara) para um papel sem permissão.

## Para ir além (ferramentas open source do mundo real)

- [**Keycloak**](https://www.keycloak.org/) e [**Casbin**](https://casbin.org/)
  são soluções open source completas de controle de acesso (RBAC/ABAC).
- [**Argon2**](https://github.com/P-H-C/phc-winner-argon2) é hoje o
  algoritmo recomendado para hashing de senha (mais robusto que
  PBKDF2), disponível para Python via a biblioteca `argon2-cffi`.
- [**HashiCorp Vault**](https://www.vaultproject.io/) (edição open source)
  gerencia segredos e chaves de forma centralizada e auditável.

## Próximo módulo

[`../09-etica-privacidade-lgpd/`](../09-etica-privacidade-lgpd/)
