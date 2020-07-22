from kivy.core.window import Window


class ScreenUtils:
    def __init__(self, rows_number, cols_number, start_point, size):
        self.size = size
        self.rows_number = rows_number
        self.cols_number = cols_number
        self.points_centers = []
        self.start = start_point
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
        return (self.size[0] / self.cols_number, self.size[1] / self.rows_number)

    def get_scrollview_size(self):
        h = Window.size[1] * 3 / 4
        w = Window.size[0] / 3
        return (2 * w - 10, 75), (w, h)
