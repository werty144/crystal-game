from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import Instruction, InstructionGroup
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from src.backend.ScreenUtils import ScreenUtils
from src.frontend.custom_widgets.PlaygroundWidget import Playground


class Task(FloatLayout):
    def calculate_focus_window_pos_n_size(self):
        if isinstance(self.focus_object, Instruction):
            '''That means we're working with a grid'''
            return self.screen_utils.start, self.screen_utils.size
        else:
            '''Otherwise we're working with widget'''
            return self.focus_object.pos, self.focus_object.size

    def create_shadowed_background(self, *args):
        focus_window_pos, focus_window_size = self.calculate_focus_window_pos_n_size()
        focus_window_width, focus_window_height = focus_window_size[0], focus_window_size[1]
        focus_window_x, focus_window_y = focus_window_pos[0], focus_window_pos[1]
        window_width, window_height = self.screen_utils.window.size[0], self.screen_utils.window.size[1]
        background = InstructionGroup()
        background.add(Color(0, 0, 0, 0.5))
        background.add(Rectangle(pos=(0, 0), size=(focus_window_x, window_height)))
        background.add(Rectangle(pos=(focus_window_x, 0), size=(window_width - focus_window_x, focus_window_y)))
        background.add(Rectangle(pos=(focus_window_x, focus_window_y + focus_window_height),
                                 size=(window_width - focus_window_x,
                                       window_height - focus_window_y - focus_window_height)))
        background.add(Rectangle(pos=(focus_window_x + focus_window_width, focus_window_y),
                                 size=(window_width - focus_window_width - focus_window_x, focus_window_height)))
        self.background = background
        self.canvas.add(background)

    def __init__(self, focus_object, title_text, touch_function, screen_utils: ScreenUtils):
        self.focus_object = focus_object
        self.title_text = title_text
        self.screen_utils = screen_utils
        super().__init__()
        self.touch_function = touch_function
        self.background = None
        self.create_shadowed_background()
        self.bind(size=self.update_background)

    def update_background(self, *args):
        self.canvas.remove(self.background)
        self.remove_widget(self.ids.title)
        self.create_shadowed_background()
        self.add_widget(self.ids.title)

    def touch_is_inside_focus_window(self, touch):
        touch_x, touch_y = touch.pos
        wp, ws = self.calculate_focus_window_pos_n_size()
        return wp[0] <= touch_x <= wp[0] + ws[0] and wp[1] <= touch_y <= wp[1] + ws[1]

    def on_touch_down(self, touch):
        if not self.touch_is_inside_focus_window(touch):
            print('Not inside')
            return True
        return super(Task, self).on_touch_down(touch)


class Tutorial(Playground):
    tasks = ListProperty()

    def start(self, **kwargs):
        super().start(lvl='tutorial')
        task = Task(self.rules_scroll_view.ids.rule_scroll_view, 'huy', None, self.engine.screen_utils)
        self.tasks.append(task)
        self.add_widget(task)
        self.bind(size=self.update_tasks)

    def update_tasks(self, *args):
        for task in self.tasks:
            task.size = self.size

    # def make_tasks(self):

    def check_win(self):
        if self.engine.win and not self.engine.any_animation_in_progress():
            self.update_event.cancel()
            self.parent.show_winning_widget()
