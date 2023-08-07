from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
import webbrowser
import os
import logging
from dotenv import load_dotenv

# Import necessary functions from app.utils.api.py
from app.utils import api

# Import Resort Dictionary
from app.config.config import resorts

# Import geolocation
from app.utils.geolocation import get_user_location

# Import Screens
from app.screens.resort_screen import ResortScreen

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env
load_dotenv()

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
        for location, resort_data in resorts.items():
            roadcam_img_src_urls = resort_data.get("roadcam_img_src_urls", [])
            resort_screen = Screen(name=location)
            resort_screen.add_widget(ResortScreen(location, resort_data["twitter_handle"], roadcam_img_src_urls=roadcam_img_src_urls))
            self.screen_manager.add_widget(resort_screen)

        return self.screen_manager
    

if __name__ == '__main__':
    user_lat_lng_string = get_user_location()
    app = SkiResortWeatherApp()
    app.run()
