import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea, QMessageBox
from PyQt5.QtCore import Qt
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")

# Dictionary to map location names to their AccuWeather location keys
locations = {
    "Brighton": "1-28182_1_poi_al",   # Brighton Ski Resort, Utah
    "Snowbird": "101347_poi",         # Snowbird Ski Resort, Utah
    "Snowbasin": "101346_poi"         # Snowbasin Ski Resort, Utah
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
        # Replace this with your Wi-Fi connection check logic
        # For now, return True to simulate a successful Wi-Fi connection
        return True

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

        for location, location_key in locations.items():
            label = QLabel("Fetching weather data...")
            weather_layout.addWidget(label)
            self.result_labels[location] = label

        self.setCentralWidget(main_widget)
        self.fetch_weather_data()

    def fetch_weather_data(self):
        for location, location_key in locations.items():
            print(f"Fetching weather data for {location} (location key: {location_key})")

            # Fetch current weather data from AccuWeather using location key
            current_params = {
                "apikey": ACCUWEATHER_API_KEY,
                "details": True
            }

            try:
                current_response = requests.get(f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}", params=current_params)
                current_data = current_response.json()

                if current_data and isinstance(current_data, list):
                    weather_data = current_data[0]
                    current_temp = weather_data.get("Temperature", {}).get("Imperial", {}).get("Value")
                    current_condition = weather_data.get("WeatherText")

                    location_data = f"{location}\n"
                    location_data += f"Current Temperature: {current_temp}°F\n"
                    location_data += f"Current Conditions: {current_condition}\n"
                    self.result_labels[location].setText(location_data)
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
