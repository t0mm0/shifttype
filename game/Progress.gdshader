shader_type canvas_item;

uniform float progress: hint_range(0, 1) = 0.3;
uniform vec4 bg_color: hint_color = vec4(1.0, 0.82, 0.4, 1.0);
uniform vec4 fg_color: hint_color = vec4(0.93, 0.28, 0.43, 1.0);
uniform vec4 selected_color: hint_color = vec4(1.0);
uniform bool draw_select = false;

vec4 overlay(vec4 base, vec4 blend){
	vec4 limit = step(0.5, base);
	return mix(2.0 * base * blend, 1.0 - 2.0 * (1.0 - base) * (1.0 - blend), limit);
}

void fragment() {
    COLOR = fg_color;
    if(UV.y < (sin((TIME * 4.7) + UV.x) + sin((-TIME * 2.2) + UV.x)) * 0.01 + (.975 - progress)) {
        COLOR = bg_color;
    }
    if(draw_select && (UV.y > 0.465 && UV.y < 0.549)) {
        COLOR = overlay(COLOR, selected_color);
    }
}