from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
import os
import logging
from dotenv import load_dotenv

# Import necessary functions from app.utils.api.py
from app.utils.api import fetch_hourly_forecast_data, fetch_weather_data, fetch_forecast_data, fetch_traffic_info, fetch_historical_current_data
from app.config.config import resorts

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env
load_dotenv()
ACCUWEATHER_API_KEY = os.getenv("ACCUWEATHER_API_KEY")

class CustomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 1  # Set size_hint_y to 1 so that the label will always be at least as tall as the text

class ResortScreen(BoxLayout):
    def __init__(self, location, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.location = location

        # Top row with resort name centered
        top_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height='50dp')
        resort_name_label = CustomLabel(text=f"[color=FFD700][b]{self.location}[/b][/color]", halign='center', valign='middle', markup=True)
        top_layout.add_widget(resort_name_label)
        self.add_widget(top_layout)

        # Scroll view to contain the data
        scroll_view = ScrollView(do_scroll=True)
        self.add_widget(scroll_view)

        # Main layout for all data sets
        main_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing='10dp')
        main_layout.bind(minimum_height=main_layout.setter('height'))
        scroll_view.add_widget(main_layout)

        # Traffic info container
        traffic_info_container = BoxLayout(orientation='vertical', size_hint_y=None, height='150dp')
        self.traffic_info_label = CustomLabel(text="Fetching traffic info...")
        traffic_info_container.add_widget(self.traffic_info_label)
        main_layout.add_widget(traffic_info_container)

        # Weather data container
        weather_data_container = BoxLayout(orientation='vertical', size_hint_y=None, height='150dp')
        self.weather_label = CustomLabel(text="Fetching weather data...")
        weather_data_container.add_widget(self.weather_label)
        main_layout.add_widget(weather_data_container)

        # Daily (forecast) data container
        forecast_data_container = BoxLayout(orientation='vertical', size_hint_y=None, height='150dp')
        self.forecast_label = CustomLabel(text="Fetching forecast data...", markup=True)
        forecast_data_container.add_widget(self.forecast_label)
        main_layout.add_widget(forecast_data_container)

        # Hourly forecast data container
        hourly_forecast_container = BoxLayout(orientation='vertical', size_hint_y=None, height='150dp')
        self.hourly_forecast_label = CustomLabel(text="Fetching hourly forecast data...")
        hourly_forecast_container.add_widget(self.hourly_forecast_label)
        main_layout.add_widget(hourly_forecast_container)

        # Historical data container
        historical_data_container = BoxLayout(orientation='vertical', size_hint_y=None, height='300dp')
        self.historical_data_label = CustomLabel(text="Fetching historical current data...")
        historical_data_container.add_widget(self.historical_data_label)
        main_layout.add_widget(historical_data_container)

        # Bottom row with "Back to Menu" button (as before)
        bottom_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height='50dp')
        back_button = Button(text="Back to Menu")
        back_button.bind(on_release=self.switch_to_main_menu)
        bottom_layout.add_widget(back_button)
        self.add_widget(bottom_layout)

    def fetch_data(self):
        # Fetch all the required data for the specific resort (traffic info, historical current data, weather data, forecast data)
        self.fetch_traffic_info()
        self.fetch_historical_current_data()
        self.fetch_weather_data()
        self.fetch_forecast_data()
        self.fetch_hourly_forecast_data()

    def fetch_hourly_forecast_data(self):
        # Use the API method to fetch hourly forecast data
        location_key = resorts[self.location]["accuweather_key"]
        hourly_forecast_data = fetch_hourly_forecast_data(location_key)
        self.hourly_forecast_label.text = hourly_forecast_data

    def fetch_traffic_info(self):
        # Use the API method to fetch traffic info
        resort_location = resorts[self.location]["location"]
        user_location = os.getenv("PHYSICAL_ADDRESS")  # Use the PHYSICAL_ADDRESS from config.py as the user's location
        traffic_info = fetch_traffic_info(user_location, resort_location)
        self.traffic_info_label.text = traffic_info

    def fetch_historical_current_data(self):
        # Use the API method to fetch historical current data
        location_key = resorts[self.location]["accuweather_key"]
        historical_current_data = fetch_historical_current_data(location_key)
        self.historical_data_label.text = historical_current_data
        self.historical_data_label.texture_update()  # Update the texture to calculate the new size
        self.historical_data_label.height = self.historical_data_label.texture_size[1]  # Update the height

    def fetch_weather_data(self):
        # Use the API method to fetch weather data
        location_key = resorts[self.location]["accuweather_key"]
        weather_data = fetch_weather_data(location_key)
        self.weather_label.text = weather_data

    def fetch_forecast_data(self):
        # Use the API method to fetch forecast data
        location_key = resorts[self.location]["accuweather_key"]
        forecast_data = fetch_forecast_data(location_key)
        self.forecast_label.text = forecast_data

    def switch_to_main_menu(self, instance):
        app = App.get_running_app()
        app.root.current = 'Main Menu'

class MainMenuScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Create buttons for each resort
        for location, _ in resorts.items():
            button = Button(text=location)
            button.bind(on_release=self.switch_to_resort_screen)
            button.resort_location = resorts[location]['location']
            self.add_widget(button)

    def switch_to_resort_screen(self, button):
        app = App.get_running_app()

        # Get the instance of ResortScreen from the ScreenManager
        resort_screen = app.root.get_screen(button.text).children[0]

        # Fetch the data for the specific resort screen
        resort_screen.fetch_data()

        # Switch to the specific resort screen
        app.root.current = button.text

class SkiResortWeatherApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # Add the main menu screen
        main_menu_screen = Screen(name='Main Menu')
        main_menu_screen.add_widget(MainMenuScreen())
        self.screen_manager.add_widget(main_menu_screen)

        # Add resort-specific screens
        for location, _ in resorts.items():
            resort_screen = Screen(name=location)
            resort_screen.add_widget(ResortScreen(location))
            self.screen_manager.add_widget(resort_screen)

        return self.screen_manager
    

if __name__ == '__main__':
    app = SkiResortWeatherApp()
    app.run()
