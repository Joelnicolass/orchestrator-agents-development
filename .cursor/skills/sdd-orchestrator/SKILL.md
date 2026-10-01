---
name: sdd-orchestrator
description: >-
  Orquesta desarrollo spec-driven y multiagente sobre OpenSpec, agnóstico de
  stack. El default es fast-track. El carril completo pide critique, aprobación
  y tech lead. Un hueco de spec se parcha con amend, sin abrir otro change.
  Usar ante una feature, un RFC, un bug, un cambio de comportamiento, OpenSpec
  o cuando piden el orquestador SDD.
disable-model-invocation: true
---

# Orquestador SDD

El agente de este chat es el orquestador. Reparte trabajo. No implementa el change en este hilo. Los subagentes `sdd-*` no leen este skill.

Motor de specs: **OpenSpec**, carpeta `openspec/`. Schemas: `sdd-fast` (default) y `sdd-orchestrated`.

## Invariantes

1. Un solo árbol de specs: `openspec/`.
2. Fast-track salvo capacidad nueva, contrato, datos persistentes o flujo nuevo.
3. Un agente no escribe `status: approved`. Lo hacen `sdd-approve` y el sí del amend.
4. Ejecución (dev, tests, review, QA, documenter, triage) usa el modelo de su archivo. Critique y tech lead heredan el modelo del chat. No pases `model` al lanzar.
5. Cada subagente recibe solo su recorte, en [prompts.md](prompts.md). No pegues el change entero.
6. Proposal de máximo 40 líneas. Un solo spec. Critique con máximo cinco preguntas.
7. `e2e` nace en `no`. Se lanza con un comando ya existente y un sí en este chat (`e2e: confirmed`).
8. Un hueco encontrado al implementar se cierra con `sdd-amend`. No abras otro change.
9. Máximo dos vueltas de critique y dos de `FAIL`.
10. Si el pedido edita este kit (`agents/`, `skills/`, `schemas/`, `hooks/`, `tools/`), trabaja directo.

Carriles: [lanes.md](lanes.md). Lanzamiento: [prompts.md](prompts.md). Fragmento de dominio: [domain.md](domain.md).

## Arranque

1. Lee `openspec/config.yaml` si existe. Si no hay `openspec/`, hace falta `./install.sh` en el repo de la app.
2. Clasifica con [lanes.md](lanes.md). `sdd-triage` solo si de verdad no se sabe si hay capacidad, contrato, datos o flujo nuevo.
3. Sigue el comando de la fase. Instalados quedan en `.cursor/commands/`.

| Pedido | Comando |
| --- | --- |
| Clasificar | `sdd-triage` |
| Borrador | `sdd-propose` |
| Critique | `sdd-critique` |
| Sí humano | `sdd-approve` |
| Dominios | `sdd-plan` |
| Implementar | `sdd-implement` |
| Hueco de spec | `sdd-amend` |
| Revisar | `sdd-review` |
| Estado | `sdd-status` |
| Cerrar | `sdd-close` |

## Amend

`amend.md` con `status: pending` frena a los agentes de ejecución. El critique sí puede correr: recibe solo el delta. Con el sí, `status: approved`. Si `design_impact: no`, se retoman las tareas. Si `design_impact: yes`, un tech lead del dominio afectado y `merge-domains.py`. El `approval.md` original no se reabre.

## Parada humana

Después del critique, enseña hallazgos y termina el turno. Lo mismo después de un amend, antes de seguir implementando.
