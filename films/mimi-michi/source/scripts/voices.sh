#!/bin/sh
# Rebuild the voice lines with Kokoro (local TTS through HyperFrames). The committed WAVs are these outputs.
# Needs a Python with kokoro-onnx and soundfile: uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
tts() { npx --yes hyperframes@0.8.181 tts "$1" -v "$2" -o "assets/voice/$3"; }
tts "Excuse me, how do I get to the station?" bm_george ask-bm_george.wav
tts "Thank you!" bm_george thanks-bm_george.wav
