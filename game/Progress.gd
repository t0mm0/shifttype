extends Sprite

func _ready() -> void:
    Events.connect("progress_changed", self, "_on_progress_changed")
    Events.connect("bg_color_changed", self, "_on_bg_color_changed")
    Events.connect("prog_color_changed", self, "_on_prog_color_changed")
    get_material().set_shader_param("bg_color", Globals.BG_Color)
    get_material().set_shader_param("fg_color", Globals.Prog_Color)


func _on_progress_changed(progress: float) -> void:
    var tween := create_tween()
    tween.tween_property(get_material(), "shader_param/progress", progress / 100, 1
        ).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)

func _on_bg_color_changed(color: Color) -> void:
    get_material().set_shader_param("bg_color", color)

func _on_prog_color_changed(color: Color) -> void:
    get_material().set_shader_param("fg_color", color)
