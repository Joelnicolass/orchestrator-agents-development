---
name: sdd-plan
description: Parte un change aprobado en dominios y genera design.md y tasks.md.
---

Sigue el skill `sdd-orchestrator`.

1. Confirma `status: approved` en `approval.md`. Si no está, detente en `sdd-approve`.
2. Lee proposal y specs. Parte en dominios solo donde los árboles de archivos sean disjuntos. Un solo dominio si el change es cohesivo. Los nombres salen del cambio, no de una lista fija.
3. Lanza un `sdd-tech-lead` por dominio, en paralelo si no comparten rutas. Cada uno escribe `domains/<dominio>.md`.
4. Corre `python3 .cursor/sdd-tools/merge-domains.py openspec/changes/<slug>`.
5. Enseña el perfil de QA y el árbol. No implementes en este turno salvo que la persona ya haya pedido el flujo completo y el plan no tenga huecos. En ese caso sigue con `sdd-implement`.
