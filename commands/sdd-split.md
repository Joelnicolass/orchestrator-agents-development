---
name: sdd-split
description: Parte los features en changes chicos, en orden, sin implementar.
---

Sigue el skill `sdd-orchestrator`. No abras carpetas de change y no escribas código.

Lee `openspec/features.md` y `openspec/config.yaml`. Si no hay features, vuelve a `sdd-features`.

Escribe `openspec/roadmap.md`. Cada change cabe en una pasada: un feature must, o dos que no se pueden separar. El primero que muestra una pantalla incluye el stack visual del config. No dejes el estilo para un change posterior.

```markdown
# Roadmap

## C1 slug

- Features: F1
- Predecesores: ninguno
- Pantalla: sí|no
- Hecho cuando:
```

Orden: un change se puede implementar cuando sus predecesores están hechos. Todo feature `must` que no esté `[REMOVED]` aparece en un change. Ningún ID se repite.

Antes de cerrar, recorre "Incluye" del producto y los must de features. Si alguno no está en el roadmap, agrégalo. Dilo en el chat.

Muestra el corte y termina el turno. No arranques `sdd-next` en este turno.
