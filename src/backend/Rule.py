from src.backend.constants import *


class Rule:
    def __init__(self, initial_box_kind, direction, *result_box_kinds):
        self.marginal = direction == LEFT or direction == RIGHT
        self.direction = direction
        self.initial_box_kind = initial_box_kind
        self.result_box_kinds = result_box_kinds

    def __repr__(self):
        return f'Rule(direction: {self.direction}, init_box: {self.initial_box_kind}, ' \
               f'res_boxes: {self.result_box_kinds})'
