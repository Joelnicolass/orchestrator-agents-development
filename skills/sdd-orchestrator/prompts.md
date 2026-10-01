# Prompts de subagentes

Sustituye `{{...}}` antes de lanzar. El tipo de subagente es el `name` del agente. Un dominio por tech lead. No lances dev y reviewer a la vez sobre el mismo change.

## Bloque común

```
Repo: {{root}}
Change: openspec/changes/{{slug}}
Lane: {{lane}}
Dominio: {{domain}}
Lee openspec/config.yaml y .cursor/rules. El stack es el del repo.
No abras otro sistema de specs.
Al terminar responde solo con el contrato de tu agente.
```

`{{lane}}` es `fast-track` o `full`. En fast-track la línea tiene que quedar literal: `Lane: fast-track` no alcanza para el hook; escribe también una línea sola `lane: fast-track`.

## Orden de ejecución

- Tech leads en paralelo cuando los `## Files` no comparten rutas.
- Si los tests y el código de producto se solapan, el test engineer escribe primero. Si los paths son disjuntos, van en paralelo.
- El dev no arranca si el test engineer todavía no escribió los casos que le tocan, salvo que `## Tests` diga que no hay casos.
- Reviewer después de `.eval-pass`.
- QA de diseño y e2e solo si el perfil dice `yes`, después del reviewer en `PASS`.
- Segunda vuelta de FAIL como máximo. A la tercera, para y pregunta.

## Contratos

Triage:

```
LANE: fast-track|full
SCHEMA: sdd-fast|sdd-orchestrated
REASON: una frase
```

Critique (además escribe `critique.md`):

```
STATUS: block|pass
```

Tech lead (además escribe solo `domains/<dominio>.md`):

```
STATUS: READY
DOMAIN: nombre
FILES: cantidad
```

Test engineer:

```
STATUS: WRITTEN
RESULT: red|green
TESTS: rutas
```

`red` es válido si el test expresa el caso y el producto todavía no cumple. No reescribas el producto.

Developer:

```
STATUS: PASS|FAIL
EVAL: pass|fail|skipped
TASKS: ids marcados
```

Reviewer, QA design, QA e2e:

```
STATUS: PASS|FAIL|SKIP
OWNER: developer|test-engineer|none
FINDINGS:
- archivo: hallazgo
```

`SKIP` cuando el perfil está en `no`, o cuando no hay fuente de diseño / comando e2e. `SKIP` no es `PASS`.

Documenter:

```
STATUS: DRAFT
FILES: pr-body.md notes.md
```
