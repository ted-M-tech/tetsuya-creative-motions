#!/bin/sh
# The side cast's English lines with Kokoro (local TTS through HyperFrames). The committed WAVs are these outputs.
# Fixed voices (kits/mimi-short/cast/README.md): Bruno am_michael, Pippa af_nicole, Coco af_bella. Mimi and the lecturer have no voice.
# Needs a Python with kokoro-onnx and soundfile: uv venv ~/.local/share/hyperframes-tts && uv pip install --python ~/.local/share/hyperframes-tts kokoro-onnx soundfile
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
tts() { npx --yes hyperframes@0.8.181 tts "$1" -v "$2" -s "${4:-1.0}" -o "assets/voice/$3"; }
# The discussion (overlapping, fast)
tts "Honestly, I think remote work is better for everyone." am_michael b1.wav 1.15
tts "No way! You need people in the same room!" af_nicole p1.wav 1.15
tts "But what about the cost of living, though?" af_bella c1.wav 1.15
tts "Exactly, and the commute is just crazy." am_michael b2.wav 1.15
tts "Okay, okay, but listen to this!" af_nicole p2.wav 1.15
tts "Right? That's what I keep saying!" af_bella c2.wav 1.15
# Confident, with grammar mistakes
tts "Yesterday I go to the meeting, and I say my idea!" am_michael b3.wav 1.05
tts "I think this plan no good, because too much money!" af_bella c3.wav 1.05
# The canned self-introduction (Mimi's answers are bubbles only)
tts "Where are you from?" am_michael q1.wav 1.05
tts "What do you like?" af_nicole q2.wav 1.05
tts "Nice to meet you!" af_bella q3.wav 1.05
tts "Oh, why do you like traveling?" am_michael q4.wav 1.0
