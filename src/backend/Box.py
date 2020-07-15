class Box:
    def __init__(self, x, y, size, i, j, kind, id=0):
        self.x = x
        self.y = y
        self.size = size
        self.i = i
        self.j = j
        self.kind = kind
        self.id = id
        self.animations = []
        self.rules = []

    def __str__(self):
        return 'Box' + str(self.kind)

    def add_rule(self, rule):
        if rule not in self.rules:
            self.rules.append(rule)

