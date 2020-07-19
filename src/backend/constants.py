from os.path import dirname, abspath, join

UP = 'UP'
DOWN = 'DOWN'
RIGHT = 'RIGHT'
LEFT = 'LEFT'

PROJECT_PATH = dirname(dirname(dirname(abspath(__file__))))
LEVELS_PATH = join(PROJECT_PATH, 'resources', 'levels')
IMAGES_PATH = join(PROJECT_PATH, 'resources', 'images')
ARROW_IMAGE = 'yan.jpg'

FRAME_RATE_SEC = 0.01

KIND_IMAGE_MAP = {
    1: join(IMAGES_PATH, 'red_yan.png'),
    2: join(IMAGES_PATH, 'green_yan.png'),
    3: join(IMAGES_PATH, 'blue_yan.png'),
    4: join(IMAGES_PATH, 'yellow_yan.png'),
    5: join(IMAGES_PATH, 'purple_yan.png')
}
