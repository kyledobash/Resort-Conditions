from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from app.config.config import resorts

class MainMenuScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = '10dp'
        self.padding = '20dp'

        # Create label for the title
        title_label = Label(text='Resort Conditions', font_size='24sp', bold=True, size_hint=(1, 0.2))
        self.add_widget(title_label)

        # Create buttons for each resort
        for location, _ in resorts.items():
            button = Button(text=location, size_hint=(1, None), height='50dp')
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