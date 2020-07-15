import os
from os.path import dirname, abspath, join
# os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import *
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from src.backend.Engine import Engine
from src.backend.constants import *

Builder.load_file(join(project_path, 'src', 'frontend', 'crystal_game.kv'))


class BoxWidget(Image):
    source_dir = StringProperty()
    position = Property((0, 0))
    size_variable = Property((0, 0))

    def __init__(self, source_dir, pos, size):
        super().__init__()
        self.source_dir = source_dir
        self.position = pos
        self.size_variable = size


class Playground(Widget):
    engine = ObjectProperty()
    # that's for test purposes
    lovely_only_box_widget = ObjectProperty()

    def start(self):
        self.engine = Engine(0)
        for box in self.engine.all_game_objects():
            box_widget = BoxWidget(join(images_path, 'yan.jpg'), (box.x, box.y), (box.size, box.size))
            self.lovely_only_box_widget = box_widget
            self.add_widget(box_widget)
        Clock.schedule_interval(self.update, 0.01)

    def update(self, _):
        self.engine.tick()

        # Here the mapping should be, but I'm to tired
        self.lovely_only_box_widget.position = \
            (self.engine.all_game_objects()[0].x, self.engine.all_game_objects()[0].y)


class MenuScreen(Screen):
    pass


class GameScreen(Screen):

    def on_enter(self, *args):
        playground = Playground()
        self.add_widget(playground)
        playground.start()


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(GameScreen(name='game'))


class Crystal_game(App):

    def build(self):
        return sm


if __name__ == '__main__':
    Crystal_game().run()
