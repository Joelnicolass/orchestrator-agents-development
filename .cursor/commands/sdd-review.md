---
name: sdd-review
description: Corre code review y el QA que el perfil del change dejó encendido.
---

Sigue el skill `sdd-orchestrator`.

1. Lee el perfil en `tasks.md`.
2. Lanza `sdd-reviewer` si `code_review: yes`.
3. Con `PASS`, lanza `sdd-qa-design` solo si `design: yes`. Si no, anota SKIP.
4. Lanza `sdd-qa-e2e` solo si `e2e: yes` y el diseño no devolvió `FAIL`. Si el perfil está en `no`, anota SKIP.
5. Un `FAIL` vuelve al `OWNER` que indique el informe. Segunda vez incluida. A la tercera, para y pregunta.
6. Cuando todo está en `PASS` o `SKIP`, lanza `sdd-documenter`.
7. No archives y no abras el PR aquí.
