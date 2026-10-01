#!/usr/bin/env python3
"""Pide una pasada de auto-eval si el dev cerró sin .eval-pass."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SLUG = re.compile(r"openspec/changes/([a-z0-9][a-z0-9-]*)")


def emit(payload: dict) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")


def blob(data: dict) -> str:
    parts: list[str] = []

    def take(value: object) -> None:
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, dict):
            for key in ("prompt", "task", "description", "text", "content"):
                take(value.get(key))

    for key in ("prompt", "task", "description", "user_message", "input", "context"):
        take(data.get(key))
    for key in ("subagent", "agent"):
        take(data.get(key))
    return "\n".join(parts)


def agent_type(data: dict) -> str:
    for key in ("subagent_type", "subagentType", "agent_type", "name"):
        value = data.get(key)
        if isinstance(value, str) and value:
            return value
    return ""


def root_of(data: dict) -> Path:
    for key in ("cwd", "workspace_root", "root"):
        value = data.get(key)
        if isinstance(value, str) and Path(value).is_dir():
            return Path(value)
    return Path.cwd()


def main() -> int:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        emit({})
        return 0
    if not isinstance(data, dict) or agent_type(data) != "sdd-developer":
        emit({})
        return 0
    text = blob(data)
    match = SLUG.search(text)
    if not match:
        emit({})
        return 0
    marker = root_of(data) / "openspec" / "changes" / match.group(1) / ".eval-pass"
    if marker.is_file():
        emit({})
        return 0
    emit(
        {
            "followup_message": (
                "Falta .eval-pass. Corre .cursor/sdd-tools/auto-eval.sh "
                f"{match.group(1)} y corrige lo que falle antes de cerrar."
            )
        }
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
