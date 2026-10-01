# Por qué OpenSpec y no los dos

Spec Kit y OpenSpec cubren el mismo hueco: poner el comportamiento en archivos antes de gastar tokens en código. Correr los dos en un repo parte el historial en `.specify/` y `openspec/` y los agentes empiezan a contradecirse.

Este kit usa **OpenSpec** como único motor.

- Cada change es una carpeta. Eso es el historial del producto, el que antes vivía como RFC.
- Un schema propio mete critique y aprobación humana **antes** de que apply deje implementar. Spec Kit analiza en solo lectura y no tiene esa compuerta.
- El carril chico es otro schema (`sdd-fast`), no una excepción informal.
- El CLI es opcional. Los archivos se pueden escribir a mano. `openspec list`, `schema validate` y `archive` suman cuando está instalado.

Lo que Spec Kit hace bien queda absorbido, sin instalarlo:

| Spec Kit | En este kit |
| --- | --- |
| constitution | `openspec/config.yaml` más las reglas del repo |
| specify | `proposal.md` y `specs/` |
| clarify / analyze | agente `sdd-critique` y la parada humana |
| plan / tasks | tech leads por dominio y `tasks.md` |
| implement | `sdd-implement` con dev y test engineer |
| converge | `sdd-review` contra los specs; los huecos vuelven como FAIL, no como tareas mudas |
| bugfix | schema `sdd-fast` |

Spec Kit solo, sin este kit, tiene sentido cuando un único agente va a recorrer `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` y no hace falta critique, dominios ni QA selectivo. En ese caso no mezcles los dos árboles.
