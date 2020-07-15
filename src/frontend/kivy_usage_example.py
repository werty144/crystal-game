import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window


class MyApp(App):

    def build(self):
        print(Window)
        return Label(text='Hello world')


if __name__ == '__main__':
    MyApp().run()
