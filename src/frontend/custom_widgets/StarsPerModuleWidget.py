from kivy.uix.floatlayout import FloatLayout


class StarsPerModule(FloatLayout):
    def __init__(self, module):
        self.module = module
        super().__init__()
