from src.backend.LevelParser import parse


class Engine:
    def __init__(self, cur_lvl):
        self.field, self.target = parse(cur_lvl)
        self.boxes = []
        for i in range(self.field.rows):
            for box in self.field[i]:
                if box is not None:
                    self.boxes.append(box)

    def adjust_rule(self, box, rule):
        pass

    def tick(self):
        # for test purposes
        self.boxes[0].x += 2

    def all_game_objects(self):
        return self.boxes
