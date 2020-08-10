from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import Instruction, InstructionGroup
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import ListProperty, ObjectProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

from src.backend.ScreenUtils import ScreenUtils
from src.backend.constants import FRAME_RATE_SEC
from src.frontend.custom_widgets.PlaygroundWidget import Playground


class Task(FloatLayout):
    def calculate_focus_window_pos_n_size(self):
        if isinstance(self.focus_object, Instruction):
            '''That means we're working with a grid'''
            return self.screen_utils.start, self.screen_utils.size
        else:
            '''Otherwise we're working with widget'''
            return self.focus_object.to_window(*self.focus_object.pos), self.focus_object.size

    def create_shadowed_background(self, *args):
        focus_window_pos, focus_window_size = self.calculate_focus_window_pos_n_size()
        focus_window_width, focus_window_height = focus_window_size[0] * 2 if self.double_width else focus_window_size[0], focus_window_size[1]
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

    def __init__(self, focus_object, title_text, on_touch_option, screen_utils: ScreenUtils, double_width=False):
        self.focus_object = focus_object
        self.title_text = title_text
        self.on_touch_option = on_touch_option
        self.screen_utils = screen_utils
        self.double_width = double_width
        super().__init__()
        self.background = None
        self.create_shadowed_background()

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
        if self.on_touch_option == 'pass':
            self.parent.need_next_task = True
            return True
        if self.on_touch_option == 'act':
            if not self.touch_is_inside_focus_window(touch):
                return True
            self.parent.need_next_task = True

            '''Make sure touch_down is totally dispatched before update'''
            self.parent.update_event.cancel()

            def start_updating(_):
                self.parent.update_event = Clock.schedule_interval(self.parent.update, FRAME_RATE_SEC)

            Clock.schedule_once(start_updating, 0.1)

            return super(Task, self).on_touch_down(touch)


class Tutorial(Playground):
    tasks = ListProperty()
    cur_task = ObjectProperty(allownone=True)
    need_next_task = BooleanProperty(False)

    def start(self, **kwargs):
        super().start(lvl='tutorial')
        self.make_tasks()
        self.bind(size=self.update_tasks)

    def update_tasks(self, *args):
        for task in self.tasks:
            task.size = self.size

    def make_tasks(self):
        su = self.engine.screen_utils
        field_task = Task(self.grid,
                          'Это игровое поле. На нем расположены коробки, которые падают, если под ними нет опоры!\n\n'
                          'Нажмите, чтобы продолжить.',
                          'pass', su)
        self.tasks.append(field_task)

        rule_scroll_view_task = Task(self.rules_scroll_view.ids.rule_scroll_view,
                                     'Коробки можно заменять на другие, применяя эти правила\n\n'
                                     'Нажмите, чтобы продолжить.',
                                     'pass', su)
        self.tasks.append(rule_scroll_view_task)

        first_box_in_rule_task = Task(self.rules_scroll_view.ids.grid.children[-1].children[-1],
                                      'Первая коробка правила показывает, какую коробку это правило заменяет.\n\n'
                                      'Нажмите, чтобы продолжить.',
                                      'pass', su)
        self.tasks.append(first_box_in_rule_task)

        first_in_right_side = self.rules_scroll_view.ids.grid.children[-1].children[1]
        right_side_of_the_rule_task = Task(first_in_right_side,
                                           'Коробки справа от стрелочки показывают,'
                                           ' во что превратится замененная коробка.\n\n'
                                           'Нажмите, чтобы продолжтиь',
                                           'pass', su, True)
        self.tasks.append(right_side_of_the_rule_task)

        target_field_button_task = Task(self.parent.ids.field_switch, 'switch', 'act', su)
        self.tasks.append(target_field_button_task)

        target_field_task = Task(self.grid, 'target field', 'pass', su)
        self.tasks.append(target_field_task)

        game_field_button_task = Task(self.parent.ids.field_switch, 'switch again', 'act', su)
        self.tasks.append(game_field_button_task)

        open_box_task = Task(self.game_widgets[0], 'box', 'act', su)
        self.tasks.append(open_box_task)

        rule_scroll_view_task = Task(self.rules_scroll_view.ids.rule_scroll_view, 'selected box rules', 'pass', su)
        self.tasks.append(rule_scroll_view_task)

        '''...children[-1] -- пиздецкий костыль. Поскольку rule_widgets нумеруются снизу, получается, что таким образом
        я получаю координаты верхнего rule_widget-a, хотя когда эта task
        становится актуальна, там уже другой rule_widget, и он всего один.'''
        rule_widget_task = Task(self.rules_scroll_view.ids.grid.children[-1], 'rule', 'act', su)
        self.tasks.append(rule_widget_task)

        final_task = Task(Widget(size=(0, 0)), "Now it's up to you!", 'pass', su)
        self.tasks.append(final_task)

        '''Tasks are stored stack-wise'''
        self.tasks.reverse()
        self.cur_task = self.tasks[-1]
        self.add_widget(self.cur_task)

    def update(self, _):
        super(Tutorial, self).update(_)
        if not self.cur_task:
            return

        ''' Make sure cur_task is on top'''
        self.remove_widget(self.cur_task)
        self.add_widget(self.cur_task)

        if self.engine.any_animation_in_progress():
            self.remove_widget(self.cur_task)
        if not self.engine.any_animation_in_progress() and self.need_next_task:
            self.need_next_task = False
            self.switch_to_next_task()

    def switch_to_next_task(self):
        self.remove_widget(self.cur_task)
        self.tasks.pop()
        if len(self.tasks) == 0:
            self.cur_task = None
            return
        self.cur_task = self.tasks[-1]
        self.cur_task.update_background()
        self.add_widget(self.cur_task)

    def check_win(self):
        if self.engine.win and not self.engine.any_animation_in_progress():
            self.update_event.cancel()
            self.parent.show_winning_widget()
