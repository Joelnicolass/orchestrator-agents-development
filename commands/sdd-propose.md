---
name: sdd-propose
description: Abre un change OpenSpec y redacta proposal y specs, sin diseñar.
---

Sigue el skill `sdd-orchestrator`. Este comando solo cubre el borrador.

1. Si el carril es fast-track, no uses este comando: escribe `tasks.md` con el schema `sdd-fast` y pasa a `sdd-implement`.
2. Elige un slug kebab-case. Si `openspec/changes/<slug>/` ya existe, detente.
3. Crea `.openspec.yaml`:

```yaml
schema: sdd-orchestrated
created: YYYY-MM-DD
```

4. Redacta `proposal.md` y `specs/<capacidad>/spec.md` con las plantillas de `openspec/schemas/sdd-orchestrated/templates/`. El problema y el comportamiento observable. Sin archivos ni framework.
5. No escribas critique, approval, design ni tasks.
6. Sigue con `sdd-critique` si la persona pidió el flujo. Si no, entrega las rutas y espera.
