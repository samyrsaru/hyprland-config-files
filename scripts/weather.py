#!/usr/bin/env python3
import requests
import json
import sys
import os
from datetime import datetime

class WeatherApp:
    def __init__(self):
        pass
        
    def get_location(self):
        """Get location from IP geolocation"""
        try:
            response = requests.get("http://ipapi.co/json/", timeout=5)
            data = response.json()
            return data.get('city', 'Unknown'), data.get('country', 'Unknown')
        except:
            return "Unknown", "Unknown"
    
    def get_weather(self, city=None):
        """Fetch weather data"""
        if not city:
            city, country = self.get_location()
            location = f"{city}, {country}"
        else:
            location = city
            
        try:
            # Using wttr.in API which doesn't require API key
            response = requests.get(f"http://wttr.in/{location}?format=j1", timeout=10)
            return response.json(), location
        except Exception as e:
            return None, location
    
    def get_weather_icon(self, condition, is_day=True):
        """Return ASCII art for weather conditions"""
        icons = {
            'clear': {
                'day': [
                    "        \\         /        ",
                    "         \\       /         ",
                    "          \\     /          ",
                    "           .-.             ",
                    "  ――――――― (   ) ―――――――  ",
                    "           `-'             ",
                    "          /     \\          ",
                    "         /       \\         ",
                    "        /         \\        "
                ],
                'night': [
                    "                          ",
                    "         .-.              ",
                    "        (   )             ",
                    "       (_____)            ",
                    "                          ",
                    "                          ",
                    "                          ",
                    "                          ",
                    "                          "
                ]
            },
            'cloudy': [
                "                          ",
                "         .----.           ",
                "      .-(      )-.        ",
                "     (            )       ",
                "    (______________)      ",
                "                          ",
                "                          ",
                "                          ",
                "                          "
            ],
            'rain': [
                "         .----.           ",
                "      .-(      )-.        ",
                "     (            )       ",
                "    (______________)      ",
                "     ‚‚  ‚‚  ‚‚  ‚‚       ",
                "    ‚‚  ‚‚  ‚‚  ‚‚        ",
                "     ‚‚  ‚‚  ‚‚  ‚‚       ",
                "    ‚‚  ‚‚  ‚‚  ‚‚        ",
                "     ‚‚  ‚‚  ‚‚  ‚‚       "
            ],
            'snow': [
                "         .----.           ",
                "      .-(      )-.        ",
                "     (            )       ",
                "    (______________)      ",
                "     * * * * * * * *      ",
                "    * * * * * * * * *     ",
                "     * * * * * * * *      ",
                "    * * * * * * * * *     ",
                "     * * * * * * * *      "
            ],
            'thunderstorm': [
                "         .----.           ",
                "      .-(      )-.        ",
                "     (            )       ",
                "    (______________)      ",
                "     ‚‚ ⚡ ‚‚ ⚡ ‚‚       ",
                "    ‚‚  ‚‚  ‚‚  ‚‚        ",
                "     ‚‚ ⚡ ‚‚ ⚡ ‚‚       ",
                "    ‚‚  ‚‚  ‚‚  ‚‚        ",
                "     ‚‚  ‚‚  ‚‚  ‚‚       "
            ]
        }
        
        condition_lower = condition.lower()
        if 'clear' in condition_lower or 'sunny' in condition_lower:
            return icons['clear']['day' if is_day else 'night']
        elif 'cloud' in condition_lower:
            return icons['cloudy']
        elif 'rain' in condition_lower or 'drizzle' in condition_lower:
            return icons['rain']
        elif 'snow' in condition_lower:
            return icons['snow']
        elif 'thunder' in condition_lower or 'storm' in condition_lower:
            return icons['thunderstorm']
        else:
            return icons['cloudy']
    
    def get_clothing_advice(self, temp_c, condition, wind_speed):
        """Generate clothing advice based on weather conditions"""
        advice = []
        
        # Temperature-based advice
        if temp_c >= 25:
            advice.append("Light clothes (t-shirt, shorts)")
        elif temp_c >= 20:
            advice.append("Light shirt or blouse")
        elif temp_c >= 15:
            advice.append("Light sweater or cardigan")
        elif temp_c >= 10:
            advice.append("Jacket or hoodie")
        elif temp_c >= 0:
            advice.append("Warm coat and layers")
        else:
            advice.append("Heavy winter coat and layers")
        
        # Condition-based advice
        condition_lower = condition.lower()
        if 'rain' in condition_lower or 'drizzle' in condition_lower:
            advice.append("Bring an umbrella or raincoat")
        elif 'snow' in condition_lower:
            advice.append("Warm boots and waterproof clothing")
        elif 'thunder' in condition_lower or 'storm' in condition_lower:
            advice.append("Stay indoors if possible, or bring rain gear")
        
        # Wind-based advice
        if int(wind_speed) > 20:
            advice.append("Windbreaker recommended")
        
        return advice
    
    def display_weather(self, weather_data, location):
        """Display weather in ASCII format"""
        if not weather_data:
            print("❌ Unable to fetch weather data")
            return
            
        try:
            current = weather_data['current_condition'][0]
            temp_c = current['temp_C']
            temp_f = current['temp_F']
            humidity = current['humidity']
            condition = current['weatherDesc'][0]['value']
            feels_like_c = current['FeelsLikeC']
            wind_speed = current['windspeedKmph']
            wind_dir = current['winddir16Point']
            
            # Determine if it's day or night (simplified)
            hour = datetime.now().hour
            is_day = 6 <= hour <= 18
            
            weather_icon = self.get_weather_icon(condition, is_day)
            clothing_advice = self.get_clothing_advice(int(temp_c), condition, wind_speed)
            
            # Create the display
            print("\n" + "="*50)
            print(f"🌍 Weather for: {location}")
            print("="*50)
            
            # Display weather icon
            for line in weather_icon:
                print(f"    {line}")
            
            print(f"\n🌡️  Temperature: {temp_c}°C ({temp_f}°F)")
            print(f"🤔 Feels like: {feels_like_c}°C")
            print(f"☁️  Condition: {condition}")
            print(f"💧 Humidity: {humidity}%")
            print(f"💨 Wind: {wind_speed} km/h {wind_dir}")
            
            # Display clothing advice
            print(f"\n👕 How to dress:")
            for i, advice in enumerate(clothing_advice, 1):
                print(f"   {i}. {advice}")
            
            # Display hourly forecast
            print(f"\n⏰ Hourly forecast:")
            if 'weather' in weather_data and weather_data['weather']:
                today = weather_data['weather'][0]
                if 'hourly' in today:
                    current_hour = datetime.now().hour
                    hourly_data = today['hourly']
                    
                    # Filter future hours only
                    future_hours = []
                    max_rain_chance = 0
                    
                    for hour_data in hourly_data:
                        hour_time = int(hour_data['time']) // 100
                        if hour_time >= current_hour:
                            future_hours.append(hour_data)
                            rain_chance = int(hour_data['chanceofrain'])
                            if rain_chance > max_rain_chance:
                                max_rain_chance = rain_chance
                    
                    # Show future hours only
                    for hour_data in future_hours:
                        hour_time = int(hour_data['time']) // 100
                        temp = hour_data['tempC']
                        rain_chance = hour_data['chanceofrain']
                        
                        print(f"   {hour_time:02d}:00 - {temp}°C - Rain: {rain_chance}%")
                    
                    # Rain summary for remaining day
                    if max_rain_chance == 0:
                        print(f"\n🌞 No rain expected for the rest of today!")
                    elif max_rain_chance <= 20:
                        print(f"\n🌤️  Very low chance of rain today (max {max_rain_chance}%)")
                    elif max_rain_chance <= 50:
                        print(f"\n🌦️  Possible rain today (max {max_rain_chance}%)")
                    else:
                        print(f"\n🌧️  Rain likely today (max {max_rain_chance}%)")
            
            print("\n" + "="*50)
            
        except Exception as e:
            print(f"❌ Error parsing weather data: {e}")
    
    def run(self):
        """Main application loop"""
        os.system('clear')
        
        # Show loading animation
        print("🌐 Fetching weather data", end="", flush=True)
        for _ in range(3):
            print(".", end="", flush=True)
            import time
            time.sleep(0.5)
        
        # Check if city was provided as argument
        city = None
        if len(sys.argv) > 1:
            city = " ".join(sys.argv[1:])
            
        weather_data, location = self.get_weather(city)
        
        # Clear loading message and display weather
        os.system('clear')
        self.display_weather(weather_data, location)

if __name__ == "__main__":
    app = WeatherApp()
    app.run()