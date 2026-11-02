import json
import urllib.parse
import urllib.request


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_location(city_name):
    encoded_city = urllib.parse.quote(city_name)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1&language=en&format=json"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception:
        return None

    if not data.get("results"):
        return None

    result = data["results"][0]
    return {
        "name": result.get("name"),
        "country": result.get("country", "Unknown"),
        "latitude": result.get("latitude"),
        "longitude": result.get("longitude"),
    }


def get_weather(city_name):
    location = get_location(city_name)
    if not location:
        return None

    latitude = location["latitude"]
    longitude = location["longitude"]
    base_url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m"
        "&timezone=auto"
    )

    try:
        with urllib.request.urlopen(base_url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception:
        return None

    current = data.get("current", {})
    weather_code = current.get("weather_code")
    weather = WEATHER_CODES.get(weather_code, "Unknown condition")

    return {
        "city": location["name"],
        "country": location["country"],
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "wind_speed": current.get("wind_speed_10m"),
        "condition": weather,
    }


def weather_app():
    print("Weather App")
    city = input("Enter city name: ").strip()

    if not city:
        print("City name cannot be empty.")
        return

    weather = get_weather(city)

    if not weather:
        print(f"Could not find weather information for '{city}'.")
        return

    print(f"\nWeather for {weather['city']}, {weather['country']}")
    print(f"Condition: {weather['condition']}")
    print(f"Temperature: {weather['temperature']}°C")
    print(f"Humidity: {weather['humidity']}%")
    print(f"Wind Speed: {weather['wind_speed']} km/h")


if __name__ == "__main__":
    weather_app()