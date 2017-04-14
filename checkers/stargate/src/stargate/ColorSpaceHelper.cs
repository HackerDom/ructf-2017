using System;
using System.Drawing;

namespace checker.stargate
{
	internal static class ColorSpaceHelper
	{
		public static HSL ToHSL(this Color color)
		{
			int r = color.R, g = color.G, b = color.B;

			var max = Math.Max(Math.Max(r, g), b);
			var min = Math.Min(Math.Min(r, g), b);

			var l = (max + min) >> 1;

			int sum = max + min;
			int delta = max - min;

			int s;
			if(delta == 0)
				s = 0;
			else
			{
				if(sum > MAX)
					sum = 510 - sum;
				s = MAX * delta / sum;
			}

			int h = 0;
			if(r == g && g == b)
				h = 0;
			else
			{
				var deltaX2 = delta << 1;
				if(r == max)
					h = (g < b ? MAX : 0) + MAXdiv3 * (g - b) / deltaX2;
				else if(g == max)
					h = MAXdiv3 + (b - r) * MAXdiv3 / deltaX2;
				else if(b == max)
					h = MAXdiv3mul2 + (r - g) * MAXdiv3 / deltaX2;
			}

			return new HSL {H = (byte)h, S = (byte)s, L = (byte)l};
		}

		private const int MAX = byte.MaxValue;
		private const int MAXdiv3 = MAX / 3;
		private const int MAXdiv3mul2 = MAXdiv3 * 2;
	}

	internal struct HSL
	{
		public byte H;
		public byte S;
		public byte L;
	}
}