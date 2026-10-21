#!/bin/sh
# The "own voice in every language" is a TTS stand-in, NOT a voice clone: Kokoro (local, through HyperFrames), one female voice
# per language where Kokoro has one. English af_bella (the friend's English voice since films/mimi-action-add); French ff_siwis,
# Spanish ef_dora, Mandarin zf_xiaobei, Italian if_sara, Brazilian Portuguese pf_dora, Hindi hf_alpha. Korean, German, Russian,
# Turkish, Japanese and the rest stay speech bubbles (Kokoro has no voice for them, and its Japanese garbles).
# The app sentences are the app's own AI-voice passage (native-ios/Lanclo/Resources/voice-readings.json, auditions.fr).
# Needs a Python with kokoro-onnx and soundfile: uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
tts() { npx --yes hyperframes@0.8.181 tts "$1" -v "$2" --lang "$3" -s "$4" -o "assets/voice/$5"; }
# the hook: one greeting per language, quick
tts "Hello!" af_bella en-us 1.15 hi-en.wav
tts "Bonjour !" ff_siwis fr-fr 1.25 hi-fr.wav
tts "¡Hola!" ef_dora es 1.15 hi-es.wav
tts "你好！" zf_xiaobei zh 1.2 hi-zh.wav
tts "Ciao!" if_sara it 1.2 hi-it.wav
tts "Olá!" pf_dora pt-br 1.15 hi-pt.wav
tts "नमस्ते!" hf_alpha hi 1.25 hi-hi.wav
# the app: the AI-voice passage after switching the study language
tts "Partons un peu plus tôt pour prendre le petit déjeuner dans notre café préféré." ff_siwis fr-fr 1.0 app-fr.wav
