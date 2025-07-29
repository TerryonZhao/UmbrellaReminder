from src.fetch_weather import fetch
from src.rain_process import rain_process
from src.send_email import send_rain_email
import datetime

def main():
    log_path = "/private/tmp/daily.log"
    with open(log_path, 'a') as f:
        f.write(f"Script triggered at {datetime.datetime.now()}\n")

        weather_data = fetch()
        if weather_data:
            try:
                rain_summary = rain_process(weather_data)
                print("Step 3: Send rain email...")
                if send_rain_email(rain_summary):
                    f.write("Email sent successfully.\n")
                else:
                    f.write("No rain expected today.\n")
            except Exception as e:
                print(f"Error processing rain data: {e}")
                f.write(f"Error: {e}\n")
        else:
            print("No weather data available.")
            f.write("No weather data available.\n")

        f.write("<<<<<<<<<<<< New Log >>>>>>>>>>>>\n")



if __name__ == "__main__":
    main()