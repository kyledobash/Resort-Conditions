from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from app.config.config import resorts
import webbrowser

class MainMenuScreen(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create label for the title
        title_label = Label(
            text='Resort Conditions',
            color='#1E90FF',
            font_size='24sp',
            bold=True,
            size_hint=(None, None)
        )
        title_label.pos_hint = {'center_x': 0.5, 'top': 0.65}
        self.add_widget(title_label)

        # Create buttons for each resort
        button_width = '500dp'
        button_height = '80dp'
        for index, (location, _) in enumerate(resorts.items()):
            button = Button(
                text="[color=#1E90FF][b]" + location + "[/b][/color]",
                size_hint=(None, None),
                size=(button_width, button_height),
                markup=True,
                background_color=(0.3, 0.3, 0.3, 1),
                color=(1, 1, 1, 1),
                font_size='18sp',
                bold=True
            )
            button.bind(on_release=self.switch_to_resort_screen)
            button.resort_location = resorts[location]['location']
            button.pos_hint = {'center_x': 0.5, 'center_y': 0.5 - index * 0.102}
            self.add_widget(button)

         # Add watermark label
        watermark_label = Label(
            text='[ref=github]github.com/kyledobash[/ref]',
            color='#808080',
            font_size='12sp',
            bold=False,
            size_hint=(None, None),
            pos_hint={'right': .965, 'y': .020},
            markup=True
        )
        watermark_label.bind(on_ref_press=self.open_link)
        self.add_widget(watermark_label)

        # Add MIT license watermark label
        license_label = Label(
            text='[ref=license]© MIT License[/ref]',
            color='#808080',
            font_size='10sp',
            bold=False,
            size_hint=(None, None),
            pos_hint={'right': .965, 'bottom': 1},
            markup=True
        )
        license_label.bind(on_ref_press=self.open_link)
        self.add_widget(license_label)

    def open_link(self, instance, ref):
        if ref == 'github':
            webbrowser.open('https://github.com/kyledobash')
        elif ref == 'license':
            webbrowser.open('https://mit-license.org/')
            pass

    def switch_to_resort_screen(self, button):
        app = App.get_running_app()

        # Get the instance of ResortScreen from the ScreenManager using the location without markup
        resort_screen = app.root.get_screen(button.text.replace('[color=#1E90FF][b]', '').replace('[/b][/color]', '')).children[0]

        # Fetch the data for the specific resort screen
        resort_screen.fetch_data()

        # Switch to the specific resort screen
        app.root.current = button.text.replace('[color=#1E90FF][b]', '').replace('[/b][/color]', '')