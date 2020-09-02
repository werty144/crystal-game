from src.backend.MyAdaptiveLabel import MyAdaptiveLabel
from src.frontend.Screens.GameScreen import GameScreen
from src.frontend.custom_widgets.TutorialWidget import Tutorial
from src.frontend.custom_widgets.WinningWidget import WinningWidget


class TutorialScreen(GameScreen):

    def on_enter(self, *args):
        self.playground = Tutorial(sound_handler=self.sound_handler)
        self.add_widget(self.playground)
        self.playground.start()
        MyAdaptiveLabel.fonts_setted = False
        MyAdaptiveLabel.small_font = 100
        MyAdaptiveLabel.large_font = 100

    def show_winning_widget(self):
        self.sound_handler.play_winning_sound()
        self.winning_widget = WinningWidget()
        self.winning_widget.ids.buttons.remove_widget(self.winning_widget.ids.next_lvl_button)
        self.add_widget(self.winning_widget)

    def go_to_next_lvl(self):
        self.clean()
        self.manager.get_screen('game').lvl = 0
        self.manager.current = 'game'