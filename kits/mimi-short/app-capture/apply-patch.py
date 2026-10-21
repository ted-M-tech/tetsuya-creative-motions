"""Apply a tiny capture-only patch: for each hunk, find its context lines (' ' and '-') exactly once and insert the '+' lines.
usage: python3 apply-patch.py film/app-capture/x.patch <app checkout>   (unified-diff look, but matched by text, not line numbers)
A patch may hold several files (each starting with '--- a/' / '+++ b/') and several '@@' hunks per file.
"""
import sys
from pathlib import Path

patch, root = Path(sys.argv[1]).read_text().splitlines(), Path(sys.argv[2])
files, target, hunk = {}, None, None
for line in patch:
    if line.startswith('+++ b/'):
        target = line[6:]; files.setdefault(target, []); hunk = None
    elif line.startswith('--- a/') or target is None:
        continue
    elif line.startswith('@@'):
        hunk = []; files[target].append(hunk)
    elif hunk is not None:
        hunk.append(line)
for target, hunks in files.items():
    f = root / target
    s = f.read_text()
    for body in hunks:
        old = '\n'.join(l[1:] for l in body if l[:1] in (' ', '-'))
        new = '\n'.join(l[1:] for l in body if l[:1] in (' ', '+'))
        assert s.count(old) == 1, f'context not found exactly once in {target}:\n{old}'
        s = s.replace(old, new)
    f.write_text(s)
    print(f'patched {target} ({len(hunks)} hunk{"s" if len(hunks) > 1 else ""})')
