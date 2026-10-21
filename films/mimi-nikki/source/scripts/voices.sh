#!/bin/sh
# Rebuild the voice lines with Kokoro (local TTS through HyperFrames). The committed WAVs are these outputs.
# Needs a Python with kokoro-onnx and soundfile: uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
npx --yes hyperframes@0.8.181 tts "Yesterday... I go to cafe." -v af_heart -o assets/voice/rough-af_heart.wav
npx --yes hyperframes@0.8.181 tts "Yesterday, I went to a cafe." -v af_heart -o assets/voice/model-af_heart.wav
