using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.CompilerServices;

namespace checker.stargate
{
	internal class DirectBitmap : IDisposable
	{
		public unsafe DirectBitmap(Bitmap bmp)
		{
			this.bmp = bmp;
			if(bmp.PixelFormat != PixelFormat.Format32bppArgb)
				throw new ArgumentException($"Unsupported pixel format '{bmp.PixelFormat}'", nameof(bmp));
			data = bmp.LockBits(new Rectangle(0, 0, bmp.Width, bmp.Height), ImageLockMode.ReadOnly, bmp.PixelFormat);
			ptr = (int*)data.Scan0;
		}

		[MethodImpl(MethodImplOptions.AggressiveInlining)]
		public unsafe Color FastGetPixel(int x, int y)
		{
			if(x >= data.Width || y >= data.Height)
				throw new ArgumentOutOfRangeException();
			return Color.FromArgb(ptr[y * data.Width + x]);
		}

		[MethodImpl(MethodImplOptions.AggressiveInlining)]
		public unsafe void FastSetPixel(int x, int y, Color color)
		{
			if(x >= data.Width || y >= data.Height)
				throw new ArgumentOutOfRangeException();
			ptr[y * data.Width + x] = color.ToArgb();
		}

		public unsafe Spectrum CalcSpectrum()
		{
			var spectrum = Spectrum.Create();
			for(int i = 0; i < data.Width * data.Height; i++)
				spectrum.Update(Color.FromArgb(ptr[i]));
			return spectrum;
		}

		public void Dispose()
		{
			bmp.UnlockBits(data);
			bmp.Dispose();
		}

		public int Width => data.Width;
		public int Height => data.Height;

		private readonly Bitmap bmp;
		private readonly BitmapData data;
		private readonly unsafe int* ptr;
	}
}