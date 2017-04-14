using System;
using System.Threading.Tasks;

namespace checker.rnd
{
	internal static class RndUtil
	{
		public static Random ThreadStaticRnd => rnd ?? (rnd = new Random(Guid.NewGuid().GetHashCode()));

		public static Task RndDelay(int max) => Task.Delay(ThreadStaticRnd.Next(max));

		[ThreadStatic] private static Random rnd;
	}
}