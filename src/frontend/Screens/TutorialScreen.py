from src.frontend.Screens.GameScreen import GameScreen
from src.frontend.custom_widgets.TutorialWidget import Tutorial
from src.frontend.custom_widgets.WinningWidget import WinningWidget


class TutorialScreen(GameScreen):

    def on_enter(self, *args):
        self.playground = Tutorial()
        self.add_widget(self.playground)
        self.playground.start()
        self.set_buttons()

    def show_winning_widget(self):
        self.winning_widget = WinningWidget()
        self.winning_widget.ids.next_lvl_button.text = 'Lvl 0'
        self.add_widget(self.winning_widget)

    def go_to_next_lvl(self):
        self.clean()
        self.manager.get_screen('game').lvl = 0
        self.manager.current = 'game'