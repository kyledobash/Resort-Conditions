from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
import requests
from dotenv import load_dotenv
import tweepy
import os

# Load environment variables from .env
load_dotenv()
ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")

# Read the Twitter API credentials from the .env file
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Set up tweepy with your Twitter API credentials
auth = tweepy.OAuth1BearerHandler(TWITTER_BEARER_TOKEN, resource_owner_key=TWITTER_ACCESS_TOKEN, resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Dictionary to map location names to their AccuWeather location keys
locations = {
    "Brighton": "1-28182_1_poi_al",   # Brighton Ski Resort, Utah
    "Snowbird": "101347_poi",         # Snowbird Ski Resort, Utah
    "Snowbasin": "101346_poi"         # Snowbasin Ski Resort, Utah
}

class ResortScreen(BoxLayout):
    def __init__(self, location, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.location = location

        # Top row with resort name centered
        top_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        resort_name_label = Label(text=f"[color=FFD700][b]{self.location}[/b][/color]", halign='center', valign='middle', markup=True)
        top_layout.add_widget(resort_name_label)
        self.add_widget(top_layout)

        # Two-column layout using GridLayout
        grid_layout = GridLayout(cols=2, size_hint=(1, 0.8))
        self.add_widget(grid_layout)

        # Left column for weather data and forecast
        left_layout = BoxLayout(orientation='vertical')
        self.weather_label = Label(text="Fetching weather data...")
        left_layout.add_widget(self.weather_label)
        self.forecast_label = Label(text="Fetching forecast data...", markup=True)
        left_layout.add_widget(self.forecast_label)
        grid_layout.add_widget(left_layout)

        # Right column (empty for now)
        grid_layout.add_widget(BoxLayout())

        # Fetch both current conditions and 1-day daily forecasts
        self.fetch_weather_data()
        self.fetch_forecast_data()

        # Bottom row with "Back to Menu" button
        bottom_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        back_button = Button(text="Back to Menu")
        back_button.bind(on_release=self.switch_to_main_menu)
        bottom_layout.add_widget(back_button)
        self.add_widget(bottom_layout)

    def fetch_weather_data(self):
        location_key = locations[self.location]

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

                # Extract weather data
                current_temp = weather_data.get("Temperature", {}).get("Imperial", {}).get("Value")
                current_condition = weather_data.get("WeatherText")
                humidity = weather_data.get("RelativeHumidity")
                wind_speed = weather_data.get("Wind", {}).get("Speed", {}).get("Imperial", {}).get("Value")
                visibility = weather_data.get("Visibility", {}).get("Imperial", {}).get("Value")

                # Format current weather data for display
                location_data = f"Current Conditions\n"
                location_data += f"Temperature: {current_temp}°F\n"
                location_data += f"Conditions: {current_condition}\n"
                location_data += f"Humidity: {humidity}%\n"
                location_data += f"Wind Speed: {wind_speed} mph\n"
                location_data += f"Visibility: {visibility} miles\n"

                # Display the current weather data
                self.weather_label.text = location_data
            else:
                self.weather_label.text = f"Weather data not available for {self.location}\n"
        except requests.exceptions.RequestException as e:
            self.weather_label.text = f"Failed to fetch weather data for {self.location}\n"
            print(f"Error: {e}")

    def fetch_forecast_data(self):
        location_key = locations[self.location]

        # Fetch 1-day daily forecasts from AccuWeather using location key
        forecast_params = {
            "apikey": ACCUWEATHER_API_KEY,
            "details": True
        }

        try:
            forecast_response = requests.get(f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}", params=forecast_params)
            forecast_data = forecast_response.json()

            if "DailyForecasts" in forecast_data:
                forecast_data = forecast_data["DailyForecasts"][0]

                # Extract forecast data
                forecast_temp_min = forecast_data.get("Temperature", {}).get("Minimum", {}).get("Value")
                forecast_temp_max = forecast_data.get("Temperature", {}).get("Maximum", {}).get("Value")
                forecast_day_condition = forecast_data.get("Day", {}).get("IconPhrase")

                # Format forecast data for display
                forecast_data = f"Forecast for {forecast_data['Date']}\n"
                forecast_data += f"Temperature Min: {forecast_temp_min}°F\n"
                forecast_data += f"Temperature Max: {forecast_temp_max}°F\n"
                forecast_data += f"Day Conditions: {forecast_day_condition}\n"

                # Display the forecast data
                self.forecast_label.text = forecast_data
            else:
                print(f"Forecast data not available for {self.location}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast data for {self.location}: {e}")

    def switch_to_main_menu(self, button):
        app = App.get_running_app()
        app.root.current = 'Main Menu'

class MainMenuScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Create buttons for each resort
        for location, _ in locations.items():
            button = Button(text=location)
            button.bind(on_release=self.switch_to_resort_screen)
            self.add_widget(button)

    def switch_to_resort_screen(self, button):
        app = App.get_running_app()
        app.root.current = button.text

class SkiResortWeatherApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # Add the main menu screen
        main_menu_screen = Screen(name='Main Menu')
        main_menu_screen.add_widget(MainMenuScreen())
        self.screen_manager.add_widget(main_menu_screen)

        # Add resort-specific screens
        for location, _ in locations.items():
            resort_screen = Screen(name=location)
            resort_screen.add_widget(ResortScreen(location))
            self.screen_manager.add_widget(resort_screen)

        return self.screen_manager

if __name__ == '__main__':
    app = SkiResortWeatherApp()
    app.run()
