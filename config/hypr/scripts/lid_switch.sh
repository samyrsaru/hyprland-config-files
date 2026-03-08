#!/bin/bash

LAPTOP_MONITOR="eDP-1"

# Check if an external monitor is connected
EXTERNAL_MONITOR_CONNECTED=$(hyprctl monitors | grep -v "eDP-1" | grep "Monitor")

if [[ "$1" == "close" ]]; then
  if [ -n "$EXTERNAL_MONITOR_CONNECTED" ]; then
    hyprctl keyword monitor "$LAPTOP_MONITOR,disable"
  fi
elif [[ "$1" == "open" ]]; then
  hyprctl keyword monitor "$LAPTOP_MONITOR, 2160x1440@60, 0x0, 1"
fi

