---
name: sdd-features
description: Saca de openspec/product.md una lista estable de features con criterios.
---

Sigue el skill `sdd-orchestrator`. No implementes.

Lee `openspec/product.md` y `openspec/config.yaml`. Si no hay producto, vuelve a `sdd-start`.

Escribe `openspec/features.md`. Cada ítem de "Incluye" es al menos un feature. No se omite ninguno. Las librerías de interfaz del config no son un feature aparte: entran en el criterio de cada pantalla.

```markdown
# Features

## F1 Nombre

- Prioridad: must|should|could|wont
- Qué se observa:
- Criterios:
- Depende de:
```

Los ID son permanentes. Si el archivo ya existe, no renumeres. Un feature que sale se marca `[REMOVED]`.

Antes de cerrar, cuenta los must y compáralos con "Incluye". Si falta uno, agrégalo. Dilo en el chat.

Muestra la lista y termina el turno. El siguiente comando es `sdd-split`.
