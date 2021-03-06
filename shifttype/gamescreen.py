import datetime
import os

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex

from plyer import vibrator

from . import puzzle

from jnius import autoclass

PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
String = autoclass('java.lang.String')


class BackgroundColor(Widget):
    pass


class GameOver(BoxLayout):
    game_over_text = StringProperty()
    time = StringProperty()
    found = NumericProperty()
    core_found = NumericProperty()
    core = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self.ids.game_over_label.text = self.game_over_text

    def share(self):
        share_text = (
            f"I solved the ShiftType Daily Puzzle in {self.time} - "
            f"I found {self.found} words, and {self.core_found} of {self.core} core words!")
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND)
        intent.putExtra(Intent.EXTRA_TEXT, String(share_text))
        intent.setType('text/plain')
        chooser = Intent.createChooser(intent, String('Share...'))
        PythonActivity.mActivity.startActivity(chooser)


class TsTile(Label, BackgroundColor):
    letter = StringProperty()
    used = BooleanProperty(defaultvalue=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.debug(f"new tile: {self.letter}")

    def get_color(self, used, unused_color, used_color):
        if used:
            return get_color_from_hex(used_color)
        return get_color_from_hex(unused_color)


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
        self.tiles = [TsTile(letter=letter) for letter in self.letters]
        for tile in self.tiles:
            self.slider.add_widget(tile)
        self.add_widget(self.slider)
        self.selected = len(self.letters) - 1
        self.slider.settle_down()

    def use_selected(self):
        self.tiles[self.selected].used = True


class GameScreen(Screen, BackgroundColor):
    reels = []
    num_letters = NumericProperty(defaultvalue=5)
    num_core = NumericProperty(defaultvalue=4)
    running = BooleanProperty(defaultvalue=False)
    found_words = ListProperty()
    time = NumericProperty(defaultvalue=0)
    timer = None
    real_game = ObjectProperty(None)
    store = None
    game_over = None
    vibrate = False

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)
        self.app = App.get_running_app()
        self.store = JsonStore(os.path.join(
            self.app.user_data_dir, 'st.json'))
        self.vibrate = self.app.config.getboolean('shifttype', 'vibrate')

    def _finish_init(self, dt):
        self.load()

    def reset(self, saved=None):
        self.time = 0
        seed = None

        if saved:
            seed = saved['seed']
            self.num_core = saved['num_core']
            self.num_letters = saved['num_letters']
            self.time = saved['time']
            self.found_words = saved['found_words']
        else:
            self.num_letters, self.num_core = puzzle.DIFFICULTY[
                datetime.datetime.today().weekday()]
            self.time = 0
            self.found_words = []

        self.puzzle = puzzle.Puzzle(
            seed=seed,
            num_letters=self.num_letters,
            num_core=self.num_core)
        Logger.debug(f"core_words: {self.puzzle.core_words}")
        self._make_reels(self.puzzle.reels)

        if saved:
            for i, reel in enumerate(self.reels):
                for j, tile in enumerate(reel.tiles):
                    tile.used = saved['reels'][i][j]['used']

        if self.test_complete():
            self.display_game_over()
        elif self.game_over:
            self.remove_widget(self.game_over)
            self.game_over = None

    def on_running(self, instance, value):
        Logger.debug(f"on_running: {value}")
        if value:
            self.timer = Clock.schedule_interval(self.update_time, 1)
        else:
            self.timer.cancel()

    def update_time(self, dt):
        self.time += 1
        Logger.debug(f"timer: {self.time}")
        self.check_current_daily()

    def check_current_daily(self):
        if self.puzzle.seed[:10] != str(datetime.date.today()):
            Logger.debug('it is a new day, moving to new puzzle')
            self.reset()

    def _make_reels(self, reels):
        for reel in self.reels:
            self.real_game.remove_widget(reel)
        self.reels = [Reel(letters=reel) for reel in reels]
        for reel in self.reels:
            reel.bind(selected=self._selected)
            self.real_game.add_widget(reel)

    def _selected(self, instance, value):
        if self.running:
            if self.vibrate:
                vibrator.vibrate(.01)
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
                        self.display_game_over()

    def run_if_incomplete(self):
        self.check_current_daily()
        self.running = not self.test_complete()

    def display_game_over(self):
        self.running = False
        t = str(datetime.timedelta(seconds=self.time))
        game_over_text = ("[size=36sp][b]Well done![/b][/size]\n\n"
                          f"You found {len(self.found_words)} words:\n\n"
                          f"{', '.join(sorted(self.found_words))}"
                          f"\n\nIt took you {t}!\n\n"
                          f"Today's core words were:\n\n"
                          f"{', '.join(self._format_core_words())}")
        core_found = len(
            set(self.puzzle.core_words).intersection(self.found_words))
        if self.game_over:
            self.remove_widget(self.game_over)
        self.game_over = GameOver(
            game_over_text=game_over_text,
            time=t,
            found=len(
                self.found_words),
            core=self.num_core,
            core_found=core_found)
        self.add_widget(self.game_over)

    def _format_core_words(self):
        return [
            f"[color=#00ff00]{w}[/color]" if w in self.found_words
            else w for w in self.puzzle.core_words]

    def test_complete(self):
        for reel in self.reels:
            for tile in reel.tiles:
                if not tile.used:
                    return False
        return True

    def save(self):
        Logger.debug('save game')
        saved = {}
        saved['found_words'] = list(self.found_words)
        saved['num_core'] = self.num_core
        saved['num_letters'] = self.num_letters
        saved['time'] = self.time
        saved['seed'] = self.puzzle.seed
        saved['reels'] = []
        for i, reel in enumerate(self.reels):
            saved['reels'].append([])
            for tile in reel.tiles:
                saved['reels'][i].append(
                    {'letter': tile.letter, 'used': tile.used})
        self.store['daily'] = saved
        Logger.debug(saved)

    def load(self):
        Logger.debug('load game')
        saved = None
        if 'daily' in self.store:
            saved = self.store.get('daily')
            if saved['seed'][:10] != str(datetime.date.today()):
                saved = None
                Logger.debug('ignored daily saved data is not from today')
            Logger.debug(saved)
        self.reset(saved=saved)
