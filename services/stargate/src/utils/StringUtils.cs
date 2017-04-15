using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;

namespace stargåte.utils
{
	static class StringUtils
	{
		[MethodImpl(MethodImplOptions.AggressiveInlining)]
		public static string RemoveWhiteSpaces(this string value) => value == null ? null : WhiteSpaces.Replace(value, string.Empty);

		private static readonly Regex WhiteSpaces = new Regex(@"\s+", RegexOptions.Compiled | RegexOptions.CultureInvariant);
	}
}