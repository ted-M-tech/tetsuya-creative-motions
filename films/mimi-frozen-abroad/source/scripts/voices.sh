#!/bin/sh
# The staff lines with Kokoro (local TTS through HyperFrames); Mimi's replies are the owner's voice (own-voice.json, ownvoice.py).
# Needs a Python with kokoro-onnx and soundfile: uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
tts() { npx --yes hyperframes@0.8.181 tts "$1" -v "$2" -o "assets/voice/$3"; }
tts "May I see your passport?" bf_emma passport-bf_emma.wav
tts "Welcome. Do you have a reservation?" af_bella reservation-af_bella.wav
tts "Hello. Where are you going?" am_michael going-am_michael.wav
