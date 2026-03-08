#!/bin/bash

# Get weather data using wttr.in API
get_weather() {
    local response
    response=$(curl -s "http://wttr.in/?format=j1" 2>/dev/null)
    
    if [ $? -eq 0 ] && [ -n "$response" ]; then
        # Parse temperature and condition from JSON
        local temp=$(echo "$response" | jq -r '.current_condition[0].temp_C // "N/A"')
        local condition=$(echo "$response" | jq -r '.current_condition[0].weatherDesc[0].value // "Unknown"')
        
        # Choose appropriate weather icon
        local icon
        case $(echo "$condition" | tr '[:upper:]' '[:lower:]') in
            *clear*|*sunny*) icon="☀️" ;;
            *cloud*) icon="☁️" ;;
            *rain*|*drizzle*) icon="🌧️" ;;
            *snow*) icon="❄️" ;;
            *thunder*|*storm*) icon="⛈️" ;;
            *) icon="🌤️" ;;
        esac
        
        if [ "$temp" != "N/A" ]; then
            echo "{\"text\":\"$temp°C $icon\", \"tooltip\":\"$condition in your area\", \"class\":\"weather\"}"
        else
            echo "{\"text\":\"--°C 🌤️\", \"tooltip\":\"Weather data unavailable\", \"class\":\"weather-error\"}"
        fi
    else
        echo "{\"text\":\"--°C 🌤️\", \"tooltip\":\"Weather data unavailable\", \"class\":\"weather-error\"}"
    fi
}

get_weather