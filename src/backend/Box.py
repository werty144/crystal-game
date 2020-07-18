class Box:
    def __init__(self, i, j, kind, game_id=0):
        self.x = None
        self.y = None
        self.size = None
        self.i = i
        self.j = j
        self.kind = kind
        self.game_id = game_id
        self.source = ''
        self.rules = []

    def __str__(self):
        return 'Box' + str(self.kind)

    def add_rule(self, rule):
        if rule not in self.rules:
            self.rules.append(rule)

