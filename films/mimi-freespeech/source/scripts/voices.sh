#!/bin/sh
# Kokoro (local TTS through HyperFrames). Mimi describes the café photo in halting English (af_heart, her English voice since
# mimi-shashin); the French friend says "three minutes is too short" in French (ff_siwis). Japanese lines are bubbles only.
# The committed WAVs are this output. Needs a Python with kokoro-onnx and soundfile:
#   uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
tts() { npx --yes hyperframes@0.8.181 tts "$1" -v "$2" -o "assets/voice/$3"; }
tts "Um... there are people... at a café. And, uh... a lamp. It's... nice?" af_heart describe-af_heart.wav
tts "Trois minutes, c'est trop court !" ff_siwis court-ff_siwis.wav
