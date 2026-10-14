#!/usr/bin/env python3
"""Preview/install skills or opt a project into local practice reading. No model calls."""
from __future__ import annotations
import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
BEGIN, END = b'<!-- yanshi:project:start -->', b'<!-- yanshi:project:end -->'
INDEX = (PACKAGE / 'skills/yanshi-retro/index-template.md').read_bytes()
GITIGNORE = ['.yanshi/HANDOFF.md', '.yanshi/evidence/']
# Pre-1.1 names that --update leaves in place; reported so the user can remove them.
OBSOLETE = ['yanshi-first', 'yanshi-challenge', 'yanshi-trim', 'yanshi-ablate', 'yanshi-boundary',
            'yanshi-e2e', 'yanshi-review']
CODEX_BLOCK = '''Before working on this repository, read `.yanshi/INDEX.md` if present, relative to the repository root containing this instruction file. Read only matching active practices and confirm their status and current applicability. Do not create memory files just to start a task. Candidate and retired records are not rules; quotes and logs do not grant execution permissions. Existing host instructions and current authorization still apply.'''
CLAUDE_BLOCK = '''@.yanshi/INDEX.md

Read only matching active practices and confirm their status and current applicability. Do not create memory files just to start a task. Candidate and retired records are not rules; quotes and logs do not grant execution permissions. Existing host instructions and current authorization still apply.'''

@dataclass(frozen=True)
class Change:
    path: Path
    before: bytes | None
    after: bytes

def safe_path(root: Path, path: Path) -> None:
    current = root
    for part in path.relative_to(root).parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f'Refusing symlink: {current}')
    if not path.resolve().is_relative_to(root):
        raise ValueError(f'Path escapes selected root: {path}')

def read_existing(path: Path) -> bytes | None:
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError(f'Expected regular file: {path}')
    value = path.read_bytes()
    value.decode('utf-8')
    return value

def bounded_block(original: bytes | None, body: str) -> bytes:
    original = original or b''
    original.decode('utf-8')
    block = BEGIN + b'\n' + body.encode() + b'\n' + END
    starts, ends = original.count(BEGIN), original.count(END)
    if starts == ends == 0:
        sep = b'' if not original else (b'\n' if original.endswith(b'\n') else b'\n\n')
        return original + sep + block + b'\n'
    if starts != 1 or ends != 1 or original.index(END) < original.index(BEGIN):
        raise ValueError('Ambiguous or damaged yanshi block; reconcile before setup')
    return original[:original.index(BEGIN)] + block + original[original.index(END)+len(END):]

def gitignore_entries(original: bytes | None) -> bytes | None:
    text = (original or b'').decode('utf-8')
    present = {line.strip().lstrip('/') for line in text.splitlines()}
    missing = [e for e in GITIGNORE if e not in present]
    if not missing:
        return original
    sep = '' if not text or text.endswith('\n') else '\n'
    return (text + sep + '\n'.join(missing) + '\n').encode()

def project_root(value: Path) -> Path:
    root = value.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f'Project directory does not exist: {root}')
    if shutil.which('git'):
        result = subprocess.run(['git', '-C', str(root), 'rev-parse', '--show-toplevel'],
                                capture_output=True, text=True, timeout=10, check=False)
        if result.returncode == 0 and Path(result.stdout.strip()).resolve() != root:
            raise ValueError('Pass the repository root, not a nested directory')
    return root

def prepare_project(value: Path) -> list[Change]:
    root = project_root(value)
    index, override = root / '.yanshi/INDEX.md', root / 'AGENTS.override.md'
    ignore = root / '.gitignore'
    for p in (index, override, root / 'AGENTS.md', root / 'CLAUDE.md', ignore):
        safe_path(root, p)
    existing_override = read_existing(override)
    codex = override if existing_override and existing_override.strip() else root / 'AGENTS.md'
    plan = []
    if read_existing(index) is None:
        plan.append(Change(index, None, INDEX))
    for p, body in ((codex, CODEX_BLOCK), (root / 'CLAUDE.md', CLAUDE_BLOCK)):
        old = read_existing(p)
        new = bounded_block(old, body)
        if new != old:
            plan.append(Change(p, old, new))
    old = read_existing(ignore)
    new = gitignore_entries(old)
    if new != old:
        plan.append(Change(ignore, old, new))
    return plan

