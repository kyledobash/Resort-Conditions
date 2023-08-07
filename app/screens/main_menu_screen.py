from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from app.config.config import resorts

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