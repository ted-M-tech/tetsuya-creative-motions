"""Apply a tiny capture-only patch: for each hunk, find its context lines (' ' and '-') exactly once and replace them with
the ' ' and '+' lines. Several files ('+++ b/<path>' sections) and several hunks ('@@') per file are allowed.
usage: python3 apply-patch.py film/app-capture/x.patch <app checkout>   (unified-diff look, but matched by text, not line numbers)
"""
import sys
from pathlib import Path

lines, root = Path(sys.argv[1]).read_text().splitlines(), Path(sys.argv[2])
target, hunks = None, []
for l in lines:
    if l.startswith('+++ b/'):
        target = l[6:]
    elif l.startswith('--- '):
        continue
    elif l.startswith('@@'):
        hunks.append((target, []))
    elif hunks:
        hunks[-1][1].append(l)
for target, body in hunks:
    f = root / target
    s = f.read_text()
    old = '\n'.join(l[1:] for l in body if l[:1] in (' ', '-'))
    new = '\n'.join(l[1:] for l in body if l[:1] in (' ', '+'))
    assert s.count(old) == 1, f'context not found exactly once in {target}'
    f.write_text(s.replace(old, new))
    print(f'patched {target}')
