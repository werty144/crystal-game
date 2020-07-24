from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Line, Rectangle
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty, Property
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from src.backend.Engine import Engine
from src.backend.constants import FRAME_RATE_SEC
from src.frontend.custom_widgets.BoxWidget import BoxWidget
from src.frontend.custom_widgets.RuleWidget import RuleWidget


class Playground(Widget):
    engine = ObjectProperty()
    game_widgets = ListProperty()
    screen_utils = ObjectProperty()
    grid = ObjectProperty()
    target_field_widgets = ListProperty()
    is_target_field = BooleanProperty(False)
    scroll_view = Property(None)
    update_event = ObjectProperty(None, allownone=True)
    storage = ObjectProperty()

    def start(self, lvl):
        self.engine = Engine(lvl)
        self.add_missing_game_widgets()
        self.make_grid()
        self.set_target_field_widgets()
        self.make_scroll_view(self.engine.get_all_rules(), lambda _: None)
        self.update_event = Clock.schedule_interval(self.update, FRAME_RATE_SEC)

    def update(self, _):
        self.engine.tick()
        self.add_missing_game_widgets()
        self.update_all_game_widgets()
        self.check_win()

    def update_all_game_widgets(self):
        for game_widget in self.game_widgets:
            corresponding_game_obj = next((obj for obj in self.engine.all_game_objects()
                                           if obj.game_id == game_widget.game_id), None)
            if corresponding_game_obj is None:
                self.remove_widget(game_widget)
                self.game_widgets.remove(game_widget)
                continue
            self.update_game_widget(game_widget, corresponding_game_obj)

    @staticmethod
    def update_game_widget(game_widget, game_object):
        for attr, value in game_object.__dict__.items():
            if hasattr(game_widget, attr):
                setattr(game_widget, attr, value)

    def add_missing_game_widgets(self):
        for obj in self.engine.all_game_objects():
            if any(widg.game_id == obj.game_id for widg in self.game_widgets):
                continue
            wimg = BoxWidget(obj)
            self.game_widgets.append(wimg)
            self.add_widget(wimg)

    def check_win(self):
        if self.engine.win and not self.engine.any_animation_in_progress():
            self.storage.put('lvl' + str(self.engine.lvl), status='Passed')
            self.storage.put('lvl' + str(self.engine.lvl + 1), status='Unlocked')
            self.update_event.cancel()
            self.parent.show_winning_widget()

    def make_grid(self):
        self.grid = InstructionGroup()
        points = self.engine.screen_utils.create_grid()
        for a, b in points:
            self.grid.add(Line(points=[a[0], a[1], b[0], b[1]]))
        self.canvas.add(self.grid)

    def set_target_field_widgets(self):
        for box in self.engine.get_target_field_boxes():
            box_wimg = Image()
            for attr, value in box.__dict__.items():
                if hasattr(box_wimg, attr):
                    setattr(box_wimg, attr, value)
            self.target_field_widgets.append(box_wimg)

    def switch_field(self):
        if not self.is_target_field:
            self.parent.ids.field_switch.text = 'to game\nfield'
            for widg in self.game_widgets:
                self.remove_widget(widg)
            for box_wimg in self.target_field_widgets:
                self.add_widget(box_wimg)
        else:
            self.parent.ids.field_switch.text = 'to target\nfield'
            for widg in self.target_field_widgets:
                self.remove_widget(widg)
            for widg in self.game_widgets:
                self.add_widget(widg)
        self.is_target_field = not self.is_target_field

    def make_scroll_view(self, rules, click_on_rule_function):
        if self.scroll_view is not None:
            self.remove_widget(self.scroll_view)
        pos, size = self.engine.screen_utils.get_scrollview_pos_n_size()
        self.scroll_view = ScrollView(size_hint=(None, None), size=(size[0], size[1]), pos=(pos[0], pos[1]))
        layout = GridLayout(cols=1, spacing=50, padding=(0, 50), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        if len(rules) == 0:
            # Write that there is no rules
            self.scroll_view = ScrollView(size_hint=(None, None), size=(size[0], size[1]), pos=(pos[0], pos[1]))
            label = Label(text='No rules', color=(0, 0, 0, 1), font_size=(0.4 * min(self.height / 4, self.width)))
            self.scroll_view.add_widget(label)
            with self.scroll_view.canvas.before:
                Color(1, 1, 1, 1)
                Rectangle(size=self.scroll_view.size, pos=self.scroll_view.pos)
            self.add_widget(self.scroll_view)
            return
        max_right_side_len = max([len(rule.result_box_kinds) for rule in rules])
        for rule in rules:
            rule_widget = RuleWidget(rule, click_on_rule_function, max_right_side_len)
            layout.add_widget(rule_widget)
        self.scroll_view.add_widget(layout)
        with self.scroll_view.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(size=self.scroll_view.size, pos=self.scroll_view.pos)
        self.add_widget(self.scroll_view)

    def show_all_rules(self):
        self.make_scroll_view(self.engine.get_all_rules(), lambda rule: None)

    def on_touch_down(self, touch):
        if self.engine.any_animation_in_progress():
            return True
        return super(Playground, self).on_touch_down(touch)