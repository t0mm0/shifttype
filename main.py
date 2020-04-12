import kivy
kivy.require('1.11.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.properties import ConfigParserProperty
from kivy.uix.settings import Settings, SettingsWithNoMenu
from kivy.uix.screenmanager import ScreenManager
import logging

from shifttype.settings import SettingColorPicker


Logger.setLevel(logging.DEBUG)

DEFAULTS = {
    'VIBRATE': 1,
    'TILE_BG': '#7f7f7fff',
    'TILE_USED_BG': '#ff0000ff',
    'LETTER_COLOR': '#ffffffff',
    'LETTER_USED_COLOR': '#ffffffff',
    'SELECTION_COLOR': '#00ff00ff',
    'BACKGROUND_COLOR': '#000000ff',
}


class TsScreenManager(ScreenManager):
    def go_back(self):
        Logger.debug(f"go_back from: {self.current}")
        if self.current == 'game':
            self.get_screen('game').running = False
            self.transition.direction = 'right'
            self.current = 'menu'
            return True


class MainApp(App):
    tile_bg = ConfigParserProperty(
        DEFAULTS['TILE_BG'], 'shifttype', 'tile_bg', 'app')
    tile_used_bg = ConfigParserProperty(
        DEFAULTS['TILE_USED_BG'],
        'shifttype',
        'tile_used_bg',
        'app')
    letter_color = ConfigParserProperty(
        DEFAULTS['LETTER_COLOR'],
        'shifttype',
        'letter_color',
        'app')
    letter_used_color = ConfigParserProperty(
        DEFAULTS['LETTER_USED_COLOR'],
        'shifttype',
        'letter_used_color',
        'app')
    selection_color = ConfigParserProperty(
        DEFAULTS['SELECTION_COLOR'],
        'shifttype',
        'selection_color',
        'app')
    background_color = ConfigParserProperty(
        DEFAULTS['BACKGROUND_COLOR'],
        'shifttype',
        'background_color',
        'app')

    def __init__(self, **kwargs):
        self.title = "shiftTYPE"
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.on_keypress)
        self.settings_cls = SettingsWithNoMenu
        self.use_kivy_settings = False

    def build_config(self, config):
        config.setdefaults('shifttype', {
            'vibrate': DEFAULTS['VIBRATE'],
            'tile_bg': DEFAULTS['TILE_BG'],
            'tile_used_bg': DEFAULTS['TILE_USED_BG'],
            'letter_color': DEFAULTS['LETTER_COLOR'],
            'letter_used_color': DEFAULTS['LETTER_USED_COLOR'],
            'selection_color': DEFAULTS['SELECTION_COLOR'],
            'background_color': DEFAULTS['BACKGROUND_COLOR'],
        })

    def on_config_change(self, config, section, key, value):
        Logger.debug(f"on_config_change: {section}, {key}, {value}")
        if section == 'shifttype':
            if key == 'vibrate':
                self.root.get_screen('game').vibrate = config.getboolean(
                    section, key)

    def build_settings(self, settings):
        settings.register_type('colorpicker', SettingColorPicker)
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
