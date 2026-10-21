#!/bin/sh
# The English lines with Kokoro (local TTS through HyperFrames). The committed WAVs are these outputs.
# The friend asks the same question twice (the same take is used for the opening and the rematch).
# The friend's English voice is af_bella (since films/mimi-action-add), Mimi's is af_heart (films/mimi-roleplay).
# Needs a Python with kokoro-onnx and soundfile: uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
tts() { npx --yes hyperframes@0.8.181 tts "$1" -v "$2" -s "${4:-1.0}" -o "assets/voice/$3"; }
tts "Dog person or cat person?" af_bella ask-af_bella.wav
tts "Dog person! They get me outside every day. How about you?" af_heart answer-af_heart.wav 1.1   # brisk: the confident rematch
