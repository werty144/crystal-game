from kivy.app import App
from kivy.uix.screenmanager import Screen
from src.backend.constants import *


class ModulesScreen(Screen):
    def on_pre_enter(self, *args):
        self.set_stars_amount()

    def set_stars_amount(self):
        storage = App.get_running_app().storage
        got = 0
        for lvl in get_final_levels():
            if storage.get(f'lvl{lvl}')['status'] == 'Passed':
                got += storage.get('module_stars')[str(get_module(lvl))]
        self.ids.stars_amount.text = str(got) + '/' + str(total_stars())
