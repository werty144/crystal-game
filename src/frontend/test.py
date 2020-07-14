import os

from kivy.graphics import Line

os.environ["KIVY_NO_CONSOLELOG"] = "1"


from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.properties import NumericProperty, Property
from kivy.uix.widget import Widget
from kivy.clock import Clock


class Cell(Widget):
    r = NumericProperty(1)
    b = NumericProperty(1)

    def __init__(self, x, y, size):
        super().__init__()
        self.size = (size, size)
        self.pos = (x, y)


class Parabola(Widget):
    def __init__(self):
        super().__init__()
        points_pairs = [(x, (x - 400) ** 2//30) for x in range(100, 701)]
        points = [x for p in points_pairs for x in p]

        with self.canvas:
            Color(0, 0, 1, 1)
            Line(points=points, width=2)


class Form(Widget):
    r = NumericProperty(0)
    g = NumericProperty(1)
    rec_size = Property((100, 100))

    def __init__(self):
        super().__init__()
        self.cell = Cell(100, 100, 30)
        self.add_widget(Parabola())
        self.add_widget(self.cell)

    def start(self):
        Clock.schedule_interval(self.update, 0.1)

    def update(self, _):
        self.r ^= 1
        self.cell.pos = (self.cell.pos[0] + 2, self.cell.pos[1] + 3)
        self.cell.r ^= 1
        if self.rec_size[0] > 400:
            self.rec_size = (100, 100)
        else:
            self.rec_size = (self.rec_size[0] + 10, self.rec_size[1] + 10)


class WormApp(App):
    def build(self):
        form = Form()
        form.start()
        return form


if __name__ == '__main__':
    WormApp().run()
