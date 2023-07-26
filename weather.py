import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea, QMessageBox
from PyQt5.QtCore import Qt
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import pywifi
from pywifi import const

# Load environment variables from .env
load_dotenv()
WEATHERAPI_BASE_URL = "http://api.weatherapi.com/v1/forecast.json"

# Get the API key from the environment variable
WEATHERAPI_API_KEY = os.getenv("WEATHERAPI_API_KEY")

# Dictionary to map location names to their city names and coordinates
locations = {
    "Brighton": (40.5980, -111.5832),   # Brighton Ski Resort, Utah
    "Snowbird": (40.5812, -111.6557),   # Snowbird Ski Resort, Utah
    "Snowbasin": (41.2163, -111.8583)   # Snowbasin Ski Resort, Utah
}

class SkiResortWeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ski Resort Weather")
        self.setGeometry(100, 100, 800, 600)

        # Check Wi-Fi connection
        if not self.check_wifi_connection():
            self.show_wifi_message()
            sys.exit(0)

        self.init_ui()

    def check_wifi_connection(self):
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]

        if iface.status() in [const.IFACE_CONNECTED, const.IFACE_CONNECTING]:
            return True
        else:
            return False

    def show_wifi_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Wi-Fi Connection Required")
        msg.setText("You are not connected to Wi-Fi. Please connect to Wi-Fi and restart the application.")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def init_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)

        # Create a label for the title
        title_label = QLabel("Ski Resort Weather")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Create a scroll area to hold the weather data
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Create a widget to hold the weather data
        weather_widget = QWidget()
        scroll_area.setWidget(weather_widget)
        weather_layout = QVBoxLayout(weather_widget)

        self.result_labels = {}  # Dictionary to hold the weather data labels

        for location, coordinates in locations.items():
            latitude, longitude = coordinates
            label = QLabel("Fetching weather data...")
            weather_layout.addWidget(label)
            self.result_labels[location] = label

        self.setCentralWidget(main_widget)
        self.fetch_weather_data()

    def fetch_weather_data(self):
        for location, coordinates in locations.items():
            latitude, longitude = coordinates
            print(f"Fetching weather data for {location} (lat: {latitude}, lon: {longitude})")

            # Fetch current weather data from WeatherAPI using latitude and longitude
            current_params = {
                "key": WEATHERAPI_API_KEY,
                "q": f"{latitude},{longitude}",
                "units": "imperial"  # Request units in Fahrenheit
            }

            try:
                current_response = requests.get(WEATHERAPI_BASE_URL, params=current_params)
                current_data = current_response.json()

                if "current" in current_data:
                    current_temp = current_data["current"]["temp_f"]
                    current_condition = current_data["current"]["condition"]["text"]

                    location_data = f"{location}\n"
                    location_data += f"Current Temperature: {current_temp}°F\n"
                    location_data += f"Current Conditions: {current_condition}\n"

                    # Fetch hourly forecast from WeatherAPI using latitude and longitude
                    forecast_params = {
                        "key": WEATHERAPI_API_KEY,
                        "q": f"{latitude},{longitude}",
                        "units": "imperial",  # Request units in Fahrenheit
                        "hour": 2  # Show the next 2-hour forecast starting from the current hour
                    }

                    forecast_response = requests.get(WEATHERAPI_BASE_URL, params=forecast_params)
                    forecast_data = forecast_response.json()

                    if "forecast" in forecast_data and "forecastday" in forecast_data["forecast"]:
                        forecast_days = forecast_data["forecast"]["forecastday"]
                        unique_dates = set()  # Keep track of unique dates

                        for forecast in forecast_days:
                            date = forecast["date"]
                            if date not in unique_dates:
                                unique_dates.add(date)
                                location_data += f"\nDate: {date}\n"

                            for i in range(min(2, len(forecast["hour"]))):  # Show the next 2-hour forecasts (up to 2 if available)
                                hour = forecast["hour"][i]
                                time = datetime.strptime(hour["time"], "%Y-%m-%d %H:%M")
                                time_str = time.strftime("%H:%M")  # Remove the seconds from the time
                                temp = hour["temp_f"]
                                condition = hour["condition"]["text"]
                                location_data += f"{time_str}: {temp}°F, {condition}\n"

                        location_data += "-------------------------------------------\n"
                        self.result_labels[location].setText(location_data)
                    else:
                        self.result_labels[location].setText(f"Weather forecast data not available for {location}\n")
                else:
                    self.result_labels[location].setText(f"Weather data not available for {location}\n")
            except requests.exceptions.RequestException as e:
                self.result_labels[location].setText(f"Failed to fetch weather data for {location}\n")
                print(f"Error: {e}")

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SkiResortWeatherApp()
    window.show()
    sys.exit(app.exec_())
