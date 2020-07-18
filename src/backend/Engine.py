from src.backend.Box import Box
from src.backend.LevelParser import parse
from src.backend.Rule import Rule
from src.backend.ScreenUtils import ScreenUtils
from src.backend.constants import *
from src.backend.Animation import *
from src.backend.Geometry import *
import time
from src.backend.Exception import *


def map_kind_to_texture_source(kind):
    return join(IMAGES_PATH, 'yan.jpg')


class Engine:
    def __init__(self, cur_lvl):
        self.field, self.target = parse(cur_lvl)
        self.boxes = []
        self.animations = []
        self.screen_utils = ScreenUtils(self.field.rows)
        self.init_boxes()
        # box = self.field[1][1]
        # anim1 = Steady_linear_movement_animation(box, Point(200, 200))
        # anim2 = Steady_linear_movement_animation(box, Point(200, 300), start_point=Point(200, 200))
        # anim3 = Steady_linear_movement_animation(box, Point(300, 300), start_point=Point(200, 300))
        # self.add_animation(anim1 + anim2 + anim3)

        # self.adjust_rule(self.field[2][1], self.field[2][1].rules[1])
        # print(self.field)

    def init_boxes(self):
        for i in range(self.field.rows):
            for box in self.field[i]:
                if box is not None:
                    self.add_box(box)

    def add_animation(self, animation):
        self.animations.append(animation)

    def add_box(self, box):
        if any(obj.game_id == box.game_id for obj in self.all_game_objects()):
            raise AlreadyExistsException('Object with such id already exists')
        box_center = self.screen_utils.get_start_point(box.i, box.j)
        box.x, box.y = box_center[0], box_center[1]
        cell_side = self.screen_utils.get_cell_side_length()
        box.size = (cell_side, cell_side)
        box.source = map_kind_to_texture_source(box.kind)
        self.boxes.append(box)
        self.field[box.i][box.j] = box

    '''Needs to be applied after each rule to source box'''

    def remove_box(self, box):
        self.boxes.remove(box)

    def get_spare_id(self):
        id_list = [box.game_id for box in self.boxes]
        for i in range(1, len(id_list) + 2):
            if i not in id_list:
                return i

    # TODO fix appearing of the box on the screen after adding
    def box_fall(self, box):
        i = box.i
        while i + 1 < self.field.rows and self.field[i + 1][box.j] is None:
            i += 1
        if i != box.i:
            p = self.screen_utils.get_start_point(i, box.j)
            box.i = i
            return p
        return self.screen_utils.get_start_point(box.i, box.j)

    def apply_fall(self, i, j):
        new_i = self.field[i][j].i
        new_j = self.field[i][j].j
        if new_i != i or new_j != j:
            self.field[new_i][new_j] = self.field[i][j]
            self.field[i][j] = None

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
                    finish_point = self.box_fall(self.field([i][j]))
                    self.add_animation(Steady_linear_movement_animation(self.field([i][j]),
                                                                        Point(finish_point[0], finish_point[1])))
                    self.apply_fall(i, j)
            else:
                for i in range(0, box.i - rule_len + 1):
                    if self.field[i + rule_len - 1][j] is None:
                        continue
                    self.field[i][j] = self.field[i + rule_len - 1][j]
                    start_point = self.screen_utils.get_start_point(i + rule_len - 1, j)
                    finish_point = self.screen_utils.get_start_point(i, j)
                    self.add_animation(Steady_linear_movement_animation(self.field[i][j],
                                                                        Point(finish_point[0], finish_point[1]),
                                                                        start_point=Point(start_point[0],
                                                                                          start_point[1])))
                    self.field[i][j].i = i
                for i in range(box.i - rule_len + 1, box.i):
                    # TODO fix generation parameters, add rules generation when adding new box
                    self.add_box(Box(i, j, rule.result_box_kinds[box.i - i],
                                     game_id=self.get_spare_id()))
                    start_point = self.screen_utils.get_start_point(box.i, j)
                    finish_point = self.screen_utils.get_start_point(i, j)
                    self.add_animation(Steady_linear_movement_animation(self.field[i][j],
                                                                        Point(finish_point[0], finish_point[1]),
                                                                        start_point=Point(start_point[0],
                                                                                          start_point[1])))
                i = box.i
                self.remove_box(self.field[i][j])
                self.add_box(Box(i, j, rule.result_box_kinds[0], game_id=self.get_spare_id()))
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
                    finish_point = self.screen_utils.get_start_point(i, k)
                    anim1 = Steady_linear_movement_animation(self.field[i][k], Point(finish_point[0], finish_point[1]))
                    self.field[i][k].j = k
                    start_point = finish_point
                    finish_point = self.box_fall(self.field[i][k])
                    anim2 = Steady_linear_movement_animation(self.field[i][k], Point(finish_point[0], finish_point[1]),
                                                             start_point=Point(start_point[0], start_point[1]))
                    self.add_animation(anim1 + anim2)
                    self.apply_fall(i, k)

                # TODO fix generation parameters, add rules generation when adding new box
                self.add_box(Box(i, j + 1, rule.result_box_kinds[0],
                                 game_id=self.get_spare_id()))
                start_point = self.screen_utils.get_start_point(i, j)
                finish_point = self.screen_utils.get_start_point(i, j + 1)
                anim1 = Steady_linear_movement_animation(self.field[i][j + 1], Point(finish_point[0], finish_point[1]),
                                                         start_point=Point(start_point[0], start_point[1]))
                start_point = finish_point
                finish_point = self.box_fall(self.field[i][j + 1])
                anim2 = Steady_linear_movement_animation(self.field[i][j + 1], Point(finish_point[0], finish_point[1]),
                                                         start_point=Point(start_point[0], start_point[1]))
                self.add_animation(anim1 + anim2)
                self.apply_fall(i, j + 1)
                self.remove_box(self.field[i][j])
                self.add_box(Box(i, j, rule.result_box_kinds[1], game_id=self.get_spare_id()))

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
                    finish_point = self.screen_utils.get_start_point(i, k)
                    anim1 = Steady_linear_movement_animation(self.field[i][k], Point(finish_point[0], finish_point[1]))
                    self.field[i][k].j = k
                    start_point = finish_point
                    finish_point = self.box_fall(self.field[i][k])
                    anim2 = Steady_linear_movement_animation(self.field[i][k], Point(finish_point[0], finish_point[1]),
                                                             start_point=Point(start_point[0], start_point[1]))
                    self.add_animation(anim1 + anim2)
                    self.apply_fall(i, k)
                # TODO fix generation parameters, add rules generation when adding new box
                self.add_box(Box(i, j - 1, rule.result_box_kinds[0],
                                 game_id=self.get_spare_id()))
                start_point = self.screen_utils.get_start_point(i, j)
                finish_point = self.screen_utils.get_start_point(i, j - 1)
                anim1 = Steady_linear_movement_animation(self.field[i][j - 1], Point(finish_point[0], finish_point[1]),
                                                         start_point=Point(start_point[0], start_point[1]))
                start_point = finish_point
                finish_point = self.box_fall(self.field[i][j - 1])
                anim2 = Steady_linear_movement_animation(self.field[i][j - 1], Point(finish_point[0], finish_point[1]),
                                                         start_point=Point(start_point[0], start_point[1]))
                self.add_animation(anim1 + anim2)
                self.apply_fall(i, j - 1)
                self.remove_box(self.field[i][j])
                self.add_box(Box(i, j, rule.result_box_kinds[1], game_id=self.get_spare_id()))

    def get_rules(self, obj_id):
        for box in self.boxes:
            if box.game_id == obj_id:
                return box.rules

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
