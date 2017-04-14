using System;
using System.Globalization;
using System.Runtime.CompilerServices;

namespace stargåte.utils
{
	static class PrimitiveTypeUtils
	{
		[MethodImpl(MethodImplOptions.AggressiveInlining)]
		public static int TryParseOrDefault(this string value, int defaultValue) => int.TryParse(value, NumberStyles.Integer, NumberFormatInfo.InvariantInfo, out int result) ? result : defaultValue;

		[MethodImpl(MethodImplOptions.AggressiveInlining)]
		public static TimeSpan TryParseOrDefault(this string value, TimeSpan defaultValue) => TimeSpan.TryParse(value, CultureInfo.InvariantCulture, out TimeSpan result) ? result : defaultValue;
	}
}