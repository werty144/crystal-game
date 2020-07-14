import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.graphics import Line
from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.properties import *
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


class MyTriangle(Widget):
    r, g, b, a = NumericProperty(0), NumericProperty(0), NumericProperty(1), NumericProperty(1)
    points = ListProperty()

    def __init__(self, points):
        super().__init__()
        self.points = points


class Polygon(Widget):
    tr_colors = ListProperty([])
    points = ListProperty([0, 0])

    def __init__(self, points):
        super().__init__()
        self.points = points
        self.triangles = []
        triplets = [points[:6], points[2:], points[4:] + points[:2]]
        with self.canvas:
            for triplet in triplets:
                triangle = MyTriangle(points=triplet)
                self.add_widget(triangle)
                self.triangles.append(triangle)


class Form(Widget):
    r = NumericProperty(1)
    g = NumericProperty(1)
    rec_size = Property((100, 100))

    def __init__(self):
        super().__init__()
        self.i = 0
        self.cell = Cell(100, 100, 30)
        self.add_widget(Parabola())
        self.add_widget(self.cell)
        self.polygon = Polygon([10, 10, 100, 10, 200, 100, 100, 100])
        self.add_widget(self.polygon)
        self.add_widget(MyTriangle([10, 500, 100, 500, 50, 450]))

    def start(self):
        Clock.schedule_interval(self.update, 0.1)

    def update(self, _):
        self.polygon.triangles[self.i].g ^= 1
        self.i = (self.i + 1) % 3
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
