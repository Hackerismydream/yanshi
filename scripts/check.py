#!/usr/bin/env python3
"""Check this repository's text format and links, not agent effectiveness."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

POLICY = {
    "yanshi": True,
    "yanshi-challenge": False,
    "yanshi-e2e": True,
    "yanshi-review": False,
}
ROOT_FILES = {
    ".gitignore", "LICENSE", "README.md", "README_CN.md", "llms.txt",
    "CHANGELOG.md", "design-notes.md", "verification.md",
    "design/DESIGN.md", "design/logo-v2-notes.md", "scripts/check.py",
}
IMAGE_REFERENCES = {
    "assets/logo/yanshi-logo-transparent-128.png",
    "assets/logo/yanshi-logo-transparent-ink-128.png",
    "design/images/logo-v2-2.png", "design/images/readme-hero.png",
    "design/images/x-cover-a.png", "design/images/x-cover-b.png",
}
RUNTIME_NOISE = re.compile(
    r"推断|\bP[01]\d\b|Call the Skill tool|article\.md|e2e-post\.md|"
    r"matt-skills\.md|design/DESIGN\.md|来源见|原文直接引用"
)
DAMAGED = re.compile(
    r"。。|，；|[：；]。|(?:格式|字段|规则|场景|设计|整理)(?:全部|均)?为。"
)
LINK = re.compile(r"\[[^\]\n]*\]\(([^\s)]+)\)")
HTML_LINK = re.compile(r'(?:src|srcset|href)="([^"\s]+)"')


def audit(root: Path, text_only: bool) -> list[str]:
    """Validate this repo's deliberately narrow Markdown/YAML format."""
    errors: list[str] = []
    root = root.resolve()
    for name in sorted(ROOT_FILES):
        if not (root / name).is_file():
            errors.append(f"missing file: {name}")
    actual = {p.name for p in (root / "skills").glob("*") if p.is_dir()}
    if actual != set(POLICY):
        errors.append(f"skill set mismatch: {sorted(actual)}")

    for name, implicit in POLICY.items():
        skill = root / "skills" / name
        manifest = skill / "SKILL.md"
        metadata = skill / "agents" / "openai.yaml"
        try:
            text = manifest.read_text(encoding="utf-8")
            match = re.fullmatch(
                r'---\nname: ([a-z0-9-]+)\ndescription: ("[^\n]*")\n---\n(.+)',
                text, flags=re.DOTALL,
            )
            if not match or match[1] != name:
                raise ValueError("frontmatter or directory name mismatch")
            description = json.loads(match[2])
            if not description.strip() or description.startswith(("模型调用：", "用户调用：")):
                raise ValueError("description missing or prefixed with invocation label")
            meta = metadata.read_text(encoding="utf-8")
            pattern = (
                r'interface:\n  display_name: ("[^\n]*")\n'
                r'  short_description: ("[^\n]*")\n'
                r'  brand_color: "#[0-9A-Fa-f]{6}"\n'
                r'policy:\n  allow_implicit_invocation: (true|false)\n'
            )
            fields = re.fullmatch(pattern, meta)
            if not fields:
                raise ValueError("metadata format mismatch")
            if not all(json.loads(fields[i]).strip() for i in (1, 2)):
                raise ValueError("empty interface text")
            if (fields[3] == "true") != implicit:
                raise ValueError("invocation policy mismatch")
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{name}: {exc}")

    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.relative_to(root).parts:
            continue
        if path.suffix not in {".md", ".txt", ".yaml"}:
            continue
        relative = path.relative_to(root)
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{relative}: {exc}")
            continue
        runtime = relative.parts[0] == "skills"
        if runtime and RUNTIME_NOISE.search(text):
            errors.append(f"{relative}: runtime annotation or proprietary invocation")
        if DAMAGED.search(text):
            errors.append(f"{relative}: damaged sentence or punctuation")
        if path.suffix == ".md":
            fences = re.findall(r"^```[^\n]*$", text, flags=re.MULTILINE)
            if len(fences) % 2:
                errors.append(f"{relative}: unclosed code fence")
        for target in LINK.findall(text) + HTML_LINK.findall(text):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            dest = (path.parent / unquote(parsed.path)).resolve()
            if not dest.is_relative_to(root):
                errors.append(f"{relative}: link escapes repository: {target}")
                continue
            dest_name = dest.relative_to(root).as_posix()
            if text_only and dest_name in IMAGE_REFERENCES:
                continue
            if not dest.exists():
                errors.append(f"{relative}: missing link: {target}")
            if runtime and relative.parts[1] != "yanshi":
                if not dest.is_relative_to(root / "skills" / relative.parts[1]):
                    errors.append(f"{relative}: specialist depends on another directory")

    for name in ("README.md", "README_CN.md", "llms.txt"):
        path = root / name
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            if any(skill not in text for skill in POLICY):
                errors.append(f"{name}: missing current skill name")
            if "22.20" not in text:
                errors.append(f"{name}: missing Node requirement")
    return errors


def self_test(root: Path) -> list[str]:
    """Inject defects into isolated copies; never mutate the source package."""
    skill = "skills/yanshi-challenge/SKILL.md"
    trials = [
        ("runtime marker", skill, "append", "\n（推断）\n"),
        ("double punctuation", skill, "append", "\n完成。。\n"),
        ("damaged sentence", skill, "append", "\n输出格式为。\n"),
        ("invented sibling", skill, "append", "\n[x](../grilling/SKILL.md)\n"),
        ("missing reference", "skills/yanshi-challenge/shortcuts.md", "delete", ""),
        ("wrong policy", "skills/yanshi-e2e/agents/openai.yaml", "policy", ""),
        ("wrong name", skill, "name", ""),
        ("proprietary tool", skill, "append", '\nCall the Skill tool with "tdd"\n'),
        ("broken metadata", "skills/yanshi-review/agents/openai.yaml", "append", "invalid\n"),
        ("unclosed fence", skill, "append", "\n```text\n"),
        ("unknown image", "README.md", "append", '\n<img src="assets/logo/missing.png">\n'),
        ("missing Node requirement", "llms.txt", "node", ""),
    ]
    if audit(root, True):
        raise ValueError("self-test requires a clean text package")
    results = []
    for label, relative, action, content in trials:
        with tempfile.TemporaryDirectory(prefix="yanshi-check-") as directory:
            copy = Path(directory) / "repo"
            shutil.copytree(root, copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            path = copy / relative
            if action == "delete":
                path.unlink()
            else:
                text = path.read_text(encoding="utf-8")
                if action == "append":
                    text += content
                elif action == "policy":
                    text = text.replace("allow_implicit_invocation: true", "allow_implicit_invocation: false")
                elif action == "name":
                    text = text.replace("name: yanshi-challenge", "name: wrong-name", 1)
                elif action == "node":
                    text = text.replace("22.20", "unspecified")
                path.write_text(text, encoding="utf-8")
            if not audit(copy, True):
                raise ValueError(f"defect escaped detection: {label}")
            results.append(f"PASS detect: {label}")
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--text-only", action="store_true", help="allow only known image references to be absent")
    parser.add_argument("--self-test", action="store_true", help="test defect detection in temporary copies")
    args = parser.parse_args()
    try:
        errors = audit(args.root, args.text_only)
        if errors:
            print("\n".join(f"FAIL {message}" for message in errors))
            return 1
        print("PASS package structure, metadata, runtime hygiene, and local links")
        if args.self_test:
            results = self_test(args.root)
            print("\n".join(results))
            print(f"PASS mutation checks: {len(results)}/{len(results)}")
        print("Scope: package checks only; no host-behavior or business-efficacy claim.")
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
