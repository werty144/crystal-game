import os

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager

from src.LanguageUtils import LanguageUtils
from src.backend.SoundHandler import SoundHandler
from src.frontend.Screens.GameScreen import GameScreen
from src.frontend.Screens.LevelsScreen import LevelsScreen
from src.frontend.Screens.MenuScreen import MenuScreen
from src.frontend.Screens.ModulesScreen import ModulesScreen
from src.frontend.Screens.TutorialScreen import TutorialScreen
from src.backend.constants import MODULE_AMOUNT

os.environ['KIVY_AUDIO'] = 'sdl2'
from kivy.core.window import Window
from src.frontend.custom_widgets.RuleWidget import *


# Call only once at first start
def init_storage(storage):
    if storage.exists('inited'):
        return
    storage.put('inited')
    storage.put('language', status='en')
    storage.put('lvl1', status='Unlocked')
    storage.put('module_stars', **{str(number): 0 for number in range(1, MODULE_AMOUNT + 1)})
    for i in range(2, 101):
        storage.put('lvl' + str(i), status='Locked')


def on_key(window, key, *args):
    sm_ = args[0]
    game_screen = args[1]
    ts = args[2]
    if key == 27:  # the esc key
        if sm_.current_screen.name == "menu":
            return False  # exit the app from this page
        elif sm_.current_screen.name == "modules":
            sm_.transition.direction = 'right'
            sm_.current = "menu"
            return True  # do not exit the app
        elif sm_.current_screen.name == "levels":
            sm_.transition.direction = 'right'
            sm_.current = "modules"
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
    storage = ObjectProperty()
    sound_handler = ObjectProperty()

    def build(self):
        self.storage = JsonStore(STORAGE_PATH)
        init_storage(self.storage)
        self.language_utils = LanguageUtils(self.storage)
        self.sound_handler = SoundHandler()
        self.sound_handler.play_theme()
        sm = ScreenManager()
        ms = MenuScreen(name='menu')
        self.language_utils.init_menu_screen(ms)
        sm.add_widget(ms)
        sm.add_widget(ModulesScreen(name='modules'))
        sm.add_widget(LevelsScreen(name='levels', storage=self.storage, sound_handler=self.sound_handler, module=1))
        gs = GameScreen(name='game', storage=self.storage, sound_handler=self.sound_handler)
        sm.add_widget(gs)
        ts = TutorialScreen(name='tutorial', sound_handler=self.sound_handler)
        sm.add_widget(ts)
        Window.bind(on_keyboard=lambda window, key, *args: on_key(window, key, sm, gs, ts, *args))
        return sm
