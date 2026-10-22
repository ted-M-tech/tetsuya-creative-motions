#!/bin/sh
# The staff lines (Pippa) with Kokoro (local TTS through HyperFrames); Mimi's replies are the owner's voice (own-voice.json, ownvoice.py).
# Needs a Python with kokoro-onnx and soundfile: uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
tts() { npx --yes hyperframes@0.8.181 tts "$1" -v "$2" -s "$3" -o "assets/voice/$4"; }
# All three staff are Pippa the duck (kits/mimi-short/cast/), voice af_nicole; speeds keep each question ending on its freeze
tts "May I see your passport?" af_nicole 1 passport-af_nicole.wav
tts "Welcome. Do you have a reservation?" af_nicole 1.12 reservation-af_nicole.wav
tts "Hello. Where are you going?" af_nicole 1.15 going-af_nicole.wav
