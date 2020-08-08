from src.backend.constants import ENG_ID_TEXTURE_MAP, RU_ID_TEXTURE_MAP

LANGUAGE = 'en'
ID_TEXTURE_MAP = ENG_ID_TEXTURE_MAP


def change_language(lang):
    global LANGUAGE, ID_TEXTURE_MAP
    LANGUAGE = lang
    if lang == 'eng':
        ID_TEXTURE_MAP = ENG_ID_TEXTURE_MAP
    if lang == 'ru':
        ID_TEXTURE_MAP = RU_ID_TEXTURE_MAP


def set_texture(identifier):
    return ID_TEXTURE_MAP[identifier]
