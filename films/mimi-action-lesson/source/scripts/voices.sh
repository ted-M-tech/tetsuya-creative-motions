#!/bin/sh
# Mimi's mother, off-screen, with Kokoro (local TTS through HyperFrames). The committed WAV is this output.
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
npx --yes hyperframes@0.8.181 tts "ミミー！早く起きなさーい！" -v jf_alpha -o assets/voice/mom-jf_alpha.wav
