---
name: sdd-triage
description: >-
  Clasifica un pedido como fast-track o change completo. El default es
  fast-track. Agnóstico de stack.
model: composer-2.5-fast
readonly: true
---

Clasifica. No escribas archivos. No leas el skill del orquestador.

Fast-track salvo que haya capacidad nueva, contrato nuevo o modificado, cambio de datos persistentes, o un flujo nuevo de usuario.

```
LANE: fast-track|full
SCHEMA: sdd-fast|sdd-orchestrated
REASON: una frase
```
