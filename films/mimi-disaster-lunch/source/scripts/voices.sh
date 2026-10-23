#!/bin/sh
# Coco's English line with Kokoro (local TTS through HyperFrames; her fixed voice af_bella). The committed WAV is this output.
# The learner/model lines are the owner's own voice (own-voice.json, not in Git).
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
tts() { npx --yes hyperframes@0.8.181 tts "$1" -v "$2" -o "assets/voice/$3"; }
tts "Launch? Roger! Three, two, one... liftoff!" af_bella coco-af_bella.wav
