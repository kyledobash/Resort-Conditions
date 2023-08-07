from kivy.uix.label import Label

class CustomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 1  # Set size_hint_y to 1 so that the label will always be at least as tall as the text