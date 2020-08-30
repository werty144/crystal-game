from src.backend.constants import LEVELS_PER_MODULE, STARS_PER_MODULE
from kivy.app import App

'''
Modules and levels enumerated from 1
'''


def get_module(lvl):
    module = 0
    for lvl_amount in LEVELS_PER_MODULE.values():
        lvl -= lvl_amount
        module += 1
        if lvl <= 0:
            return module
    raise Exception('Bad lvl')


def get_final_levels():
    return [sum(list(LEVELS_PER_MODULE.values())[0:i + 1]) for i in range(len(LEVELS_PER_MODULE))]


def total_stars():
    return sum(STARS_PER_MODULE.values())


def module_passed(module):
    final_lvl = get_final_levels()[module - 1]
    storage = App.get_running_app().storage
    return storage.get(f'lvl{final_lvl}')['status'] == 'Passed'


def stars_got_in_module(module):
    storage = App.get_running_app().storage
    return storage.get('module_stars')[str(module)]
