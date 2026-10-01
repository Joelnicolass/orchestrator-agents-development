---
name: sdd-amend
description: Parcha un spec ya aprobado y relanza solo el critique sobre ese delta.
---

Sigue el skill `sdd-orchestrator`. No abras otro change.

1. Para la implementación.
2. Escribe `openspec/changes/<slug>/amend.md`:

```markdown
---
status: pending
design_impact: no
---

# Amend

## Hueco

## Requisito tocado

## Párrafos nuevos
```

`design_impact: yes` solo si cambian los archivos o el perfil de QA.

3. Parcha ese requisito en el spec. No reescribas el proposal salvo que haya cambiado el porqué. No borres tareas hechas.
4. Lanza `sdd-critique` con `amend.md` y el requisito citado. Nada más del change.
5. Muestra el delta y detente. Hace falta un sí a este amend, no un "sigue".
6. Con el sí, cambia `status` a `approved` en `amend.md`. No toques el `approval.md` original.
7. Si `design_impact` es `no`, retoma `sdd-implement` en las tareas que ya estaban. Si es `yes`, relanza el tech lead de ese dominio y `merge-domains.py`.
