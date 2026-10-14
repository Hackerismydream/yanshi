#!/usr/bin/env python3
"""Structural checks for this repository; never infers model behavior."""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ['README.md','README_CN.md','llms.txt','LICENSE','VERSION','CHANGELOG.md','CONTRIBUTING.md',
            'design-notes.md','verification.md','skills.json','scripts/setup.py','scripts/test_setup.py',
            'docs/usage.md','docs/project-memory.md','docs/author-practices.md','docs/source-excerpts.json',
            'docs/host-validation.md','docs/hosts.md','skills/yanshi-retro/index-template.md']
FRONTMATTER = re.compile(r'---\nname: ([a-z0-9-]+)\ndescription: ("[^\n]*")\n(disable-model-invocation: true\n)?---\n')
SIDECAR = re.compile(r'interface:\n  display_name: "[^"\n]+"\n  short_description: "[^"\n]+"\n'
                     r'  brand_color: "#[0-9a-fA-F]{6}"\npolicy:\n  allow_implicit_invocation: (true|false)\n')
MODEL = re.compile(r'\b(?:gpt-\d[\w.-]*|claude-(?:opus|sonnet|haiku|fable|instant|\d)[\w.-]*|'
                   r'gemini-\d[\w.-]*|o[134]-(?:mini|preview|pro)|(?:opus|sonnet|haiku)\s?\d(?:\.\d)?)\b', re.I)
LINK = re.compile(r'\[[^\]\n]*\]\(([^\s)]+)\)')
HTML = re.compile(r'(?:src|srcset|href)="([^"\s]+)"')
TEXT = {'.md','.txt','.yaml','.json','.py'}


def audit(root: Path) -> list[str]:
    root = root.resolve()
    errors = [f'missing {name}' for name in REQUIRED if not (root / name).is_file()]
    try:
        data = json.loads((root / 'skills.json').read_text())
        rows = data['skills']
        names = [r['name'] for r in rows]
        if len(names) != len(set(names)):
            errors.append('duplicate skill names in skills.json')
        if data['version'] != (root / 'VERSION').read_text().strip():
            errors.append('skills.json version differs from VERSION')
        actual = {p.name for p in (root / 'skills').iterdir() if p.is_dir()}
        if actual != set(names):
            errors.append(f'skills/ dirs differ from skills.json: {sorted(actual ^ set(names))}')
        contexts = set()
        for row in rows:
            n, directory = row['name'], root / 'skills' / row['name']
            m = FRONTMATTER.match((directory / 'SKILL.md').read_text())
            if not m:
                errors.append(f'{n}: invalid frontmatter')
                continue
            description = json.loads(m[2])
            if m[1] != n:
                errors.append(f'{n}: frontmatter name mismatch')
            if not re.search(r'[一-鿿]', description) or not re.search(r'[A-Za-z]{3}', description):
                errors.append(f'{n}: description is not bilingual')
            sidecar = SIDECAR.fullmatch((directory / 'agents/openai.yaml').read_text())
            if not sidecar:
                errors.append(f'{n}: invalid agents/openai.yaml')
            elif bool(m[3]) == row['implicit'] or (sidecar[1] == 'true') != row['implicit']:
                errors.append(f'{n}: invocation policy differs between skills.json, frontmatter and sidecar')
            if (directory / 'project-context.md').exists():
                contexts.add((directory / 'project-context.md').read_bytes())
        if len(contexts) > 1:
            errors.append('project-context.md copies differ')
        for file in ['README.md','README_CN.md','llms.txt','docs/usage.md']:
            text = (root / file).read_text()
            missing = [n for n in names if f'`{n}`' not in text and f'{n}:' not in text and f'/{n}' not in text]
            if missing:
                errors.append(f'{file}: does not mention {missing}')
    except (OSError, ValueError, KeyError, TypeError) as ex:
        errors.append(f'catalog: {ex}')
    IGNORED_TOP = {'materials', 'vendor-skills', 'node_modules', '.venv'}
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if '.git' in rel.parts or '__pycache__' in rel.parts:
            continue
        if rel.parts and rel.parts[0] in IGNORED_TOP:
            continue
        if path.is_symlink():
            errors.append(f'symlink in repository: {rel}')
            continue
        if not path.is_file() or path.suffix not in TEXT:
            continue
        text = path.read_text()
        if rel.as_posix() != 'scripts/check.py' and MODEL.search(text):
            errors.append(f'{rel}: hardcoded model name {MODEL.search(text)[0]!r}')
        if path.suffix != '.md' and path.name != 'llms.txt':
            continue
        for link in LINK.findall(text) + HTML.findall(text):
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            dest = (path.parent / unquote(parsed.path)).resolve()
            if not dest.exists():
                errors.append(f'{rel}: broken link {link}')
            elif rel.parts[0] == 'skills' and rel.parts[1] != 'yanshi' and \
                    not dest.is_relative_to(root / 'skills' / rel.parts[1]):
                errors.append(f'{rel}: links outside its own skill directory, breaks single install')
    try:
        excerpts = json.loads((root / 'docs/source-excerpts.json').read_text())
        cards = (root / 'docs/author-practices.md').read_text()
        for x in excerpts:
            if x['author_quote'] not in cards:
                errors.append(f'author-practices.md lacks quote from source-excerpts.json: {x["author_quote"][:20]}')
    except (OSError, ValueError, KeyError) as ex:
        errors.append(f'source excerpts: {ex}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--self-test', action='store_true', help='Also run scripts/test_setup.py')
    args = parser.parse_args()
    errors = audit(args.root)
    if errors:
        print('\n'.join('FAIL ' + x for x in errors))
        return 1
    print('PASS required files, frontmatter, sidecars, skills.json, links, project-context copies, model names')
    if args.self_test:
        return subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', str(args.root / 'scripts'),
                               '-p', 'test_*.py', '-v'], cwd=args.root, check=False).returncode
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
