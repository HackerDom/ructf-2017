precision mediump float;
uniform sampler2D tex;
varying mediump vec2 uv;

void main()
{
#if VARIANT0 == 1
	// X_GR, Y_GR  > 1.0, X_LS, Y_LS < 0.0
	if( uv.x > X_GR )
		discard;
	if( uv.y > Y_GR )
		discard;
	if( uv.x < X_LS )
		discard;
	if( uv.y < Y_LS )
		discard;
#endif

#if VARIANT1 == 1
	// A_X_GR, A_Y_GR > 1.0, A_X_LS, A_Y_LS < -1.0
	vec2 a = uv * 2.0 - 1.0;
	if( a.x > A_X_GR )
		discard;
	if( a.y > A_Y_GR )
		discard;
	if( a.x < A_X_LS )
		discard;
	if( a.y < A_Y_LS )
		discard;
#endif

#if VARIANT2 == 1
	// 0 - 1
	// 1 - -1
	// B_X_GR, B_Y_GR > 1.0, B_X_LS, B_Y_LS < -1.0
	vec2 b = uv * -2.0 + 1.0;
	if( b.x > B_X_GR )
		discard;
	if( b.y > B_Y_GR )
		discard;
	if( b.x < B_X_LS )
		discard;
	if( b.y < B_Y_LS )
		discard;
#endif


	vec2 testUv = gl_FragCoord.xy / vec2( WIDTH, HEIGHT );
	if( length( uv - testUv ) < 0.01 )
		gl_FragColor = vec4( R, G, B, A ) / 255.0;
	else
		gl_FragColor = vec4( 0.0, 0.0, 0.0, 0.0 );
}