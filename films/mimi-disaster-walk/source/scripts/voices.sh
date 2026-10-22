#!/bin/sh
# Bruno's English lines with Kokoro (local TTS through HyperFrames, his fixed voice am_michael). The committed WAVs are this output.
# The learner/model lines are the owner's own voice (own-voice.json, not in Git).
set -e
cd "$(dirname "$0")/.."
export HYPERFRAMES_PYTHON=${HYPERFRAMES_PYTHON:-$HOME/.local/share/hyperframes-tts/bin/python}
tts() { npx --yes hyperframes@0.8.181 tts "$1" -v "$2" -o "assets/voice/$3"; }
tts "So, how did you get here today?" am_michael bruno-ask-am_michael.wav
tts "You worked?! On a Sunday?!" am_michael bruno-sunday-am_michael.wav
