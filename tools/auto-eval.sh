#!/usr/bin/env bash
# Corre el chequeo del repo antes de que el dev entregue.
# Uso: auto-eval.sh <slug>
# Orden: .cursor/sdd-auto-eval.cmd, si no los command: del change, si no lint/typecheck de package.json.
set -u

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"
SLUG="${1:-${SDD_CHANGE:-}}"
STATUS=0
RAN=0

run_cmd() {
  RAN=1
  echo "auto-eval: $*"
  if ! "$@"; then
    STATUS=1
  fi
}

run_shell() {
  RAN=1
  echo "auto-eval: $1"
  if ! bash -lc "$1"; then
    STATUS=1
  fi
}

if [[ -f .cursor/sdd-auto-eval.cmd ]]; then
  run_cmd bash .cursor/sdd-auto-eval.cmd
else
  if [[ -n "$SLUG" && -d "openspec/changes/$SLUG" ]]; then
    while IFS= read -r cmd; do
      [[ -z "$cmd" ]] && continue
      run_shell "$cmd"
    done < <(python3 - "$SLUG" <<'PY'
import pathlib, sys
slug = sys.argv[1]
root = pathlib.Path("openspec/changes") / slug
cmds = []
for name in ("design.md", "tasks.md"):
    path = root / name
    if not path.is_file():
        continue
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip().lstrip("-").strip()
        if stripped.lower().startswith("command:"):
            cmd = stripped.split(":", 1)[1].strip()
            if cmd and cmd not in cmds:
                cmds.append(cmd)
print("\n".join(cmds))
PY
)
  fi

  if [[ "$RAN" -eq 0 && -f package.json ]]; then
    PM="npm"
    if [[ -f pnpm-lock.yaml ]]; then PM="pnpm"
    elif [[ -f yarn.lock ]]; then PM="yarn"
    elif [[ -f bun.lock || -f bun.lockb ]]; then PM="bun"
    fi
    SCRIPTS=()
    while IFS= read -r script; do
      [[ -n "$script" ]] && SCRIPTS+=("$script")
    done < <(node -e 'const s=(require("./package.json").scripts)||{}; for (const n of ["lint","typecheck"]) if (s[n]) console.log(n)')
    if [[ "${#SCRIPTS[@]}" -gt 0 ]]; then
      if [[ ! -d node_modules ]]; then
        echo "auto-eval: falta node_modules; instala dependencias y vuelve a correr"
        STATUS=1
        RAN=1
      else
        for script in "${SCRIPTS[@]}"; do
          run_cmd "$PM" run "$script"
        done
      fi
    fi
  fi
fi

RESULT="fail"
if [[ "$STATUS" -eq 0 && "$RAN" -eq 0 ]]; then
  RESULT="skipped"
  echo "auto-eval: sin chequeo de proyecto. Define .cursor/sdd-auto-eval.cmd o un command: en el change."
elif [[ "$STATUS" -eq 0 ]]; then
  RESULT="pass"
fi

if [[ -n "$SLUG" && -d "openspec/changes/$SLUG" && "$RESULT" != "fail" ]]; then
  printf 'result: %s\ntime: %s\n' "$RESULT" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "openspec/changes/$SLUG/.eval-pass"
fi

echo "auto-eval: $RESULT"
exit "$STATUS"
