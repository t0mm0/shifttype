extends Sprite

func _ready() -> void:
    Events.connect("progress_changed", self, "_on_progress_changed")

func _on_progress_changed(progress: float) -> void:
    var tween := create_tween()
    tween.tween_property(get_material(), "shader_param/progress", progress / 100, 1
        ).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)
