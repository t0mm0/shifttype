extends Label

class_name LetterTile

export var letter: String setget set_letter, get_letter
export var used: bool = false setget set_used

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
    pass # Replace with function body.

func set_letter(text: String = '') -> void:
    # make sure we only get 1 letter
    self.text = text.left(1).to_upper()

func get_letter() -> String:
    return text

func set_used(new_used: bool = false) -> void:
    used = new_used
    # gray out background when letter is used
    var new_color: Color = Color.darkgray if used else Color(0, 0.564706, 1)
    if used:
        flash()
    var tween := create_tween()
    tween.tween_property(get_stylebox("normal"), "bg_color", new_color, 0.2
        ).set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_LINEAR)

func flash() -> void:
    var tween := create_tween()
    tween.tween_property(self, "modulate", Color(1.4, 1.4, 1.4, 1), 0.1
        ).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_SINE)
    tween.tween_property(self, "modulate", Color(1, 1, 1, 1), 0.5
        ).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_SINE)


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta: float) -> void:
#    pass
