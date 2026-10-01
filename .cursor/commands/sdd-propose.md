---
name: sdd-propose
description: Abre un change completo con un proposal corto y un solo spec.
---

Sigue el skill `sdd-orchestrator`.

1. Si el carril es fast-track, no uses este comando. Escribe `tasks.md` con el schema `sdd-fast` y pasa a `sdd-implement`.
2. Slug kebab-case. Si la carpeta ya existe, detente.
3. Crea `.openspec.yaml` con `schema: sdd-orchestrated`.
4. `proposal.md` de máximo 40 líneas, sin archivos ni framework. Un solo `specs/<capacidad>/spec.md`.
5. No escribas critique, approval, design ni tasks.
6. Sigue con `sdd-critique` si pidieron el flujo. Si no, entrega las rutas y espera.
