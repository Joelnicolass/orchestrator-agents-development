---
name: sdd-status
description: Resume los changes OpenSpec activos, sin implementar.
---

Corre `python3 .cursor/sdd-tools/change-status.py` en la raíz del repo.

Si `openspec` está en el PATH, puedes sumar `openspec list`. Si contradice al script, enseña las dos salidas.

No edites archivos. Si un change tiene `amend.md` en `pending`, el siguiente paso es el sí del amend. Si no, di el comando que toca: `sdd-critique`, `sdd-approve`, `sdd-plan`, `sdd-implement`, `sdd-review` o `sdd-close`.
