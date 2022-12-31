extends PopupPanel

var share = null # our share singleton instance
var share_text : String = ""

func _ready():
    # initialize the share singleton if it exists
    if Engine.has_singleton("GodotShare"):
        share = Engine.get_singleton("GodotShare")


func update_and_show(puzzle: Puzzle, found_words: Array, time: float) -> void:
    var score_text : String = "[center]You found %s words:\n\n" % len(found_words)
    if not share:
        $CenterContainer/VBoxContainer/ShareButton.hide()

    var time_string = _time_convert(time)
    score_text += ", ".join(found_words).to_lower()
    score_text += "\n\nIt took you %s\n\n" % time_string
    score_text += _format_core_words(puzzle.core_words, found_words).to_lower()
    score_text += "\n"
    get_node("CenterContainer/VBoxContainer/ScoreLabel").bbcode_text = score_text

    share_text = "I solved the ShiftType Daily Puzzle in %s - " % time_string
    share_text += "I found %s words, and %s of %s core words!" % [
        len(found_words),
        _found_core(puzzle.core_words, found_words),
        len(puzzle.core_words)
    ]

    popup_centered()

func _time_convert(time_in_sec: float) -> String:
    var sec: int = int(time_in_sec)
    var seconds = sec % 60
    var minutes = (sec / 60) % 60
    var hours = (sec / 60) / 60

    return "%02d:%02d:%02d" % [hours, minutes, seconds]

func _format_core_words(core_words: Array, found_words: Array) -> String:
    var core_words_color: PoolStringArray = []

    for word in core_words:
        if word in found_words:
            core_words_color.append("[color=#00ff00]%s[/color]" % word)
        else:
            core_words_color.append(word)

    return ", ".join(core_words_color)

func _found_core(core_words: Array, found_words: Array) -> int:
    var found : int
    for word in core_words:
        if word in found_words:
            found += 1
    return found

func _on_ShareButton_pressed() -> void:
    share.shareText("shiftTYPE", "I won today's shiftType!", share_text)

