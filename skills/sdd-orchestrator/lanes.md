# Carriles

Clasifica antes de escribir specs. Si el pedido ya nombra archivo y resultado, y cabe en los criterios de abajo, es fast-track: no hace falta un subagente.

## fast-track → schema `sdd-fast`

Todo esto es cierto:

- El resultado cabe en 1–3 archivos que ya existen, o en un texto/estilo puntual.
- No hay capacidad nueva, ni contrato de API, ni flujo nuevo de pantallas, ni cambio de datos persistentes.
- El usuario describió el resultado. No hay que inventar alcance.

Escribe `openspec/changes/<slug>/.openspec.yaml` con `schema: sdd-fast` y un `tasks.md` de hasta 8 checkboxes. En el prompt del dev incluye la línea `lane: fast-track`.

## full → schema `sdd-orchestrated`

Cualquier otra cosa: feature, cambio de comportamiento, refactor que mueve responsabilidades, o un bug cuya causa no está acotada.

Orden, y no saltes la parada humana:

1. `proposal.md` + `specs/<capacidad>/spec.md`
2. Critique. Si `status: block`, corrige proposal/specs y repite. Máximo dos vueltas; después muestra lo que quede y pregunta.
3. `approval.md` en `pending`. Detente. Muestra blockers, gaps y preguntas.
4. Con un sí explícito, `sdd-approve` pone `status: approved`.
5. Un tech lead por dominio, en paralelo solo si los árboles de archivos no se solapan.
6. `merge-domains.py` escribe `design.md` y `tasks.md`.
7. Tests y dev según `prompts.md`. Auto-eval antes del reviewer.
8. Reviewer de código. QA solo donde el perfil dice `yes`.
9. Documenter escribe `pr-body.md` y `notes.md`. Archivar o abrir PR solo con `sdd-close` si la persona lo pide.

## Perfil de QA

Lo decide el tech lead en el fragmento de dominio. El merge hace la unión: si un dominio pide `e2e: yes`, el change lo pide.

- `code_review`: sí por defecto.
- `design`: sí solo si hay una fuente de diseño en el repo o en el change (archivo, URL, MCP ya conectado).
- `e2e`: sí solo si hay un flujo de usuario y el repo ya tiene cómo ejecutarlo.

`no` significa que esa capa no se lanza.
