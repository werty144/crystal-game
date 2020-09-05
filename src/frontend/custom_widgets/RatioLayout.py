from kivy.properties import NumericProperty
from kivy.uix.relativelayout import RelativeLayout


class RatioLayout(RelativeLayout):
    spacing = NumericProperty()
    free_width = NumericProperty()
    width_per_child = NumericProperty()

    def do_layout(self, *args):
        self.free_width = self.width - (len(self.children) + 1) * self.spacing
        self.width_per_child = self.free_width / len(self.children)
        for i, child in enumerate(self.children):
            self.count_child_pos_n_size(child, i)
        super(RatioLayout, self).do_layout(*args)

    def count_child_pos_n_size(self, child, child_n):
        child.size_hint = (None, None)
        potential_height = self.width_per_child / child.ratio
        if potential_height <= self.height:
            child.width = self.width_per_child
            child.height = potential_height
        else:
            child.height = self.height
            child.width = child.height * child.ratio
        child.pos = (self.width_per_child * child_n + self.spacing + (self.width_per_child - child.width) / 2, 0)
