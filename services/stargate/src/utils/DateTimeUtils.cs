using System;

namespace stargåte.utils
{
	static class DateTimeUtils
	{
		public static long ToTimestamp(this DateTime dateTime) => (long)(dateTime - UnixEpoch).TotalMilliseconds;

		private static readonly DateTime UnixEpoch = new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc);
	}
}