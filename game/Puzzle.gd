extends Node

class_name Puzzle

enum puzzle_mode {
    DAILY,
    RANDOM,
}

var _rng = RandomNumberGenerator.new()
var num_core: int
var num_letters: int
var mode: int
var core_words: PoolStringArray
var reels: Array
var rng_seed: int

func _init(mode: int = puzzle_mode.DAILY, num_letters: int = 5, num_core: int = 4, rng_seed: int = 0) -> void:
    self.num_core = num_core
    self.num_letters = num_letters
    self.mode = mode

    if rng_seed != 0:
        _rng.seed = rng_seed
    elif mode == puzzle_mode.DAILY:
        _rng.seed = get_daily_seed()
    else:
        _rng.randomize()
    self.rng_seed = _rng.seed

    core_words = _pick_words()
    reels = _pick_reels()

#    print(core_words)
#    print(reels)

static func get_daily_seed() -> int:
    return Time.get_date_string_from_system().hash()

func test_word(word: String, uncommon: bool = true) -> bool:
    return WordLists.words[num_letters]["common"].has(word) or (uncommon and
           WordLists.words[num_letters]["uncommon"].has(word))


func _pick_words() -> PoolStringArray:
    var choices := PoolStringArray()
    while len(choices) < num_core:
        var choice = WordLists.words[num_letters]["common"][_rng.randi() %
                     WordLists.words[num_letters]["common"].size()]
        if !choices.has(choice):
            choices.append(choice)
    choices.sort()
    return choices

func _pick_reels() -> Array:
    var new_reels = []
    for l in num_letters:
        var reel = PoolStringArray()
        for w in core_words:
            var letter = w.substr(l, 1)
            if !reel.has(letter):
                reel.append(letter)
        new_reels.append(_shuffleList(reel))
    return new_reels

func _shuffleList(list):
    var shuffledList = []
    var indexList = range(list.size())
    for _i in range(list.size()):
        var x = _rng.randi() % indexList.size()
        shuffledList.append(list[indexList[x]])
        indexList.remove(x)
    return shuffledList
