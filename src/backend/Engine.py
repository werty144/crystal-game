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
    return BOX_ATLAS_URL + KIND_ATLAS_ID_MAP[kind]


class Engine:
    def __init__(self, cur_lvl):
        self.field, self.target, self.kind_to_rules = parse(cur_lvl)
        self.boxes = []
        self.animations = []
        self.screen_utils = ScreenUtils(self.field.rows)
        self.win = False
        self.init_boxes()

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
        box.game_id = self.get_spare_id()
        box_center = self.screen_utils.get_start_point(box.i, box.j)
        box.x, box.y = box_center[0], box_center[1]
        cell_side = self.screen_utils.get_cell_side_length()
        box.size = (cell_side, cell_side)
        box.source = map_kind_to_texture_source(box.kind)
        box.rules = self.kind_to_rules[box.kind]
        self.boxes.append(box)
        self.field[box.i][box.j] = box

    '''Needs to be applied after each rule to source box'''

    def remove_box(self, box):
        self.boxes.remove(box)
        if self.field[box.i][box.j] == box:
            self.field[box.i][box.j] = None

    def get_spare_id(self):
        id_list = [box.game_id for box in self.boxes]
        for i in range(1, len(id_list) + 2):
            if i not in id_list:
                return i

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

    def move_up(self, box, i):
        self.field[i][box.j] = box
        start_point = self.screen_utils.get_start_point(box.i, box.j)
        finish_point = self.screen_utils.get_start_point(i, box.j)
        self.add_animation(Smooth_linear_movement_animation(box,
                                                            Point(finish_point[0], finish_point[1]),
                                                            start_point=Point(start_point[0],
                                                                              start_point[1])))
        box.i = i

    def move_aside(self, box, j):
        i = box.i
        self.field[i][j] = box
        finish_point = self.screen_utils.get_start_point(i, j)
        anim1 = Smooth_linear_movement_animation(box, Point(finish_point[0], finish_point[1]))
        box.j = j
        start_point = finish_point
        finish_point = self.box_fall(box)
        anim2 = Falling_linear_movement_animation(box, Point(finish_point[0], finish_point[1]),
                                                  start_point=Point(start_point[0], start_point[1]))
        self.add_animation(anim1 + anim2)
        self.apply_fall(i, j)

    def adjust_rule(self, box, rule):
        if rule.initial_box_kind != box.kind:
            # TODO throw error
            return box
        rows = self.field.rows
        cols = self.field.cols
        rule_len = len(rule.result_box_kinds)
        if rule.direction == UP:
            j = box.j
            # Can't use rule
            if rule_len > 1 and self.field[rule_len - 2][box.j] is not None:
                # TODO can't use rule
                return box
            # Eps rule
            if rule_len == 0:
                self.remove_box(box)
                # Apply box_fall for each box
                for i in range(box.i - 1, -1, -1):
                    if self.field[i][j] is None:
                        break
                    finish_point = self.box_fall(self.field[i][j])
                    self.add_animation(Falling_linear_movement_animation(self.field[i][j],
                                                                         Point(finish_point[0], finish_point[1])))
                    self.apply_fall(i, j)
            else:
                # Move every box above initial by rule_len - 1
                for i in range(0, box.i - rule_len + 1):
                    if self.field[i + rule_len - 1][j] is None:
                        continue
                    self.move_up(self.field[i + rule_len - 1][j], i)
                # Add boxes according to the rule
                for i in range(box.i - rule_len + 1, box.i):
                    self.add_box(Box(i, j, rule.result_box_kinds[box.i - i]))
                    start_point = self.screen_utils.get_start_point(box.i, j)
                    finish_point = self.screen_utils.get_start_point(i, j)
                    self.add_animation(Smooth_linear_movement_animation(self.field[i][j],
                                                                        Point(finish_point[0], finish_point[1]),
                                                                        start_point=Point(start_point[0],
                                                                                          start_point[1])))
                # Change initial box
                i = box.i
                self.remove_box(self.field[i][j])
                self.add_box(Box(i, j, rule.result_box_kinds[0]))
                box = self.field[i][j]
        elif rule.marginal:
            i = box.i
            j = box.j
            if rule.direction == RIGHT:
                # No empty cols to the right
                if j == cols - 1:
                    return box
                # Check if can apply rule
                first_none = -1
                for k in range(j, cols):
                    if self.field[i][k] is None:
                        first_none = k
                        break
                if first_none == -1:
                    return box
                for k in range(first_none, j + 1, -1):
                    self.move_aside(self.field[i][k - 1], k)

                self.remove_box(self.field[i][j])
                self.add_box(Box(i, j, rule.result_box_kinds[1]))
                box = self.field[i][j]
                self.move_aside(self.field[i][j], j + 1)
                self.add_box(Box(i, j, rule.result_box_kinds[0]))

            elif rule.direction == LEFT:
                if j == 0:
                    return box
                first_none = -1
                for k in range(j, -1, -1):
                    if self.field[i][k] is None:
                        first_none = k
                        break
                if first_none == -1:
                    return box
                for k in range(first_none, j - 1):
                    self.move_aside(self.field[i][k + 1], k)
                self.remove_box(self.field[i][j])
                self.add_box(Box(i, j, rule.result_box_kinds[0]))
                box = self.field[i][j]
                self.move_aside(self.field[i][j], j - 1)
                self.add_box(Box(i, j, rule.result_box_kinds[1]))
        return box

    def get_box(self, obj_id):
        for box in self.boxes:
            if box.game_id == obj_id:
                return box

    @staticmethod
    def box_to_string(maybe_box):
        if maybe_box is None:
            return 'None'
        return str(maybe_box.kind)

    def check_win(self):
        cur_field = [[self.box_to_string(box) for box in row] for row in self.field]
        if cur_field == self.target:
            self.win = True

    def process_animations(self):
        to_remove = []
        for animation in self.animations:
            if animation.finished:
                to_remove.append(animation)
                continue
            animation.tick(FRAME_RATE_SEC)
        for animation in to_remove:
            self.animations.remove(animation)

    def tick(self):
        self.check_win()
        self.process_animations()

    def any_animation_in_progress(self):
        return len(self.animations) > 0

    def all_game_objects(self):
        return self.boxes

    def get_target_field_boxes(self):
        res = []
        for i, row in enumerate(self.target):
            for j, maybe_box_kind in enumerate(row):
                if maybe_box_kind == 'None':
                    continue
                box_kind = int(maybe_box_kind)
                box = Box(i, j, box_kind)
                box_center = self.screen_utils.get_start_point(box.i, box.j)
                box.x, box.y = box_center[0], box_center[1]
                cell_side = self.screen_utils.get_cell_side_length()
                box.size = (cell_side, cell_side)
                box.source = map_kind_to_texture_source(box.kind)
                res.append(box)
        return res
