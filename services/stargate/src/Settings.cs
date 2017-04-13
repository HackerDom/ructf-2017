using System.Text;

namespace stargåte
{
	static class Settings
	{
		static Settings()
		{
			/*Key = new byte[16];
			using(var rng = RandomNumberGenerator.Create())
				rng.GetBytes(Key);*/
		}

		public const int MaxFieldLength = 340;

		public const int MaxMatterSize = 65536;
		public const int MaxMatterDimensions = 32768;

		public const long MaxSpectrumSize = 16384;
		public static int MaxTransmissionInfoSize = 1024;

		public static readonly byte[] Key = Encoding.ASCII.GetBytes("It's_is_a_secret");

		public const int ReadWriteTimeout = 3000;
	}
}