#!/usr/bin/env python3
"""Resume changes activos de OpenSpec sin depender del CLI."""

from __future__ import annotations

import sys
from pathlib import Path


def approval(change: Path) -> str:
    path = change / "approval.md"
    if not path.is_file():
        return "sin approval"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "sin status"


def schema(change: Path) -> str:
    path = change / ".openspec.yaml"
    if not path.is_file():
        return "sin schema"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("schema:"):
            return line.split(":", 1)[1].strip()
    return "sin schema"


def boxes(change: Path) -> tuple[int, int]:
    path = change / "tasks.md"
    if not path.is_file():
        return (0, 0)
    done = pending = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- [x]") or stripped.startswith("- [X]"):
            done += 1
        elif stripped.startswith("- [ ]"):
            pending += 1
    return done, pending


def main() -> int:
    root = Path("openspec/changes")
    if not root.is_dir():
        print("No hay openspec/changes.")
        return 0
    active = [p for p in sorted(root.iterdir()) if p.is_dir() and p.name != "archive"]
    if not active:
        print("No hay changes activos.")
        return 0
    for change in active:
        done, pending = boxes(change)
        print(
            f"{change.name}  schema={schema(change)}  approval={approval(change)}  "
            f"tareas={done} hechas / {pending} pendientes"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
