class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __repr__(self):
        return f'P({self.x}, {self.y})'


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def divide_in_ratio(self, ratio):
        assert ratio <= 1
        return self.p1 + (self.p2 - self.p1) * ratio


