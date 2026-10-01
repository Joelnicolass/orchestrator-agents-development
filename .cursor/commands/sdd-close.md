---
name: sdd-close
description: Archiva un change y, si la persona lo pide, abre el pull request.
---

Sigue el skill `sdd-orchestrator`.

1. Hace falta `pr-body.md`. Si falta, corre el documenter antes.
2. Enseña el cuerpo del PR y los SKIP. Pregunta si se archiva, salvo que en este mensaje ya hayan pedido cerrar.
3. Si `openspec` está en el PATH, corre `openspec archive --help` y usa el subcomando que mueve el change a archivo. Si el CLI no está, mueve la carpeta a `openspec/changes/archive/YYYY-MM-DD-<slug>/`.
4. Abre el PR solo si la persona lo pidió en este pedido. Publicar la rama también tiene que estar pedido.
