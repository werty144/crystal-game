from kivy.uix.label import Label

from src.backend.constants import MODULE_AMOUNT
from src.frontend.custom_widgets.StarsPerModuleWidget import StarsPerModule
from src.frontend.custom_widgets.StarsPopup import StarsPopup
from kivy.uix.screenmanager import Screen
from src.backend.ModuleUtils import *


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

    def show_star_popup(self):
        star_popup = StarsPopup()
        for module in range(1, MODULE_AMOUNT + 1):
            star_popup.ids.grid.add_widget(StarsPerModule(module))
        star_popup.open()

