"""The owner's own registered voice (Lanclo's "AI voice" of Tetsuya) for an episode's spoken lines.

usage: python3 kits/mimi-short/scripts/ownvoice.py films/<id>/source/own-voice.json [--force id ...]

own-voice.json lists the lines:
    {"lines": [{"id": "model", "text": "Could I have the check?", "accent": "us"},
               {"id": "rough", "text": "Could I have the check?", "accent": "learner"},
               {"id": "bonjour", "text": "Bonjour !", "accent": "native", "language": "French"}]}
accent: us | uk | learner | native (with language); "style" overrides the preset with your own direction.

Each line becomes assets/own-voice/<id>.wav next to own-voice.json (place it with Mix(voice_dir=SRC / 'assets/own-voice')).
The voice and its clips are the owner's biometric data: they stay out of Git (the repo is public) — keep the WAVs in the
episode's Drive folder, <prefix>_assets/own-voice/. Git keeps own-voice.receipt.json (text, style, hashes; no voice ID).
Only already generated lines are skipped, so a rerun costs nothing; --force regenerates the named lines.
Needs ~/.config/lanclo/gemini-dedicated.env (the dedicated Lanclo Gemini project, where the voice is registered).
Every call is a paid generation in the owner's voice: run it only for lines the owner asked for.
"""
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


def key():
    env = {}
    for line in (Path.home() / '.config/lanclo/gemini-dedicated.env').read_text().splitlines():
        p = shlex.split(line)
        if p and p[0] == 'export':
            p = p[1:]
        if len(p) == 1 and '=' in p[0]:
            k, v = p[0].split('=', 1)
            env[k] = v
    return env['GEMINI_API_KEY']


def voice_id(h):
    """The one replicated voice named VOICE_NAME in the project (the owner's)."""
    found, token = [], None
    for _ in range(50):
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


def speak(h, vid, text, style):
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


def main(spec, force=()):
    spec = Path(spec)
    out = spec.parent / 'assets/own-voice'
    out.mkdir(parents=True, exist_ok=True)
    rpath = spec.parent / 'own-voice.receipt.json'
    receipt = json.loads(rpath.read_text()) if rpath.exists() else {'model': MODEL, 'voice': VOICE_NAME, 'lines': {}}
    h = {'x-goog-api-key': key()}
    vid = None
    for line in json.loads(spec.read_text())['lines']:
        wav_path, style = out / f"{line['id']}.wav", style_of(line)
        old = receipt['lines'].get(line['id'], {})
        if wav_path.exists() and line['id'] not in force and old.get('text') == line['text'] and old.get('style') == style:
            continue
        vid = vid or voice_id(h)
        wav = speak(h, vid, line['text'], style)
        wav_path.write_bytes(wav)
        receipt['voiceIdentitySha256'] = hashlib.sha256(vid.encode()).hexdigest()
        receipt['lines'][line['id']] = {'text': line['text'], 'style': style, 'wavSha256': hashlib.sha256(wav).hexdigest(),
                                        'at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}
        rpath.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n')
        print('generated', wav_path)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args[0], args[args.index('--force') + 1:] if '--force' in args else ())
