using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using checker.stargate;

namespace checker.rnd
{
	internal static class RndBitmap
	{
		public static Bitmap RndBmp(int width, int height)
		{
			var files = Directory.GetFiles(DirPath);

			var file1 = (Bitmap)Image.FromFile(RndUtil.Choice(files));
			var file2 = (Bitmap)Image.FromFile(RndUtil.Choice(files));

			var bmp = new Bitmap(width, height, PixelFormat.Format32bppArgb);

			using(var dbmp = new DirectBitmap(bmp, 0, 0, width, height))
			using(var dbmp1 = GetRandomWindow(file1, width, height))
			using(var dbmp2 = GetRandomWindow(file2, width, height))
			{
				for(int x = 0; x < width; x++)
				for(int y = 0; y < height; y++)
					dbmp.FastSetPixel(x, y, dbmp1.FastGetPixel(x, y).Blend(dbmp2.FastGetPixel(x, y)));
			}

			return bmp;
		}

		private static DirectBitmap GetRandomWindow(Bitmap bmp, int width, int height) => new DirectBitmap(bmp, RndUtil.ThreadStaticRnd.Next(bmp.Width - width), RndUtil.ThreadStaticRnd.Next(bmp.Height - height), width, height);

		private static readonly string DirPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "img");
	}

	internal static class ColorHelper
	{
		public static Color Blend(this Color color1, Color color2)
		{
			var c1 = color1.ToArgb();
			var c2 = color2.ToArgb();
			return Color.FromArgb(((c1 >> 1) & NoHighestBits) + ((c2 >> 1) & NoHighestBits) + ((((c1 & LowestBits) + (c2 & LowestBits)) >> 1) & LowestBits));
		}

		private const int NoHighestBits = 0x7f7f7f7f;
		private const int LowestBits = 0x01010101;
	}
}