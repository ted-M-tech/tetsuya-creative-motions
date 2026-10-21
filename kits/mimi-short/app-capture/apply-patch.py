"""Apply a tiny capture-only patch: for each hunk, find its context lines (' ' and '-') exactly once and insert the '+' lines.
usage: python3 apply-patch.py film/app-capture/x.patch <app checkout>   (unified-diff look, but matched by text, not line numbers)
"""
import sys
from pathlib import Path

patch, root = Path(sys.argv[1]).read_text().splitlines(), Path(sys.argv[2])
target = next(l[6:] for l in patch if l.startswith('+++ b/'))
f = root / target
s = f.read_text()
body = patch[patch.index(next(l for l in patch if l.startswith('@@'))) + 1:]
old = '\n'.join(l[1:] for l in body if l[:1] in (' ', '-'))
new = '\n'.join(l[1:] for l in body if l[:1] in (' ', '+'))
assert s.count(old) == 1, f'context not found exactly once in {target}'
f.write_text(s.replace(old, new))
print(f'patched {target}')
