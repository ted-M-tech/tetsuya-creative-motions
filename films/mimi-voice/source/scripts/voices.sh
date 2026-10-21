#!/bin/sh
# The native speaker the friend admires (Kokoro am_michael, local TTS through HyperFrames). The committed WAV is this output.
# The same sentence in her own AI voice is the owner's registered Lanclo voice: kits/mimi-short/scripts/ownvoice.py source/own-voice.json.
# Needs a Python with kokoro-onnx and soundfile: uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
LINE="Let's grab a coffee and catch up this weekend."
tts() { npx --yes hyperframes@0.8.181 tts "$LINE" -v "$1" -o "assets/voice/$2"; }
tts am_michael model-am_michael.wav
