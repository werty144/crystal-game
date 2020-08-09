from os.path import join

from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen

from src.backend.constants import SOUND_PATH
from src.frontend.custom_widgets.PlaygroundWidget import Playground
from src.frontend.custom_widgets.WinningWidget import WinningWidget


class GameScreen(Screen):
    playground = ObjectProperty(None, allownone=True)
    lvl = NumericProperty()
    winning_widget = ObjectProperty(None, allownone=True)
    sound = SoundLoader.load(join(SOUND_PATH, 'moan.wav'))
    storage = ObjectProperty()

    def on_enter(self, *args):
        self.playground = Playground(storage=self.storage)
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
