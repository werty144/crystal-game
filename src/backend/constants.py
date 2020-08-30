from os.path import dirname, abspath, join

UP = 'UP'
DOWN = 'DOWN'
RIGHT = 'RIGHT'
LEFT = 'LEFT'

PROJECT_PATH = dirname(dirname(dirname(abspath(__file__))))
FRONTEND_PATH = join(PROJECT_PATH, 'src', 'frontend')
LEVELS_PATH = join(PROJECT_PATH, 'resources', 'levels')
IMAGES_PATH = join(PROJECT_PATH, 'resources', 'images')
SOUND_PATH = join(PROJECT_PATH, 'resources', 'sound')
KV_FILE_PATH = join(FRONTEND_PATH, 'crystal_game.kv')
STORAGE_PATH = join(PROJECT_PATH, 'resources', 'storage', 'storage.js')

FRAME_RATE_SEC = 0.01

FALLING_SOUND_DELAY = 0.15

KIND_BOX_ATLAS_ID_MAP = {
    1: 'red_yan',
    2: 'green_yan',
    3: 'blue_yan',
    4: 'yellow_yan',
    5: 'purple_yan',
}

KIND_RULE_ATLAS_ID_MAP = {
    1: 'rule_red',
    2: 'rule_green',
    3: 'rule_blue',
    4: 'rule_yellow',
    5: 'rule_purple'
}

BOX_ATLAS_URL = 'atlas://' + IMAGES_PATH + '/boxesatlas/'
RULE_ATLAS_URL = 'atlas://' + IMAGES_PATH + '/rule_atlas/'

UP_ARROW_IMAGE = join(IMAGES_PATH, 'up_arrow.png')
RIGHT_ARROW_IMAGE = join(IMAGES_PATH, 'right_arrow.png')
LEFT_ARROW_IMAGE = join(IMAGES_PATH, 'left_arrow.png')

BUTTONS_WIDTH_COEF = 1 / 15

STANDARD_MARGIN = 1 / 80

SCROLL_VIEW_PARAMETERS = {
    'horizontal_coef': 1 / 4,
    'right_margin_coef': STANDARD_MARGIN,
    'bot_margin_coef': STANDARD_MARGIN,
    'top_margin_coef': STANDARD_MARGIN
}

FIELD_PARAMETERS = {
    'horizontal_coef': 1 - BUTTONS_WIDTH_COEF - STANDARD_MARGIN * 2 - SCROLL_VIEW_PARAMETERS['horizontal_coef'] -
                       SCROLL_VIEW_PARAMETERS['right_margin_coef'],
    'bot_margin_coef': STANDARD_MARGIN,
    'top_margin_coef': STANDARD_MARGIN,
    'x_coef': BUTTONS_WIDTH_COEF + STANDARD_MARGIN,
    'border_width': 10
}


ID_TEXTURE_MAP = {
    'up_arrow': join(IMAGES_PATH, 'up_arrow.png'),
    'right_arrow': join(IMAGES_PATH, 'right_arrow.png'),
    'left_arrow': join(IMAGES_PATH, 'left_arrow.png'),
    'button_yellow_pressed': join(IMAGES_PATH, 'button_yellow_pressed.png'),
    'button_yellow': join(IMAGES_PATH, 'button_yellow.png'),
    'button': join(IMAGES_PATH, 'button.png'),
    'button_green': join(IMAGES_PATH, 'button_green.png'),
    'button_green_pressed': join(IMAGES_PATH, 'button_green_pressed.png'),
    'button_red': join(IMAGES_PATH, 'button_red.png'),
    'button_red_pressed': join(IMAGES_PATH, 'button_red_pressed.png'),
    'no_rules': join(IMAGES_PATH, 'no_rules.jpg'),
    'notebook': join(IMAGES_PATH, 'notebook.jpg'),
    'you_win': join(IMAGES_PATH, 'you_win.png'),
    'menu_background': join(IMAGES_PATH, 'menu_background.png'),
    'star': join(IMAGES_PATH, 'star.png'),
    'opened_envelope': join(IMAGES_PATH, 'opened_envelope.png'),
    'opened_envelope1': join(IMAGES_PATH, 'opened_envelope1.png'),
    'opened_envelope2': join(IMAGES_PATH, 'opened_envelope2.png'),
    'opened_envelope3': join(IMAGES_PATH, 'opened_envelope3.png'),
    'closed_envelope': join(IMAGES_PATH, 'closed_envelope.png'),
    'back_btn': join(IMAGES_PATH, 'back_btn.png'),
    'restart_btn': join(IMAGES_PATH, 'restart_btn.png'),
    'background': join(IMAGES_PATH, 'background.png'),
    'undo_btn': join(IMAGES_PATH, 'undo_btn.png'),
    'levels_label_btn': join(IMAGES_PATH, 'levels_label_btn.png'),
    'next_lvl_label_btn': join(IMAGES_PATH, 'next_lvl_label_btn.png'),
    'restart_label_btn': join(IMAGES_PATH, 'restart_label_btn.png')
}

ENG_ID_TEXTURE_MAP = {
    'all_rules_btn': join(IMAGES_PATH, 'all_rules_btn_eng.png'),
    **ID_TEXTURE_MAP
}

RU_ID_TEXTURE_MAP = {
    'all_rules_btn': join(IMAGES_PATH, 'button_ru.png'),
    **ID_TEXTURE_MAP
}

IMAGE_RATIOS = {
    'button_red': 256 / 256,
    'button': 488 / 488,
    'en_flag': 1024 / 683,
    'ru_flag': 1024 / 683,
    'opened_envelope': 3259 / 3439,
    'closed_envelope': 3259 / 3439,
    'all_rules': 1280 / 192,
    'restart': 843 / 921,
    'back': 1209 / 983,
    'undo': 584 / 463,
    'levels_label_btn': 2359 / 1322,
    'next_lvl_label_btn': 2359 / 1322,
    'restart_label_btn': 2359 / 1322
}

MODULE_AMOUNT = 3

STARS_PER_MODULE = {
    1: 2,
    2: 2,
    3: 7
}

MODULE_OFFSET = {
    1: 0,
    2: 20,
    3: 40
}

LEVELS_PER_MODULE = {
    1: 20,
    2: 20,
    3: 20
}
