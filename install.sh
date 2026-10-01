#!/usr/bin/env bash
# Copia el kit a un repo de aplicación.
# Uso: ./install.sh [ruta-del-repo]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
TARGET="$(cd "${1:-.}" && pwd)"

mkdir -p \
  "$TARGET/.cursor/agents" \
  "$TARGET/.cursor/commands" \
  "$TARGET/.cursor/hooks" \
  "$TARGET/.cursor/sdd-tools" \
  "$TARGET/.cursor/rules" \
  "$TARGET/.cursor/skills" \
  "$TARGET/openspec/schemas"

for src in "$ROOT"/agents/*.md; do
  cp "$src" "$TARGET/.cursor/agents/$(basename "$src")"
done

for src in "$ROOT"/commands/*.md; do
  cp "$src" "$TARGET/.cursor/commands/$(basename "$src")"
done

rm -rf "$TARGET/.cursor/skills/sdd-orchestrator"
cp -R "$ROOT/skills/sdd-orchestrator" "$TARGET/.cursor/skills/sdd-orchestrator"

cp "$ROOT/hooks/gate-apply.py" "$ROOT/hooks/nudge-auto-eval.py" "$TARGET/.cursor/hooks/"
cp "$ROOT/hooks/hooks.json" "$TARGET/.cursor/hooks.json"
cp "$ROOT"/tools/*.py "$ROOT"/tools/*.sh "$TARGET/.cursor/sdd-tools/"
cp "$ROOT/rules/sdd-orchestrator.mdc" "$TARGET/.cursor/rules/sdd-orchestrator.mdc"

chmod +x "$ROOT"/hooks/*.py "$ROOT"/tools/*.py "$ROOT"/tools/*.sh "$ROOT/install.sh"
chmod +x "$TARGET"/.cursor/hooks/*.py "$TARGET"/.cursor/sdd-tools/*.py "$TARGET"/.cursor/sdd-tools/*.sh

for schema in sdd-orchestrated sdd-fast; do
  rm -rf "$TARGET/openspec/schemas/$schema"
  cp -R "$ROOT/schemas/$schema" "$TARGET/openspec/schemas/$schema"
done

if [[ ! -f "$TARGET/openspec/config.yaml" ]]; then
  if [[ "$TARGET" == "$ROOT" ]]; then
    cat > "$TARGET/openspec/config.yaml" <<'EOF'
schema: sdd-orchestrated

context: |
  Este repo es el kit del orquestador. Los changes de una aplicación viven
  en el repo donde se instaló el kit. Editar agents, skills, schemas, hooks
  y tools es trabajo sobre el kit y no abre un change de producto.
EOF
  else
    cp "$ROOT/schemas/config.example.yaml" "$TARGET/openspec/config.yaml"
    echo "Escrito openspec/config.yaml. Completa el stack y las reglas del repo."
  fi
else
  echo "openspec/config.yaml ya estaba. Déjalo en schema: sdd-orchestrated, o sdd-fast solo en un change chico."
fi

echo "Instalado en $TARGET"
