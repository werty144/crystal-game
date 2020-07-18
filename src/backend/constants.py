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
