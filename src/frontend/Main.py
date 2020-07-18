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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView

from src.backend.Engine import Engine
from src.backend.ScreenUtils import ScreenUtils
from src.backend.constants import *
from src.frontend.RuleWidget import *

Builder.load_file(join(PROJECT_PATH, 'src', 'frontend', 'crystal_game.kv'))


class Playground(Widget):
    engine = ObjectProperty()
    game_widgets = ListProperty()
    screen_utils = ObjectProperty()

    def start(self):
        self.screen_utils = ScreenUtils(4)
        self.engine = Engine(0)
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
            wimg = BoxWidget(obj, self)
            self.game_widgets.append(wimg)
            self.add_widget(wimg)


class BoxWidget(ButtonBehavior, Image):
    def __init__(self, obj, playground):
        super(BoxWidget, self).__init__()
        self.engine = playground.engine
        self.playground = playground
        setattr(self, 'game_id', obj.game_id)
        for attr, value in obj.__dict__.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        self.rules = self.engine.get_rules(self.game_id)
        self.scroll_view = None

    def on_press(self):
        pass

    def on_release(self):
        if self.scroll_view is not None:
            return
        layout = GridLayout(cols=1, spacing=50, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(len(self.rules)):
            rule_widget = RuleWidget(self.rules[i], self.btn_on_release)
            rule_widget.height = 50
            rule_widget.size_hint_y = None
            layout.add_widget(rule_widget)
        pos, size = self.playground.screen_utils.get_scrollview_size()
        self.scroll_view = ScrollView(size_hint=(None, None), size=(size[0], size[1]), pos=(pos[0], pos[1]))
        self.scroll_view.add_widget(layout)
        with self.scroll_view.canvas.before:
            Color(1, 1, 1, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.scroll_view.size,
                                  pos=self.scroll_view.pos)
        self.playground.add_widget(self.scroll_view)

    def btn_on_release(self):
        print('HERR')
        self.playground.remove_widget(self.scroll_view)
        self.scroll_view = None


class MenuScreen(Screen):
    pass


class GameScreen(Screen):
    playground = ObjectProperty()
    grid = ObjectProperty()

    def on_enter(self, *args):
        self.playground = Playground()
        self.grid = InstructionGroup()
        self.playground.start()
        self.make_grid()
        self.add_widget(self.playground)

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
