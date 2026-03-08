#!/bin/bash

TIMER_FILE="/tmp/waybar_timer"
POMODORO_FILE="/tmp/waybar_pomodoro"

get_timer_info() {
    if [[ -f "$TIMER_FILE" ]]; then
        local start_time=$(cat "$TIMER_FILE")
        local current_time=$(date +%s)
        local elapsed=$((current_time - start_time))
        
        local hours=$((elapsed / 3600))
        local minutes=$(((elapsed % 3600) / 60))
        local seconds=$((elapsed % 60))
        
        if [[ -f "$POMODORO_FILE" ]]; then
            local pomodoro_info=$(cat "$POMODORO_FILE")
            local session_type=$(echo "$pomodoro_info" | cut -d: -f1)
            local target_duration=$(echo "$pomodoro_info" | cut -d: -f2)
            local remaining=$((target_duration - elapsed))
            
            if [[ $remaining -le 0 ]]; then
                # Timer finished
                rm -f "$TIMER_FILE" "$POMODORO_FILE"
                notify-send "Pomodoro" "$session_type session finished!" --urgency=normal
                # Play notification sound
                paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null || \
                paplay /usr/share/sounds/alsa/Front_Right.wav 2>/dev/null || \
                aplay /usr/share/sounds/alsa/Front_Right.wav 2>/dev/null || \
                speaker-test -t sine -f 1000 -l 1 -s 1 2>/dev/null &
                echo '{"text": "󰔛", "tooltip": "Click to start timer"}'
                return
            fi
            
            local rem_hours=$((remaining / 3600))
            local rem_minutes=$(((remaining % 3600) / 60))
            local rem_seconds=$((remaining % 60))
            
            local icon=""
            case "$session_type" in
                "Work") icon="󰔛" ;;
                "Short Break") icon="󰖚" ;;
                "Long Break") icon="󰖚" ;;
            esac
            
            if [[ $rem_hours -gt 0 ]]; then
                printf '{"text": "%s %02d:%02d:%02d ⏹", "tooltip": "%s session - %02d:%02d:%02d remaining (Click to stop)"}' \
                    "$icon" $rem_hours $rem_minutes $rem_seconds "$session_type" $rem_hours $rem_minutes $rem_seconds
            else
                printf '{"text": "%s %02d:%02d ⏹", "tooltip": "%s session - %02d:%02d remaining (Click to stop)"}' \
                    "$icon" $rem_minutes $rem_seconds "$session_type" $rem_minutes $rem_seconds
            fi
        else
            if [[ $hours -gt 0 ]]; then
                printf '{"text": "󰔛 %02d:%02d:%02d ⏹", "tooltip": "Timer running - Click to stop"}' \
                    $hours $minutes $seconds
            else
                printf '{"text": "󰔛 %02d:%02d ⏹", "tooltip": "Timer running - Click to stop"}' \
                    $minutes $seconds
            fi
        fi
    else
        echo '{"text": "󰔛", "tooltip": "Click to start timer"}'
    fi
}

start_timer() {
    echo $(date +%s) > "$TIMER_FILE"
    # Play start sound
    paplay /usr/share/sounds/freedesktop/stereo/service-login.oga 2>/dev/null || \
    paplay /usr/share/sounds/alsa/Front_Left.wav 2>/dev/null || \
    aplay /usr/share/sounds/alsa/Front_Left.wav 2>/dev/null &
}

stop_timer() {
    rm -f "$TIMER_FILE" "$POMODORO_FILE"
}

start_pomodoro() {
    local session_type="$1"
    local duration="$2"
    
    start_timer
    echo "$session_type:$duration" > "$POMODORO_FILE"
    
    # Convert duration to readable format
    local hours=$((duration / 3600))
    local minutes=$(((duration % 3600) / 60))
    local seconds=$((duration % 60))
    local time_str=""
    
    if [[ $hours -gt 0 ]]; then
        time_str="${hours}h"
    fi
    if [[ $minutes -gt 0 ]]; then
        time_str="${time_str}${minutes}m"
    fi
    if [[ $seconds -gt 0 ]]; then
        time_str="${time_str}${seconds}s"
    fi
    
    notify-send "Pomodoro" "Starting $session_type session ($time_str)" --urgency=low
}

case "$1" in
    "toggle")
        if [[ -f "$TIMER_FILE" ]]; then
            stop_timer
        else
            # Show rofi menu for timer options
            choice=$(echo -e "Free Timer\nPomodoro Work (25m)\nShort Break (5m)\nLong Break (15m)\nCustom Timer" | rofi -dmenu -p "Timer")
            case "$choice" in
                "Free Timer") start_timer ;;
                "Pomodoro Work (25m)") start_pomodoro "Work" 1500 ;;
                "Short Break (5m)") start_pomodoro "Short Break" 300 ;;
                "Long Break (15m)") start_pomodoro "Long Break" 900 ;;
                "Custom Timer") 
                    # Get custom duration from user
                    duration=$(rofi -dmenu -p "Enter time (e.g. 30s, 5m, 1h30m):" -filter "")
                    if [[ -n "$duration" ]]; then
                        # Parse duration
                        total_seconds=0
                        
                        # Extract hours
                        if [[ "$duration" =~ ([0-9]+)h ]]; then
                            hours=${BASH_REMATCH[1]}
                            total_seconds=$((total_seconds + hours * 3600))
                        fi
                        
                        # Extract minutes
                        if [[ "$duration" =~ ([0-9]+)m ]]; then
                            minutes=${BASH_REMATCH[1]}
                            total_seconds=$((total_seconds + minutes * 60))
                        fi
                        
                        # Extract seconds
                        if [[ "$duration" =~ ([0-9]+)s ]]; then
                            seconds=${BASH_REMATCH[1]}
                            total_seconds=$((total_seconds + seconds))
                        fi
                        
                        # If just a number, assume minutes
                        if [[ "$duration" =~ ^[0-9]+$ ]]; then
                            total_seconds=$((duration * 60))
                        fi
                        
                        if [[ $total_seconds -gt 0 ]]; then
                            start_pomodoro "Custom ($duration)" $total_seconds
                        fi
                    fi
                    ;;
            esac
        fi
        ;;
    *)
        get_timer_info
        ;;
esac