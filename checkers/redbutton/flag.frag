precision mediump float;
uniform sampler2D tex;

const vec3 COLOR = vec3( COLOR_R, COLOR_G, COLOR_B ) / 255.0;
// L0, L1, ANGLE

const float colorEpsilon = 8.0 / 255.0;
const float Lepsilon = 1.0;
const float angleEpsilon = 4.0 / 360.0 * 2.0 * 3.1415926;


//
bool CheckColor( vec3 c )
{
	return length( COLOR - c ) < colorEpsilon;
}


//
bool CheckLength( vec2 p0, vec2 p1 )
{
	float l = length( p0 - p1 );
	return abs( l - L0 ) < Lepsilon || abs( l - L1 ) < Lepsilon;
}


float DegToRad( float deg )
{
	return deg / 360.0 * 2.0 * 3.1415926;
}


//
bool CheckAngle( float cosA )
{
	float CosA = cos( DegToRad( ANGLE ) );
	return abs( cosA - CosA ) < angleEpsilon;
}


//
bool CheckCrossing( vec2 v11, vec2 v12, vec2 v21, vec2 v22 )
{
	vec3 cut1 = vec3( vec3( v12, 0.0 ) - vec3( v11, 0.0 ) );
	vec3 cut2 = vec3( vec3( v22, 0.0 ) - vec3( v21, 0.0 ) );
	vec3 prod1, prod2;

	prod1 = cross( cut1, vec3( v21, 0.0 ) - vec3( v11, 0.0 ) );
	prod2 = cross( cut1, vec3( v22, 0.0 ) - vec3( v11, 0.0 ) );

	float signDiff = abs( sign( prod1.z ) - sign( prod2.z ) );
	if( signDiff < 0.001 || abs( prod1.z ) < 0.001 || abs( prod2.z ) < 0.001 )
		return false;

	prod1 = cross( cut2, vec3( v11, 0.0 ) - vec3( v21, 0.0 ) );
	prod2 = cross( cut2, vec3( v12, 0.0 ) - vec3( v21, 0.0 ) );

	signDiff = abs( sign( prod1.z ) - sign( prod2.z ) );
	if( signDiff < 0.001 || abs( prod1.z ) < 0.001 || abs( prod2.z ) < 0.001 )
		return false;

	return true;
}


//
void main()
{
	ivec2 offset[ 8 ];
	offset[ 0 ] = ivec2( -1, -1 );
	offset[ 1 ] = ivec2(  0, -1 );
	offset[ 2 ] = ivec2(  1, -1 );
	offset[ 3 ] = ivec2(  1,  0 );
	offset[ 4 ] = ivec2(  1,  1 );
	offset[ 5 ] = ivec2(  0,  1 );
	offset[ 6 ] = ivec2( -1,  1 );
	offset[ 7 ] = ivec2( -1,  0 );

	int sx = int( gl_FragCoord.x );
	int sy = int( gl_FragCoord.y );

	const int PointsNum = 1024;
	const int LinesNum = 1024;
	vec2 points[ PointsNum ];
	int pointsCounter = 0;
	vec4 ret =  vec4( 0.0, 1.0, 0.0, 1.0 );
	vec4 C =  vec4( 0.0, 0.0, 0.0, 0.0 );
	for( int y = 0; y < HEIGHT; y++ )
	{
		for( int x = 0; x < WIDTH; x++ )
		{
			ivec2 iuv = ivec2( x, y );
			vec2 uv = vec2( iuv ) / vec2( WIDTH, HEIGHT );
			vec4 centerPixel = texture2D( tex, uv );
			if( !CheckColor( centerPixel.rgb ) )
				continue;
			C = centerPixel;

			int counter = 0;
			for( int o = 0; o < 8; o++ )
			{

				ivec2 iuv = ivec2( x, y ) + offset[ o ];
				uv =  vec2( iuv ) / vec2( WIDTH, HEIGHT );
				vec4 pixel = texture2D( tex, uv );
				if( CheckColor( pixel.rgb ) )
					counter++;
			}

			if( counter != 1 )
				continue;

			if( pointsCounter >= PointsNum )
				break;

			points[ pointsCounter++ ] = vec2( iuv );
		}
	}

	vec4 lines[ LinesNum ];
	int linesCounter = 0;

	for( int i = 0; i < pointsCounter; i++ )
		for( int j = i + 1; j < pointsCounter; j++ )
		{
			vec2 pi = points[ i ];
			vec2 pj = points[ j ];
			if( !CheckLength( pi, pj ) )
				continue;

			lines[ linesCounter++ ] = vec4( pi.x, pi.y, pj.x, pj.y );
		}

	//
	ivec2 crossingLines[ LinesNum ];
	int crossingLinesCounter = 0;
	for( int i = 0; i < linesCounter; i++ )
		for( int j = i + 1; j < linesCounter; j++ )
		{
			vec2 Li0 = lines[ i ].xy;
			vec2 Li1 = lines[ i ].zw;
			vec2 Li = Li0 - Li1;
			vec2 Lj0 = lines[ j ].xy;
			vec2 Lj1 = lines[ j ].zw;
			vec2 Lj = Lj0 - Lj1;

			float cosA = dot( Li, Lj ) / length( Li ) / length( Lj );
			if( !CheckAngle( cosA ) )
				continue;

			if( !CheckCrossing( Li0, Li1, Lj0, Lj1 ) )
				continue;

			crossingLines[ crossingLinesCounter ] = ivec2( i, j );
			crossingLinesCounter++;
		}


	/*ret.x = float( pointsCounter ) / 256.0;
	ret.y = float( linesCounter ) / 256.0;
	ret.z = float( crossingLinesCounter ) / 256.0;
	ret.WIDTH = 0.0;
	if( sx == 1 )
		ret = C;
	if( sx >= 2){
		ret = vec4( 0.0, 0.0, 0.0, 0.0 );
		
		int pi = sx - 2;
		if( pi >= 0 && pi < pointsCounter ){
			ret.x = float( points[ pi ].x ) / 256.0;
			ret.y = float( points[ pi ].y ) / 256.0;
		}
		int li = sx - pointsCounter - 1;
		if( li >= 0 && li < linesCounter ){
			ret = lines[ li ] / 256.0;
		}
		int cli = sx - pointsCounter - linesCounter - 1;
		if( cli >= 0 && cli < crossingLinesCounter ){
			ret.x = ( float( crossingLines[ cli ].x ) ) / 256.0;
			ret.y = ( float( crossingLines[ cli ].y ) ) / 256.0;
		}

	}
	gl_FragColor = ret;*/
	if( crossingLinesCounter == 0 )
		discard;

	vec4 flag[ 8 ];
	flag[ 0 ] = vec4( F0,  F1,  F2,  F3 )  / 255.0;
	flag[ 1 ] = vec4( F4,  F5,  F6,  F7 )  / 255.0;
	flag[ 2 ] = vec4( F8,  F9,  F10, F11 ) / 255.0;
	flag[ 3 ] = vec4( F12, F13, F14, F15 ) / 255.0;
	flag[ 4 ] = vec4( F16, F17, F18, F19 ) / 255.0;
	flag[ 5 ] = vec4( F20, F21, F22, F23 ) / 255.0;
	flag[ 6 ] = vec4( F24, F25, F26, F27 ) / 255.0;
	flag[ 7 ] = vec4( F28, F29, F30, F31 ) / 255.0;
	
	gl_FragColor = flag[ int( gl_FragCoord.x ) ];
}
