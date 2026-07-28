#!/bin/bash

WALLPAPER_PATH="$1"

SET="tell application \"System Events\" to set picture of every desktop to POSIX file \"$WALLPAPER_PATH\""
osascript -e "$SET" &>/dev/null

for i in 1 2 3; do
  SPACES=$(yabai -m query --spaces 2>/dev/null | python3 -c "
import sys,json
data = json.load(sys.stdin)
for s in data:
    print(s['index'], s.get('has-focus', False))
" 2>/dev/null) && break
  sleep 1
done

[ -z "$SPACES" ] && exit 0

while IFS=' ' read -r IDX FOCUS; do
  [ "$FOCUS" = "True" ] && CURRENT="$IDX" || SPACE_LIST="$SPACE_LIST $IDX"
done <<< "$SPACES"

for SPACE in $SPACE_LIST; do
  yabai -m space --focus "$SPACE" 2>/dev/null
  osascript -e "$SET" &>/dev/null
done

[ -n "$CURRENT" ] && yabai -m space --focus "$CURRENT" 2>/dev/null
