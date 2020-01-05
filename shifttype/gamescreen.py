import datetime
from kivy.animation import Animation
from kivy.app import App
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
from kivymd.uix.dialog import MDDialog

from . import puzzle


class Tile(Button):
    letter = StringProperty()
    used = BooleanProperty(defaultvalue=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.debug(f"new tile: {self.letter}")

    def get_color(self, used):
        if used:
            return App.get_running_app().theme_cls.primary_color
        return App.get_running_app().theme_cls.bg_normal


class ReelSlider(BoxLayout):
    moving = False
    tile_height = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.moving = True

    def on_touch_up(self, touch):
        if self.moving:
            self.moving = False
            self.settle_down()

    def on_touch_move(self, touch):
        if self.moving:
            new_pos = self.y + touch.dy
            min_move = self.tile_height * .25
            if new_pos > min_move:
                new_pos = min_move
            max_move = (self.tile_height * .75) - self.height
            if new_pos < max_move:
                new_pos = max_move
            self.y = new_pos

    def settle_down(self):
        Logger.debug(f"settle_down: {self.parent.letters}")
        self.tile_height = self.height / len(self.parent.letters)
        target_pos = self.tile_height * round(self.y / self.tile_height)
        anim = Animation(y=target_pos, duration=.1)
        anim.bind(on_complete=self._settled)
        anim.start(self)

    def _settled(self, anim=None, widget=None):
        self.parent.selected = len(
            self.parent.letters) - 1 - int(self.y / -self.tile_height)


class Reel(RelativeLayout):
    letters = ListProperty()
    tiles = []
    selected = NumericProperty(defaultvalue=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.debug(f"new reel: {self.letters}")
        self.slider = ReelSlider()
        self.tiles = [Tile(letter=letter) for letter in self.letters]
        for tile in self.tiles:
            self.slider.add_widget(tile)
        self.add_widget(self.slider)
        self.selected = len(self.letters) - 1
        self.slider.settle_down()

    def use_selected(self):
        self.tiles[self.selected].used = True


class GameArea(BoxLayout):
    reels = []
    num_letters = NumericProperty(defaultvalue=5)
    running = False
    found_words = ListProperty()
    time = NumericProperty()
    timer = None

    def __init__(self, **kwargs):
        super(GameArea, self).__init__(**kwargs)
        self.reset(num_letters=5, num_core=4)

    def reset(self, num_letters=5, num_core=4):
        self.time = 0
        self.num_letters = num_letters
        self.puzzle = puzzle.Puzzle(num_letters=num_letters, num_core=num_core)
        Logger.debug(f"core_words: {self.puzzle.core_words}")
        self._make_reels(self.puzzle.reels)
        self.running = True
        self.timer = Clock.schedule_interval(self.update_time, 1)

    def update_time(self, dt):
        self.time += 1
        Logger.debug(f"timer: {self.time}")

    def _make_reels(self, reels):
        self.found_words = []
        for reel in self.reels:
            self.remove_widget(reel)
        self.reels = [Reel(letters=reel) for reel in reels]
        for reel in self.reels:
            reel.bind(selected=self._selected)
            self.add_widget(reel)

    def _selected(self, instance, value):
        if self.running:
            word = ''
            for reel in self.reels:
                word += reel.letters[reel.selected]
            if self.puzzle.test_word(word):
                Logger.debug(f"found: {word}")
                if word not in self.found_words:
                    self.found_words.append(word)
                    Logger.debug(f"total found: {self.found_words}")
                    for reel in self.reels:
                        reel.use_selected()
                    Logger.debug(f"finished: {self.test_complete()}")
                    if self.test_complete():
                        self.timer.cancel()
                        t = str(datetime.timedelta(seconds=self.time))
                        dialog = MDDialog(
                            title="You Won!!!",
                            text=f"Found {len(self.found_words)} words: " +
                            ', '.join(self.found_words) +
                            f"\n\nIt took you {t}!",
                            size_hint=(0.8, 0.4),
                            text_button_ok="Woohoo ;)",
                            events_callback=lambda *args: self.reset(),
                        )
                        dialog.open()

    def test_complete(self):
        for reel in self.reels:
            for tile in reel.tiles:
                if not tile.used:
                    return False
        return True


class GameScreen(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(GameArea(num_letters=5))
        if platform == 'linux':
            Window.size = (800, 1200)
