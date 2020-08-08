from kivy.storage.jsonstore import JsonStore

from src.backend.constants import ENG_ID_TEXTURE_MAP, RU_ID_TEXTURE_MAP, STORAGE_PATH


class LanguageUtils:
    storage = JsonStore(STORAGE_PATH)

    def change_language(self, lang):
        if lang == 'en':
            self.storage.put('language', status='en')
        elif lang == 'ru':
            self.storage.put('language', status='ru')

    def set_texture(self, identifier):
        cur_lang = self.storage.get('language')['status']
        id_texture_map = None
        if cur_lang == 'en':
            id_texture_map = ENG_ID_TEXTURE_MAP
        elif cur_lang == 'ru':
            id_texture_map = RU_ID_TEXTURE_MAP
        return id_texture_map[identifier]
