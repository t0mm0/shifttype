from kivy.core.window import Window
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingItem, SettingSpacer
from kivy.utils import get_color_from_hex, get_hex_from_color

Builder.load_file('shifttype/settings.kv', rulesonly=True)


class SettingColorPicker(SettingItem):
    '''Implementation of a colorpicker setting on top of a :class:`SettingItem`.
    It is visualized with a :class:`~kivy.uix.label.Label` widget that, when
    clicked, will open a :class:`~kivy.uix.popup.Popup` with a
    :class:`~kivy.uix.colorpicker.Coloricker` so the user can enter a custom
    value.
    '''

    popup = ObjectProperty(None, allownone=True)
    '''(internal) Used to store the current popup when it's shown.
    :attr:`popup` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    colorpicker = ObjectProperty(None)
    '''(internal) Used to store the current colorpicker from the popup and
    to listen for changes.
    :attr:`popup` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    def on_panel(self, instance, value):
        if value is None:
            return
        self.bind(on_release=self._create_popup)
        # if self.content is None:
        #     layout = BoxLayout(orientation='horizontal')
        #     layout.add_widget(Button(text='test'))

    def _dismiss(self, *largs):
        if self.colorpicker:
            self.colorpicker.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None

    def _validate(self, instance):
        self._dismiss()
        value = get_hex_from_color(self.colorpicker.color)
        self.value = value

    def _create_popup(self, instance):
        # create popup layout
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            title=self.title, content=content, size_hint=(None, 0.9),
            width=popup_width)

        # create the colorpicker used for numeric input
        colorpicker = ColorPicker(
            color=get_color_from_hex(self.value))
        colorpicker.bind(on_color=self._validate)
        self.colorpicker = colorpicker

        # construct the content
        content.add_widget(colorpicker)
        content.add_widget(SettingSpacer())

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        btn = Button(text='Ok')
        btn.bind(on_release=self._validate)
        btnlayout.add_widget(btn)
        btn = Button(text='Cancel')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()
