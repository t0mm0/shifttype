extends Node

var t: LetterTile

func _ready() -> void:
    $VBoxContainer/GridContainer/BGColorPickerButton.color = Globals.BG_Color
    $VBoxContainer/GridContainer/ProgColorPickerButton.color = Globals.Prog_Color
    $VBoxContainer/GridContainer/TileColorPickerButton.color = Globals.Tile_Color
    $VBoxContainer/GridContainer/UsedColorPickerButton.color = Globals.Used_Color

    var tileScene = preload("res://game/LetterTile.tscn")
    var size = Vector2(Globals.TILE_SIZE, Globals.TILE_SIZE)
    t = tileScene.instance()
    t.set_size(size)
    t.rect_min_size = size
    t.letter = "T"
    t.size_flags_horizontal = 0
    $VBoxContainer/GridContainer/TestTile.replace_by(t)

    var timer = Timer.new()
    add_child(timer)
    timer.autostart = true
    timer.wait_time = 1.0
    timer.one_shot = false
    timer.connect("timeout", self, "_timeout")
    timer.start()

func _timeout() -> void:
    if t.letter == "T":
        t.letter = "U"
        t.used = true
    else:
        t.letter = "T"
        t.used = false


func _notification(what: int) -> void:
    match what:
        NOTIFICATION_WM_QUIT_REQUEST:
            get_tree().quit()
        NOTIFICATION_WM_GO_BACK_REQUEST:
            get_tree().change_scene("res://game/menus/MainMenu.tscn")

func _on_BackButton_pressed() -> void:
    get_tree().change_scene("res://game/menus/MainMenu.tscn")


func _on_BGColorPickerButton_color_changed(color: Color) -> void:
    Globals.BG_Color = color
    Events.emit_signal("bg_color_changed", color)
    Globals.save_config()


func _on_ProgColorPickerButton_color_changed(color: Color) -> void:
    Globals.Prog_Color = color
    Events.emit_signal("prog_color_changed", color)
    Globals.save_config()


func _on_TileColorPickerButton_color_changed(color: Color) -> void:
    Globals.Tile_Color = color
    Events.emit_signal("tile_color_changed", color)
    Globals.save_config()


func _on_UsedColorPickerButton_color_changed(color: Color) -> void:
    Globals.Used_Color = color
    Events.emit_signal("used_color_changed", color)
    Globals.save_config()


func _on_ResetColors_pressed() -> void:
    Globals.BG_Color = Globals.BG_COLOR
    Globals.Prog_Color = Globals.PROG_COLOR
    Globals.Tile_Color = Globals.TILE_COLOR
    Globals.Used_Color = Globals.USED_COLOR
    $VBoxContainer/GridContainer/BGColorPickerButton.color = Globals.BG_COLOR
    $VBoxContainer/GridContainer/ProgColorPickerButton.color = Globals.PROG_COLOR
    $VBoxContainer/GridContainer/TileColorPickerButton.color = Globals.TILE_COLOR
    $VBoxContainer/GridContainer/UsedColorPickerButton.color = Globals.USED_COLOR
    Events.emit_signal("bg_color_changed", Globals.BG_Color)
    Events.emit_signal("prog_color_changed", Globals.Prog_Color)
    Events.emit_signal("tile_color_changed", Globals.Tile_Color)
    Events.emit_signal("used_color_changed", Globals.Used_Color)
    Globals.save_config()

