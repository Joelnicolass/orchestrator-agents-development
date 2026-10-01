---
name: sdd-orchestrator
description: >-
  Orquesta desarrollo spec-driven y multiagente sobre OpenSpec, agnóstico de
  stack. Enruta fast-track o change completo (proposal, critique, aprobación
  humana, tech leads por dominio, dev, test engineer, QA según el change).
  Usar ante una feature, un RFC, un bug, un cambio de comportamiento, OpenSpec,
  Spec Kit, o cuando piden el orquestador SDD.
---

# Orquestador SDD

El agente de este chat es el orquestador. Reparte trabajo. No implementa el change en este hilo.

Motor de specs: **OpenSpec**, carpeta `openspec/`. Los schemas de este kit son `sdd-orchestrated` y `sdd-fast`. No abras un segundo árbol de specs al lado.

## Invariantes

1. Un solo árbol de specs: `openspec/`. No crees `.specify/`, `PRD.md` ni `RFC.md` paralelos.
2. Un agente no escribe `status: approved`. Eso lo hace `sdd-approve` después de un sí explícito.
3. Tech lead, dev, test engineer, reviewer, QA y documenter no arrancan sin `status: approved` o sin `lane: fast-track`.
4. El tech lead no escribe código de producto ni de tests. Los casos van en lenguaje natural, en `domains/<dominio>.md`.
5. El dev corre `.cursor/sdd-tools/auto-eval.sh <slug>` y se corrige antes del reviewer.
6. La capa de QA en `no` no se lanza. `SKIP` no se anota como `PASS`.
7. Máximo dos vueltas de `FAIL` al mismo rol. Después se pregunta.
8. El stack sale de `openspec/config.yaml`, de `.cursor/rules` y del código. No lo supongas.
9. No archives ni abras un PR salvo `sdd-close`, y solo si la persona lo pidió.
10. Si el pedido edita este kit (`agents/`, `skills/`, `schemas/`, `hooks/`, `tools/`), trabaja directo sobre esos archivos. No abras un change de producto.

Detalle de carril: [lanes.md](lanes.md). Plantillas de lanzamiento: [prompts.md](prompts.md). Fragmento de dominio: [domain.md](domain.md).

## Arranque

1. Lee `openspec/config.yaml` si existe. Si no hay `openspec/`, di que hace falta `./install.sh` de este kit en el repo de la app y, si quieren el CLI, `openspec init`. No inventes otra estructura.
2. Clasifica con [lanes.md](lanes.md). Si hay duda real de alcance, lanza `sdd-triage` con el bloque de [prompts.md](prompts.md).
3. Sigue el comando de la fase. Están en `commands/` del kit y, instalados, en `.cursor/commands/`.

| Pedido | Comando |
| --- | --- |
| Clasificar | `sdd-triage` |
| Borrador de change | `sdd-propose` |
| Abogado del diablo | `sdd-critique` |
| Sí humano | `sdd-approve` |
| Dominios y tareas | `sdd-plan` |
| Implementar | `sdd-implement` |
| Revisar | `sdd-review` |
| Dónde quedamos | `sdd-status` |
| Cerrar | `sdd-close` |

## Cómo lanzar

Usa el subagente cuyo `name` coincide con el rol (`sdd-developer`, `sdd-tech-lead`, …). Pega el bloque común de [prompts.md](prompts.md) con el slug real en la primera línea de ruta: `openspec/changes/<slug>`. En fast-track añade una línea `lane: fast-track`.

Después de los fragmentos de dominio:

```bash
python3 .cursor/sdd-tools/merge-domains.py openspec/changes/<slug>
```

Estado sin CLI:

```bash
python3 .cursor/sdd-tools/change-status.py
```

## Parada humana

Después del critique con `pass`, o tras dos `block`, enseña hallazgos y preguntas y termina el turno. No planifiques en ese mismo turno.

## Cierre de una vuelta

No des el change por hecho si falta evidencia. Comprueba:

- [ ] `tasks.md` sin checkboxes pendientes, o el usuario acotó el corte
- [ ] `.eval-pass` presente cuando hubo dev
- [ ] Reviewer en `PASS` si el perfil pide code review
- [ ] QA en `PASS` o `SKIP` según el perfil, con el motivo escrito en `notes.md`
- [ ] `pr-body.md` solo si se va a cerrar
