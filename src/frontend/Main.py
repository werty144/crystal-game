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
from kivy.uix.label import Label
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

    def start(self, lvl):
        self.screen_utils = ScreenUtils(4)
        self.engine = Engine(lvl)
        self.add_missing_game_widgets()
        Clock.schedule_interval(self.update, FRAME_RATE_SEC)

    def update(self, _):
        self.engine.tick()
        self.add_missing_game_widgets()
        self.update_all_game_widgets()
        self.check_win()

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

    def check_win(self):
        if self.engine.win and not self.engine.any_animation_in_progress():
            self.add_widget(Label(text='You win!', font_size='100sp', center_x=self.width/2 + self.x,
                            center_y=self.height*5/6 + self.y))


class BoxWidget(ButtonBehavior, Image):
    def __init__(self, obj, playground):
        super(BoxWidget, self).__init__()
        self.engine = playground.engine
        self.playground = playground
        setattr(self, 'game_id', obj.game_id)
        for attr, value in obj.__dict__.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        self.box = obj
        self.rules = self.box.rules
        self.scroll_view = None

    def on_press(self):
        pass

    def on_release(self):
        if self.scroll_view is not None:
            return
        pos, size = self.playground.screen_utils.get_scrollview_size()
        self.scroll_view = ScrollView(size_hint=(None, None), size=(size[0], size[1]), pos=(pos[0], pos[1]))
        layout = GridLayout(cols=1, spacing=50, padding=(0, 50), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        if len(self.rules) == 0:
            # Write that there is no rules
            return
        for i in range(len(self.rules)):
            rule_widget = RuleWidget(self.rules[i], self.btn_on_release)
            layout.add_widget(rule_widget)
        self.scroll_view.add_widget(layout)
        with self.scroll_view.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.scroll_view.size,
                                  pos=self.scroll_view.pos)
        self.playground.add_widget(self.scroll_view)

    def btn_on_release(self, rule):
        self.playground.engine.adjust_rule(self.box, rule)
        self.playground.remove_widget(self.scroll_view)
        self.scroll_view = None


class MenuScreen(Screen):
    pass


class LevelsScreen(Screen):
    cur_lvl = NumericProperty()

    def go_to_lvl(self, lvl):
        self.cur_lvl = lvl
        sm.current = 'game'


class GameScreen(Screen):
    playground = ObjectProperty()
    grid = ObjectProperty()
    lvl = NumericProperty()

    def on_enter(self, *args):
        self.lvl = sm.get_screen('levels').cur_lvl
        self.playground = Playground()
        self.grid = InstructionGroup()
        self.playground.start(self.lvl)
        self.make_grid()
        self.add_widget(self.playground)

    def make_grid(self):
        points = self.playground.screen_utils.create_grid()
        for a, b in points:
            self.grid.add(Line(points=[a[0], a[1], b[0], b[1]]))
        self.canvas.add(self.grid)

    def restart(self):
        self.clean()
        self.on_enter()

    def clean(self):
        self.remove_widget(self.playground)
        self.canvas.remove(self.grid)


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(LevelsScreen(name='levels'))
sm.add_widget(GameScreen(name='game'))
sm.current = 'levels'


class Crystal_game(App):

    def build(self):
        return sm


if __name__ == '__main__':
    Crystal_game().run()
