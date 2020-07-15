class Field:
    def __init__(self, rows, cols):
        self.cols = cols
        self.rows = rows
        self.field = []
        for _ in range(rows):
            self.field.append([None] * cols)

    def __getitem__(self, item):
        return self.field[item]

    def __repr__(self):
        s = ''
        for i in range(self.rows):
            s += ' '.join(list(map(str, self.field[i]))) + '\n'
        return s

    def add_box(self, i, j, box):
        assert self.field[i][j] is None
        self.field[i][j] = box

    def remove_box(self, i, j):
        self.field[i][j] = None

    def get_col(self, i):
        return [self.field[j][i] for j in range(self.rows)]
