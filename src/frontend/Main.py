import os
import time
from os.path import dirname, abspath, join
# os.environ["KIVY_NO_CONSOLELOG"] = "1"
from kivy.config import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import *
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import *

from src.backend.Engine import Engine
from src.backend.ScreenUtils import ScreenUtils
from src.backend.constants import *

Builder.load_file(join(PROJECT_PATH, 'src', 'frontend', 'crystal_game.kv'))


class Playground(Widget):
    engine = ObjectProperty()
    game_widgets = ListProperty()
    screen_utils = ObjectProperty()

    def start(self):
        self.screen_utils = ScreenUtils(4)
        self.engine = Engine(0, self.screen_utils)
        self.add_missing_game_widgets()
        Clock.schedule_interval(self.update, FRAME_RATE_SEC)

    def update(self, _):
        self.engine.tick()
        self.add_missing_game_widgets()
        self.update_all_game_widgets()

    def update_all_game_widgets(self):
        for game_widget in self.game_widgets:
            corresponding_game_obj = next((obj for obj in self.engine.all_game_objects()
                                           if obj.game_id == game_widget.game_id), None)
            if corresponding_game_obj is None:
                self.remove_widget(game_widget)
                self.game_widgets.remove(game_widget)
                continue
            self.update_game_widget(game_widget, corresponding_game_obj)

    @staticmethod
    def update_game_widget(game_widget, game_object):
        for attr, value in game_object.__dict__.items():
            if hasattr(game_widget, attr):
                setattr(game_widget, attr, value)

    def add_missing_game_widgets(self):
        for obj in self.engine.all_game_objects():
            if any(widg.game_id == obj.game_id for widg in self.game_widgets):
                continue
            wimg = Image()
            setattr(wimg, 'game_id', obj.game_id)
            for attr, value in obj.__dict__.items():
                if hasattr(wimg, attr):
                    setattr(wimg, attr, value)
            self.game_widgets.append(wimg)
            self.add_widget(wimg)


class MenuScreen(Screen):
    pass


class GameScreen(Screen):
    playground = ObjectProperty()
    grid = ObjectProperty()

    def on_enter(self, *args):
        self.playground = Playground()
        self.grid = InstructionGroup()
        self.add_widget(self.playground)
        self.playground.start()
        self.make_grid()

    def make_grid(self):
        points = self.playground.screen_utils.create_grid()
        for a, b in points:
            with self.canvas:
                self.grid.add(Line(points=[a[0], a[1], b[0], b[1]]))
        self.canvas.add(self.grid)

    def restart(self):
        self.remove_widget(self.playground)
        self.canvas.remove(self.grid)
        self.on_enter()


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(GameScreen(name='game'))


class Crystal_game(App):

    def build(self):
        return sm


if __name__ == '__main__':
    Crystal_game().run()
