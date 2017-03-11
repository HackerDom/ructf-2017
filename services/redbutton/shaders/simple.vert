attribute vec4 v_pos;
attribute vec2 v_uv;

varying vec2 uv;

void main()
{
	gl_Position = v_pos;
	uv = v_uv;
}