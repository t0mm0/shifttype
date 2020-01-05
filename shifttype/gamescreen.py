from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import platform

from . import puzzle


class Tile(Button):
    letter = StringProperty()
    used = BooleanProperty(defaultvalue=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.debug(f"new tile: {self.letter}")


class ReelSlider(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Reel(RelativeLayout):
    letters = ListProperty()
    tiles = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.debug(f"new reel: {self.letters}")
        self.slider = ReelSlider()
        self.tiles = [Tile(letter=letter) for letter in self.letters]
        for tile in self.tiles:
            self.slider.add_widget(tile)
        self.add_widget(self.slider)


class GameArea(BoxLayout):
    reels = []
    num_letters = NumericProperty(defaultvalue=5)

    def __init__(self, **kwargs):
        super(GameArea, self).__init__(**kwargs)
        print(self.num_letters)
        self.puzzle = puzzle.Puzzle(num_letters=self.num_letters)
        Logger.debug(f"core_words: {self.puzzle.core_words}")
        self._make_reels(self.puzzle.reels)

    def _make_reels(self, reels):
        self.reels = [Reel(letters=reel) for reel in reels]
        for reel in self.reels:
            self.add_widget(reel)


class GameScreen(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(GameArea(num_letters=5))
        if platform == 'linux':
            Window.size = (800, 1200)
