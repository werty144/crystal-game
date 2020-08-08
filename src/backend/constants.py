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

KIND_IMAGE_MAP = {
    1: join(IMAGES_PATH, 'red_yan.png'),
    2: join(IMAGES_PATH, 'green_yan.png'),
    3: join(IMAGES_PATH, 'blue_yan.png'),
    4: join(IMAGES_PATH, 'yellow_yan.png'),
    5: join(IMAGES_PATH, 'purple_yan.png')
}

KIND_ATLAS_ID_MAP = {
    1: 'red_yan',
    2: 'green_yan',
    3: 'blue_yan',
    4: 'yellow_yan',
    5: 'purple_yan',
}

BOX_ATLAS_URL = 'atlas://' + IMAGES_PATH + '/boxesatlas/'

UP_ARROW_IMAGE = join(IMAGES_PATH, 'up_arrow.png')
RIGHT_ARROW_IMAGE = join(IMAGES_PATH, 'right_arrow.png')
LEFT_ARROW_IMAGE = join(IMAGES_PATH, 'left_arrow.png')
BUTTON_YELLOW_PRESSED_IMAGE = join(IMAGES_PATH, 'button_yellow_pressed.png')
BUTTON_YELLOW_IMAGE = join(IMAGES_PATH, 'button_yellow.png')
BUTTON_IMAGE = join(IMAGES_PATH, 'button.png')
BUTTON_GREEN_IMAGE = join(IMAGES_PATH, 'button_green.png')
BUTTON_GREEN_PRESSED_IMAGE = join(IMAGES_PATH, 'button_green_pressed.png')
BUTTON_RED_IMAGE = join(IMAGES_PATH, 'button_red.png')
BUTTON_RED_PRESSED_IMAGE = join(IMAGES_PATH, 'button_red_pressed.png')
NO_RULES_IMAGE = join(IMAGES_PATH, 'no_rules.jpg')
NOTEBOOK_IMAGE = join(IMAGES_PATH, 'notebook.jpg')
YOU_WIN_IMAGE = join(IMAGES_PATH, 'you_win.jpg')

BUTTONS_WIDTH_COEF = 1 / 10

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
    'x_coef': BUTTONS_WIDTH_COEF + STANDARD_MARGIN
}


ENG_ID_TEXTURE_MAP = {
    'all_rules_btn': join(IMAGES_PATH, 'button_eng.png')
}

RU_ID_TEXTURE_MAP = {
    'all_rules_btn': join(IMAGES_PATH, 'button_ru.png')
}
