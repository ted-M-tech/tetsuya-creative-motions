#!/bin/sh
# The first imported phrase, heard on the review card, with Kokoro (local TTS through HyperFrames). af_bella is the friend's own English
# voice since films/mimi-action-add, standing in for "the model in your own voice" (the simulator take has no sound). The committed WAV is this output.
# Needs a Python with kokoro-onnx and soundfile: uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
npx --yes hyperframes@0.8.181 tts "Could I have the check?" -v af_bella -o assets/voice/phrase-af_bella.wav
