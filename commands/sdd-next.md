---
name: sdd-next
description: Implementa un solo change del roadmap, con el flujo completo.
---

Sigue el skill `sdd-orchestrator`. Un change por vez. No abras el siguiente.

1. Lee `openspec/roadmap.md`, `openspec/features.md` y `openspec/config.yaml`.
2. Elige el primer change cuyos predecesores estén archivados o con todas las tareas hechas, y que todavía no tenga carpeta en `openspec/changes/`. Si la persona nombró un slug, usa ese si sus predecesores están hechos.
3. Sigue `sdd-propose` solo con los features de ese change. Copia cada criterio al spec. Si "Pantalla" es sí, el spec nombra las librerías de interfaz del config y exige usarlas.
4. Sigue el flujo completo de ese change: critique, parada humana, plan, implementación, review. No marques el change como hecho si un criterio no se ve en el diff.
5. Al cerrar, anota en el roadmap que ese change quedó hecho. El próximo espera otro pedido.
