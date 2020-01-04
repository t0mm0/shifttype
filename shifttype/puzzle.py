from datetime import date
import random
import re

MODE_DAILY = 0
MODE_RANDOM = 1


class Puzzle:
    def __init__(self, mode=MODE_DAILY, num_letters=5, num_core=4):
        if mode == MODE_DAILY:
            self.random = random.Random(str(date.today()))
        else:
            self.random = random.Random()

        self.num_core_words = num_core
        self.num_letters = num_letters
        self.core_words = self._pick_words()
        self.reels = self._make_reels()

    def _pick_words(self, filename='/usr/share/dict/words'):
        choice = set()
        lower = re.compile('^[a-z]+$')
        with open(filename) as dict_file:
            self.dictionary = [word.strip() for word in dict_file if len(
                word) == self.num_letters + 1 and lower.match(word)]
            while len(choice) < self.num_core_words:
                choice.add(self.random.choice(self.dictionary))
        return sorted(choice)

    def _make_reels(self):
        reels = [(sorted(set([word[letter] for word in self.core_words])))
                 for letter in range(self.num_letters)]
        for reel in reels:
            self.random.shuffle(reel)
        return reels

    def test_word(self, guess):
        if guess in self.dictionary:
            return True
        return False


if __name__ == '__main__':
    p = Puzzle()
    q = Puzzle(MODE_RANDOM)
    print(p.core_words)
    print(p.reels)
    print(q.core_words)
    print(q.reels)
    print(p.test_word('pants'))
    print(p.test_word('xxxxx'))
