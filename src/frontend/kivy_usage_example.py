from kivy.app import App
from kivy.uix.label import Label

from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.app import App
from kivy.graphics.svg import Svg
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter


class MyWidget(Scatter):
    i = 0

    def __init__(self, filename, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        with self.canvas:
            Rectangle(source='/home/evgeny/spdu/kivy/crystal-game/images/test.png')
        Clock.schedule_interval(self.update, 5 / 60.)

    def update(self, delta):
        self.i += 1
        self.canvas.clear()
        self.canvas.add(Color(1., 1., 1.))
        self.canvas.add(Rectangle(source='/home/evgeny/spdu/kivy/crystal-game/images/test{}.png'.format(self.i % 5)))
        print(self.i)


class SvgApp(App):

    def build(self):
        self.root = FloatLayout()

        svg1 = MyWidget('/home/evgeny/spdu/kivy/crystal-game/images/cloud.svg')
        self.root.add_widget(svg1)
        svg1.center = Window.center


if __name__ == "__main__":
    SvgApp().run()