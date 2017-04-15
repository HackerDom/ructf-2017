using System.Drawing;
using System.IO;

namespace stargåte.utils
{
	static class BitmapHelper
	{
		public static Bitmap TryFromBuffer(byte[] array, int length)
		{
			try { return Image.FromStream(new MemoryStream(array, 0, length, false, true)) as Bitmap; } catch { return null; }
		}
	}
}