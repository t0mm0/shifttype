extends Node

var words: Dictionary = {}

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
    load_word_lists(Globals.WORDS_PATH)

func load_word_lists(path: String) -> void:
    for l in range(Globals.WORDS_MIN_LENGTH, Globals.WORDS_MAX_LENGTH + 1):
        var file_name := '%s/common_%d.txt' % [path, l]
        var common := _load_from_file(file_name)
        file_name = '%s/uncommon_%d.txt' % [path, l]
        var uncommon := _load_from_file(file_name)
        words[l] = {'common': common, 'uncommon': uncommon}

func _load_from_file(file_name: String) -> PoolStringArray:
    var f := File.new()
    var err := f.open(file_name, File.READ)
    if err:
        return PoolStringArray()
    var word_array := PoolStringArray()
    while not f.eof_reached():
        var line := f.get_line()
        if len(line):
            word_array.append(line.to_upper())
    f.close()

    return word_array
