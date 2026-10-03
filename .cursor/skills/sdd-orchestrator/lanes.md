# Carriles

El default es fast-track. El carril completo se abre solo si el pedido cumple alguno de estos:

- Capacidad nueva para quien usa el producto.
- Contrato nuevo o cambio de contrato (API, eventos, esquema persistente).
- Cambio de datos que ya están guardados.
- Flujo nuevo de pantallas o de pasos de usuario.

Un bug con reproducción, un ajuste de 1–3 archivos, un texto o un estilo de algo que ya existe se queda en fast-track. Un producto con más de una capacidad no entra a fast-track: va a `product.md`, `features.md` y `roadmap.md`, y se implementa de a un change.

## Producto, features, cortes

1. `sdd-start` escribe `openspec/product.md` y se detiene.
2. `sdd-features` escribe `openspec/features.md`. Cada ítem de "Incluye" tiene ID y criterios. Se detiene.
3. `sdd-split` escribe `openspec/roadmap.md`. Cada change es un feature, o dos que no se pueden separar. Se detiene. No implementa.
4. `sdd-next` toma el primer change listo y corre el flujo completo solo para ese. El estilo pedido en el config entra en el primer change que tiene pantalla.

## fast-track → schema `sdd-fast`

Escribe `openspec/changes/<slug>/.openspec.yaml` con `schema: sdd-fast` y un `tasks.md` de hasta 8 checkboxes. En el prompt del dev incluye una línea sola `lane: fast-track`.

Sin proposal, sin critique, sin tech lead, sin documenter. Reviewer solo si el diff toca lógica. Diseño y e2e no se lanzan.

## full → schema `sdd-orchestrated`

1. `proposal.md` y un spec que copia los criterios de los features de ese change. Si hay pantalla, el spec exige el stack visual del config.
2. Critique. `block` si falta un criterio o el estilo pedido. Si `status: block`, corrige y repite una vez.
3. `approval.md` en `pending`. Detente.
4. Con un sí explícito, `sdd-approve`.
5. Un tech lead por dominio. `e2e` queda en `no`.
6. `merge-domains.py` escribe `design.md` y `tasks.md`.
7. Tests y dev, cada uno con su recorte. Auto-eval antes del reviewer.
8. Reviewer de código. e2e solo con comando ya existente y un sí en este chat.
9. El documenter no forma parte del camino habitual.

## Amend

Si al implementar aparece un hueco del spec, para. No abras otro change. `sdd-amend` parcha el requisito, relanza solo el critique sobre ese delta y pide un sí corto. Con `design_impact: no` se retoma la implementación. Con `design_impact: yes` se relanza solo el tech lead del dominio afectado.
