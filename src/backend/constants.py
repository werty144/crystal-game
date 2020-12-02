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
STORAGE_FOLDER = join(PROJECT_PATH, 'resources', 'storage')
STORAGE_PATH = join(STORAGE_FOLDER, 'storage.js')

FRAME_RATE_SEC = 0.01

FALLING_SOUND_DELAY = 0.15

TUTORIAL_LABELS_AMOUNT = 13

KIND_BOX_ATLAS_ID_MAP = {
    1: 'red_box',
    2: 'green_box',
    3: 'blue_box',
    4: 'yellow_box',
    5: 'purple_box',
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
    'opened_envelope': join(IMAGES_PATH, 'opened_envelope.png'),
    'opened_envelope1': join(IMAGES_PATH, 'opened_envelope1.png'),
    'opened_envelope2': join(IMAGES_PATH, 'opened_envelope2.png'),
    'opened_envelope3': join(IMAGES_PATH, 'opened_envelope3.png'),
    'opened_envelope4': join(IMAGES_PATH, 'opened_envelope4.png'),
    'closed_envelope': join(IMAGES_PATH, 'closed_envelope.png'),
    'back_btn': join(IMAGES_PATH, 'back_btn.png'),
    'restart_btn': join(IMAGES_PATH, 'restart_btn.png'),
    'background': join(IMAGES_PATH, 'background.png'),
    'undo_btn': join(IMAGES_PATH, 'undo_btn.png'),
    'target_field_btn': join(IMAGES_PATH, 'target_field_btn.png'),
    'target_field_btn_switched': join(IMAGES_PATH, 'target_field_btn_switched.png'),
    'q_mark': join(IMAGES_PATH, 'q_mark.png'),
    'en_flag': join(IMAGES_PATH, 'en_flag.jpg'),
    'ru_flag': join(IMAGES_PATH, 'ru_flag.png'),
    'stamp': join(IMAGES_PATH, 'stamp.png'),
    'stamp_a': join(IMAGES_PATH, 'stamp_a.png'),
    'stamp_b': join(IMAGES_PATH, 'stamp_b.png'),
    'stamp_c': join(IMAGES_PATH, 'stamp_c.png'),
    'stamp_d': join(IMAGES_PATH, 'stamp_d.png'),
    'box_next_to': join(IMAGES_PATH, 'box_next_to.png'),
    'box_over': join(IMAGES_PATH, 'box_over.png'),
    'postbox_a': join(IMAGES_PATH, 'postbox_a.png'),
    'postbox_b': join(IMAGES_PATH, 'postbox_b.png'),
    'postbox_c': join(IMAGES_PATH, 'postbox_c.png'),
    'postbox_d': join(IMAGES_PATH, 'postbox_d.png'),
    'BrainMail': join(IMAGES_PATH, 'BrainMail.png'),
    'stars_popup_background': join(IMAGES_PATH, 'stars_popup_background.png'),
    'donat': join(IMAGES_PATH, 'donat.png'),
    'loading': join(IMAGES_PATH, 'loading.png'),
    'qiwi_logo': join(IMAGES_PATH, 'qiwi_logo.png'),
    'sber_logo': join(IMAGES_PATH, 'sber_logo.png'),
    'clipboard': join(IMAGES_PATH, 'clipboard.png')
}

ENG_ID_TEXTURE_MAP = {
    'all_rules_btn': join(IMAGES_PATH, 'all_rules_btn_eng.png'),
    'box_play': join(IMAGES_PATH, 'box_play_eng.png'),
    'box_quit': join(IMAGES_PATH, 'box_quit_eng.png'),
    'box_tutorial': join(IMAGES_PATH, 'box_tutorial_eng.png'),
    'levels_label_btn': join(IMAGES_PATH, 'levels_label_btn_eng.png'),
    'levels': join(IMAGES_PATH, 'levels_eng.png'),
    'next_lvl_label_btn': join(IMAGES_PATH, 'next_lvl_label_btn_eng.png'),
    'no_rules': join(IMAGES_PATH, 'no_rules_eng.png'),
    'postbox_label': join(IMAGES_PATH, 'postbox_label_eng.png'),
    'restart_label_btn': join(IMAGES_PATH, 'restart_label_btn_eng.png'),
    'you_win': join(IMAGES_PATH, 'you_win_eng.png'),
    **ID_TEXTURE_MAP
}

RU_ID_TEXTURE_MAP = {
    'all_rules_btn': join(IMAGES_PATH, 'all_rules_btn_ru.png'),
    'box_play': join(IMAGES_PATH, 'box_play_ru.png'),
    'box_quit': join(IMAGES_PATH, 'box_quit_ru.png'),
    'box_tutorial': join(IMAGES_PATH, 'box_tutorial_ru.png'),
    'levels_label_btn': join(IMAGES_PATH, 'levels_label_btn_ru.png'),
    'levels': join(IMAGES_PATH, 'levels_ru.png'),
    'next_lvl_label_btn': join(IMAGES_PATH, 'next_lvl_label_btn_ru.png'),
    'no_rules': join(IMAGES_PATH, 'no_rules_ru.png'),
    'postbox_label': join(IMAGES_PATH, 'postbox_label_ru.png'),
    'restart_label_btn': join(IMAGES_PATH, 'restart_label_btn_ru.png'),
    'you_win': join(IMAGES_PATH, 'you_win_ru.png'),
    **ID_TEXTURE_MAP
}

IMAGE_RATIOS = {
    'en_flag': 1024 / 683,
    'ru_flag': 1024 / 683,
    'opened_envelope': 3259 / 3439,
    'closed_envelope': 3259 / 3439,
    'all_rules': 1280 / 192,
    'restart': 128 / 126,
    'back': 228 / 228,
    'undo': 128 / 126,
    'levels_label_btn': 2359 / 1322,
    'next_lvl_label_btn': 2359 / 1322,
    'restart_label_btn': 2359 / 1322,
    'q_mark': 128 / 126,
    'stamp': 1353 / 955,
    'postbox': 360 / 428,
    'target_field': 128 / 126,
    'donat': 176 / 173
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
