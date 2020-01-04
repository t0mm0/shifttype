from kivy.logger import Logger
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from . import puzzle


class Tile(Button):
    letter = StringProperty()
    used = BooleanProperty(defaultvalue=False)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.debug(f"new tile: {self.letter}")


class Reel(BoxLayout):
    letters = ListProperty()
    tiles = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.debug(f"new reel: {self.letters}")
        self.tiles = [Tile(letter=letter) for letter in self.letters]
        for tile in self.tiles:
            self.add_widget(tile)
        self.height = len(self.tiles) * 100



class GameScreen(Widget):
    reels = []

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.puzzle = puzzle.Puzzle()
        Logger.debug(f"core_words: {self.puzzle.core_words}")
        self._make_reels(self.puzzle.reels)

    def _make_reels(self, reels):
        self.reels = [Reel(letters=reel) for reel in reels]
        x = 200
        for reel in self.reels:
            reel.pos = (x,100)
            self.add_widget(reel)
            x += 100
