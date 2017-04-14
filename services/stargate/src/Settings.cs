using System;
using System.Security.Cryptography;

namespace stargåte
{
	static class Settings
	{
		static Settings()
		{
			Key = new byte[16];
			using(var rng = RandomNumberGenerator.Create())
				rng.GetBytes(Key);
		}

		public const int MaxFieldLength = 340;

		public const int MaxIncomingSize = 65536;
		public const int MaxIncomingDimensions = 32768;

		public const int MaxSpectrumSize = 16384;
		public const int MaxTransmissionInfoSize = 1024;

		public static readonly byte[] Key;

		public static TimeSpan Ttl = TimeSpan.FromMinutes(30);

		public const int ReadWriteTimeout = 3000;

		public static TimeSpan WsPingInterval = TimeSpan.FromSeconds(3);
	}
}