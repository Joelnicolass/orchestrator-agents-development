---
name: sdd-triage
description: Clasifica un pedido como fast-track o change completo de OpenSpec.
---

Lee el skill `sdd-orchestrator` y `lanes.md`.

Si el pedido ya cabe en fast-track, responde el contrato de triage sin subagente. Si el alcance no es obvio, lanza `sdd-triage` con el bloque de `prompts.md`.

No escribas specs en este comando. Entrega solo:

```
LANE: fast-track|full
SCHEMA: sdd-fast|sdd-orchestrated
REASON: una frase
```
