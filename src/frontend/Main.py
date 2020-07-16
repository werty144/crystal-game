import os
import time
from os.path import dirname, abspath, join
# os.environ["KIVY_NO_CONSOLELOG"] = "1"
from kivy.config import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import *
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from src.backend.Engine import Engine
from src.backend.constants import *

Builder.load_file(join(PROJECT_PATH, 'src', 'frontend', 'crystal_game.kv'))


class BoxWidget(Image):
    source_dir = StringProperty()

    def __init__(self, source_dir, pos, size):
        super().__init__()
        self.source_dir = source_dir
        self.pos = pos
        self.size = size


class Playground(Widget):
    engine = ObjectProperty()
    game_widgets = ListProperty()

    def start(self):
        self.engine = Engine(0)
        for obj in self.engine.all_game_objects():
            obj_widget = BoxWidget(join(IMAGES_PATH, 'yan.jpg'), (obj.x, obj.y), (obj.size, obj.size))
            setattr(obj_widget, 'game_id', obj.game_id)
            self.game_widgets.append(obj_widget)
            self.add_widget(obj_widget)
        Clock.schedule_interval(self.update, FRAME_RATE_SEC)

    def update(self, _):
        self.engine.tick()
        self.update_all_game_widgets()

    def update_all_game_widgets(self):
        for game_widget in self.game_widgets:
            corresponding_game_obj = next((obj for obj in self.engine.all_game_objects()
                                           if obj.game_id == game_widget.game_id), None)
            if corresponding_game_obj is None:
                self.remove_widget(game_widget)
                continue
            self.update_game_widget(game_widget, corresponding_game_obj)

    @staticmethod
    def update_game_widget(game_widget, game_object):
        for attr, value in game_object.__dict__.items():
            if hasattr(game_widget, attr):
                setattr(game_widget, attr, value)


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
