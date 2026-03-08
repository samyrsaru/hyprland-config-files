#!/bin/bash
# Pause all media players
for player in $(playerctl --list-all); do
    playerctl --player="$player" pause 2>/dev/null
done