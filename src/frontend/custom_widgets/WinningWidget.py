from kivy.uix.floatlayout import FloatLayout


class WinningWidget(FloatLayout):
    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        return True
