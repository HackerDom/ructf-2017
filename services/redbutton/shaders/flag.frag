precision mediump float;

void main()
{
	vec4 a[ 4 ];
	a[ 0 ] = vec4( 1.0, 0.0, 0.0, 1.0 );
	a[ 1 ] = vec4( 0.0, 1.0, 0.0, 1.0 );
	a[ 2 ] = vec4( 0.0, 0.0, 1.0, 1.0 );
	a[ 3 ] = vec4( 1.0, 1.0, 1.0, 1.0 );
	const int size = 1 * 1024;
	vec4 c[ size ];
	for( int i = 0; i < int( gl_FragCoord.y ); i++ )
		c[ i ].x = gl_FragCoord.x;
	for( int i = 0; i < size; i++ )
		a[ 0 ].a += c[ i ].x;
	gl_FragColor = a[ int( gl_FragCoord.y ) * 2 + int( gl_FragCoord.x ) ];
}
