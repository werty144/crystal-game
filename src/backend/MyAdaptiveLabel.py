from collections import Counter

from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.label import Label
from resources.strings.Strings import *


class MyAdaptiveLabel(Label):
    adaptive_height = NumericProperty()
    adaptive_width = NumericProperty()
    adapt_height = BooleanProperty(False)
    adapt_width = BooleanProperty(False)
    adapt_tasks = BooleanProperty(False)
    fonts_setted = False
    small_font = 100
    large_font = 100

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def bind_height(self):
        self.bind(size=self.set_adaptive_height)
        return 0

    def set_adaptive_height(self, *args):
        self.adaptive_height = self.height
        self.adapt()

    def bind_width(self):
        self.bind(size=self.set_adaptive_width)

    def set_adaptive_width(self, *args):
        self.adaptive_width = self.width
        self.adapt()

    def bind_size(self):
        self.bind(size=self.set_adaptive_size)

    def set_adaptive_size(self, *args):
        self.adaptive_height = self.height
        self.adaptive_width = self.width
        self.adapt()

    def bind_tasks(self):
        self.bind(size=self.set_tasks)

    def set_tasks(self, *args):
        self.adaptive_height = self.height
        self.adaptive_width = self.width
        if MyAdaptiveLabel.fonts_setted:
            self.set_task_font()
            return
        MyAdaptiveLabel.fonts_setted = True
        text = self.text
        fonts = Counter()
        ''' Here we don't look on last 2 elements because there is no task strings there'''
        for s in list(RU_ID_STRING_MAP.values())[:-2]:
            self.text = s
            self.set_font()
            MyAdaptiveLabel.small_font = min(self.font_size, self.small_font)
            fonts[int(self.font_size)] += 1
        for s in list(ENG_ID_STRING_MAP.values())[:-2]:
            self.text = s
            self.set_font()
            MyAdaptiveLabel.small_font = min(self.font_size, self.small_font)
            fonts[int(self.font_size)] += 1
        fonts_list = sorted(list(fonts.elements()))
        middle = len(fonts_list) // 2
        MyAdaptiveLabel.large_font = fonts_list[middle]
        self.text = text
        self.set_task_font()

    def set_task_font(self):
        self.font_size = MyAdaptiveLabel.large_font
        self.texture_update()
        if self.texture_size[0] > self.width or self.texture_size[1] > self.height:
            self.font_size = MyAdaptiveLabel.small_font


    def on_kv_post(self, base_widget):
        if self.adapt_height and self.adapt_width:
            self.bind_size()
        elif self.adapt_height:
            self.bind_height()
        elif self.adapt_width:
            self.bind_width()
        elif self.adapt_tasks:
            self.bind_tasks()
        else:
            self.adapt()

    def adapt(self):
        self.unbind(size=self.set_adaptive_height)
        self.unbind(size=self.set_adaptive_width)
        self.unbind(size=self.set_adaptive_size)
        if self.adaptive_height > 0 and self.adaptive_width == 0:
            self.size_hint = (None, None)
            self.height = self.adaptive_height
            self.set_width()
        elif self.adaptive_width > 0 and self.adaptive_height == 0:
            self.size_hint = (None, None)
            self.width = self.adaptive_width
            self.set_height()
        elif self.adaptive_width > 0 and self.adaptive_height > 0:
            self.size_hint = (None, None)
            self.set_font()

    def set_width(self):
        self.bin_search(lambda x: self.texture_size[1] > self.height)
        if self.texture_size[1] <= self.height:
            self.width = self.texture_size[0]
        else:
            self.font_size -= 1
            self.texture_update()
            self.width = self.texture_size[0]

    def set_height(self):
        self.bin_search(lambda x: self.texture_size[0] > self.width)
        if self.texture_size[0] <= self.width:
            self.height = self.texture_size[1]
        else:
            self.font_size -= 1
            self.texture_update()
            self.height = self.texture_size[1]

    def set_font(self):
        self.bin_search(lambda x: self.texture_size[0] > self.width or self.texture_size[1] > self.height)
        if self.texture_size[0] > self.width or self.texture_size[1] > self.height:
            self.font_size -= 1

    def bin_search(self, condition):
        r = 50.0
        l = 1.0
        eps = 0.001
        self.font_size = (l + r) / 2
        while r - l > eps:
            m = (l + r) / 2
            self.font_size = m
            self.texture_update()
            if condition(0):
                r = m
            else:
                l = m
