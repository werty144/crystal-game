from kivy.core.window import Window


class ScreenUtils:
    def __init__(self, cells_number):
        self.window_sizes = Window.size
        self.table_size = min(self.window_sizes[0], self.window_sizes[1])
        self.cells_number = cells_number
        self.points_centers = []
        self.init_start_points()

    def init_start_points(self):
        size = self.table_size / self.cells_number
        indent = abs(self.window_sizes[0] - self.window_sizes[1]) / 2
        for i in range(self.cells_number):
            self.points_centers.append([])
            k = self.cells_number - i - 1
            for j in range(self.cells_number):
                if self.window_sizes[0] < self.window_sizes[1]:
                    self.points_centers[i].append((size * j, indent + size * k))
                else:
                    self.points_centers[i].append((indent + size * j, size * k))

    def get_start_point(self, i, j):
        return self.points_centers[i][j]

    def create_table(self):
        size = self.table_size / self.cells_number
        points = []
        indent = abs(self.window_sizes[0] - self.window_sizes[1]) / 2
        for i in range(self.cells_number + 1):
            if self.window_sizes[0] < self.window_sizes[1]:
                points.append(((size * i, indent), (size * i, indent + self.table_size)))
                points.append(((0, indent + size * i), (self.table_size, indent + size * i)))
            else:
                points.append(((indent + size * i, 0), (indent + size * i, self.table_size)))
                points.append(((indent, size * i), (indent + self.table_size, size * i)))

        return points
