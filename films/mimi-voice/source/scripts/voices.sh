#!/bin/sh
# The English model sentence twice with Kokoro (local TTS through HyperFrames): the native speaker the friend admires (am_michael)
# and the same sentence "in the friend's own voice" (af_bella, her English voice since films/mimi-action-add). The committed WAVs are this output.
# Needs a Python with kokoro-onnx and soundfile: uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
LINE="Let's grab a coffee and catch up this weekend."
tts() { npx --yes hyperframes@0.8.181 tts "$LINE" -v "$1" -o "assets/voice/$2"; }
tts am_michael model-am_michael.wav
tts af_bella friend-af_bella.wav
