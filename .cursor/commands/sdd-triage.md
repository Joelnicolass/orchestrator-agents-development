---
name: sdd-triage
description: Clasifica un pedido como fast-track o change completo de OpenSpec.
---

Lee el skill `sdd-orchestrator` y `lanes.md`.

El default es fast-track. Responde sin subagente si ya se ve si hay capacidad, contrato, datos persistentes o flujo nuevo. Lanza `sdd-triage` solo cuando eso no se puede saber.

No escribas specs en este comando. Entrega solo:

```
LANE: fast-track|full
SCHEMA: sdd-fast|sdd-orchestrated
REASON: una frase
```
