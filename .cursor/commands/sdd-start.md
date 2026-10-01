---
name: sdd-start
description: Arranca el flujo con preguntas o escaneando el proyecto ya creado.
---

Sigue el skill `sdd-orchestrator`. Este comando no implementa. No escribas `PRD.md` ni una carpeta `RFCs/`.

Elige el modo en este orden:

1. Hay código, manifiesto o `README` en el repo: escanea primero.
2. El pedido ya dice el resultado y el archivo o el flujo: con el escaneo alcanza. No preguntes lo que el repo ya responde.
3. Falta el resultado, o no hay proyecto: pregunta.

## Escanear

Lee solo lo que hace falta para nombrar el stack y el chequeo. No recorras el árbol entero.

- `openspec/config.yaml`, `README`, manifiestos (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `*.csproj`, `Gemfile`, `composer.json`, `pubspec.yaml`) y `.cursor/sdd-auto-eval.cmd` si existen.
- Changes abiertos en `openspec/changes/`, sin contar `archive`.
- Si la persona señaló un path, léelo.

Di el tipo de producto que viste (app web, móvil, librería, CLI, servicio, pipeline, u otro) y qué checks no aplican. Un check que no pegue con ese tipo no se menciona.

Si `context:` de `openspec/config.yaml` sigue siendo el texto de ejemplo ("Escribe aquí el stack"), reemplaza ese bloque con stack, comando de chequeo y reglas que sí encontraste. Si el contexto ya está escrito por el equipo, no lo pises: anota solo lo que falte.

## Preguntar

Tandas de 3 a 5. Una tanda y se termina el turno. Máximo dos tandas; después se sigue con lo que haya y las suposiciones quedan escritas.

Primera tanda, solo lo que el escaneo no contestó:

- Qué resultado se quiere ahora, observable.
- Si eso ya existe en el repo o en otro proyecto: path, y hay que leerlo.
- Qué queda fuera.

Segunda tanda solo si de ahí sale un carril completo y todavía no se puede redactar el proposal: para quién es, y si este pedido es un change o va a partirse en varios.

No preguntes negocio, auth, SQL o infraestructura si el producto no los tiene.

## Cerrar el arranque

Cuando el carril se puede elegir, escribe `openspec/intake.md` en máximo 40 líneas:

```markdown
# Intake

- Tipo:
- Lane: fast-track|full
- Resultado:
- Fuera:
- Leído:
- Suposiciones:
```

Después entra al carril sin pedir otro comando. Fast-track sigue en `sdd-implement`. Completo sigue en `sdd-propose`, usando este intake como pedido. Si el pedido se parte en varios changes, el primero es el que desbloquea a los demás; los otros quedan nombrados en el intake y no se abren todavía.
