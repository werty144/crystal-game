import re

from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from src.backend.constants import ID_TEXTURE_MAP


class LevelsScreen(Screen):
    storage = ObjectProperty()
    sound_handler = ObjectProperty()

    def on_enter(self, *args):
        btn_list = self.children[0].children[0].children
        for obj in btn_list:
            if type(obj) is Button:
                lvl = int(re.search(r'\d+', obj.text).group())
                button_image = self.get_button_image(lvl)
                obj.background_normal = button_image[0]
                obj.background_down = button_image[1]

    def get_button_image(self, lvl):
        if self.storage.get('lvl' + str(lvl))['status'] == 'Passed':
            return ID_TEXTURE_MAP['opened_envelope'], 'resources/images/button_green_pressed.png'
        elif self.storage.get('lvl' + str(lvl))['status'] == 'Unlocked':
            return ID_TEXTURE_MAP['opened_envelope'], 'resources/images/button_yellow_pressed.png'
        return ID_TEXTURE_MAP['closed_envelope'], 'resources/images/button_red_pressed.png'

    def go_to_lvl(self, lvl):
        self.sound_handler.play_button_tap()
        if self.storage.get('lvl' + str(lvl))['status'] == 'Locked':
            # Level is locked
            return
        self.manager.transition.direction = 'left'
        self.manager.get_screen('game').lvl = lvl
        self.manager.current = 'game'
