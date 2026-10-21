#!/bin/sh
# Rebuild the voice lines with Kokoro (local TTS through HyperFrames). The committed WAVs are these outputs.
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
npx --yes hyperframes@0.8.181 tts "Please leave the light on." -v af_heart -o assets/voice/model-af_heart.wav
npx --yes hyperframes@0.8.181 tts "Please leave the right on." -v af_heart -o assets/voice/rough-af_heart.wav