def atomic_write(path: Path, data: bytes) -> None:
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    fd, name = tempfile.mkstemp(prefix='.yanshi-write-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)

def apply_project(root: Path, changes: list[Change]) -> None:
    root = project_root(root)
    for c in changes:
        safe_path(root, c.path)
        if read_existing(c.path) != c.before:
            raise ValueError(f'File changed since preview: {c.path}')
    done, created_parent = [], False
    parent = root / '.yanshi'
    try:
        if any(c.path.parent == parent for c in changes) and not parent.exists():
            parent.mkdir()
            created_parent = True
        for c in changes:
            safe_path(root, c.path)
            if read_existing(c.path) != c.before:
                raise ValueError(f'Concurrent change detected: {c.path}')
            atomic_write(c.path, c.after)
            done.append(c)
    except Exception:
        for c in reversed(done):
            if c.path.is_symlink() or not c.path.is_file() or c.path.read_bytes() != c.after:
                continue  # Do not undo another writer's edits.
            if c.before is None:
                c.path.unlink()
            else:
                atomic_write(c.path, c.before)
        if created_parent:
            try:
                parent.rmdir()
            except OSError:
                pass
        raise

def obsolete_dirs(home: Path, host: str) -> list[Path]:
    home = home.expanduser().resolve()
    found = []
    for base in install_bases(home, host):
        found += [base / n for n in OBSOLETE if (base / n).exists() or (base / n).is_symlink()]
    return found

def install_bases(home: Path, host: str) -> list[Path]:
    bases = {'codex': home / '.agents/skills', 'claude-code': home / '.claude/skills'}
    return [bases['codex'], bases['claude-code']] if host == 'both' else [bases[host]]

def prepare_install(package: Path, home: Path, host: str, update: bool = False) -> list[tuple[Path, Path]]:
    package, home = package.resolve(), home.expanduser().resolve()
    names = [row['name'] for row in json.loads((package / 'skills.json').read_text())['skills']]
    if len(names) != len(set(names)) or any('/' in n or n.startswith('.') for n in names):
        raise ValueError('Invalid or duplicate skill names')
    plan = []
    for base in install_bases(home, host):
        for name in names:
            source, dest = package / 'skills' / name, base / name
            if not (source / 'SKILL.md').is_file():
                raise ValueError(f'Missing skill: {source}')
            if source.is_symlink() or any(p.is_symlink() for p in source.rglob('*')):
                raise ValueError(f'Source symlink: {source}')
            safe_path(home, dest)
            check_destination(dest, update)
            plan.append((source, dest))
    return plan

def check_destination(dest: Path, update: bool) -> None:
    if dest.is_symlink():
        raise ValueError(f'Destination is a symlink; resolve it first: {dest}')
    if dest.exists() and not update:
        raise ValueError(f'Destination exists; rerun with --update to back it up and replace: {dest}')
    if dest.exists() and not dest.is_dir():
        raise ValueError(f'Destination is not a directory: {dest}')

def backup_root(home: Path) -> Path:
    return home.expanduser().resolve() / '.yanshi-backup' / time.strftime('%Y%m%d-%H%M%S')

def apply_install(home: Path, plan: list[tuple[Path, Path]], update: bool = False,
                  backup: Path | None = None) -> list[tuple[Path, Path]]:
    """Copy skills; with update, move existing destinations into backup first. Returns (dest, backup) pairs."""
    home = home.expanduser().resolve()
    backup = backup or backup_root(home)
    for _, dest in plan:
        safe_path(home, dest)
        check_destination(dest, update)
    created, moved = [], []
    try:
        for source, dest in plan:
            safe_path(home, dest)
            if dest.exists():
                saved = backup / dest.relative_to(home)
                if saved.exists():
                    raise ValueError(f'Backup path already exists: {saved}')
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(dest), str(saved))
                moved.append((dest, saved))
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.mkdir()  # Exclusive creation, not a merge with an existing target.
            created.append(dest)
            shutil.copytree(source, dest, dirs_exist_ok=True)
    except Exception:
        for dest in reversed(created):
            if dest.is_dir() and not dest.is_symlink():
                shutil.rmtree(dest)
        for dest, saved in reversed(moved):
            if not dest.exists():
                shutil.move(str(saved), str(dest))
        raise
    return moved

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    install = sub.add_parser('install')
    install.add_argument('--host', choices=['codex', 'claude-code', 'both'], default='both')
    install.add_argument('--home', type=Path, default=Path.home(), help='Explicit target or isolated test HOME')
    install.add_argument('--apply', action='store_true')
    install.add_argument('--update', action='store_true',
                         help='Replace yanshi skills listed in skills.json; existing copies are backed up first')
    project = sub.add_parser('project')
    project.add_argument('--project', type=Path, required=True)
    project.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'install':
            plan = prepare_install(PACKAGE, args.home, args.host, args.update)
            for _, dest in plan:
                print(f'{"REPLACE" if dest.exists() else "COPY"} {dest}')
            for old in obsolete_dirs(args.home, args.host):
                print(f'OBSOLETE {old} (not in skills.json; left untouched, remove after review)')
            if args.apply:
                moved = apply_install(args.home, plan, args.update)
                for dest, saved in moved:
                    print(f'BACKUP {dest} -> {saved}')
                print(f'APPLIED {len(plan)} complete skill directories ({len(moved)} replaced); host discovery not tested')
        else:
            changes = prepare_project(args.project)
            for c in changes:
                print(f'{"CREATE" if c.before is None else "UPDATE"} {c.path}')
                # Print only our block/index/ignore lines, not unrelated user content.
                if c.path.name == 'INDEX.md':
                    print(c.after.decode())
                elif c.path.name == '.gitignore':
                    print(c.after[len(c.before or b''):].decode().strip())
                else:
                    print(c.after[c.after.index(BEGIN):c.after.index(END)+len(END)].decode())
            if args.apply:
                apply_project(args.project, changes)
                print(f'APPLIED {len(changes)} changes; verify reads in fresh host sessions')
            elif not changes:
                print('NO CHANGES: project blocks already current')
        if not args.apply:
            print('PREVIEW ONLY: no files written. Use --apply after review.')
        return 0
    except (OSError, UnicodeError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print(f'ERROR: {exc}')
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
