---
name: sdd-approve
description: Marca un change como aprobado solo con un sí explícito de la persona.
---

Sigue el skill `sdd-orchestrator`.

1. Localiza `openspec/changes/<slug>/approval.md`. Tiene que existir y estar en `pending`.
2. Cambia `status` a `approved` solo si en esta conversación la persona dijo que el change está bien. Un "sigue" o el silencio no alcanzan: pregunta cuál change y espera el sí.
3. Completa fecha y quién con lo que la persona haya dicho. No inventes un nombre.
4. No escribas design ni tasks aquí. El siguiente paso es `sdd-plan`.
