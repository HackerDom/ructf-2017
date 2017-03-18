precision mediump float;
uniform sampler2D tex;

const vec3 color = vec3( 237.0, 28.0, 36.0 ) / 256.0;
//const float L0 = 30.0;
//const float L1 = 40.0;
//const float angle = 89.5;
const float L0 = 40.0;
const float L1 = 26.0;
const float angle = 90.0;
//const float L0 = 55.0;
//const float L1 = 42.2;
//const float angle = 61.8;
//const float L0 = 28.6;
//const float L1 = 72.45;
//const float angle = 79.5;

const float colorEpsilon = 8.0 / 256.0;
const float Lepsilon = 1.0;
const float angleEpsilon = 4.0 / 360.0 * 2.0 * 3.1415926;


void PrintFlag()
{
	vec4 a[ 4 ];
	a[ 0 ] = vec4( 1.0, 0.0, 0.0, 1.0 );
	a[ 1 ] = vec4( 0.0, 1.0, 0.0, 1.0 );
	a[ 2 ] = vec4( 0.0, 0.0, 1.0, 1.0 );
	a[ 3 ] = vec4( 1.0, 1.0, 1.0, 1.0 );
	
	gl_FragColor = a[ int( gl_FragCoord.y ) * 2 + int( gl_FragCoord.x ) ];
}


//
void PrintBlank()
{
	gl_FragColor = vec4( 0.0, 0.0, 0.0, 0.0 );
}


//
bool CheckColor( vec3 c )
{
	return length( c ) > 0.0;//length( color - c ) < colorEpsilon;
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
	float CosA = cos( DegToRad( angle ) );
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
	const int w = 256;
	const int h = 256;
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
	for( int y = 0; y < h; y++ )
	{
		for( int x = 0; x < w; x++ )
		{
			ivec2 iuv = ivec2( x, y );
			vec2 uv = vec2( iuv ) / vec2( w, h );
			vec4 centerPixel = texture2D( tex, uv );
			if( !CheckColor( centerPixel.rgb ) )
				continue;
			C = centerPixel;

			int counter = 0;
			for( int o = 0; o < 8; o++ )
			{

				ivec2 iuv = ivec2( x, y ) + offset[ o ];
				uv =  vec2( iuv ) / vec2( w, h );
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


	ret.x = float( pointsCounter ) / 256.0;
	ret.y = float( linesCounter ) / 256.0;
	ret.z = float( crossingLinesCounter ) / 256.0;
	ret.w = 0.0;
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
	gl_FragColor = ret;
}
