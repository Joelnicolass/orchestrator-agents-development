#!/usr/bin/env python3
"""Bloquea subagentes de ejecución si el change no está aprobado."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

GATED = {
    "sdd-tech-lead",
    "sdd-developer",
    "sdd-test-engineer",
    "sdd-reviewer",
    "sdd-qa-design",
    "sdd-qa-e2e",
    "sdd-documenter",
}
SLUG = re.compile(r"openspec/changes/([a-z0-9][a-z0-9-]*)")
APPROVED = re.compile(r"(?m)^status:\s*['\"]?approved['\"]?\s*$")


def emit(payload: dict) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")


def allow() -> None:
    emit({"permission": "allow"})


def deny(message: str) -> None:
    emit({"permission": "deny", "user_message": message})


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
    for key in ("subagent", "agent"):
        value = data.get(key)
        if isinstance(value, dict):
            for inner in ("type", "name", "subagent_type"):
                if isinstance(value.get(inner), str):
                    return value[inner]
    return ""


def root_of(data: dict) -> Path:
    for key in ("cwd", "workspace_root", "root"):
        value = data.get(key)
        if isinstance(value, str) and Path(value).is_dir():
            return Path(value)
    return Path.cwd()


def change_dir(root: Path, text: str) -> Path | None:
    match = SLUG.search(text)
    if not match:
        return None
    return root / "openspec" / "changes" / match.group(1)


def first_status(path: Path) -> str:
    if not path.is_file():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("status:"):
            return line.split(":", 1)[1].strip().strip("'\"")
    return ""


def amend_pending(root: Path, text: str) -> bool:
    change = change_dir(root, text)
    if change is None:
        return False
    return first_status(change / "amend.md") == "pending"


def fast_or_approved(root: Path, text: str) -> bool:
    if "lane: fast-track" in text:
        return True
    change = change_dir(root, text)
    if change is None:
        return False
    meta = change / ".openspec.yaml"
    if meta.is_file():
        meta_text = meta.read_text(encoding="utf-8")
        if re.search(r"(?m)^schema:\s*sdd-fast\s*$", meta_text):
            return True
        if re.search(r"(?m)^lane:\s*fast-track\s*$", meta_text):
            return True
    approval = change / "approval.md"
    if approval.is_file() and APPROVED.search(approval.read_text(encoding="utf-8")):
        return True
    return False


def main() -> int:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        allow()
        return 0
    if not isinstance(data, dict):
        allow()
        return 0
    kind = agent_type(data)
    if kind not in GATED:
        allow()
        return 0
    text = blob(data)
    root = root_of(data)
    if amend_pending(root, text):
        deny(
            "Hay un amend de spec pendiente. Hasta que amend.md pase a "
            "status: approved no sigue la ejecución."
        )
        return 0
    if fast_or_approved(root, text):
        allow()
        return 0
    deny(
        "Change sin aprobación. Hace falta status: approved en approval.md, "
        "o lane: fast-track para un cambio chico."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
