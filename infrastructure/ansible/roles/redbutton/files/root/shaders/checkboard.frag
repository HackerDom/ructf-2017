precision mediump float;
varying mediump vec2 uv;
uniform vec4 color;

void main()
{
	float x = gl_FragCoord.x;
	float y = gl_FragCoord.y;
	vec4 ret = vec4( 0 );
	if( mod( x, 2.0 ) > 1.0 && mod( y, 2.0 ) > 1.0 )
		ret = color;
	x = x + 1.0;
	y = y + 1.0;
	if( mod( x, 2.0 ) > 1.0 && mod( y, 2.0 ) > 1.0 )
		ret = color;
	ret.a = 1.0;
	gl_FragColor = ret * vec4( uv.x, uv.x, uv.y, 1.0 );
}
