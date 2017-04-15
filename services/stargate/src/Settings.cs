using System;
using System.IO;
using System.Security.Cryptography;
using Microsoft.Extensions.Configuration;
using stargåte.utils;

namespace stargåte
{
	static class Settings
	{
		static Settings()
		{
			ConfigRoot = new ConfigurationBuilder()
				.SetBasePath(Directory.GetCurrentDirectory())
				.AddIniFile(SettingsFilename, true, true)
				.Build();

			ConfigRoot.GetReloadToken().RegisterChangeCallback(o =>
			{
				Console.WriteLine("Reload settings");
				Update();
			}, null);

			var key = ConfigRoot["key"];
			if(key == null || !Guid.TryParse(key, out _))
			{
				Key = new byte[16];
				using(var rng = RandomNumberGenerator.Create())
					rng.GetBytes(Key);

				File.WriteAllText(SettingsFilename, $"key={new Guid(Key)}{Environment.NewLine}");
			}

			ConfigRoot.Reload();
		}

		public const int MaxFieldLength = 340;

		public const int MaxIncomingSize = 65536;
		public const int MaxIncomingDimensions = 32768;

		public const int MaxSpectrumSize = 8192;
		public const int MaxTransmissionInfoSize = 8192;

		public static TimeSpan WsPingInterval = TimeSpan.FromSeconds(3);

		public static byte[] Key;

		public static TimeSpan Ttl;
		public static int ReadWriteTimeout;
		public static int WsSendTimeout;

		private static void Update()
		{
			if(Guid.TryParse(ConfigRoot["key"], out var key))
				Key = key.ToByteArray();

			Ttl = ConfigRoot["ttl"].TryParseOrDefault(TimeSpan.FromMinutes(30));
			ReadWriteTimeout = ConfigRoot["rwTimeout"].TryParseOrDefault(3000);
			WsSendTimeout = ConfigRoot["wsSendTimeout"].TryParseOrDefault(2000);
		}

		private const string SettingsFilename = "stargate.ini";

		private static readonly IConfigurationRoot ConfigRoot;
	}
}