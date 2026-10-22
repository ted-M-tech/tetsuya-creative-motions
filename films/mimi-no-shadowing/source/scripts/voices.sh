#!/bin/sh
# The native stranger's line with Kokoro (local TTS through HyperFrames); Mimi's lines and the model are the owner's voice
# (own-voice.json, kits/mimi-short/scripts/ownvoice.py).
# Needs a Python with kokoro-onnx and soundfile: uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
npx --yes hyperframes@0.8.181 tts "Please leave the light on." -v am_michael -s 1.15 -o assets/voice/light-am_michael.wav
