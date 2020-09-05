from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from src.backend.ModuleUtils import get_final_levels
from src.frontend.custom_widgets.PlaygroundWidget import Playground
from src.frontend.custom_widgets.WinningWidget import WinningWidget


class GameScreen(Screen):
    playground = ObjectProperty(None, allownone=True)
    lvl = NumericProperty()
    winning_widget = ObjectProperty(None, allownone=True)
    storage = ObjectProperty()
    sound_handler = ObjectProperty()
    switch_frame = ObjectProperty(None, allownone=True)

    def on_enter(self, *args):
        self.playground = Playground(storage=self.storage, sound_handler=self.sound_handler)
        self.playground.start(self.lvl)
        self.add_widget(self.playground)

    def restart(self):
        self.clean()
        self.on_enter()

    def clean(self):
        if self.switch_frame is not None:
            self.canvas.remove(self.switch_frame)
        if self.playground is not None:
            self.playground.update_event.cancel()
            self.remove_widget(self.playground)
            self.playground = None
        if self.winning_widget is not None:
            self.remove_widget(self.winning_widget)
            self.winning_widget = None

    def switch_field(self):
        if not self.playground.is_target_field:
            with self.canvas:
                from kivy.graphics.vertex_instructions import Line
                from kivy.graphics.context_instructions import Color
                switch = self.ids.field_switch
                Color(232/300, 58/300, 88/300, 1)
                self.switch_frame = Line(rectangle=(switch.x - 2, switch.y - 2, switch.width + 4, switch.height + 4),
                                         width=2)
        else:
            if self.switch_frame is not None:
                self.canvas.remove(self.switch_frame)
                self.switch_frame = None
        self.playground.switch_field()

    def show_winning_widget(self):
        self.clean()
        self.sound_handler.play_winning_sound()
        self.winning_widget = WinningWidget()
        if self.lvl in get_final_levels():
            self.winning_widget.ids.buttons.remove_widget(self.winning_widget.ids.next_lvl_button)
        self.add_widget(self.winning_widget)

    def go_to_next_lvl(self):
        self.clean()
        self.lvl += 1
        self.on_enter()

    def undo(self):
        self.playground.undo()
