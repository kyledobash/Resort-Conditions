from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.core.text import LabelBase
from dotenv import load_dotenv
from app.utils import api
from app.config.config import resorts
from app.utils.geolocation import get_user_location
from app.screens.resort_screen import ResortScreen
from app.screens.main_menu_screen import MainMenuScreen

# Load environment variables from .env
load_dotenv()

class SkiResortWeatherApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # Register the custom font
        LabelBase.register(name='DrippyFont', fn_regular='app/fonts/Meltdownmf-OEyd.ttf')
        LabelBase.register(name='GoreFont', fn_regular='app/fonts/GorefontIi-2vAw.ttf')

        # Add the main menu screen
        main_menu_screen = Screen(name='Main Menu')
        main_menu_screen.add_widget(MainMenuScreen())
        self.screen_manager.add_widget(main_menu_screen)

        # Add resort-specific screens
        for location, resort_data in resorts.items():
            roadcam_img_src_urls = resort_data.get("roadcam_img_src_urls", [])
            resort_screen = Screen(name=location)
            twitter_api_user_id = resort_data.get("twitter_api_user_id")  # Get the twitter_api_user_id from the resort_data
            resort_screen.add_widget(ResortScreen(location, resort_data["twitter_handle"], twitter_api_user_id=twitter_api_user_id, roadcam_img_src_urls=roadcam_img_src_urls))
            self.screen_manager.add_widget(resort_screen)

        self.adjust_root_width(self.screen_manager, 800)  # Call the adjust_root_width method with the desired width

        # Set the title of the app window
        self.title = 'Resort Conditions'  # Change the title here

        return self.screen_manager
    
    def adjust_root_width(self, instance, width):
        instance.width = width

    def on_start(self):
        Window.maximize()
    

if __name__ == '__main__':
    user_lat_lng_string = get_user_location()
    app = SkiResortWeatherApp()
    app.run()
