import kivy
kivy.require('1.11.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.uix.settings import Settings, SettingsWithNoMenu
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
        self.settings_cls = SettingsWithNoMenu
        self.use_kivy_settings = False

    def build_config(self, config):
        config.setdefaults('shifttype', {
            'vibrate': '1',
        })

    def on_config_change(self, config, section, key, value):
        Logger.debug(f"on_config_change: {section}, {key}, {value}")
        if section == 'shifttype':
            if key == 'vibrate':
                self.root.get_screen('game').vibrate = config.getboolean(
                    section, key)

    def build_settings(self, settings):
        settings.add_json_panel(
            'ShiftType',
            self.config,
            'assets/settings/shifttype.json')

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
