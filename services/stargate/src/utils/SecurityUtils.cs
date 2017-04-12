namespace stargåte.utils
{
	static class SecurityUtils
	{
		public static unsafe bool FastTimingSecureEquals(this byte[] x, byte[] y)
		{
			if(ReferenceEquals(x, y))
				return true;
			if(x == null || y == null || x.Length != y.Length)
				return false;
			int len = x.Length;
			if(len == 0)
				return true;
			ulong res = 0UL;
			int ulonglen = len >> 3;
			fixed(byte* px = x, py = y)
			{
				byte* ppx = px, ppy = py;
				for(int i = 0; i < ulonglen; i++, ppx += sizeof(long), ppy += sizeof(long))
					res |= *((ulong*)ppx) ^ *((ulong*)ppy);
				for(int i = ulonglen << 3; i < len; i++, ppx++, ppy++)
					res |= (ulong)(*ppx) ^ (ulong)(*ppy);
				return res == 0;
			}
		}
	}
}