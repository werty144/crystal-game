from os.path import dirname, abspath, join

UP = 'UP'
DOWN = 'DOWN'
RIGHT = 'RIGHT'
LEFT = 'LEFT'

project_path = dirname(dirname(dirname(abspath(__file__))))
levels_path = join(project_path, 'resources', 'levels')
images_path = join(project_path, 'resources', 'images')
