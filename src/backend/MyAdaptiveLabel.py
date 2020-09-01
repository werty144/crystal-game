from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import NumericProperty, Clock, BooleanProperty
from kivy.uix.label import Label


class MyAdaptiveLabel(Label):
    adaptive_height = NumericProperty()
    adaptive_width = NumericProperty()
    adapt_height = BooleanProperty(False)
    adapt_width = BooleanProperty(False)

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

    def on_kv_post(self, base_widget):
        if self.adapt_height and self.adapt_width:
            self.bind_size()
        elif self.adapt_height:
            self.bind_height()
        elif self.adapt_width:
            self.bind_width()
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
