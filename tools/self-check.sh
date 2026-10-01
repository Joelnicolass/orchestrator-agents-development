#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
chmod +x hooks/*.py tools/*.py tools/*.sh install.sh

python3 tools/validate-schemas.py

python3 - <<'PY'
import re
from pathlib import Path
errors = []
for folder in ("agents", "commands"):
    for path in Path(folder).glob("*.md"):
        match = re.search(r"(?m)^name:\s*(\S+)\s*$", path.read_text(encoding="utf-8"))
        got = match.group(1) if match else None
        if got != path.stem:
            errors.append(f"{path}: name={got}")
skill = Path("skills/sdd-orchestrator/SKILL.md").read_text(encoding="utf-8").splitlines()
if len(skill) > 500:
    errors.append(f"SKILL.md tiene {len(skill)} líneas")
models = {
    "sdd-critique": "inherit",
    "sdd-tech-lead": "inherit",
    "sdd-triage": "composer-2.5-fast",
    "sdd-developer": "composer-2.5-fast",
    "sdd-test-engineer": "composer-2.5-fast",
    "sdd-reviewer": "composer-2.5-fast",
    "sdd-qa-design": "composer-2.5-fast",
    "sdd-qa-e2e": "composer-2.5-fast",
    "sdd-documenter": "composer-2.5-fast",
}
for name, model in models.items():
    text = Path(f"agents/{name}.md").read_text(encoding="utf-8")
    if f"model: {model}\n" not in text:
        errors.append(f"{name}: se esperaba model {model}")
if not Path("commands/sdd-amend.md").is_file():
    errors.append("falta commands/sdd-amend.md")
if errors:
    raise SystemExit("\n".join(errors))
print("nombres ok")
PY

python3 -m json.tool hooks/hooks.json >/dev/null

expect_perm() {
  local payload="$1" want="$2"
  local got
  got="$(printf '%s' "$payload" | python3 "$ROOT/hooks/gate-apply.py")"
  python3 -c 'import json,sys; data=json.loads(sys.argv[1]); assert data["permission"]==sys.argv[2], data' "$got" "$want"
}

TMP="$(mktemp -d)"
(
  cd "$TMP"
  mkdir -p openspec/changes/add-login openspec/changes/typo
  expect_perm '{"subagent_type":"sdd-developer","prompt":"openspec/changes/add-login"}' deny
  expect_perm '{"subagent_type":"sdd-critique","prompt":"openspec/changes/add-login"}' allow
  expect_perm '{"subagent_type":"sdd-developer","prompt":"lane: fast-track\nopenspec/changes/add-login"}' allow
  printf 'schema: sdd-fast\n' > openspec/changes/typo/.openspec.yaml
  expect_perm '{"subagent_type":"sdd-developer","prompt":"openspec/changes/typo"}' allow
  printf 'status: approved\n' > openspec/changes/add-login/approval.md
  expect_perm '{"subagent_type":"sdd-tech-lead","prompt":"openspec/changes/add-login"}' allow
  cat > openspec/changes/add-login/amend.md <<'EOF'
---
status: pending
design_impact: no
---
EOF
  expect_perm '{"subagent_type":"sdd-developer","prompt":"lane: fast-track\nopenspec/changes/add-login"}' deny
  expect_perm '{"subagent_type":"sdd-critique","prompt":"openspec/changes/add-login"}' allow
  printf 'status: approved\n' > openspec/changes/add-login/amend.md
  expect_perm '{"subagent_type":"sdd-developer","prompt":"openspec/changes/add-login"}' allow
  rm openspec/changes/add-login/amend.md
  printf '%s' '{"subagent_type":"sdd-developer","prompt":"openspec/changes/add-login"}' | python3 "$ROOT/hooks/nudge-auto-eval.py" | python3 -c 'import json,sys; data=json.loads(sys.stdin.read()); assert "followup_message" in data'
  printf 'result: pass\n' > openspec/changes/add-login/.eval-pass
  printf '%s' '{"subagent_type":"sdd-developer","prompt":"openspec/changes/add-login"}' | python3 "$ROOT/hooks/nudge-auto-eval.py" | python3 -c 'import json,sys; data=json.loads(sys.stdin.read()); assert data=={}'

  mkdir -p openspec/changes/add-login/domains
  cat > openspec/changes/add-login/domains/api.md <<'EOF'
# Domain: api

## Files
- src/api/login.ts — handler

## Decisions
- Token en header

## Out of scope
- Pantallas

## Tests
- [ ] login valido: GIVEN credenciales WHEN post THEN 200

## Tasks
- [ ] implementar handler

## QA
- code_review: yes
- design: no
- e2e: yes

## Verify
- command: true
EOF
  cat > openspec/changes/add-login/domains/web.md <<'EOF'
# Domain: web

## Files
- src/web/login.tsx — formulario

## Decisions
- Sin librería de forms

## Out of scope
- API

## Tests
- [ ] formulario: GIVEN vacío WHEN enviar THEN error visible

## Tasks
- [ ] armar el formulario

## QA
- code_review: yes
- design: yes
- e2e: no

## Verify
- command: true
EOF
  python3 "$ROOT/tools/merge-domains.py" openspec/changes/add-login
  grep -q "e2e: yes" openspec/changes/add-login/tasks.md
  grep -q "design: yes" openspec/changes/add-login/tasks.md
  grep -q "api: implementar handler" openspec/changes/add-login/tasks.md
  grep -q "web: armar el formulario" openspec/changes/add-login/tasks.md

  bash "$ROOT/tools/auto-eval.sh" add-login
  grep -q "result: pass" openspec/changes/add-login/.eval-pass
)
rm -rf "$TMP"

EMPTY="$(mktemp -d)"
(
  cd "$EMPTY"
  bash "$ROOT/tools/auto-eval.sh"
)
rm -rf "$EMPTY"

"$ROOT/install.sh" "$ROOT"
test -f "$ROOT/.cursor/agents/sdd-developer.md"
test -f "$ROOT/.cursor/skills/sdd-orchestrator/SKILL.md"
test -f "$ROOT/openspec/schemas/sdd-orchestrated/schema.yaml"
diff -q "$ROOT/agents/sdd-developer.md" "$ROOT/.cursor/agents/sdd-developer.md"

echo "self-check ok"
