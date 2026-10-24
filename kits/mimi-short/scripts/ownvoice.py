"""The owner's own registered voice (Lanclo's "AI voice" of Tetsuya) for an episode's spoken lines.

usage: python3 kits/mimi-short/scripts/ownvoice.py films/<id>/source/own-voice.json [--force id ...] [--max-calls N] [--dry-run]

own-voice.json lists the lines:
    {"lines": [{"id": "model", "text": "Could I have the check?", "accent": "us"},
               {"id": "rough", "text": "Could I have the check?", "accent": "learner"},
               {"id": "bonjour", "text": "Bonjour !", "accent": "native", "language": "French"}]}
accent: us | uk | learner | native (with language); "style" overrides the preset with your own direction.

Each line becomes assets/own-voice/<id>.wav next to own-voice.json (place it with Mix(voice_dir=SRC / 'assets/own-voice')).
The voice and its clips are the owner's biometric data: they stay out of Git (the repo is public) — keep the WAVs in the
episode's Drive folder, <prefix>_assets/own-voice/. Git keeps own-voice.receipt.json (text, style, hashes; no voice ID).
Only already generated lines are skipped, so a rerun costs nothing; --force regenerates the named lines.
Every call is a paid generation in the owner's voice: run it only for lines the owner asked for.

Credentials: only ~/.config/lanclo/gemini-internal.env (0600), the internal tools project lanclo-internal-tools, with
    GEMINI_API_KEY=...
    GEMINI_PROJECT_ID=lanclo-internal-tools
The owner creates it (Gemini capacity architecture, step O6). There is no fallback: without it the script stops. It refuses
any other project id (only lanclo-internal-tools passes), a symlink, a file readable by group/others, a file that is the
same file as another ~/.config/lanclo/*.env (hard link) and a key that appears in any GEMINI*/MVT_GEMINI* value of another
~/.config/lanclo/*.env (production, legacy, renamed or rotated copies). The SNS voice must be registered in the internal project as VOICE_NAME with a
fresh consent recording (owner step O7); this script only looks the voice up and never registers one.

Budget: a run makes at most --max-calls provider calls (default 20: one voice lookup plus one call per generated or
--force regenerated line). The plan is printed first; a larger plan is refused before any call. The plan is a lower bound: a paginated voice list
costs one call per page, and the run stops before the call that would exceed the budget. --dry-run validates the
config and prints the plan without calling the provider.
"""
import argparse
import base64
import datetime
import hashlib
import json
import shlex
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = 'https://generativelanguage.googleapis.com/v1beta'
MODEL = 'gemini-3.8-flash-tts'
VOICE_NAME = 'Lanclo private practice'
KEEP = 'Preserve the selected speaker’s vocal identity. Read the supplied text verbatim. Do not add any words or commentary.'
NATIVE = 'Use native vowel and consonant sounds, accurate word stress, smooth linking and natural sentence intonation.'
ACCENTS = {
    'us': 'Speak fluent General American English. ' + NATIVE + ' Reduced unstressed syllables, stress-timed rhythm, rhotic r, flapped t.',
    'uk': ('Speak fluent, clearly British English (Southern Standard British / RP), so a listener instantly hears it is British, '
           'not American. ' + NATIVE + ' Non-rhotic: drop the r after vowels ("car", "water"). Crisp, unflapped t ("better", '
           '"water" with a clear t). Long broad a in "can\'t", "bath", "ask". Rounded short o in "hot", "lot". '
           'British intonation with a gentle rise and fall.'),
    'learner': ('Speak English as a Japanese beginner who learned it from textbooks: katakana-like vowels added after consonants, '
                'r and l mixed up, flat syllable-by-syllable timing, every syllable equally stressed, a little hesitant. '
                'Keep it natural, not a caricature.'),
    'native': 'Speak fluent, natural {language} like a native speaker. ' + NATIVE,
}


INTERNAL_ENV = '.config/lanclo/gemini-internal.env'
PRODUCTION_ENV = '.config/lanclo/gemini-dedicated.env'
PRODUCTION_PROJECT = 'myvoicetutor-production-01'
DEFAULT_MAX_CALLS = 20


