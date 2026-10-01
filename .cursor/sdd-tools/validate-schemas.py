#!/usr/bin/env python3
"""Comprueba que los schemas del kit tienen plantillas y el grafo esperado."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"

REQUIRED = {
    "sdd-orchestrated": [
        "id: proposal",
        "id: specs",
        "id: critique",
        "id: approval",
        "id: design",
        "id: tasks",
        "generates: specs/**/*.md",
        "tracks: tasks.md",
        "status: approved",
        "Máximo 40 líneas",
        "Como máximo cinco preguntas",
    ],
    "sdd-fast": [
        "id: tasks",
        "Lane fast-track",
        "tracks: tasks.md",
    ],
}

TEMPLATES = {
    "sdd-orchestrated": [
        "proposal.md",
        "spec.md",
        "critique.md",
        "approval.md",
        "design.md",
        "tasks.md",
    ],
    "sdd-fast": ["tasks.md"],
}


def main() -> int:
    errors: list[str] = []
    for name, tokens in REQUIRED.items():
        schema = SCHEMAS / name / "schema.yaml"
        if not schema.is_file():
            errors.append(f"falta {schema}")
            continue
        text = schema.read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                errors.append(f"{name}: no está `{token}`")
        for template in TEMPLATES[name]:
            path = SCHEMAS / name / "templates" / template
            if not path.is_file():
                errors.append(f"falta plantilla {path}")
        fast_tasks = SCHEMAS / "sdd-fast" / "templates" / "tasks.md"
        if fast_tasks.is_file() and "lane: fast-track" not in fast_tasks.read_text(encoding="utf-8"):
            errors.append("sdd-fast tasks.md debe declarar lane: fast-track")
        approval = SCHEMAS / name / "templates" / "approval.md"
        if approval.is_file() and "status: pending" not in approval.read_text(encoding="utf-8"):
            errors.append("approval.md debe nacer en pending")
    if errors:
        print("\n".join(errors))
        return 1
    print("schemas ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
