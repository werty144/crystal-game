from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from src.backend.Rule import Rule
from src.backend.constants import *


def get_arrow_image(rule):
    if rule.direction == UP:
        return UP_ARROW_IMAGE
    if rule.direction == RIGHT:
        return RIGHT_ARROW_IMAGE
    if rule.direction == LEFT:
        return LEFT_ARROW_IMAGE


def map_kind_to_texture_source(kind):
    return RULE_ATLAS_URL + KIND_RULE_ATLAS_ID_MAP[kind]


class RuleWidget(ButtonBehavior, BoxLayout):
    def __init__(self, rule: Rule, on_press_func, max_right_side_len):
        super().__init__()
        self.spacing = 5
        self.rule = rule
        self.on_press_func = on_press_func
        self.size_hint_y = None
        self.add_widget(Image(source=map_kind_to_texture_source(rule.initial_box_kind)))
        self.add_widget(Image(source=get_arrow_image(rule)))
        for res_box_kind in rule.result_box_kinds:
            self.add_widget(Image(source=map_kind_to_texture_source(res_box_kind)))
        for _ in range(max_right_side_len - len(rule.result_box_kinds)):
            self.add_widget(Widget())
        for child in self.children:
            child.size_hint = (1, None)
            child.bind(size=self.update)

    def update(self, *args):
        images = list(filter(lambda child: isinstance(child, Image), self.children))
        for image in images:
            image.height = image.width * image.image_ratio
        self.height = max([image.norm_image_size[1] for image in images])

    def on_press(self):
        self.on_press_func(self.rule)
