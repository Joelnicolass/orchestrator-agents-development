---
name: sdd-review
description: Corre code review y, con un sí, el e2e que ya tiene comando.
---

Sigue el skill `sdd-orchestrator`.

1. Lanza `sdd-reviewer` con el diff y los escenarios. En fast-track, solo si el diff toca lógica; si es texto o estilo, anota SKIP y termina.
2. Con `PASS` y `design: yes`, lanza `sdd-qa-design` con la fuente y los archivos de UI. Si no, SKIP.
3. e2e no sale del perfil. Si no hay comando en el design, anota SKIP y no preguntes. Si hay comando y un flujo de usuario, pregunta una vez. Solo con un sí, lanza `sdd-qa-e2e` con la línea `e2e: confirmed`, el comando y el escenario.
4. Un `FAIL` vuelve al `OWNER` con los hallazgos y las rutas, sin reenviar el spec. Segunda vez incluida. A la tercera, para y pregunta.
5. No lances al documenter salvo que hayan pedido cerrar el change.
