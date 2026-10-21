#!/bin/sh
# The English lines with Kokoro (local TTS through HyperFrames). The committed WAVs are these outputs.
# Needs a Python with kokoro-onnx and soundfile: uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
tts() { npx --yes hyperframes@0.8.181 tts "$1" -v "$2" -o "assets/voice/$3"; }
tts "For here, or to go?" bf_emma here-bf_emma.wav
tts "For here, please. I'd like a latte!" af_heart order-af_heart.wav
tts "Would you like it hot, or iced?" bf_emma hot-bf_emma.wav
