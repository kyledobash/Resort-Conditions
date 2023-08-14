from kivy.uix.label import Label

class CustomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(width=self.update_text_width)

    def update_text_width(self, instance, width):
        self.text_size = (width, None)
        self.texture_update()