from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.app import App
import webbrowser

from app.widgets.label import CustomLabel
from app.utils import api
from app.utils.geolocation import get_user_location
from app.config.config import resorts


class ResortScreen(BoxLayout):
    def __init__(self, location, twitter_handle, roadcam_img_src_urls, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.location = location
        self.twitter_handle = twitter_handle
        self.roadcam_img_src_urls = roadcam_img_src_urls

        # # Set the background image using an Image widget
        # background_image = Image(source='app/images/matterhorn-vector.jpg', allow_stretch=True)
        # self.add_widget(background_image)

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        # Top row with resort name centered
        top_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height='50dp')
        resort_name_label = CustomLabel(
            text=f"[color=#808080][b]{self.location}[/b][/color]",
            halign='center',
            valign='bottom',
            markup=True,
            font_size='24sp',  # Increase the font size
        )
        top_layout.add_widget(resort_name_label)
        self.add_widget(top_layout)

        # Scroll view to contain the data
        scroll_view = ScrollView(do_scroll=True)
        self.add_widget(scroll_view)

        # Main layout for all data sets
        main_layout = GridLayout(cols=1, spacing='15dp', size_hint_y=None, padding='20dp')
        main_layout.bind(minimum_height=main_layout.setter('height'))
        scroll_view.add_widget(main_layout)

        # Resort data container
        resort_data_container = BoxLayout(orientation='vertical', size_hint_y=None, height='80dp')
        self.resort_data_label = CustomLabel(text="Fetching resort data...", font_size='18sp')
        resort_data_container.add_widget(self.resort_data_label)
        main_layout.add_widget(resort_data_container)

        # Traffic info container
        traffic_info_container = BoxLayout(orientation='vertical', size_hint_y=None, height='80dp')
        self.traffic_info_label = CustomLabel(text="Fetching traffic info...", font_size='18sp')
        traffic_info_container.add_widget(self.traffic_info_label)
        main_layout.add_widget(traffic_info_container)

        # Weather data container
        weather_data_container = BoxLayout(orientation='vertical', size_hint_y=None, height='150dp')
        self.weather_label = CustomLabel(text="Fetching weather data...", font_size='18sp')
        weather_data_container.add_widget(self.weather_label)
        main_layout.add_widget(weather_data_container)

        # Daily (forecast) data container
        forecast_data_container = BoxLayout(orientation='vertical', size_hint_y=None, height='50dp')
        self.forecast_label = CustomLabel(text="Fetching forecast data...", font_size='18sp', markup=True)
        forecast_data_container.add_widget(self.forecast_label)
        main_layout.add_widget(forecast_data_container)

        # Hourly forecast data container
        hourly_forecast_container = BoxLayout(orientation='vertical', size_hint_y=None, height='175dp')
        self.hourly_forecast_label = CustomLabel(text="Fetching hourly forecast data...", font_size='18sp')
        hourly_forecast_container.add_widget(self.hourly_forecast_label)
        main_layout.add_widget(hourly_forecast_container)

        # Historical data container
        historical_data_container = BoxLayout(orientation='vertical', size_hint_y=None, height='500dp')
        self.historical_data_label = CustomLabel(text="Fetching historical current data...", font_size='18sp')
        historical_data_container.add_widget(self.historical_data_label)
        main_layout.add_widget(historical_data_container)

        # Create the roadcam images container and label
        self.roadcam_images_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.roadcam_images_label = CustomLabel(text="Fetching Roadcam Images...", font_size='18sp')
        self.roadcam_images_container.add_widget(self.roadcam_images_label)
        main_layout.add_widget(self.roadcam_images_container)

        # Bind the width property of main_layout to adjust its width dynamically
        main_layout.bind(width=self.adjust_main_layout_width)
        bottom_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height='100dp', padding='20dp')

        back_button = Button(
            text="[color=#808080][b]Back to Menu[/b][/color]",
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size='18sp',
            markup=True
        )
        back_button.bind(on_release=self.switch_to_main_menu)
        bottom_layout.add_widget(back_button)

        twitter_button = Button(
            text=f"[color=#808080][b]{self.location} Twitter Feed[/b][/color]",
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size='18sp',
            markup=True
        )
        twitter_button.bind(on_release=self.open_twitter_embed)
        bottom_layout.add_widget(twitter_button)

        self.add_widget(bottom_layout)  # Add the bottom_layout to the ResortScreen widget

    def adjust_main_layout_width(self, instance, width):
        self.width = width

    def fetch_data(self):
        # Fetch all the required data for the specific resort (traffic info, historical current data, weather data, forecast data)
        self.fetch_traffic_info()
        self.fetch_historical_current_data()
        self.fetch_weather_data()
        self.fetch_forecast_data()
        self.fetch_hourly_forecast_data()
        self.fetch_resort_data()
        self.fetch_roadcam_images()

    def fetch_resort_data(self):
        # Use the API method to fetch resort data
        resort_slug = resorts[self.location]["resort_slug"]
        resort_data = api.fetch_resort_data(resort_slug)  # Renamed the variable to avoid conflict

        if resort_data is None:
            self.resort_data_label.text = f"Resort data not available for {self.location}"
            return

        # Format and update the resort data label
        lifts_status = resort_data.get('lifts', {}).get('status', {})
        lifts_open = [lift for lift, status in lifts_status.items() if status == 'open']
        lifts_open_str = ', '.join(lifts_open)
        conditions = resort_data.get('conditions', {})
        self.resort_data_label.text = f"Lifts Open: {lifts_open_str}\nConditions: Base {conditions.get('base', 0)} cm, Season Total {conditions.get('season', 0)} cm"


    def fetch_hourly_forecast_data(self):
        # Use the API method to fetch hourly forecast data
        location_key = resorts[self.location]["accuweather_key"]
        hourly_forecast_data = api.fetch_hourly_forecast_data(location_key)
        self.hourly_forecast_label.text = hourly_forecast_data

    def fetch_roadcam_images(self):
        # Use the API method to fetch roadcam images
        roadcam_img_src_urls = self.roadcam_img_src_urls
        roadcam_images = api.fetch_roadcam_images_from_api(roadcam_img_src_urls)

        if roadcam_images:
            num_images = len(roadcam_images)
            aspect_ratio = 16 / 9  # Desired aspect ratio of the images

            # Calculate the height based on the number of images and aspect ratio
            container_height = f"{num_images * 100 * aspect_ratio}dp"

            self.roadcam_images_container.height = container_height

            for img_widget in roadcam_images:
                img_widget.allow_stretch = True  # Set allow_stretch to True to stretch the image
                img_widget.keep_ratio = True  # Set keep_ratio to False to stretch the image
                self.roadcam_images_container.add_widget(img_widget)
            self.roadcam_images_container.remove_widget(self.roadcam_images_label)  # Remove the "Fetching Roadcam Images..." label
        else:
            self.roadcam_images_label.text = "No Roadcam Images Available"

    def fetch_traffic_info(self):
        # Use the API method to fetch traffic info
        resort_location = resorts[self.location]["location"]
        user_location = get_user_location()  # Use the PHYSICAL_ADDRESS from config.py as the user's location
        traffic_info = api.fetch_traffic_info(user_location, resort_location)
        self.traffic_info_label.text = traffic_info

    def fetch_historical_current_data(self):
        # Use the API method to fetch historical current data
        location_key = resorts[self.location]["accuweather_key"]
        historical_current_data = api.fetch_historical_current_data(location_key)
        self.historical_data_label.text = historical_current_data
        self.historical_data_label.texture_update()  # Update the texture to calculate the new size
        self.historical_data_label.height = self.historical_data_label.texture_size[1]  # Update the height

    def fetch_weather_data(self):
        # Use the API method to fetch weather data
        location_key = resorts[self.location]["accuweather_key"]
        weather_data = api.fetch_weather_data(location_key)
        self.weather_label.text = weather_data

    def fetch_forecast_data(self):
        # Use the API method to fetch forecast data
        location_key = resorts[self.location]["accuweather_key"]
        forecast_data = api.fetch_forecast_data(location_key)
        self.forecast_label.text = forecast_data

    def open_twitter_embed(self, *args):
        # Construct the Twitter URL based on the resort's Twitter handle
        twitter_url = f"https://twitter.com/{self.twitter_handle}?ref_src=twsrc%5Etfw"

        # Open the Twitter URL in the web browser
        webbrowser.open(twitter_url)

    def switch_to_main_menu(self, instance):
        app = App.get_running_app()
        app.root.current = 'Main Menu'