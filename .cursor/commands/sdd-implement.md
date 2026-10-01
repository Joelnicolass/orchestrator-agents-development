---
name: sdd-implement
description: Implementa un change aprobado o un fast-track, con tests y auto-eval.
---

Sigue el skill `sdd-orchestrator` y el orden de `prompts.md`.

Fast-track (`schema: sdd-fast`):

1. Un solo `sdd-developer`, con la línea `lane: fast-track` en el prompt.
2. Tiene que correr `auto-eval.sh`.
3. Si el diff toca lógica, un `sdd-reviewer`. Si es solo texto o estilo, anota el reviewer como SKIP en `notes.md`, sin lanzar QA de diseño ni e2e.

Change completo:

1. Exige `status: approved`, `design.md` y `tasks.md`.
2. Si hay casos bajo `## Tests` y se solapan con el código, `sdd-test-engineer` primero. Si los paths son disjuntos, en paralelo con el dev.
3. `sdd-developer`. No des por cerrado un `EVAL: fail`.
4. Pasa a `sdd-review`.

Máximo dos vueltas si el reviewer devuelve `FAIL`.
