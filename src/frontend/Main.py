import os

from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager

from src.LanguageUtils import LanguageUtils
from src.frontend.Screens.GameScreen import GameScreen
from src.frontend.Screens.LevelsScreen import LevelsScreen
from src.frontend.Screens.MenuScreen import MenuScreen
from src.frontend.Screens.TutorialScreen import TutorialScreen
from src.backend.constants import MODULE_AMOUNT

os.environ['KIVY_AUDIO'] = 'sdl2'
from kivy.core.window import Window
from src.frontend.custom_widgets.RuleWidget import *


storage = JsonStore(STORAGE_PATH)


# Call only once at first start
def init_storage():
    if storage.exists('inited'):
        return
    storage.put('inited')
    storage.put('language', status='en')
    storage.put('lvl1', status='Unlocked')
    storage.put('module_stars', **{str(number): 0 for number in range(1, MODULE_AMOUNT + 1)})
    for i in range(2, 101):
        storage.put('lvl' + str(i), status='Locked')


init_storage()


def on_key(window, key, *args):
    sm_ = args[0]
    game_screen = args[1]
    ts = args[2]
    if key == 27:  # the esc key
        if sm_.current_screen.name == "menu":
            return False  # exit the app from this page
        elif sm_.current_screen.name == "levels":
            sm_.transition.direction = 'right'
            sm_.current = "menu"
            return True  # do not exit the app
        elif sm_.current_screen.name == "game":
            sm_.transition.direction = 'right'
            sm_.current = "levels"
            game_screen.clean()
            return True  # do not exit the app
        elif sm_.current_screen.name == "tutorial":
            sm_.transition.direction = 'right'
            sm_.current = "menu"
            ts.clean()
            return True  # do not exit the app


class Crystal_game(App):
    language_utils = ObjectProperty()

    def build(self):
        self.language_utils = LanguageUtils(storage)
        sm = ScreenManager()
        ms = MenuScreen(name='menu')
        self.language_utils.init_menu_screen(ms)
        sm.add_widget(ms)
        sm.add_widget(LevelsScreen(name='levels', storage=storage))
        gs = GameScreen(name='game', storage=storage)
        sm.add_widget(gs)
        ts = TutorialScreen(name='tutorial')
        sm.add_widget(ts)
        Window.bind(on_keyboard=lambda window, key, *args: on_key(window, key, sm, gs, ts, *args))
        sm.current = 'levels'
        return sm
