import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from datetime import datetime
import os

error = "Error | "
info = "Info | "

def load_config():
    """Load configuration from config.json.

    :return dict: The configuration settings.
    """
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{error} Config file not found.")
        return None
    except json.JSONDecodeError:
        print(f"{error} Error decoding JSON from config.json.")
        return None
    
def get_weather(config):
    """Fetch weather information.

    :param dict config: The configuration settings.
    """
    lat = config["weather"]["lat"]
    lon = config["weather"]["lon"]
    api_key = config["weather"]["api_key"]
    exclude = config["weather"]["exclude"]
    lang = config["weather"].get("lang", "zh_cn")
    units = config["weather"]["units"]

    url = (
    f"https://api.openweathermap.org/data/3.0/onecall"
    f"?lat={lat}&lon={lon}"
    f"&exclude={exclude}"
    f"&units={units}"
    f"&lang={lang}"
    f"&appid={api_key}"
    )

    try:
        print(f"{info} Weather fetching...")
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"{error} Failed to fetch weather data.")
        return None

def main():
    """Main function to run the umbrella reminder."""
    print("Step 1: Load configuration")
    config = load_config()
    print("="*50)

    print("Step 2: Fetch weather data")
    weather_data = get_weather(config)
    print("="*50)
    print(weather_data)

if __name__ == "__main__":
    main()
