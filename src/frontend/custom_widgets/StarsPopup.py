from kivy.uix.popup import Popup


class StarsPopup(Popup):
    '''Binding function that normalizes length of all labels to the last label'''
    def on_pre_open(self):
        self.ids.grid.children[0].ids.label.bind(final_width=self.normalize_width)

    def normalize_width(self, *args):
        self.ids.grid.children[0].ids.label.unbind(final_width=self.normalize_width)
        max_width = 0
        for widget in self.ids.grid.children:
            max_width = max(max_width, widget.ids.label.width)
        for widget in self.ids.grid.children:
            widget.ids.label.width = max_width
        self.ids.grid.children[0].ids.label.bind(final_width=self.normalize_width)
