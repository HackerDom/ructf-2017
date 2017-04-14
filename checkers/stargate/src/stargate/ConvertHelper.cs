using System;
using System.Text;

namespace checker.stargate
{
	internal static class ConvertHelper
	{
		public static string TryFromBase64String(string b64)
		{
			try
			{
				return Encoding.UTF8.GetString(Convert.FromBase64String(b64));
			}
			catch
			{
				return null;
			}
		}
	}
}