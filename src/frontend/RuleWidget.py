from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from src.backend.Engine import map_kind_to_texture_source
from src.backend.Rule import Rule
from src.backend.constants import *


class RuleWidget(ButtonBehavior, BoxLayout):
    def __init__(self, rule: Rule, on_press_func):
        super().__init__()
        self.on_press_func = on_press_func
        self.add_widget(Image(source=map_kind_to_texture_source(rule.initial_box_kind)))
        self.add_widget(Image(source=join(IMAGES_PATH, ARROW_IMAGE)))
        for res_box_kind in rule.result_box_kinds:
            self.add_widget(Image(source=map_kind_to_texture_source(res_box_kind)))
        for child in self.children:
            child.size_hint = (1, None)

    def on_press(self):
        self.on_press_func()

    def on_release(self):
        pass
