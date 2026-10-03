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

Tandas de 3 a 5. Una tanda y se termina el turno.

Primera tanda, solo lo que el escaneo no contestó:

- Qué resultado se quiere ahora, observable.
- Si eso ya existe en el repo o en otro proyecto: path, y hay que leerlo.
- Qué queda fuera.

Tanda técnica, obligatoria antes de implementar. Si el escaneo ya nombró framework y reglas, enséñalas y pide un sí o el cambio. Si no están, pregunta y no elijas vos:

- Framework, lenguaje y librerías que sí se usan.
- Lineamientos de arquitectura: dónde vive la lógica y qué no se mezcla.
- Reglas de código que quien programa quiere exigir, y qué está prohibido.
- Comando de chequeo (lint, tipos o tests).

Otra tanda de producto solo si el carril es completo y todavía no se puede redactar el proposal: para quién es, y si este pedido es un change o va a partirse en varios.

No preguntes negocio, auth, SQL o infraestructura si el producto no los tiene. El stack no entra en esa exclusión: sin framework ni lineamientos no se cierra el arranque.

## Cerrar el arranque

Escribe el stack, la arquitectura, las reglas y el comando de chequeo en `openspec/config.yaml`, dentro de `context`. Suma las reglas de código en `rules` sin borrar las de proposal, specs, critique ni approval. Si la persona no las definió, detente en esa pregunta. No supongas un framework.

Cuando el carril se puede elegir y el config ya tiene esas reglas, escribe `openspec/intake.md` en máximo 40 líneas:

```markdown
# Intake

- Tipo:
- Lane: fast-track|full
- Resultado:
- Fuera:
- Stack y reglas: openspec/config.yaml
- Leído:
```

Después entra al carril sin pedir otro comando. Fast-track sigue en `sdd-implement`. Completo sigue en `sdd-propose`, usando este intake como pedido. Si el pedido se parte en varios changes, el primero es el que desbloquea a los demás; los otros quedan nombrados en el intake y no se abren todavía.
