from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Line, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


class BoxWidget(ButtonBehavior, Image):
    def __init__(self, obj):
        super(BoxWidget, self).__init__()
        setattr(self, 'game_id', obj.game_id)
        for attr, value in obj.__dict__.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        self.box = obj
        self.rules = self.box.rules
        self.border = None

    def on_release(self):
        self.parent.make_rules_scroll_view(self.rules, self.click_on_rule_function, str(id(self)) + str(self.rules))
        self.parent.select_box(self)

    def click_on_rule_function(self, rule):
        playground = self.parent
        engine = playground.engine
        self.box = engine.adjust_rule(self.box, rule)
        playground.make_rules_scroll_view(engine.get_all_rules(), lambda _: None, id(playground))
        playground.unselect_box()

    def select(self):
        if self.border is not None:
            return
        border = InstructionGroup()
        border.add(Color(232/256, 58/256, 88/256, 1))
        border.add(Line(width=2,
                        rectangle=(self.x, self.y, self.width, self.height)
                        ))
        self.border = border
        self.parent.canvas.add(self.border)

    def unselect(self):
        if self.border is None:
            return
        self.parent.canvas.remove(self.border)
        self.border = None

