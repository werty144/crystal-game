from os.path import dirname, abspath, join

UP = 'UP'
DOWN = 'DOWN'
RIGHT = 'RIGHT'
LEFT = 'LEFT'

PROJECT_PATH = dirname(dirname(dirname(abspath(__file__))))
LEVELS_PATH = join(PROJECT_PATH, 'resources', 'levels')
IMAGES_PATH = join(PROJECT_PATH, 'resources', 'images')
KV_FILE_PATH = join(PROJECT_PATH, 'src', 'frontend', 'crystal_game.kv')
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
