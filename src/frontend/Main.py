import os

from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager

from src.frontend.Screens.GameScreen import GameScreen
from src.frontend.Screens.LevelsScreen import LevelsScreen
from src.frontend.Screens.MenuScreen import MenuScreen
from src.frontend.Screens.TutorialScreen import TutorialScreen

os.environ['KIVY_AUDIO'] = 'sdl2'
from kivy.lang import Builder
from kivy.core.window import Window
from src.frontend.custom_widgets.RuleWidget import *

Builder.load_file(KV_FILE_PATH)


storage = JsonStore(STORAGE_PATH)


# Call only once at first start
def init_storage():
    storage.put('language', status='en')
    storage.put('lvl1', status='Unlocked')
    for i in range(2, 101):
        storage.put('lvl' + str(i), status='Locked')


init_storage()


def on_key(window, key, *args):
    sm = args[0]
    game_screen = args[1]
    if key == 27:  # the esc key
        if sm.current_screen.name == "menu":
            return False  # exit the app from this page
        elif sm.current_screen.name == "levels":
            sm.transition.direction = 'right'
            sm.current = "menu"
            return True  # do not exit the app
        elif sm.current_screen.name == "game":
            sm.transition.direction = 'right'
            sm.current = "levels"
            game_screen.clean()
            return True  # do not exit the app
        elif sm.current_screen.name == "tutorial":
            sm.transition.direction = 'right'
            sm.current = "menu"
            ts.clean()
            return True  # do not exit the app


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(LevelsScreen(name='levels', storage=storage))
gs = GameScreen(name='game', storage=storage)
sm.add_widget(gs)
ts = TutorialScreen(name='tutorial')
sm.add_widget(ts)
Window.bind(on_keyboard=lambda window, key: on_key(window, key, sm, gs))
# sm.current = 'levels'


class Crystal_game(App):

    def build(self):
        return sm

#
# if __name__ == '__main__':
#     Crystal_game().run()
