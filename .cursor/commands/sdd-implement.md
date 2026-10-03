---
name: sdd-implement
description: Implementa un fast-track o un change aprobado. Un hueco de spec abre un amend.
---

Sigue el skill `sdd-orchestrator` y los recortes de `prompts.md`. No pases `model`. Si `openspec/config.yaml` no tiene framework ni lineamientos, vuelve a `sdd-start`. No elijas el stack al implementar.

Fast-track (`schema: sdd-fast`):

1. Un `sdd-developer` con la línea `lane: fast-track`.
2. Auto-eval. Reviewer solo si el diff toca lógica. Sin diseño, sin e2e, sin documenter.

Change completo:

1. Exige `status: approved`, `design.md` y `tasks.md`. Si `amend.md` está en `pending`, detente.
2. Tests y dev según el orden de `prompts.md`.
3. Si dev o test engineer responden `AMEND`, pasa a `sdd-amend`. No lo cuentes como FAIL.
4. Con `EVAL: fail`, el dev se corrige antes del review.

Máximo dos vueltas si el reviewer devuelve `FAIL`.
