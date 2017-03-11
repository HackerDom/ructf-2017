varying mediump vec2 uv;

void main()
{
	gl_FragColor = vec4( 1.0, uv.x, uv.y, 1.0 );
}
