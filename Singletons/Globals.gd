extends Node

const WORDS_PATH := "res://assets"
const WORDS_MIN_LENGTH := 5
const WORDS_MAX_LENGTH := 7

const TILE_SIZE := 95
const TILE_SPACING := 5
const TILE_TOTAL_SIZE := TILE_SIZE + TILE_SPACING

const DIFFICULTY = {0: [7, 5], 1: [5, 4], 2: [5, 5], 3: [6, 4],
                    4: [6, 5], 5: [7, 4], 6: [7, 5]}

# defaults
const BG_COLOR : Color = Color(1.0, 0.82, 0.4, 1.0)
const PROG_COLOR : Color = Color(0.93, 0.28, 0.43, 1.0)
const TILE_COLOR : Color = Color(0.0, 0.5647, 1.0, 1.0)
const USED_COLOR : Color = Color.darkgray

var BG_Color : Color = BG_COLOR
var Prog_Color : Color = PROG_COLOR
var Tile_Color : Color = TILE_COLOR
var Used_Color : Color = USED_COLOR

func _ready() -> void:
    load_config()

func save_config() -> void:
    var config = ConfigFile.new()
    config.set_value("look", "bg_color", BG_Color)
    config.set_value("look", "prog_color", Prog_Color)
    config.set_value("look", "tile_color", Tile_Color)
    config.set_value("look", "used_color", Used_Color)
    config.save("user://shifttype.config")

func load_config() -> void:
    var config = ConfigFile.new()

    # Load data from a file.
    var err = config.load("user://shifttype.config")

    # If the file didn't load, ignore it.
    if err != OK:
        return

    BG_Color = config.get_value("look", "bg_color", BG_COLOR)
    Prog_Color = config.get_value("look", "prog_color", PROG_COLOR)
    Tile_Color = config.get_value("look", "tile_color", TILE_COLOR)
    Used_Color = config.get_value("look", "used_color", USED_COLOR)
