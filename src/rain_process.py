import src.fetch_weather as fetch_weather
from datetime import datetime, timedelta, timezone

def convert_timestamp_to_datetime(timestamp, timezone_offset):
    """Convert Unix timestamp to datetime object with timezone.
    
    :param int timestamp: Unix timestamp
    :param int timezone_offset: Timezone offset in seconds
    :return datetime: Datetime object with timezone
    """
    utc_dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    timezone_delta = timedelta(seconds=timezone_offset)
    local_dt = utc_dt + timezone_delta
    return local_dt

def extract_today_data(weather_data) -> list[dict]:
    """Extract today's weather data from the hourly data.

    :param weather_data: Weather data from OpenWeatherMap API in json format
    :return: List of hourly data for today
    """
    timezone_offset = weather_data["timezone_offset"]
    today = datetime.now(timezone.utc) + timedelta(seconds=timezone_offset)
    today_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today.replace(hour=23, minute=59, second=59, microsecond=999999)

    hourly_data = weather_data.get("hourly", [])
    return [
        hour for hour in hourly_data
        if today_start <= convert_timestamp_to_datetime(hour["dt"], timezone_offset) <= today_end
    ]

def extract_keywords(hourly_data):
    """Extract keywords from hourly weather data."""
    description = hourly_data["weather"][0]["description"]
    # set default values
    pop = hourly_data.get("pop", 0.0)
    rain = hourly_data.get("rain", {}).get("1h", 0.0)
    return description, pop, rain

def will_rain(description, pop, rain) -> str:
    """Determine if it will rain based on description, probability of precipitation, and rain amount.

    :param str description: Weather description
    :param float pop: Probability of precipitation (0-1)
    :param float rain: Rain amount in the last hour (mm)
    :return str:
        - "no": No rain
        - "light": Light rain
        - "moderate": Moderate rain
        - "heavy": Heavy rain
    """
    desc_keywords = ["rain", "雨", "雷"]
    if any(keyword in description.lower() for keyword in desc_keywords):
        if rain >= 4:
            return "heavy"
        if rain >= 1.5 or pop > 0.6:
            return "moderate"
        return "light"
    return "no"

def rain_process(weather_data) -> dict:
    """See if it will rain today based on the weather data and return the hours it will rain.

    :param weather_data: Weather data from OpenWeatherMap API in json format
    :return: dict: Rain summary with hours it will rain
    """
    timezone_offset = weather_data["timezone_offset"]
    today_hourly_data = extract_today_data(weather_data)
    max_rain_amount = 0.0
    rain_info = {
        "has_rain": False,
        "rain_hours": [],
        "rain_levels": {
            "light": [],
            "moderate": [],
            "heavy": []
        },
        "peak_rain": {
            "time": None,
            "level": "no",
            "amount": 0.0
        },
        "summary": {
            "total_hours": 0,
            "worst_level": "no"
        }
    }

    for hour in today_hourly_data:
        desc, pop, rain = extract_keywords(hour)
        level = will_rain(desc, pop, rain)
        if level != "no":
            timestamp = hour["dt"]
            local_dt = convert_timestamp_to_datetime(timestamp, timezone_offset)
            time_str = local_dt.strftime("%H:%M")

            rain_info["has_rain"] = True
            rain_info["rain_hours"].append(time_str)
            rain_info["rain_levels"][level].append(time_str)
            rain_info["summary"]["total_hours"] += 1

            if rain > max_rain_amount:
                max_rain_amount = rain
                rain_info["peak_rain"] = {
                    "time": time_str,
                    "level": level,
                    "amount": rain
                }

    if rain_info["rain_levels"]["heavy"]:
        rain_info["summary"]["worst_level"] = "heavy"
    elif rain_info["rain_levels"]["moderate"]:
        rain_info["summary"]["worst_level"] = "moderate"
    elif rain_info["rain_levels"]["light"]:
        rain_info["summary"]["worst_level"] = "light"

    return rain_info

if __name__ == "__main__":
    weather_data = fetch_weather.fetch()
    if weather_data:
        rain_summary = rain_process(weather_data)
        print(rain_summary)
    else:
        print("No weather data available.")
