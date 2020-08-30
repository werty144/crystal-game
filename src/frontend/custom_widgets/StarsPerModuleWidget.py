from kivy.uix.boxlayout import BoxLayout


class StarsPerModule(BoxLayout):
    def __init__(self, module):
        self.module = module
        super().__init__()
