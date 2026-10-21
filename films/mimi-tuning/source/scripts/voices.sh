#!/bin/sh
# Stand-in voices (Kokoro, local TTS through HyperFrames). Not Lanclo output: the film does not press「試聴音声を作る」.
# Before: Mimi's usual English voice (af_heart, her voice since films/mimi-think-sink). After: a British English voice (bf_isabella)
# standing in for a preview made with the request「イギリス英語っぽく」. The committed WAVs are this output.
# Needs a Python with kokoro-onnx and soundfile: uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
LINE="Shall we have a cup of tea?"
tts() { npx --yes hyperframes@0.8.181 tts "$LINE" -v "$1" -o "assets/voice/$2"; }
tts af_heart before-af_heart.wav
tts bf_isabella after-bf_isabella.wav
