from src.backend.Box import Box
from src.backend.LevelParser import parse
from src.backend.Rule import Rule
from src.backend.constants import *


class Engine:
    def __init__(self, cur_lvl):
        self.field, self.target = parse(cur_lvl)
        self.boxes = []
        for i in range(self.field.rows):
            for box in self.field[i]:
                if box is not None:
                    self.boxes.append(box)

    # TODO add implementation
    def add_animation(self, box, start, finish):
        pass

    def box_fall(self, box):
        i = box.i
        while i + 1 < self.field.rows and self.field[i + 1][box.j] is None:
            i += 1
        if i != box.i:
            self.field[i][box.j] = box
            self.add_animation(box, (box.i, box.j), (i, box.j))
            self.field[box.i][box.j] = None
            box.i = i

    def adjust_rule(self, box, rule):
        if rule.initial_box_kind != box.kind:
            # TODO throw error
            return
        rows = self.field.rows
        cols = self.field.cols
        rule_len = len(rule.result_box_kinds)
        if rule.direction == UP:
            j = box.j
            if rule_len > 1 and self.field[rule_len - 2][box.j] is not None:
                # TODO can't use rule
                return
            if rule_len == 0:
                self.field[box.i][box.j] = None
                for i in range(box.i, -1, -1):
                    if self.field[i][j] is None:
                        break
                    self.box_fall(self.field([i][j]))
            else:
                for i in range(0, box.i - rule_len + 1):
                    if self.field[i + rule_len - 1][j] is None:
                        continue
                    self.field[i][j] = self.field[i + rule_len - 1][j]
                    self.add_animation(self.field[i][j], (i + rule_len - 1, j), (i, j))
                    self.field[i][j].i = i
                for i in range(box.i - rule_len + 1, box.i):
                    # TODO fix generation parameters, add rules generation when adding new box
                    self.field[i][j] = Box(100, 200, 150, i, j, rule.result_box_kinds[box.i - i])
                    self.add_animation(self.field[i][j], (box.i, j), (i, j))
                self.field[box.i][j].kind = rule.result_box_kinds[0]
        elif rule.marginal:
            i = box.i
            j = box.j
            if rule.direction == RIGHT:
                if j == cols - 1:
                    return
                first_none = -1
                for k in range(j, cols):
                    if self.field[i][k] is None:
                        first_none = k
                        break
                if first_none == -1:
                    return
                for k in range(first_none, j + 1, -1):
                    self.field[i][k] = self.field[i][k - 1]
                    self.field[i][k].j = k
                    self.add_animation(self.field[i][k], (i, k - 1), (i, k))
                    self.box_fall(self.field[i][k])
                # TODO fix generation parameters, add rules generation when adding new box
                self.field[i][j + 1] = Box(100, 200, 150, i, j + 1, rule.result_box_kinds[1])
                self.box_fall(self.field[i][j + 1])
                self.field[i][j] = Box(100, 200, 150, i, j, rule.result_box_kinds[0])

            elif rule.direction == LEFT:
                if j == 0:
                    return
                first_none = -1
                for k in range(j, -1, -1):
                    if self.field[i][k] is None:
                        first_none = k
                        break
                if first_none == -1:
                    return
                for k in range(first_none, j - 1):
                    self.field[i][k] = self.field[i][k + 1]
                    self.field[i][k].j = k
                    self.add_animation(self.field[i][k], (i, k + 1), (i, k))
                    self.box_fall(self.field[i][k])
                # TODO fix generation parameters, add rules generation when adding new box
                self.field[i][j - 1] = Box(100, 200, 150, i, j - 1, rule.result_box_kinds[0])
                self.box_fall(self.field[i][j - 1])
                self.field[i][j] = Box(100, 200, 150, i, j, rule.result_box_kinds[1])

    def tick(self):
        # for test purposes
        print(self.field)
        self.adjust_rule(self.field[1][1], self.field[1][1].rules[1])
        print(self.field)

        self.boxes[0].x += 2

    def all_game_objects(self):
        return self.boxes
