#!/bin/bash

# Get capacity directly from system since Waybar isn't passing it properly
capacity=$(cat /sys/class/power_supply/BAT*/capacity 2>/dev/null | head -1)

# Debug logging
echo "$(date): Script called with capacity $capacity" >> /tmp/battery-notify.log
status_file="/tmp/waybar_battery_status"
current_status=$(cat /sys/class/power_supply/BAT*/status 2>/dev/null | head -1)

# Read previous status
prev_status=""
if [ -f "$status_file" ]; then
    prev_status=$(cat "$status_file")
fi

# Write current status
echo "$current_status" > "$status_file"

# Check if charger was just unplugged and battery is low
if [ "$prev_status" = "Charging" ] && [ "$current_status" = "Discharging" ] && [ "$capacity" -le 30 ]; then
    notify-send "Charger Unplugged!" "Battery at ${capacity}% - running on battery power" -u normal
fi

# Regular low battery notifications (only when not charging)
if [ "$current_status" != "Charging" ]; then
    if [ "$capacity" -le 5 ]; then
        notify-send "CRITICAL BATTERY!" "Battery critically low at ${capacity}%" -u critical -t 0
    elif [ "$capacity" -le 10 ]; then
        notify-send "Critical Battery" "Battery at ${capacity}% - plug in charger!" -u critical
    elif [ "$capacity" -le 20 ]; then
        notify-send "Low Battery" "Battery at ${capacity}%" -u normal
    fi
fi