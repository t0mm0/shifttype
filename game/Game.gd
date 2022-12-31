extends Node2D


# Declare member variables here. Examples:
# var a: int = 2
# var b: String = "text"
var puzzle: Puzzle
var reels: Array
var reels_left: float
var reel_moving: int = -1
var reel_offset: float = 0.0
var screen_size: Vector2
var progress: float = 0.0 setget set_progress
var time: float = 0.0
var found_words: PoolStringArray = PoolStringArray()

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
    screen_size = get_viewport().get_visible_rect().size

    var saved: Dictionary = load_game()
    get_tree().paused = false

    if saved:
        puzzle = Puzzle.new(Puzzle.puzzle_mode.DAILY, saved["num_letters"], saved["num_core"], saved["seed"])
        time = saved["time"]
    else:
        var difficulty: Array = Globals.DIFFICULTY[Time.get_date_dict_from_system()["weekday"]]
        puzzle = Puzzle.new(Puzzle.puzzle_mode.DAILY, difficulty[0], difficulty[1])
#        puzzle = Puzzle.new(Puzzle.puzzle_mode.DAILY, 5, 3)

    var x = (screen_size.x / 2) - ((len(puzzle.reels) * Globals.TILE_SIZE / 2)
        + (Globals.TILE_SPACING * (len(puzzle.reels) - 1) / 2))
    reels_left = x
    var index: int = 0
    for reel in puzzle.reels:
        var r = Reel.new(reel)
        var y: float
        if saved:
            y = saved["reel_pos"][index]
        else:
            y = (Globals.TILE_TOTAL_SIZE *
                round(screen_size.y / Globals.TILE_TOTAL_SIZE / 2) -
                    round(len(reel) / 2) * Globals.TILE_TOTAL_SIZE)
        r.set_position(Vector2(x, y))
        reels.append(r)
        add_child(r)
        x += Globals.TILE_SIZE + Globals.TILE_SPACING
        index += 1

    if saved:
        for word in saved["found_words"]:
            test_word(word)


    Events.connect("reel_changed", self, "_on_reel_changed")

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
    time += delta

func pos_to_reel(pos: Vector2) -> int:
    # get the reel number from screen position
    return int((pos.x - reels_left) / (Globals.TILE_SIZE + Globals.TILE_SPACING)) if pos.x > reels_left else -1

func _input(event: InputEvent) -> void:
    # handle dragging of reels
    if event is InputEventScreenTouch:
        # initial touch
        if event.pressed:
            var r = pos_to_reel(event.position)
            if r < reels.size():
                reel_moving = r
                reel_offset = event.position.y - reels[r].position.y
        # release touch
        else:
            reels[reel_moving].settle_down()
            reel_moving = -1
    # dragging
    elif event is InputEventScreenDrag and reel_moving > -1:
        if reel_moving > -1:
            var max_y: float = screen_size.y / 2
            var min_y: float = max_y - (
                (reels[reel_moving].num_of_letters * Globals.TILE_TOTAL_SIZE)
                - (Globals.TILE_SPACING * 2))
            reels[reel_moving].position.y = clamp(event.position.y - reel_offset, min_y, max_y)

func _on_reel_changed() -> void:
    var word: String = get_current_word()
    test_word(word)

func test_word(word: String) -> void:
    # test if a word is real and if so set its letters as used
    if(puzzle.test_word(word)):
        if word in found_words:
            return
        use(word)
        found_words.append(word)
        var new_progress = get_progress()
        if new_progress != progress:
            self.progress = new_progress

func use(word: String) -> void:
    # mark letters in word as used
    var index: int = 0
    for c in word:
        reels[index].use(c)
        index += 1

func get_progress() -> float:
    # find percentage of letters used
    var total := 0.0
    var done := 0.0
    for reel in reels:
        for tile in reel.tiles:
            total += 1
            if tile.used:
                done += 1
    return done / total * 100.0

func set_progress(new_progress: float) -> void:
    Events.emit_signal("progress_changed", new_progress)
    progress = new_progress
    if progress == 100:
        get_tree().paused = true
        save_game()
        yield(get_tree().create_timer(0.7), "timeout")
        $CompletePopup.update_and_show(puzzle, found_words, time)

func get_current_word() -> String:
    var word: String = ""
    for reel in reels:
        word += reel.selected
    return word

func _notification(what: int) -> void:
    match what:
        NOTIFICATION_WM_QUIT_REQUEST:
            save_game()
            get_tree().quit()
        NOTIFICATION_WM_GO_BACK_REQUEST:
            save_game()
            get_tree().change_scene("res://game/menus/MainMenu.tscn")
        NOTIFICATION_WM_FOCUS_OUT:
            $PausePopup.show()
            save_game()
            get_tree().paused = true
        NOTIFICATION_WM_FOCUS_IN:
            load_game()

func save_game() -> void:
    var saved: Dictionary = {}
    saved["found_words"] = found_words
    saved["num_core"] = puzzle.num_core
    saved["num_letters"] = puzzle.num_letters
    saved["time"] = time
    saved["seed"] = puzzle.rng_seed
    saved["reel_pos"] = []
    for reel in reels:
        saved["reel_pos"].append(reel.get_position().y)

#    print(saved)
    var save_game = File.new()
    save_game.open("user://daily.save", File.WRITE)
    save_game.store_line(to_json(saved))
    save_game.close()

func load_game() -> Dictionary:
    var save_game = File.new()
    if not save_game.file_exists("user://daily.save"):
        return {} # Error! We don't have a save to load.

    save_game.open("user://daily.save", File.READ)
    var saved = parse_json(save_game.get_line())
    save_game.close()

    # check it is todays save
    if not "seed" in saved or saved["seed"] != Puzzle.get_daily_seed():
        print("save game data does not have today's seed so ignoring")
        return {}

#    print(saved)
    return saved

func _on_ContinueButton_pressed() -> void:
    get_tree().paused = false
    $PausePopup.hide()

func _on_MenuButton_pressed() -> void:
    $PausePopup.hide()
    get_tree().change_scene("res://game/menus/MainMenu.tscn")

