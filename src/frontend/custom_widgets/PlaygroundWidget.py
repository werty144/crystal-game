from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Line, Rectangle
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty, Property, DictProperty
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from src.frontend.custom_widgets.RulesScrollViewWidget import RulesScrollViewWidget

from src.backend.Engine import Engine
from src.backend.constants import FRAME_RATE_SEC
from src.backend.ModuleUtils import get_module
from src.frontend.custom_widgets.BoxWidget import BoxWidget
from src.frontend.custom_widgets.RuleWidget import RuleWidget


class Playground(Widget):
    engine = ObjectProperty()
    game_widgets = ListProperty()
    grid = ObjectProperty()
    target_field_widgets = ListProperty()
    is_target_field = BooleanProperty(False)
    rules_scroll_view = Property(None)
    update_event = ObjectProperty(None, allownone=True)
    storage = ObjectProperty()
    sound_handler = ObjectProperty()
    scroll_views = DictProperty()
    selected_box = ObjectProperty(allownone=True)

    def start(self, lvl):
        self.engine = Engine(lvl, self.sound_handler)
        self.init_storage_star()
        self.add_missing_game_widgets()
        self.draw_field()
        self.set_target_field_widgets()
        self.scroll_views = {}
        self.make_rules_scroll_view(self.engine.get_all_rules(), lambda _: None, id(self))
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
        game_widget.box = game_object
        for attr, value in game_object.__dict__.items():
            if hasattr(game_widget, attr):
                setattr(game_widget, attr, value)

    def add_missing_game_widgets(self):
        for obj in self.engine.all_game_objects():
            if any(widg.game_id == obj.game_id for widg in self.game_widgets):
                continue
            wimg = BoxWidget(obj, self.sound_handler)
            self.game_widgets.append(wimg)
            self.add_widget(wimg)

    def check_win(self):
        if self.engine.win and not self.engine.any_animation_in_progress():
            self.manage_star_after_win()
            self.update_storage(f'lvl{self.engine.lvl}', status='Passed')
            if self.storage.get('lvl' + str(self.engine.lvl + 1))['status'] == 'Locked':
                self.update_storage(f'lvl{self.engine.lvl + 1}', status='Unlocked')
            self.update_event.cancel()
            self.parent.show_winning_widget()

    def manage_star_after_win(self):
        if self.engine.min_moves and self.engine.moves_done <= self.engine.min_moves and \
                not self.storage.get(f'lvl{self.engine.lvl}')['got_star']:
            self.update_storage(f'lvl{self.engine.lvl}', got_star=True)
            cur_module = str(get_module(self.engine.lvl))
            module_stars = self.storage.get('module_stars')
            module_stars[cur_module] += 1
            self.storage.put('module_stars', **module_stars)

    def draw_field(self):
        with self.canvas.before:
            Color(0.992, 0.925, 0.863, 1)
            Rectangle(pos=self.engine.screen_utils.start,
                      size=self.engine.screen_utils.size)

        self.grid = InstructionGroup()
        points = self.engine.screen_utils.create_grid()
        self.grid.add(Color(rgba=(0.29, 0, 0.153, 1)))
        for a, b in points:
            self.grid.add(Line(points=[a[0], a[1], b[0], b[1]]))

        border_width = 5
        dl = self.engine.screen_utils.start
        width, height = self.engine.screen_utils.size
        self.grid.add(Line(points=[
            dl[0] - border_width, dl[1] - border_width,
            dl[0] - border_width, dl[1] + height + border_width,
            dl[0] + width + border_width, dl[1] + height + border_width,
            dl[0] + width + border_width, dl[1] - border_width
        ],
            width=border_width,
            close=True
        ))
        self.canvas.before.add(self.grid)

    def set_target_field_widgets(self):
        for box in self.engine.get_target_field_boxes():
            box_wimg = Image()
            for attr, value in box.__dict__.items():
                if hasattr(box_wimg, attr):
                    setattr(box_wimg, attr, value)
            self.target_field_widgets.append(box_wimg)

    def switch_field(self):
        self.show_all_rules()
        self.unselect_box()
        if not self.is_target_field:
            for widg in self.game_widgets:
                self.remove_widget(widg)
            for box_wimg in self.target_field_widgets:
                self.add_widget(box_wimg)
        else:
            for widg in self.target_field_widgets:
                self.remove_widget(widg)
            for widg in self.game_widgets:
                self.add_widget(widg)
        self.is_target_field = not self.is_target_field

    def show_all_rules(self):
        self.unselect_box()
        self.make_rules_scroll_view(self.engine.get_all_rules(), lambda _: None, id(self))

    def make_rules_scroll_view(self, rules, click_on_rule_function, obj_hash):
        if self.rules_scroll_view is not None:
            self.remove_widget(self.rules_scroll_view)
        if obj_hash in self.scroll_views:
            self.rules_scroll_view = self.scroll_views[obj_hash]
            self.add_widget(self.rules_scroll_view)
            return
        self.rules_scroll_view = RulesScrollViewWidget()
        if obj_hash == id(self):
            ''' That means we're working with all rules, so no need in all rules button'''
            self.rules_scroll_view.remove_widget(self.rules_scroll_view.all_rules_btn)
        self.add_widget(self.rules_scroll_view)
        if len(rules) == 0:
            # Here image instead of label would be, so no need to calculate font size properly
            img = Image(source='resources/images/no_rules.jpg', size_hint=(1, None), allow_stretch=True,
                        keep_ratio=False)
            self.rules_scroll_view.ids.grid.add_widget(img)
        else:
            max_right_side_len = max([len(rule.result_box_kinds) for rule in rules] + [1])
            for rule in rules:
                rule_widget = RuleWidget(rule, click_on_rule_function, max_right_side_len, self.sound_handler)
                self.rules_scroll_view.ids.grid.add_widget(rule_widget)
        self.scroll_views[obj_hash] = self.rules_scroll_view

    def undo(self):
        if self.is_target_field:
            return
        self.engine.undo()
        self.unselect_box()
        self.show_all_rules()

    def on_touch_down(self, touch):
        if self.engine.any_animation_in_progress():
            self.engine.finish_all_animations()
            return True
        return super(Playground, self).on_touch_down(touch)

    def init_storage_star(self):
        if self.engine.min_moves is None:
            return
        lvl_dict = self.storage.get(f'lvl{self.engine.lvl}')
        if 'got_star' not in lvl_dict.keys():
            lvl_dict['got_star'] = False
            self.storage.put(f'lvl{self.engine.lvl}', **lvl_dict)

    def update_storage(self, key, **kwargs):
        d = self.storage.get(key)
        for key, value in kwargs.items():
            d[key] = value
        self.storage.put(key, **d)

    def select_box(self, box_widg):
        if box_widg not in self.game_widgets:
            return
        if self.selected_box is not None:
            self.selected_box.unselect()
        box_widg.select()
        self.selected_box = box_widg

    def unselect_box(self):
        if self.selected_box is None:
            return
        self.selected_box.unselect()
        self.selected_box = None
