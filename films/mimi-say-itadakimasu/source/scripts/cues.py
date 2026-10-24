"""077 cue sheet: one place for the times. Writes cues.json (read by scripts/mix.py) and hf/index.html from scripts/index.tpl.html.

usage: python3 films/mimi-say-itadakimasu/source/scripts/cues.py
App times come from scripts/app_track.sh (the take cut onto the film's clock); tap positions are % of the phone screen.
"""
import json
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
APP = 4.3
C = dict(
    LINE=1.55, PUZZLED=3.05, AMI=3.2, APP=APP,
    TYPE=[APP + 0.53, APP + 1.88],      # the two typed chunks (scripts/app_track.sh)
    CREATE=APP + 2.446, RESULT=APP + 3.246, SAVE=APP + 5.446, SAVED=APP + 5.996,
    CARD=APP + 6.646,
)
C.update(ROW1=C['CARD'] + 0.35, ROW2=C['CARD'] + 1.6)
C.update(PAYOFF=C['CARD'] + 3.3)
C.update(END=C['PAYOFF'] + 1.8)
C.update(DUR=C['END'] + 1.25)
POS = dict(CREATE_X='50%', CREATE_Y='50.5%', SAVE_X='50%', SAVE_Y='91%')

C = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in C.items()}
(SRC / 'cues.json').write_text(json.dumps(C, indent=1) + '\n')
d = lambda a, b: f'{C[b] - C[a]:.3f}'.rstrip('0').rstrip('.')
fill = {**{k: str(v) for k, v in C.items() if not isinstance(v, list)}, **POS,
        'LINE_DUR': f"{C['PUZZLED'] - 1.5:.2f}", 'AMI_DUR': d('AMI', 'APP'), 'APP_DUR': d('APP', 'CARD'),
        'CARD_DUR': d('CARD', 'PAYOFF'), 'PAY_DUR': d('PAYOFF', 'END'), 'END_DUR': d('END', 'DUR'),
        'PAYB': f"{C['PAYOFF'] + 0.1:.2f}", 'PAYB_DUR': f"{C['END'] - C['PAYOFF'] - 0.1:.2f}",
        'C1_DUR': d('PUZZLED', 'APP'), 'C2_DUR': d('APP', 'RESULT'), 'C3_DUR': d('RESULT', 'SAVE'), 'C4_DUR': d('SAVE', 'CARD'),
        'S2_DUR': f"{C['PUZZLED'] - 1.5:.2f}"}
html = (SRC / 'scripts/index.tpl.html').read_text()
for k in sorted(fill, key=len, reverse=True):
    html = html.replace(f'__{k}__', fill[k])
assert '__' not in html.replace('window.__timelines', ''), [l for l in html.splitlines() if '__' in l and '__timelines' not in l]
(SRC / 'hf/index.html').write_text(html)
print(json.dumps(C))
