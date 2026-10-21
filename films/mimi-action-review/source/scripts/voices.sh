#!/bin/sh
# The voice from outside the toilet door with Kokoro (local TTS through HyperFrames). The committed WAV is this output.
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
npx --yes hyperframes@0.8.181 tts "ちょっと！いつまで入ってんの！？" -v jf_alpha -o assets/voice/door-jf_alpha.wav
