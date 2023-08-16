from kivy.app import App
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.uix.carousel import Carousel
import webbrowser
import datetime
import json

from app.config.config import resorts
from app.utils import api
from app.utils.geolocation import get_user_location
from app.widgets.label import CustomLabel


class ResortScreen(BoxLayout):
    def __init__(self, location, twitter_handle, twitter_api_user_id, roadcam_img_src_urls, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.location = location
        self.twitter_handle = twitter_handle
        self.twitter_api_user_id = twitter_api_user_id
        self.roadcam_img_src_urls = roadcam_img_src_urls

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        # Top row with resort name centered
        top_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height='65dp')
        resort_name_label = CustomLabel(
            text=f"[color=#808080][b]{self.location}[/b][/color]",
            halign='center',
            valign='top',
            markup=True,
            font_name='DrippyFont',
            font_size='60sp',  # Increase the font size
        )
        top_layout.add_widget(resort_name_label)
        self.add_widget(top_layout)

        # Scroll view to contain the data
        scroll_view = ScrollView(do_scroll=True)
        self.add_widget(scroll_view)

        # Main layout for all data sets
        main_layout = GridLayout(cols=3, size_hint_y=3, padding='10dp')
        main_layout.bind(minimum_height=main_layout.setter('height'))
        scroll_view.add_widget(main_layout)

        # Calculate the width of each column based on the screen width
        column_width = self.width / 3 - dp(40)  # Subtract the padding (20dp) on each side

        # Traffic info container
        traffic_info_container = BoxLayout(orientation='vertical')
        traffic_info_title = CustomLabel(
            text="[color=#FFD700][b]Traffic[/b][/color]",
            halign='center',
            markup=True,
            font_name='DrippyFont',
            font_size='30sp'
        )
        self.traffic_info_label = CustomLabel(text="Fetching traffic info...", font_size='18sp')
        traffic_info_container.add_widget(traffic_info_title)
        traffic_info_container.add_widget(self.traffic_info_label)
        main_layout.add_widget(traffic_info_container)

        # Twitter data container
        twitter_data_container = BoxLayout(orientation='vertical')
        twitter_data_title = CustomLabel(
            text="[color=#FFD700][b]Twitter[/b][/color]",
            halign='center',
            markup=True,
            font_name='DrippyFont',
            font_size='30sp',
        )
        self.twitter_data_label = CustomLabel(
            text="Fetching Tweets...",
            font_size='18sp',
        )
        twitter_data_container.add_widget(twitter_data_title)
        twitter_data_container.add_widget(self.twitter_data_label)
        main_layout.add_widget(twitter_data_container)

        # Create the roadcam images container and label
        self.roadcam_images_container = BoxLayout(orientation='vertical')
        roadcams_data_title = CustomLabel(
            text="[color=#FFD700][b]Roadcams[/b][/color]",
            halign='center',
            markup=True,
            font_name='DrippyFont',
            font_size='30sp',
        )
        self.roadcam_images_label = CustomLabel(text="Fetching Roadcam Images...", font_size='18sp')
        self.roadcam_images_container.add_widget(roadcams_data_title)
        self.roadcam_images_container.add_widget(self.roadcam_images_label)
        main_layout.add_widget(self.roadcam_images_container)

        # Weather data container
        weather_data_container = BoxLayout(orientation='vertical')
        weather_data_title = CustomLabel(
            text="[color=#FFD700][b]Weather[/b][/color]",
            halign='center',
            markup=True,
            font_name='DrippyFont',
            font_size='30sp',
        )
        self.weather_label = CustomLabel(text="Fetching weather data...", font_size='18sp')
        weather_data_container.add_widget(weather_data_title)
        weather_data_container.add_widget(self.weather_label)
        main_layout.add_widget(weather_data_container)

        # Daily (forecast) data container
        forecast_data_container = BoxLayout(orientation='vertical')
        forecast_data_title = CustomLabel(
            text="[color=#FFD700][b]Daily Temps[/b][/color]",
            halign='center',
            markup=True,
            font_name='DrippyFont',
            font_size='30sp',
        )
        self.forecast_label = CustomLabel(text="Fetching forecast data...", font_size='18sp', markup=True)
        forecast_data_container.add_widget(forecast_data_title)
        forecast_data_container.add_widget(self.forecast_label)
        main_layout.add_widget(forecast_data_container)

        # Hourly forecast data container
        hourly_forecast_container = BoxLayout(orientation='vertical')
        hourly_data_title = CustomLabel(
            text="[color=#FFD700][b]Hourly Forecast[/b][/color]",
            halign='center',
            markup=True,
            font_name='DrippyFont',
            font_size='30sp',
        )
        self.hourly_forecast_label = CustomLabel(text="Fetching hourly forecast data...", font_size='18sp')
        hourly_forecast_container.add_widget(hourly_data_title)
        hourly_forecast_container.add_widget(self.hourly_forecast_label)
        main_layout.add_widget(hourly_forecast_container)

        # Historical data container
        historical_data_container = BoxLayout(orientation='vertical')
        historical_data_title = CustomLabel(
            text="[color=#FFD700][b]Past Conditions[/b][/color]",
            halign='center',
            markup=True,
            font_name='DrippyFont',
            font_size='30sp',
        )
        self.historical_data_label = CustomLabel(text="Fetching historical current data...", font_size='18sp')
        historical_data_container.add_widget(historical_data_title)
        historical_data_container.add_widget(self.historical_data_label)
        main_layout.add_widget(historical_data_container)

        # Resort data container
        resort_data_container = BoxLayout(orientation='vertical')
        resort_data_title = CustomLabel(
            text="[color=#FFD700][b]Resort Data[/b][/color]",
            halign='center',
            markup=True,
            font_name='DrippyFont',
            font_size='30sp',
        )
        self.resort_data_label = CustomLabel(text="Fetching resort data...", font_size='18sp')
        resort_data_container.add_widget(resort_data_title)
        resort_data_container.add_widget(self.resort_data_label)
        main_layout.add_widget(resort_data_container)

        # Bind the width property of main_layout to adjust its width dynamically
        main_layout.bind(width=self.adjust_main_layout_width)
        bottom_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height='70dp', padding='5dp')

        back_button = Button(
            text="[color=#808080][b]Back to Menu[/b][/color]",
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size='39sp',
            font_name='DrippyFont',
            markup=True
        )
        back_button.bind(on_release=self.switch_to_main_menu)
        bottom_layout.add_widget(back_button)

        twitter_button = Button(
            text=f"[color=#808080][b]{self.location} Twitter Feed[/b][/color]",
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size='39sp',
            font_name='DrippyFont',
            markup=True
        )
        twitter_button.bind(on_release=self.open_twitter_embed)
        bottom_layout.add_widget(twitter_button)

        self.add_widget(bottom_layout)  # Add the bottom_layout to the ResortScreen widget

    def adjust_main_layout_width(self, instance, width):
        padding = dp(10)  # 5dp on each side
        self.width = width - padding

    def fetch_data(self):
        self.fetch_traffic_info()
        self.fetch_historical_current_data()
        self.fetch_weather_data()
        self.fetch_forecast_data()
        self.fetch_hourly_forecast_data()
        self.fetch_resort_data()
        self.fetch_roadcam_images()
        self.fetch_twitter_data()

    def adjust_container_height(self, label, container):
        label.texture_update()  # Update the texture to calculate the new size
        label.height = label.texture_size[1]  # Update the height
        container.height = label.height  # Update the container height to match the label height

    def fetch_resort_data(self):
        try:
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
        except Exception as e:
            print(f"Error fetching resort data: {e}")

    def fetch_hourly_forecast_data(self):
        try:
            # Use the API method to fetch hourly forecast data
            location_key = resorts[self.location]["accuweather_key"]
            hourly_forecast_data = api.fetch_hourly_forecast_data(location_key)
            self.hourly_forecast_label.text = hourly_forecast_data
        except Exception as e:
            print(f"Error fetching hourly forecast data: {e}")

    def fetch_roadcam_images(self):
        try:
            # Use the API method to fetch roadcam images
            roadcam_images = api.fetch_roadcam_images_from_api(self.roadcam_img_src_urls)

            if roadcam_images:
                carousel = Carousel(direction='right')

                for img_src_url in roadcam_images:
                    image = AsyncImage(source=img_src_url, allow_stretch=True, keep_ratio=True)
                    carousel.add_widget(image)
                    print(f"Added image with source: {img_src_url}")

                # Remove the "Fetching Roadcam Images..." label and add the populated Carousel
                self.roadcam_images_container.remove_widget(self.roadcam_images_label)
                self.roadcam_images_container.add_widget(carousel)

                # Add the previous and next arrow buttons
                previous_button = Button(
                    text="[color=#808080][b]Previous[/b][/color]",
                    background_color=(0.3, 0.3, 0.3, 1),
                    color=(1, 1, 1, 1),
                    font_size='30sp',
                    font_name='DrippyFont',
                    markup=True
                )
                previous_button.bind(on_release=lambda _: carousel.load_previous())
                    
                next_button = Button(
                    text="[color=#808080][b]Next[/b][/color]",
                    background_color=(0.3, 0.3, 0.3, 1),
                    color=(1, 1, 1, 1),
                    font_size='30sp',
                    font_name='DrippyFont',
                    markup=True
                )
                next_button.bind(on_release=lambda _: carousel.load_next())
                    
                # Add the buttons below the carousel
                bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
                bottom_layout.add_widget(previous_button)
                bottom_layout.add_widget(next_button)
                self.roadcam_images_container.add_widget(bottom_layout)               
            else:
                self.roadcam_images_label.text = "No Roadcam Images Available"
        except Exception as e:
            print(f"Error fetching roadcam images: {e}")

    def fetch_traffic_info(self):
        try:
            # Use the API method to fetch traffic info
            resort_location = resorts[self.location]["location"]
            user_location = get_user_location()  # Use the PHYSICAL_ADDRESS from config.py as the user's location
            traffic_info = api.fetch_traffic_info(user_location, resort_location)
            self.traffic_info_label.text = traffic_info
        except Exception as e:
            print(f"Error fetching traffic info: {e}")

    def fetch_historical_current_data(self):
        try:
            # Use the API method to fetch historical current data
            location_key = resorts[self.location]["accuweather_key"]
            historical_current_data = api.fetch_historical_current_data(location_key)
            self.historical_data_label.text = historical_current_data
            self.historical_data_label.texture_update()  # Update the texture to calculate the new size
            self.historical_data_label.height = self.historical_data_label.texture_size[1]  # Update the height
        except Exception as e:
            print(f"Error fetching historical current data: {e}")

    def fetch_weather_data(self):
        try:
            # Use the API method to fetch weather data
            location_key = resorts[self.location]["accuweather_key"]
            weather_data = api.fetch_weather_data(location_key)
            self.weather_label.text = weather_data
        except Exception as e:
            print(f"Error fetching weather data: {e}")

    def fetch_forecast_data(self):
        try:
            # Use the API method to fetch forecast data
            location_key = resorts[self.location]["accuweather_key"]
            forecast_data = api.fetch_forecast_data(location_key)
            self.forecast_label.text = forecast_data
        except Exception as e:
            print(f"Error fetching forecast data: {e}")

    def fetch_twitter_data(self):
        try:
            # Use the API method to fetch Twitter data
            twitter_data = api.fetch_user_tweets(self.twitter_handle)

            if twitter_data is None or len(twitter_data) == 0:
                self.twitter_data_label.text = f"No tweets available for {self.location}"
                return

            # Iterate over the first three tweets in the list
            tweet_texts = []
            for tweet in twitter_data[:3]:
                created_at = tweet.get('created_at')
                text = tweet.get('text')

                # Create a string with the tweet data
                tweet_text = f"Created at: {created_at}\nText: {text}"
                tweet_texts.append(tweet_text)

            # Update the Twitter data label with the combined tweet texts
            self.twitter_data_label.text = "\n\n".join(tweet_texts)
        except Exception as e:
            print(f"Error fetching Twitter data: {e}")

    def open_twitter_embed(self, *args):
        try:
            # Construct the Twitter URL based on the resort's Twitter handle
            twitter_url = f"https://twitter.com/{self.twitter_handle}?ref_src=twsrc%5Etfw"

            # Open the Twitter URL in the web browser
            webbrowser.open(twitter_url)
        except Exception as e:
            print(f"Error opening Twitter embed: {e}")

    def switch_to_main_menu(self, instance):
        try:
            app = App.get_running_app()
            app.root.current = 'Main Menu'
        except Exception as e:
            print(f"Error switching to main menu: {e}")