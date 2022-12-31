extends Node2D

class_name Reel

var tileScene = preload("res://game/LetterTile.tscn")
var tiles: Array = []
var selected: String setget , get_selected
var tween: Tween
var num_of_letters: int setget , get_num_of_letters

func _init(letters: Array) -> void:
    tween = Tween.new()
    tween.connect("tween_completed", self, "_on_settled")
    add_child(tween)
    var y = 0
    for letter in letters:
        var t = tileScene.instance()
        t.set_position(Vector2(0, y))
        var size = Vector2(Globals.TILE_SIZE, Globals.TILE_SIZE)
        t.set_size(size)
        t.rect_min_size = size
        t.letter = letter
        tiles.append(t)
        add_child(t)
        y += Globals.TILE_SIZE + Globals.TILE_SPACING

func settle_down() -> void:
    # snap reel into position after release
    var pos = get_position()
    var new_y = Globals.TILE_TOTAL_SIZE * round(pos.y / Globals.TILE_TOTAL_SIZE)
    tween.interpolate_property(
        self, "position", null,
        Vector2(pos.x, new_y), .1, Tween.TRANS_LINEAR, Tween.EASE_IN_OUT)
    tween.start()

func _on_settled(_object: Object, _key: NodePath):
    Input.vibrate_handheld(10)
    if self.num_of_letters > 0:
#        self.selected = tiles[6 - int((get_position().y / Globals.TILE_TOTAL_SIZE)) - num_of_letters].letter
        Events.emit_signal("reel_changed")

func get_selected() -> String:
    return tiles[6 - int((get_position().y / Globals.TILE_TOTAL_SIZE)) - num_of_letters].letter

func get_num_of_letters() -> int:
    return len(tiles)

func use(letter: String) -> void:
    for tile in tiles:
        if tile.letter == letter:
            tile.used = true
            break


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
    pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta: float) -> void:
#    pass
