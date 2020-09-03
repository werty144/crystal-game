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

    def on_release(self):
        self.parent.make_rules_scroll_view(self.rules, self.click_on_rule_function, str(id(self)) + str(self.rules))

    def click_on_rule_function(self, rule):
        playground = self.parent
        engine = playground.engine
        self.box = engine.adjust_rule(self.box, rule)
        playground.make_rules_scroll_view(engine.get_all_rules(), lambda _: None, id(playground))
