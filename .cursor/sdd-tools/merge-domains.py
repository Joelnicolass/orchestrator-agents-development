#!/usr/bin/env python3
"""Une openspec/changes/<slug>/domains/*.md en design.md y tasks.md."""

from __future__ import annotations

import sys
from pathlib import Path


def sections(text: str) -> dict[str, str]:
    current = "_preamble"
    buf: list[str] = []
    out: dict[str, list[str]] = {}

    def flush() -> None:
        out.setdefault(current, []).append("\n".join(buf).strip())

    for line in text.splitlines():
        if line.startswith("## "):
            flush()
            current = line[3:].strip().lower()
            buf = []
        else:
            buf.append(line)
    flush()
    return {key: "\n".join(parts).strip() for key, parts in out.items()}


def bullets(block: str) -> list[str]:
    lines = []
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            lines.append(stripped)
    return lines


def checks(block: str) -> list[str]:
    found = []
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith("- [") or stripped.startswith("* ["):
            found.append(stripped if stripped.startswith("- ") else "- " + stripped[2:])
    return found


def yes(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"yes", "true", "si", "sí", "1"}


def qa_map(block: str) -> dict[str, str | None]:
    found: dict[str, str | None] = {
        "code_review": None,
        "design": None,
        "e2e": None,
    }
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        key = key.strip().lstrip("-").strip().lower().replace(" ", "_")
        if key in found:
            found[key] = raw.strip()
    return found


def commands(block: str) -> list[str]:
    found = []
    for line in block.splitlines():
        stripped = line.strip().lstrip("-").strip()
        if stripped.lower().startswith("command:"):
            cmd = stripped.split(":", 1)[1].strip()
            if cmd:
                found.append(cmd)
    return found


def domain_name(text: str, path: Path) -> str:
    for line in text.splitlines():
        if line.lower().startswith("# domain:"):
            return line.split(":", 1)[1].strip()
    return path.stem


def merge(change: Path) -> None:
    domain_dir = change / "domains"
    files = sorted(domain_dir.glob("*.md")) if domain_dir.is_dir() else []
    if not files:
        raise SystemExit(f"no hay fragmentos en {domain_dir}")

    parsed = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        parsed.append((domain_name(text, path), sections(text), path))

    code_review = False
    design = False
    e2e = False
    verify: list[str] = []
    design_parts = ["# Design", "", "## Domains", ""]
    decision_parts = ["## Decisions", ""]
    scope_parts = ["## Out of scope", ""]
    test_lines: list[str] = []
    impl_lines: list[str] = []

    for name, blocks, path in parsed:
        if "tasks" not in blocks or not checks(blocks["tasks"]):
            raise SystemExit(f"{path} no tiene ## Tasks con checkboxes")
        qa = qa_map(blocks.get("qa", ""))
        code_review = code_review or yes(qa["code_review"], True)
        design = design or yes(qa["design"], False)
        e2e = e2e or yes(qa["e2e"], False)
        for cmd in commands(blocks.get("verify", "")):
            if cmd not in verify:
                verify.append(cmd)
        design_parts.append(f"### {name}")
        design_parts.append("")
        file_lines = bullets(blocks.get("files", ""))
        design_parts.extend(file_lines or ["- (sin archivos declarados)"])
        design_parts.append("")
        decision_parts.append(f"### {name}")
        decision_parts.append("")
        decision_parts.extend(bullets(blocks.get("decisions", "")) or ["- (sin decisiones extra)"])
        decision_parts.append("")
        scope_parts.append(f"### {name}")
        scope_parts.append("")
        scope_parts.extend(bullets(blocks.get("out of scope", "")) or ["- (nada declarado)"])
        scope_parts.append("")
        for line in checks(blocks.get("tests", "")):
            test_lines.append(prefix(name, line))
        for line in checks(blocks["tasks"]):
            impl_lines.append(prefix(name, line))

    flag = lambda on: "yes" if on else "no"
    qa_block = [
        "## QA profile",
        "",
        f"- code_review: {flag(code_review)}",
        f"- design: {flag(design)}",
        f"- e2e: {flag(e2e)}",
        "",
        "## Verify",
        "",
    ]
    qa_block.extend(f"- command: {cmd}" for cmd in verify)
    if not verify:
        qa_block.append("- command:")

    design_text = "\n".join(design_parts + [""] + decision_parts + [""] + scope_parts + [""] + qa_block)
    design_text = design_text.rstrip() + "\n"
    (change / "design.md").write_text(design_text, encoding="utf-8")

    task_lines = [
        "# Tasks",
        "",
        "## QA profile",
        "",
        f"- code_review: {flag(code_review)}",
        f"- design: {flag(design)}",
        f"- e2e: {flag(e2e)}",
        "",
        "## Verify",
        "",
    ]
    task_lines.extend(f"- command: {cmd}" for cmd in verify)
    if not verify:
        task_lines.append("- command:")
    task_lines.extend(["", "## Tests", ""])
    task_lines.extend(test_lines or ["- [ ] (sin casos; el change no pide tests)"])
    task_lines.extend(["", "## Implementation", ""])
    task_lines.extend(impl_lines)
    (change / "tasks.md").write_text("\n".join(task_lines).rstrip() + "\n", encoding="utf-8")
    print(f"merged {len(parsed)} domain(s) -> {change / 'design.md'} , {change / 'tasks.md'}")


def prefix(name: str, line: str) -> str:
    body = line[6:].strip() if line.startswith("- [ ]") or line.startswith("- [x]") or line.startswith("- [X]") else line
    mark = line[:5]
    if body.lower().startswith(f"{name.lower()}:"):
        return line
    return f"{mark} {name}: {body}"


def main() -> int:
    if len(sys.argv) != 2:
        print("uso: merge-domains.py openspec/changes/<slug>", file=sys.stderr)
        return 2
    change = Path(sys.argv[1])
    if not change.is_dir():
        print(f"no existe {change}", file=sys.stderr)
        return 2
    merge(change)
    return 0


if __name__ == "__main__":
    sys.exit(main())
