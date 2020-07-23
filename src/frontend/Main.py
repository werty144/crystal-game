from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import *
from kivy.uix.scrollview import ScrollView
from src.backend.Engine import Engine
from src.frontend.RuleWidget import *

Builder.load_file(KV_FILE_PATH)


class Playground(Widget):
    engine = ObjectProperty()
    game_widgets = ListProperty()
    screen_utils = ObjectProperty()
    grid = ObjectProperty()
    target_field_widgets = ListProperty()
    is_target_field = BooleanProperty(False)
    scroll_view = Property(None)
    update_event = ObjectProperty(None, allownone=True)

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
        pos, size = self.engine.screen_utils.get_scrollview_size()
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
        for rule in rules:
            rule_widget = RuleWidget(rule, click_on_rule_function)
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
        self.parent.make_scroll_view(self.rules, self.click_on_rule_function)

    def click_on_rule_function(self, rule):
        playground = self.parent
        engine = playground.engine
        self.box = engine.adjust_rule(self.box, rule)
        playground.make_scroll_view(engine.get_all_rules(), lambda _: None)


class MenuScreen(Screen):
    pass


class WinningWidget(FloatLayout):
    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        return True


class LevelsScreen(Screen):

    @staticmethod
    def go_to_lvl(lvl):
        sm.get_screen('game').lvl = lvl
        sm.current = 'game'


class GameScreen(Screen):
    playground = ObjectProperty(None, allownone=True)
    lvl = NumericProperty()
    winning_widget = ObjectProperty(None, allownone=True)

    def on_enter(self, *args):
        self.playground = Playground()
        self.playground.start(self.lvl)
        self.add_widget(self.playground)
        self.set_buttons()

    def restart(self):
        self.clean()
        self.set_buttons()
        self.on_enter()

    def clean(self):
        if self.playground is not None:
            self.playground.update_event.cancel()
            self.remove_widget(self.playground)
            self.playground = None
        if self.winning_widget is not None:
            self.remove_widget(self.winning_widget)
            self.winning_widget = None

    def switch_field(self):
        self.playground.switch_field()

    def show_all_rules(self):
        self.playground.show_all_rules()

    def set_buttons(self):
        self.ids.field_switch.text = 'to target\nfield'

    def show_winning_widget(self):
        self.winning_widget = WinningWidget()
        self.add_widget(self.winning_widget)

    def go_to_next_lvl(self):
        self.clean()
        self.lvl += 1
        self.on_enter()


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(LevelsScreen(name='levels'))
sm.add_widget(GameScreen(name='game'))
sm.current = 'levels'


class Crystal_game(App):

    def build(self):
        return sm


if __name__ == '__main__':
    Crystal_game().run()
