#!/usr/bin/env python3
"""Install a pinned LP skill bundle; standard-library Python 3.9+ and Git only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / 'skills/lp-bundle.lock.json'
RECEIPT = '.lp-bundle-receipt.json'


def digest(directory):
    """Hash relative names, executable bits and bytes, rejecting symlinks."""
    h = hashlib.sha256()
    for p in sorted(directory.rglob('*')):
        if p.is_symlink():
            raise ValueError(f'Symlink is not allowed in a managed skill: {p}')
        if p.is_file():
            h.update(p.relative_to(directory).as_posix().encode() + b'\0')
            h.update(b'x' if p.stat().st_mode & 0o111 else b'-')
            h.update(hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


def safe_path(value):
    p = Path(value)
    if p.is_absolute() or not p.parts or '..' in p.parts or '\\' in value:
        raise ValueError(f'Invalid package path: {value}')
    return p


def read_lock(path=LOCK):
    lock = json.loads(path.read_text())
    if lock['version'] != 1:
        raise ValueError('Unsupported bundle manifest version')
    names = set()
    for s in lock['skills']:
        name = s['name']
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', name) or name in names:
            raise ValueError(f'Invalid or duplicate skill name: {name}')
        names.add(name)
        safe_path(s['path'])
        for f in s.get('licenseFiles', []):
            safe_path(f)
        if s.get('repo') and (not re.fullmatch(r'[\w.-]+/[\w.-]+', s['repo']) or not re.fullmatch(r'[0-9a-f]{40}', s['ref'])):
            raise ValueError('GitHub dependencies require a full commit SHA')
    return lock


def git(cwd, *args):
    subprocess.run(['git', '-c', 'core.hooksPath=' + os.devnull, *args], cwd=cwd,
                   check=True, stdout=subprocess.DEVNULL, timeout=180)


def stage(lock, directory, verify=True, root=ROOT):
    packages = directory / 'packages'
    packages.mkdir()
    for i, s in enumerate(lock['skills']):
        source = root
        if s.get('repo'):
            source = directory / f'repo-{i}'
            source.mkdir()
            git(source, 'init', '-q')
            git(source, 'remote', 'add', 'origin', f"https://github.com/{s['repo']}.git")
            git(source, 'fetch', '-q', '--depth=1', '--filter=blob:none', 'origin', s['ref'])
            git(source, 'sparse-checkout', 'set', '--no-cone', '/' + s['path'] + '/',
                *('/' + f for f in s.get('licenseFiles', [])))
            git(source, 'checkout', '-q', '--detach', 'FETCH_HEAD')
        src = source / safe_path(s['path'])
        digest(src)  # Reject symlinks before copying.
        target = packages / s['name']
        shutil.copytree(src, target)
        for f in s.get('licenseFiles', []):
            license_path = source / safe_path(f)
            if license_path.is_symlink():
                raise ValueError('License symlinks are not allowed')
            shutil.copy2(license_path, target / Path(f).name)
        entry = (target / 'SKILL.md').read_text()
        if not re.search(r'^name:\s*' + re.escape(s['name']) + r'\s*$', entry, re.M):
            raise ValueError(f"SKILL.md name mismatch: {s['name']}")
        actual = digest(target)
        if verify and actual != s['sha256']:
            raise ValueError(f"Package hash mismatch: {s['name']}; no skills changed")
        s['sha256'] = actual
    return packages


def install(lock, packages, dest):
    """Preflight all collisions before changing any skill; roll back on failure."""
    receipt_path = dest / RECEIPT
    if receipt_path.is_symlink():
        raise ValueError('Receipt must not be a symlink')
    previous = json.loads(receipt_path.read_text()) if receipt_path.exists() else {'skills': {}}
    changes = []
    for s in lock['skills']:
        target = dest / s['name']
        if target.is_symlink():
            raise ValueError(f'Refusing to replace symlink: {target}')
        if target.exists():
            current = digest(target)
            if current == s['sha256']:
                continue
            old = previous['skills'].get(s['name'])
            if not old or current != old['sha256']:
                raise ValueError(f'{target} has unmanaged or edited files. Back it up or choose another --dest; nothing changed.')
        changes.append(s)
    saved = receipt_path.read_bytes() if receipt_path.exists() else None
    completed = []
    with tempfile.TemporaryDirectory(prefix='.lp-backup-', dir=dest) as backup:
        try:
            for s in changes:
                target = dest / s['name']
                old = Path(backup) / s['name']
                if target.exists():
                    target.rename(old)
                completed.append((target, old))
                shutil.copytree(packages / s['name'], target)
            receipt = {'version': 1, 'skills': {s['name']: {k: v for k, v in s.items() if k != 'name'} for s in lock['skills']}}
            tmp = Path(backup) / 'receipt.json'
            tmp.write_text(json.dumps(receipt, indent=2) + '\n')
            os.replace(tmp, receipt_path)
        except BaseException:
            for target, old in reversed(completed):
                if target.exists():
                    shutil.rmtree(target)
                if old.exists():
                    old.rename(target)
            if saved is not None:
                receipt_path.write_bytes(saved)
            elif receipt_path.exists():
                receipt_path.unlink()
            raise
    return [s['name'] for s in changes]


def check(lock, dest):
    valid = True
    for s in lock['skills']:
        p = dest / s['name']
        matches = p.is_dir() and not p.is_symlink() and digest(p) == s['sha256']
        print(f"{s['name']}: {'current' if matches else 'missing or different'}")
        valid = valid and matches
    return valid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, default=Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--check', action='store_true', help='Offline comparison against the checked-in lock')
    modes.add_argument('--refresh-lock', action='store_true', help='Maintainers: rehash local skill and explicitly pinned upstream refs; installs nothing')
    args = parser.parse_args()
    lock = read_lock()
    if args.check:
        return 0 if check(lock, args.dest) else 1
    if args.refresh_lock:
        with tempfile.TemporaryDirectory(prefix='lp-skills-') as tmp:
            stage(lock, Path(tmp), verify=False)
        LOCK.write_text(json.dumps(lock, indent=2) + '\n')
        print('Lock refreshed. Review the diff and test in an isolated --dest before publishing.')
        return 0
    args.dest.mkdir(parents=True, exist_ok=True)
    guard = args.dest / '.lp-bundle-install.lock'
    guard.mkdir()  # A concurrent install must not race with receipts/backups.
    try:
        if check(lock, args.dest):
            print('All skills already match; no download or update required.')
            return 0
        with tempfile.TemporaryDirectory(prefix='lp-skills-') as tmp:
            packages = stage(lock, Path(tmp))
            changed = install(lock, packages, args.dest)
        print('Installed/updated: ' + ', '.join(changed))
        print('Open the next agent turn/session to load the installed skills.')
    finally:
        guard.rmdir()
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, subprocess.SubprocessError) as e:
        raise SystemExit(f'LP bundle: {e}')
