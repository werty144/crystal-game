class Box:
    def __init__(self, i, j, kind):
        self.i = i
        self.j = j
        self.kind = kind
        self.x = None
        self.y = None
        self.size = None
        self.game_id = None
        self.source = ''
        self.rules = []

    def __str__(self):
        return 'Box' + str(self.kind)

    def add_rule(self, rule):
        if rule not in self.rules:
            self.rules.append(rule)

