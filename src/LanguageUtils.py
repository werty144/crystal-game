from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.button import Button

from resources.strings.Strings import *
from src.backend.constants import ENG_ID_TEXTURE_MAP, RU_ID_TEXTURE_MAP


class LanguageUtils:

    def init_menu_screen(self, menu_screen):
        self.en_btn = menu_screen.ids['en_flag']
        self.ru_btn = menu_screen.ids['ru_flag']
        if self.cur_lang == 'en':
            self.make_btn_frame(self.en_btn)
        elif self.cur_lang == 'ru':
            self.make_btn_frame(self.ru_btn)

    def __init__(self):
        self.storage = App.get_running_app().storage
        self.en_btn = None
        self.ru_btn = None
        self.cur_lang = self.storage.get('language')['status']

    def change_language(self, lang):
        if lang == 'en':
            self.storage.put('language', status='en')
            self.cur_lang = 'en'
            self.clear_btn_frame(self.ru_btn)
            self.make_btn_frame(self.en_btn)
        elif lang == 'ru':
            self.storage.put('language', status='ru')
            self.cur_lang = 'ru'
            self.clear_btn_frame(self.en_btn)
            self.make_btn_frame(self.ru_btn)

    def set_texture(self, identifier):
        id_texture_map = None
        if self.cur_lang == 'en':
            id_texture_map = ENG_ID_TEXTURE_MAP
        elif self.cur_lang == 'ru':
            id_texture_map = RU_ID_TEXTURE_MAP
        return id_texture_map[identifier]

    def set_string(self, identifier):
        id_string_map = None
        if self.cur_lang == 'en':
            id_string_map = ENG_ID_STRING_MAP
        elif self.cur_lang == 'ru':
            id_string_map = RU_ID_STRING_MAP
        return id_string_map[identifier]

    @staticmethod
    def make_btn_frame(btn):
        def make_frame(*args):
            btn.canvas.before.clear()
            with btn.canvas.before:
                Color(0.8, 0.8, 0, 1)
                Line(width=2, rectangle=(btn.x, btn.y, btn.width, btn.height))
        btn.bind(size=make_frame)
        make_frame()

    @staticmethod
    def clear_btn_frame(btn: Button):
        btn.canvas.before.clear()