INTERNAL_PROJECT = 'lanclo-internal-tools'


def read_env(path, strict=True):
    """KEY=value lines (optional export, shell quoting, # comments). strict: a malformed line stops the run cleanly."""
    env = {}
    for n, line in enumerate(path.read_text().splitlines(), 1):
        try:
            p = shlex.split(line, comments=True)
        except ValueError:
            if strict:
                sys.exit(f'ownvoice: line {n} of ~/{INTERNAL_ENV} cannot be parsed (unbalanced quotes?); refusing.')
            continue
        if p and p[0] == 'export':
            p = p[1:]
        if len(p) == 1 and '=' in p[0]:
            k, v = p[0].split('=', 1)
            env[k] = v.strip()
    return env


def key():
    """The internal tools project key. Exits (never prints a key) unless the config is the internal project."""
    path = Path.home() / INTERNAL_ENV
    if not path.exists() and not path.is_symlink():
        sys.exit(f'ownvoice: ~/{INTERNAL_ENV} is missing. The owner creates it for project {INTERNAL_PROJECT} '
                 f'(Gemini capacity architecture, step O6) with GEMINI_API_KEY and GEMINI_PROJECT_ID={INTERNAL_PROJECT}, '
                 'mode 0600, then registers the SNS voice there with fresh consent (step O7). '
                 f'There is no fallback to ~/{PRODUCTION_ENV}.')
    if path.is_symlink() or not path.is_file():
        sys.exit(f'ownvoice: ~/{INTERNAL_ENV} must be a regular file, not a symlink; refusing.')
    st = path.stat()
    if st.st_mode & 0o077:
        sys.exit(f'ownvoice: ~/{INTERNAL_ENV} is readable by group/others (mode {st.st_mode & 0o777:o}); chmod 600 it.')
    env = read_env(path)
    project = env.get('GEMINI_PROJECT_ID', '')
    if project != INTERNAL_PROJECT:
        sys.exit(f'ownvoice: GEMINI_PROJECT_ID in ~/{INTERNAL_ENV} must be {INTERNAL_PROJECT} '
                 f'({"not set" if not project else "production project" if project == PRODUCTION_PROJECT else "other project"}); refusing.')
    k = env.get('GEMINI_API_KEY', '')
    if not k:
        sys.exit(f'ownvoice: GEMINI_API_KEY is not set in ~/{INTERNAL_ENV}.')
    # Every other Lanclo env file (production, legacy, renamed or rotated copies) must not share this file, key or project.
    for other in sorted(path.parent.glob('*.env')):
        if other.name == path.name:
            continue
        try:
            if other.samefile(path):
                sys.exit(f'ownvoice: ~/{INTERNAL_ENV} is the same file as {other.name}; refusing.')
            o = read_env(other, strict=False)
        except OSError:
            continue
        if any(v == k for n, v in o.items() if n.startswith(('GEMINI', 'MVT_GEMINI'))):
            sys.exit(f'ownvoice: the key in ~/{INTERNAL_ENV} is also in {other.name}; refusing.')
        if o.get('MVT_GOOGLE_PROJECT') == project:
            sys.exit(f'ownvoice: {other.name} declares MVT_GOOGLE_PROJECT={project} too; refusing.')
    return k, project


class Budget:
    """Counts provider calls; a call past the limit stops the run before it is sent."""

    def __init__(self, limit):
        self.limit, self.used = limit, 0

    def spend(self):
        if self.used >= self.limit:
            sys.exit(f'ownvoice: call budget of {self.limit} reached; stopping before another provider call.')
        self.used += 1


def voice_id(h, budget):
    """The one replicated voice named VOICE_NAME in the internal project (registered there by the owner, step O7)."""
    found, token = [], None
    for _ in range(50):
        budget.spend()
        q = {'page_size': '1000', **({'page_token': token} if token else {})}
        with urllib.request.urlopen(urllib.request.Request(f'{API}/voices?' + urllib.parse.urlencode(q), headers=h), timeout=30) as r:
            d = json.load(r)
        found += [v.get('id', v.get('name')) for v in d.get('voices', [])
                  if v.get('type') == 'replicated' and v.get('display_name') == VOICE_NAME]
        token = d.get('next_page_token') or d.get('nextPageToken')
        if not token:
            break
    assert len(found) == 1, f'expected one replicated voice "{VOICE_NAME}", found {len(found)}'
    return found[0]


