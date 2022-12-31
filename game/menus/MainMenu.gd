extends Node


# Declare member variables here. Examples:
# var a: int = 2
# var b: String = "text"


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
    get_tree().set_auto_accept_quit(false)	# Must be false to allow pause menu to work on Android
    get_tree().set_quit_on_go_back(false)	# Must be false to allow pause menu to work on Android

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta: float) -> void:
#    pass


func _on_StartButton_pressed() -> void:
    get_tree().change_scene("res://game/Game.tscn")

func _notification(what: int) -> void:
    match what:
        NOTIFICATION_WM_QUIT_REQUEST, NOTIFICATION_WM_GO_BACK_REQUEST:
            get_tree().quit()
