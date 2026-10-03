# Prompts de subagentes

Sustituye `{{...}}` antes de lanzar. No pases `model`: critique y tech lead heredan el del chat; el resto lo trae su archivo. Un dominio por tech lead. No lances dev y reviewer a la vez.

## Bloque común

```
Repo: {{root}}
Change: openspec/changes/{{slug}}
Lane: {{lane}}
Dominio: {{domain}}
No leas el skill del orquestador ni abras otro sistema de specs.
Lee openspec/config.yaml: el context y las rules son el stack y los lineamientos. No uses otro.
Lee solo el recorte de tu rol. Responde solo con tu contrato.
```

En fast-track añade una línea sola `lane: fast-track`.

## Recortes

Pega en el prompt solo esto. No adjuntes el change entero.

| Rol | Lee |
| --- | --- |
| Critique | `proposal.md` si cabe en 40 líneas, el spec, y como máximo 30 líneas de reglas pegadas en el prompt. Sin recorrer el repo. |
| Critique de amend | `amend.md` y el requisito citado. Nada más. |
| Tech lead | `openspec/config.yaml`, escenarios del spec y los directorios listados. |
| Test engineer | `openspec/config.yaml`, `## Tests` y los escenarios citados. |
| Developer | `openspec/config.yaml`, `## Implementation` o, en fast-track, `## Tasks`, más `## Files`. |
| Reviewer | `openspec/config.yaml`, el diff y los escenarios citados. |
| QA design | Fuente citada y archivos de UI del diff. |
| QA e2e | Comando y escenario. Sin la línea `e2e: confirmed`, responde SKIP. |
| Documenter | `tasks.md`. Sin leer código. |

Un FAIL se relanza con los hallazgos y las rutas, sin volver a pegar el spec.

## Orden

- Tech leads en paralelo solo si los `## Files` no comparten rutas.
- Tests y dev en secuencia si se solapan. En paralelo solo con rutas disjuntas.
- Reviewer después de `.eval-pass`.
- e2e solo si hay comando en el design y la persona dijo que sí. Entonces el prompt lleva `e2e: confirmed`.
- Segunda vuelta de FAIL como máximo.

## Contratos

Triage: `LANE`, `SCHEMA`, `REASON` en una frase.

Critique: `STATUS: block|pass`. En un amend, el status juzga el delta.

Tech lead: `STATUS: READY`, `DOMAIN`, `FILES`.

Test engineer: `STATUS: WRITTEN` o `STATUS: AMEND`, `RESULT: red|green`, `TESTS`. `red` es válido si el producto todavía no cumple. `AMEND` si el caso no se puede escribir sin inventar comportamiento: no escribas el test.

Developer: `STATUS: PASS|FAIL|AMEND`, `EVAL`, `TASKS`. `AMEND` si el spec no cubre el caso: no implementes el hueco.

Reviewer y QA: `STATUS: PASS|FAIL|SKIP`, `OWNER`, `FINDINGS`. `SKIP` no es `PASS`.

Documenter: `STATUS: DRAFT`, `FILES`.
