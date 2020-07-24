from kivy.core.window import Window
from src.backend.constants import SCROLL_VIEW_PARAMETERS, FIELD_PARAMETERS


class ScreenUtils:
    def compute_size(self):
        rows_number = self.rows_number
        cols_number = self.cols_number
        window_width = Window.size[0]
        window_height = Window.size[1]
        free_width_coef = FIELD_PARAMETERS['horizontal_coef']
        potential_width = window_width * free_width_coef
        potential_height = potential_width * (rows_number / cols_number)
        max_height = window_height * (1 - FIELD_PARAMETERS['top_margin_coef'] - FIELD_PARAMETERS['bot_margin_coef'])
        if potential_height <= max_height:
            return potential_width, potential_height
        shorten_width = max_height * (cols_number / rows_number)
        return shorten_width, max_height

    def compute_start_point(self):
        window_width = Window.size[0]
        window_height = Window.size[1]
        free_width_coef = FIELD_PARAMETERS['horizontal_coef']
        free_width = window_width * free_width_coef
        assert free_width >= self.size[0]
        x = window_width * FIELD_PARAMETERS['x_coef'] + (free_width - self.size[0]) / 2
        y = window_height * FIELD_PARAMETERS['bot_margin_coef']
        return x, y

    def __init__(self, rows_number, cols_number):
        self.rows_number = rows_number
        self.cols_number = cols_number
        self.size = self.compute_size()
        self.start = self.compute_start_point()
        self.points_centers = []
        self.init_start_points()

    def init_start_points(self):
        cell_width = self.size[0] / self.cols_number
        cell_heigth = self.size[1] / self.rows_number
        for i in range(self.rows_number):
            self.points_centers.append([])
            k = self.rows_number - i - 1
            for j in range(self.cols_number):
                self.points_centers[i].append((self.start[0] + cell_width * j, self.start[1] + cell_heigth * k))

    def get_start_point(self, i, j):
        return self.points_centers[i][j]

    def create_grid(self):
        cell_width = self.size[0] / self.cols_number
        cell_heigth = self.size[1] / self.rows_number
        points = []
        for i in range(self.cols_number + 1):
            points.append(((self.start[0] + cell_width * i, self.start[1]),
                           (self.start[0] + cell_width * i, self.start[1] + cell_heigth * self.rows_number)))
        for i in range(self.rows_number + 1):
            points.append(((self.start[0], self.start[1] + cell_heigth * i),
                           (self.start[0] + cell_width * self.cols_number, self.start[1] + cell_heigth * i)))

        return points

    def get_cell_size(self):
        return self.size[0] / self.cols_number, self.size[1] / self.rows_number

    @staticmethod
    def get_scrollview_pos_n_size():
        window_width = Window.size[0]
        window_height = Window.size[1]
        horizontal_coef = SCROLL_VIEW_PARAMETERS['horizontal_coef']
        right_margin_coef = SCROLL_VIEW_PARAMETERS['right_margin_coef']
        bot_margin_coef = SCROLL_VIEW_PARAMETERS['bot_margin_coef']
        top_margin_coef = SCROLL_VIEW_PARAMETERS['top_margin_coef']
        h = window_height * (1 - top_margin_coef - bot_margin_coef)
        w = window_width * horizontal_coef
        return (window_width * (1 - horizontal_coef - right_margin_coef), window_height * bot_margin_coef),\
               (w, h)
