import kivy
kivy.require('1.11.0')

from kivy.app import App
from kivy.logger import Logger
import logging


Logger.setLevel(logging.DEBUG)


class MainApp(App):
    def __init__(self, **kwargs):
        self.title = "shiftTYPE"
        super().__init__(**kwargs)
    pass


if __name__ == '__main__':
    app = MainApp()
    app.run()
