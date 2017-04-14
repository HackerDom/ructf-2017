uniform sampler2D tex;

varying mediump vec2 uv;

void main()
{
	gl_FragColor = texture2D( tex, uv );
}