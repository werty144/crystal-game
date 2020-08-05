import re
import os
os.environ['KIVY_AUDIO'] = 'sdl2'
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.properties import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
from src.frontend.custom_widgets.PlaygroundWidget import Playground
from src.frontend.custom_widgets.RuleWidget import *
from src.frontend.custom_widgets.TutorialWidget import Tutorial
from src.frontend.custom_widgets.WinningWidget import WinningWidget

Builder.load_file(KV_FILE_PATH)


class MenuScreen(Screen):
    pass


class LevelsScreen(Screen):

    def on_enter(self, *args):
        btn_list = self.children[0].children[0].children
        for obj in btn_list:
            if type(obj) is Button:
                lvl = int(re.search(r'\d+', obj.text).group())
                button_image = self.get_button_image(lvl)
                obj.background_normal = button_image[0]
                obj.background_down = button_image[1]

    @staticmethod
    def get_button_color(lvl):
        if storage.get('lvl' + str(lvl))['status'] == 'Passed':
            return 1, 1, 0, 1
        elif storage.get('lvl' + str(lvl))['status'] == 'Unlocked':
            return 1, 0, 1, 1
        return 1, 1, 1, 1

    @staticmethod
    def get_button_image(lvl):
        if storage.get('lvl' + str(lvl))['status'] == 'Passed':
            return 'resources/images/button_green.png', 'resources/images/button_green_pressed.png'
        elif storage.get('lvl' + str(lvl))['status'] == 'Unlocked':
            return 'resources/images/button_yellow.png', 'resources/images/button_yellow_pressed.png'
        return 'resources/images/button_red.png', 'resources/images/button_red_pressed.png'

    @staticmethod
    def go_to_lvl(lvl):
        if storage.get('lvl' + str(lvl))['status'] == 'Locked':
            # Level is locked
            return
        sm.transition.direction = 'left'
        sm.get_screen('game').lvl = lvl
        sm.current = 'game'


class GameScreen(Screen):
    playground = ObjectProperty(None, allownone=True)
    lvl = NumericProperty()
    winning_widget = ObjectProperty(None, allownone=True)
    sound = SoundLoader.load(join(SOUND_PATH, 'moan.wav'))

    def on_enter(self, *args):
        self.playground = Playground(storage=storage)
        self.playground.start(self.lvl)
        self.add_widget(self.playground)
        self.set_buttons()

    def restart(self):
        self.clean()
        self.set_buttons()
        self.on_enter()

    def clean(self):
        self.sound.stop()
        if self.playground is not None:
            self.playground.update_event.cancel()
            self.remove_widget(self.playground)
            self.playground = None
        if self.winning_widget is not None:
            self.remove_widget(self.winning_widget)
            self.winning_widget = None

    def switch_field(self):
        self.playground.switch_field()

    def set_buttons(self):
        self.ids.field_switch.text = 'to target\nfield'

    def show_winning_widget(self):
        self.winning_widget = WinningWidget()
        self.add_widget(self.winning_widget)
        if self.sound:
            self.sound.play()

    def go_to_next_lvl(self):
        self.clean()
        self.lvl += 1
        self.on_enter()

    def undo(self):
        self.playground.undo()


class TutorialScreen(GameScreen):
    def on_enter(self, *args):
        self.playground = Tutorial()
        self.add_widget(self.playground)
        self.playground.start()
        self.set_buttons()

    def show_winning_widget(self):
        self.winning_widget = WinningWidget()
        self.winning_widget.ids.next_lvl_button.text = 'Lvl 1'
        self.add_widget(self.winning_widget)

    def go_to_next_lvl(self):
        self.clean()
        sm.get_screen('game').lvl = 1
        sm.current = 'game'


storage = JsonStore(STORAGE_PATH)


# Call only once at first start
def init_storage():
    storage.put('lvl0', status='Unlocked')
    for i in range(1, 101):
        storage.put('lvl' + str(i), status='Locked')


init_storage()


def on_key(window, key, *args):
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
            gs.clean()
            return True  # do not exit the app
        elif sm.current_screen.name == "tutorial":
            sm.transition.direction = 'right'
            sm.current = "menu"
            ts.clean()
            return True  # do not exit the app


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(LevelsScreen(name='levels'))
gs = GameScreen(name='game')
sm.add_widget(gs)
ts = TutorialScreen(name='tutorial')
sm.add_widget(ts)
Window.bind(on_keyboard=on_key)
# sm.current = 'levels'


class Crystal_game(App):

    def build(self):
        return sm

#
# if __name__ == '__main__':
#     Crystal_game().run()