def style_of(line):
    if 'style' in line:
        return line['style'] + ' ' + KEEP
    return ACCENTS[line.get('accent', 'us')].format(language=line.get('language', 'English')) + ' ' + KEEP


def speak(h, vid, text, style, budget):
    budget.spend()
    body = {'model': MODEL, 'store': False,
            'input': [{'type': 'user_input', 'content': [{'type': 'text', 'text': text,
                                                           'annotations': [{'type': 'speech_metadata', 'style': style}]}]}],
            'response_format': {'type': 'audio', 'mime_type': 'audio/wav'},
            'generation_config': {'speech_config': [{'voice': vid}]}}
    req = urllib.request.Request(f'{API}/interactions', data=json.dumps(body).encode(), method='POST',
                                 headers={**h, 'Content-Type': 'application/json', 'Api-Revision': '2026-05-20'})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    audio = [p['data'] for s in d.get('steps', []) if s.get('type') == 'model_output'
             for p in s.get('content', []) if p.get('type') == 'audio']
    assert audio, 'no audio returned'
    wav = base64.b64decode(audio[-1])
    assert wav[:4] == b'RIFF' and wav[8:12] == b'WAVE'
    return wav


def main(spec, force=(), max_calls=DEFAULT_MAX_CALLS, dry_run=False):
    spec = Path(spec)
    out = spec.parent / 'assets/own-voice'
    rpath = spec.parent / 'own-voice.receipt.json'
    receipt = json.loads(rpath.read_text()) if rpath.exists() else {'model': MODEL, 'voice': VOICE_NAME, 'lines': {}}
    todo, regen = [], 0
    for line in json.loads(spec.read_text())['lines']:
        wav_path, style = out / f"{line['id']}.wav", style_of(line)
        old = receipt['lines'].get(line['id'], {})
        if wav_path.exists() and line['id'] not in force and old.get('text') == line['text'] and old.get('style') == style:
            continue
        regen += wav_path.exists()
        todo.append((line, wav_path, style))
    k, project = key()
    planned = len(todo) + (1 if todo else 0)
    print(f'ownvoice: project {project}; {len(todo)} line(s) to generate ({regen} regeneration(s)) + '
          f'{1 if todo else 0} voice lookup = {planned} planned provider call(s); budget {max_calls}.')
    if planned > max_calls:
        sys.exit(f'ownvoice: {planned} planned calls exceed the budget of {max_calls}; '
                 'generate fewer lines or pass an explicit --max-calls.')
    if dry_run:
        print('ownvoice: dry run, config valid; no provider call made.')
        return
    if not todo:
        return
    out.mkdir(parents=True, exist_ok=True)
    h, budget, vid = {'x-goog-api-key': k}, Budget(max_calls), None
    for line, wav_path, style in todo:
        vid = vid or voice_id(h, budget)
        wav = speak(h, vid, line['text'], style, budget)
        wav_path.write_bytes(wav)
        receipt['voiceIdentitySha256'] = hashlib.sha256(vid.encode()).hexdigest()
        receipt['lines'][line['id']] = {'text': line['text'], 'style': style, 'wavSha256': hashlib.sha256(wav).hexdigest(),
                                        'at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}
        rpath.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n')
        print('generated', wav_path)
    print(f'ownvoice: {budget.used} provider call(s) made.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Owner-voice lines for an episode (internal Gemini project only).')
    ap.add_argument('spec', help='films/<id>/source/own-voice.json')
    ap.add_argument('--force', nargs='+', default=[], metavar='ID', help='regenerate these line ids')
    ap.add_argument('--max-calls', type=int, default=DEFAULT_MAX_CALLS, help=f'provider call budget (default {DEFAULT_MAX_CALLS})')
    ap.add_argument('--dry-run', action='store_true', help='validate config and print the plan; no provider call')
    a = ap.parse_args()
    main(a.spec, a.force, a.max_calls, a.dry_run)
