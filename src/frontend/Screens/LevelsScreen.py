import re

from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from src.backend.constants import ID_TEXTURE_MAP, MODULE_OFFSET, LEVELS_PER_MODULE


class LevelsScreen(Screen):
    storage = ObjectProperty()
    sound_handler = ObjectProperty()
    module = NumericProperty()

    def on_pre_enter(self, *args):
        btn_list = self.children[0].children[0].children
        grid_layout = self.children[0].children[0]
        for i in range(len(btn_list)):
            grid_layout.remove_widget(btn_list[-1])
        for i in range(1, LEVELS_PER_MODULE[self.module] + 1):
            lvl_num = i + MODULE_OFFSET[self.module]
            btn_with_txt = FloatLayout()
            btn_with_txt.add_widget(
                Button(
                    background_normal=self.get_button_image(lvl_num)[0],
                    background_down=self.get_button_image(lvl_num)[1],
                    on_press=lambda _, lvl=lvl_num: self.go_to_lvl(lvl),
                    border=(0, 0, 0, 0),
                    pos_hint={'x': 0, 'y': 0}
                )
            )
            btn_with_txt.add_widget(
                Label(
                    text=f'[color=000000][b]{lvl_num}[/b][/color]',
                    font_size=20,
                    size_hint=(0.3, 0.3),
                    pos_hint={'right': 0.95, 'y': 0},
                    markup=True,
                    halign='right'
                )
            )
            grid_layout.add_widget(
                btn_with_txt
            )

    def get_button_image(self, lvl):
        if self.storage.get('lvl' + str(lvl))['status'] == 'Passed':
            return ID_TEXTURE_MAP['opened_envelope' + str(self.module)], ID_TEXTURE_MAP['opened_envelope' +
                                                                                        str(self.module)]
        elif self.storage.get('lvl' + str(lvl))['status'] == 'Unlocked':
            return ID_TEXTURE_MAP['opened_envelope'], ID_TEXTURE_MAP['opened_envelope']
        return ID_TEXTURE_MAP['closed_envelope'], ID_TEXTURE_MAP['closed_envelope']

    def go_to_lvl(self, lvl):
        self.sound_handler.play_button_tap()
        if self.storage.get('lvl' + str(lvl))['status'] == 'Locked':
            # Level is locked
            return
        self.manager.transition.direction = 'left'
        self.manager.get_screen('game').lvl = lvl
        self.manager.current = 'game'
