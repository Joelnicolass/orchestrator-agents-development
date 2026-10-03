---
name: sdd-propose
description: Abre un change completo con un proposal corto y un solo spec.
---

Sigue el skill `sdd-orchestrator`.

1. Si el carril es fast-track, no uses este comando. Escribe `tasks.md` con el schema `sdd-fast` y pasa a `sdd-implement`.
2. Slug kebab-case. Si la carpeta ya existe, detente.
3. Crea `.openspec.yaml` con `schema: sdd-orchestrated`.
4. Si `openspec/config.yaml` no tiene framework ni lineamientos, vuelve a `sdd-start`. El proposal cubre solo los features de este change. Copia sus criterios al spec, sin resumirlos. Si el roadmap marca pantalla, el spec nombra las librerías de interfaz del config. Máximo 40 líneas de problema; los criterios no se cortan para llegar a ese tope. Un solo `specs/<capacidad>/spec.md`.
5. No escribas critique, approval, design ni tasks.
6. Sigue con `sdd-critique` si pidieron el flujo. Si no, entrega las rutas y espera.
