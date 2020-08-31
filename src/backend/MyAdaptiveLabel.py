from kivy.properties import NumericProperty
from kivy.uix.label import Label


class MyAdaptiveLabel(Label):
    adaptive_height = NumericProperty()
    adaptive_width = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.size_hint = (None, None)
        if self.adaptive_height > 0:
            self.height = self.adaptive_height
            self.set_width()
        elif self.adaptive_width > 0:
            self.width = self.adaptive_width
            self.set_height()
        else:
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
        if self.texture_size[0] <= self.width:
            self.height = self.texture_size[1]
        else:
            self.font_size -= 1
            self.texture_update()
            self.height = self.texture_size[1]
        if self.texture_size[1] <= self.height:
            self.width = self.texture_size[0]
        else:
            self.font_size -= 1
            self.texture_update()
            self.width = self.texture_size[0]

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
