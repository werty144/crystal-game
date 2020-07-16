from src.backend.Box import Box
from src.backend.LevelParser import parse
from src.backend.Rule import Rule
from src.backend.ScreenUtils import ScreenUtils
from src.backend.constants import *
from src.backend.Animation import *
from src.backend.Geometry import *
import time


class Engine:
    def __init__(self, cur_lvl):
        self.field, self.target = parse(cur_lvl)
        self.boxes = []
        self.animations = []
        self.screen_utils = ScreenUtils(self.field.rows)
        for i in range(self.field.rows):
            for box in self.field[i]:
                if box is not None:
                    self.boxes.append(box)
        print(self.field)
        self.adjust_rule(self.field[1][1], self.field[1][1].rules[1])
        print(self.field)
        # Example of adding animation
        # self.add_animation(Steady_linear_movement_animation(self.boxes[0], Point(400, 300)))

    def add_animation(self, animation):
        self.animations.append(animation)

    def box_fall(self, box):
        i = box.i
        while i + 1 < self.field.rows and self.field[i + 1][box.j] is None:
            i += 1
        if i != box.i:
            self.field[i][box.j] = box
            p = self.screen_utils.get_center(i, box.j)
            self.add_animation(Steady_linear_movement_animation(box, Point(p[0], p[1])))
            self.field[box.i][box.j] = None

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
                    p = self.screen_utils.get_center(i, j)
                    self.add_animation(Steady_linear_movement_animation(self.field[i][j], Point(p[0], p[1])))
                    self.field[i][j].i = i
                for i in range(box.i - rule_len + 1, box.i):
                    # TODO fix generation parameters, add rules generation when adding new box
                    p = self.screen_utils.get_center(box.i, j)
                    self.field[i][j] = Box(p[0], p[1], 100, i, j, rule.result_box_kinds[box.i - i])
                    self.boxes.append(self.field[i][j])
                    p = self.screen_utils.get_center(i, j)
                    self.add_animation(Steady_linear_movement_animation(self.field[i][j], Point(p[0], p[1])))
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
                    p = self.screen_utils.get_center(i, k)
                    self.add_animation(Steady_linear_movement_animation(self.field[i][k], Point(p[0], p[1])))
                    self.box_fall(self.field[i][k])
                # TODO fix generation parameters, add rules generation when adding new box
                p = self.screen_utils.get_center(i, j + 1)
                self.field[i][j + 1] = Box(p[0], p[1], 100, i, j + 1, rule.result_box_kinds[1])
                self.boxes.append(self.field[i][j + 1])
                self.box_fall(self.field[i][j + 1])
                p = self.screen_utils.get_center(i, j)
                self.field[i][j] = Box(p[0], p[1], 100, i, j, rule.result_box_kinds[0])
                self.boxes.append(self.field[i][j])
                self.add_animation(Steady_linear_movement_animation(self.field[i][j], Point(p[0], p[1])))

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
                    p = self.screen_utils.get_center(i, k)
                    self.add_animation(Steady_linear_movement_animation(self.field[i][k], Point(p[0], p[1])))
                    self.box_fall(self.field[i][k])
                # TODO fix generation parameters, add rules generation when adding new box
                p = self.screen_utils.get_center(i, j)
                self.field[i][j - 1] = Box(p[0], p[1], 100, i, j - 1, rule.result_box_kinds[0])
                p = self.screen_utils.get_center(i, j - 1)
                self.add_animation(Steady_linear_movement_animation(self.field[i][j - 1], Point(p[0], p[1])))
                self.boxes.append(self.field[i][j - 1])
                self.box_fall(self.field[i][j - 1])
                self.field[i][j] = Box(p[0], p[1], 100, i, j, rule.result_box_kinds[1])
                self.boxes.append(self.field[i][j])

    def tick(self):
        to_remove = []
        for animation in self.animations:
            if animation.finished:
                to_remove.append(animation)
                continue
            animation.tick(FRAME_RATE_SEC)
        for animation in to_remove:
            self.animations.remove(animation)

    def all_game_objects(self):
        return self.boxes
