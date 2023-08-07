from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
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
from app.screens.main_menu_screen import MainMenuScreen

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env
load_dotenv()

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

        self.adjust_root_width(self.screen_manager, 800)  # Call the adjust_root_width method with the desired width

        # Set the title of the app window
        self.title = 'Resort Conditions'  # Change the title here

        return self.screen_manager
    
    def adjust_root_width(self, instance, width):
        instance.width = width
    

if __name__ == '__main__':
    user_lat_lng_string = get_user_location()
    app = SkiResortWeatherApp()
    app.run()
