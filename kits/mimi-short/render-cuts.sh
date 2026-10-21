#!/bin/sh
# Render both cuts of an episode: <name>-en.mp4 (English subtitles) and <name>.mp4 (Japanese only, <body class="no-subs">).
# usage: kits/mimi-short/render-cuts.sh films/<id>/source/hf <name>
set -e
hf=$1; name=$2; cd "$hf"
npx --yes hyperframes@0.8.181 render --output "../renders/$name-en.mp4" --fps 60
cp index.html /tmp/render-cuts.$$.html
sed -i '' 's|<body>|<body class="no-subs">|' index.html
npx --yes hyperframes@0.8.181 render --output "../renders/$name.mp4" --fps 60 || { cp /tmp/render-cuts.$$.html index.html; exit 1; }
cp /tmp/render-cuts.$$.html index.html; rm /tmp/render-cuts.$$.html
