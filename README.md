# Orquestador SDD

Kit de Cursor para desarrollar con specs y varios agentes, sin atarse a un stack. OpenSpec guarda cada cambio. Este repo reparte el trabajo: triage, critique, aprobación humana, tech leads por dominio, dev, tests, review y el QA que el propio cambio pide.

La forma de empaquetar (comandos, agentes, skills, hooks) sale de la misma idea que un kit de estudio que ya funcionaba. El contenido de aquí no arrastra ese dominio: el stack vive en `openspec/config.yaml` y el chequeo en un comando del repo.

## Decisión

OpenSpec es el único motor de specs. Spec Kit no se instala al lado: sus compuertas (constitution, clarify, analyze, converge) están cubiertas por el config, el critique y el review. El detalle está en [docs/decision.md](docs/decision.md). Los flujos están en [Flujos](#flujos).

## Instalación

En el repo de la aplicación:

```bash
git clone <este-repo> ~/orchestrator-agents-development
~/orchestrator-agents-development/install.sh .
```

Opcional, para `openspec list`, `openspec schema validate` y `openspec archive`:

```bash
npm install -g @fission-ai/openspec@latest
cd <tu-app>
openspec init
```

`install.sh` copia agentes, comandos, el skill, los hooks y los schemas `sdd-orchestrated` y `sdd-fast`. Si no hay `openspec/config.yaml`, escribe uno de ejemplo. Completa ahí el stack y las reglas. No dejes un framework inventado.

El chequeo barato, antes del reviewer, es del proyecto:

```bash
cp examples/sdd-auto-eval.cmd .cursor/sdd-auto-eval.cmd
# edita el archivo: lint, tipos o tests rápidos. exit 0 si pasa.
```

Sin ese archivo, `auto-eval.sh` usa las líneas `command:` del change y, si el repo es Node y tiene `lint` o `typecheck`, esos scripts.

Después de editar `agents/`, `commands/`, `skills/`, `hooks/` o `tools/` en este kit, vuelve a correr `./install.sh` en cada app y en este repo.

## Carriles

| Carril | Cuándo | Schema |
| --- | --- | --- |
| Rápido (default) | Todo lo que no cambia capacidad, contrato, datos persistentes ni un flujo de usuario | `sdd-fast` |
| Completo | Capacidad nueva, contrato, datos persistentes o flujo nuevo | `sdd-orchestrated` |

En el completo, el producto se parte en features y en changes chicos. Se implementa uno por vez, con critique y aprobación. Cada capacidad nombrada queda en la lista. Si el config pide un stack visual, la primera pantalla lo usa.

## Flujos

El chat principal enruta. Un producto con varias capacidades no entra a implementar de una vez.

### Enrutado

```mermaid
flowchart TD
  classDef human fill:#ffebee,stroke:#ffcdd2,color:#c62828
  classDef fast fill:#e0f7fa,stroke:#b2ebf2
  classDef full fill:#f9f0ff,stroke:#d0bfff

  pedido[Pedido] --> kit{Es trabajo sobre el kit?}
  kit -->|si| directo[Se edita en este chat, sin change]
  kit -->|no| puntual{Ajuste de 1 a 3 archivos, sin capacidad nueva?}
  puntual -->|si| rapido[Carril rapido]
  puntual -->|no| start[sdd-start escribe product.md]
  start --> features[sdd-features]
  features --> split[sdd-split escribe el roadmap]
  split --> espera[Se muestra el corte y se espera]
  espera --> next[sdd-next un solo change]
  next --> completo[Flujo completo de ese change]

  class directo,espera human
  class rapido fast
  class start,features,split,next,completo full
```

`/sdd-start` pregunta el resultado y el stack, y lista cada capacidad. `/sdd-features` le pone criterios. `/sdd-split` arma cortes chicos y no implementa. `/sdd-next` corre proposal, critique, aprobación, plan, dev y review solo para el primero que esté libre.

### Carril rápido

Schema `sdd-fast`. Sin proposal, sin critique, sin tech lead, sin diseño, sin e2e y sin documenter.

```mermaid
flowchart TD
  classDef dev fill:#e0f7fa,stroke:#b2ebf2
  classDef qa fill:#fff3e0,stroke:#ffe0b2
  classDef done fill:#e8f5e9,stroke:#c8e6c9

  tasks["tasks.md, maximo 8 tareas"] --> dev["sdd-developer con lane fast-track"]
  dev --> eval{auto-eval}
  eval -->|falla| dev
  eval -->|pasa| logica{El diff toca logica?}
  logica -->|no| skip[Review queda en SKIP]
  logica -->|si| review[sdd-reviewer]
  review -->|FAIL maximo 2| dev
  review -->|PASS| listo[Change listo]
  skip --> listo

  class tasks,dev,eval dev
  class review,logica qa
  class listo,skip done
```

El hook deja pasar a este dev porque el prompt trae `lane: fast-track` o el schema es `sdd-fast`.

### Carril completo

Schema `sdd-orchestrated`. El proposal cabe en 40 líneas y hay un solo spec. El critique hace como máximo cinco preguntas.

```mermaid
flowchart TD
  classDef plan fill:#f9f0ff,stroke:#d0bfff
  classDef human fill:#ffebee,stroke:#ffcdd2,color:#c62828
  classDef dev fill:#e0f7fa,stroke:#b2ebf2
  classDef qa fill:#fff3e0,stroke:#ffe0b2
  classDef done fill:#e8f5e9,stroke:#c8e6c9

  propose["sdd-propose"] --> critique[sdd-critique]
  critique --> veredicto{status}
  veredicto -->|block, primera vez| corregir[Se corrige proposal o spec]
  corregir --> critique
  veredicto -->|pass o segundo block| pending["approval.md en pending"]
  pending --> humano{Si explicito?}
  humano -->|ajustes| propose
  humano -->|si| approve[sdd-approve]
  approve --> dominios{Cuantos arboles de archivos?}
  dominios -->|uno| lead[Un sdd-tech-lead]
  dominios -->|disjuntos| leads[Un tech lead por dominio, en paralelo]
  lead --> merge["merge-domains.py"]
  leads --> merge
  merge --> tareas["design.md y tasks.md, e2e en no"]
  tareas --> solape{Tests y producto comparten archivos?}
  solape -->|si| tester[sdd-test-engineer]
  tester --> testerAmend{AMEND?}
  testerAmend -->|si| amend[sdd-amend]
  testerAmend -->|no| dev[sdd-developer]
  solape -->|no| ambos[Tests y dev en paralelo]
  dev --> trabajo{Sigue o AMEND?}
  ambos --> trabajo
  trabajo -->|AMEND| amend
  trabajo -->|sigue| eval{auto-eval}
  eval -->|falla| dev
  eval -->|pasa| review[sdd-reviewer]
  review --> resultado{Resultado}
  resultado -->|PASS| diseno{design en yes y hay fuente?}
  resultado -->|FAIL 1 o 2| owner{OWNER}
  resultado -->|tercer FAIL| parar[Se pregunta y se para]
  owner -->|developer| dev
  owner -->|test-engineer| tester
  diseno -->|si| qad[sdd-qa-design]
  diseno -->|no| comando{Hay comando e2e?}
  qad -->|FAIL| dev
  qad -->|PASS o SKIP| comando
  comando -->|no| listo[Listo, e2e en SKIP]
  comando -->|si| confirmar{La persona confirma e2e?}
  confirmar -->|no| listo
  confirmar -->|si| qae["sdd-qa-e2e con e2e confirmed"]
  qae -->|FAIL| owner
  qae -->|PASS o SKIP| listo
  listo --> cierre{Pidieron cerrar?}
  cierre -->|no| abierto[El change queda abierto]
  cierre -->|si| doc["sdd-documenter y sdd-close"]

  class propose,critique,corregir,lead,leads,merge,tareas plan
  class pending,humano,approve,confirmar,parar human
  class tester,dev,eval,ambos dev
  class review,qad,qae,diseno qa
  class listo,abierto,doc done
```

Mientras `approval.md` está en `pending`, el hook niega a tech lead, dev, tests, review, QA y documenter. El critique no está en ese hook.

### Amend

Sale del carril completo cuando el test engineer o el dev no pueden seguir sin inventar comportamiento. No se abre otro change y no se reabre el `approval.md` original.

```mermaid
flowchart TD
  classDef plan fill:#f9f0ff,stroke:#d0bfff
  classDef human fill:#ffebee,stroke:#ffcdd2,color:#c62828
  classDef dev fill:#e0f7fa,stroke:#b2ebf2
  classDef blocked fill:#fff3e0,stroke:#ffe0b2

  hueco[Hueco al implementar] --> parar[Se detiene la implementacion]
  parar --> archivo["amend.md en pending"]
  archivo --> bloqueo[El hook frena la ejecucion]
  archivo --> parche[Se parcha solo ese requisito]
  parche --> critique["sdd-critique del delta"]
  critique --> veredicto{status del delta}
  veredicto -->|block| parche
  veredicto -->|pass| espera{Si a este amend?}
  espera -->|no| archivo
  espera -->|si| aprobado["amend.md en approved"]
  aprobado --> impacto{design_impact}
  impacto -->|no| retoma[Se retoman las tareas que ya estaban]
  impacto -->|si| lead[Tech lead solo de ese dominio]
  lead --> merge["merge-domains.py"]
  merge --> retoma
  retoma --> implement[sdd-implement]

  class hueco,parar,parche,critique,lead,merge plan
  class archivo,bloqueo blocked
  class espera,aprobado human
  class retoma,implement dev
```

El critique del amend lee `amend.md` y el requisito citado. Con `design_impact: yes` vuelve a planificar solo ese dominio.

## Comandos

En el chat del repo instalado:

| Comando | Qué hace |
| --- | --- |
| `/sdd-start` | Pregunta, escribe el producto y se detiene |
| `/sdd-features` | Lista cada capacidad con criterios |
| `/sdd-split` | Parte el producto en changes chicos, sin implementar |
| `/sdd-next` | Corre el flujo completo de un solo change |
| `/sdd-triage` | Elige carril |
| `/sdd-propose` | Proposal y specs |
| `/sdd-critique` | Huecos y choques con las reglas; después se detiene |
| `/sdd-approve` | Pasa a `approved` con un sí de la persona |
| `/sdd-plan` | Tech leads por dominio, `design.md` y `tasks.md` |
| `/sdd-implement` | Tests, dev y auto-eval |
| `/sdd-amend` | Parcha el spec y relanza solo el critique |
| `/sdd-review` | Code review y e2e solo con un sí |
| `/sdd-status` | Changes activos |
| `/sdd-close` | Archiva y, si lo pides, abre el PR |

También puedes pedir el flujo en prosa. El skill `sdd-orchestrator` enruta.

## Agentes

`sdd-triage`, `sdd-critique`, `sdd-tech-lead`, `sdd-developer`, `sdd-test-engineer`, `sdd-reviewer`, `sdd-qa-design`, `sdd-qa-e2e`, `sdd-documenter`.

El orquestador es el chat principal. Los subagentes no ven la conversación: el prompt lleva el slug, el carril y el dominio.

## Hooks y herramientas

- `subagentStart` niega a los agentes de ejecución si el change no está aprobado y no es fast-track.
- `subagentStop` del dev pide auto-eval una vez si falta `.eval-pass`.
- `.cursor/sdd-tools/merge-domains.py` une `domains/*.md` en `design.md` y `tasks.md`.
- `.cursor/sdd-tools/change-status.py` resume changes sin el CLI.
- `./tools/self-check.sh` prueba schemas, el gate, el merge y el auto-eval.

## Fuente

Edita las carpetas de la raíz (`agents`, `commands`, `skills`, `schemas`, `hooks`, `tools`). `.cursor/` y `openspec/schemas/` de este repo las regenera `./install.sh`.
