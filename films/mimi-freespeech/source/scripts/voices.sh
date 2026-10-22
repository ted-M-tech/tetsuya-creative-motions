#!/bin/sh
# Kokoro (local TTS through HyperFrames). Mimi's halting English is the owner's own voice now (own-voice.json,
# kits/mimi-short/scripts/ownvoice.py); the French friend says "three minutes is too short" in French (ff_siwis). Japanese lines are bubbles only.
# The committed WAVs are this output. Needs a Python with kokoro-onnx and soundfile:
#   uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
tts() { npx --yes hyperframes@0.8.181 tts "$1" -v "$2" -o "assets/voice/$3"; }
tts "Trois minutes, c'est trop court !" ff_siwis court-ff_siwis.wav
