import kivy
kivy.require('1.11.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager
import logging


Logger.setLevel(logging.DEBUG)


class TsScreenManager(ScreenManager):
    def go_back(self):
        Logger.debug(f"go_back from: {self.current}")
        if self.current == 'game':
            self.get_screen('game').running = False
            self.transition.direction = 'right'
            self.current = 'menu'
            return True

class MainApp(App):
    def __init__(self, **kwargs):
        self.title = "shiftTYPE"
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.on_keypress)
    
    def on_keypress(self, window, key, *args):
        # handle back button
        if key == 27:
            return self.root.go_back()

    def on_pause(self):
        Logger.debug('on_pause')
        self.root.get_screen('game').save()
        return True

    def on_resume(self):
        Logger.debug('on_resume')
        self.root.get_screen('game').load()

    def on_start(self):
        Logger.debug('on_start')
        self.root.get_screen('game').load()

    def on_stop(self):
        Logger.debug('on_stop')
        self.root.get_screen('game').save()



if __name__ == '__main__':
    app = MainApp()
    app.run()
