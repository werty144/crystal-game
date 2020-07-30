from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.widget import Widget

from src.frontend.custom_widgets.PlaygroundWidget import Playground


class Task(Widget):
    def create_shadowed_background(self, *args):
        with self.canvas.before:
            Color(0, 0, 0, 0.4)
            Rectangle(size=self.size, pos=self.pos)
            Color(0, 0, 0, 0)
            Rectangle(size=self.focus_object.size, pos=self.focus_object.pos)

    def __init__(self, focus_object, title_text, touch_function):
        super().__init__()
        self.focus_object = focus_object
        self.bind(size=self.create_shadowed_background)


class Tutorial(Playground):
    def start(self, **kwargs):
        super().start(lvl='tutorial')
        task = Task(self.rules_scroll_view, 'huy', None)
        self.add_widget(task)

    def check_win(self):
        if self.engine.win and not self.engine.any_animation_in_progress():
            self.update_event.cancel()
            self.parent.show_winning_widget()
