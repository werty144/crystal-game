from os.path import join

from kivy.core.audio import SoundLoader

from src.backend.constants import SOUND_PATH


class SoundHandler:

    def __init__(self):
        self.theme = SoundLoader.load(join(SOUND_PATH, 'theme.wav'))
        self.button_tap = SoundLoader.load(join(SOUND_PATH, 'button_tap.wav'))
        self.falling_box = SoundLoader.load(join(SOUND_PATH, 'falling_box.wav'))
        self.winning_sound = SoundLoader.load(join(SOUND_PATH, 'win.wav'))
        self.rule_tap = SoundLoader.load(join(SOUND_PATH, 'rule_tap.wav'))

    def play_theme(self):
        self.theme.loop = True
        self.theme.play()

    def stop_theme(self):
        self.theme.stop()

    def play_button_tap(self):
        self.button_tap.play()

    def stop_button_tap(self):
        self.button_tap.stop()

    def play_winning_sound(self):
        self.winning_sound.play()

    def stop_winning_sound(self):
        self.winning_sound.stop()

    def play_falling_box(self):
        self.falling_box.play()

    def stop_falling_box(self):
        self.falling_box.stop()

    def play_rule_tap(self):
        self.rule_tap.play()

    def stop_rule_tap(self):
        self.rule_tap.stop()

    def stop_level_sounds(self):
        self.stop_button_tap()
        self.stop_winning_sound()
        self.stop_falling_box()
