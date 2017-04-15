using System.Drawing;
using System.Drawing.Imaging;
using System.IO;

namespace checker.stargate
{
	internal static class BitmapHelper
	{
		public static byte[] ToByteArray(this Bitmap bitmap)
		{
			using(var ms = new MemoryStream())
			{
				bitmap.Save(ms, ImageFormat.Png);
				return ms.ToArray();
			}
		}

		public static Spectrum CalcSpectrum(this Bitmap bmp)
		{
			using(var dbmp = new DirectBitmap(bmp))
				return dbmp.CalcSpectrum();
		}
	}
}