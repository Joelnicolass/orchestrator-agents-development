---
name: sdd-critique
description: Lanza el critique de un change y se detiene antes de implementar.
---

Sigue el skill `sdd-orchestrator`.

1. Hace falta `proposal.md` y al menos un spec. Si faltan, vuelve a `sdd-propose`.
2. Lanza `sdd-critique` sobre `openspec/changes/<slug>`.
3. Si responde `block`, corrige proposal o specs y relanza una vez. No borres los hallazgos anteriores: el critique reescribe `critique.md`.
4. A la segunda vuelta, o si responde `pass`, crea `approval.md` desde la plantilla (`status: pending`) si todavía no está.
5. Muestra blockers, gaps y preguntas. Detente. No lances tech lead en este turno.
