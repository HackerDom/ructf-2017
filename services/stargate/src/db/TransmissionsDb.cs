using System;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;

namespace stargåte.db
{
	static class TransmissionsDb
	{
		public static async Task<bool> TryAdd(Transmission item)
		{
			if(!Index.TryAdd(item.Name, item))
				return false;
			await Store.WriteAsync(item).ConfigureAwait(false);
			return true;
		}

		[MethodImpl(MethodImplOptions.AggressiveInlining)]
		public static Transmission Find(string name)
		{
			return Index.GetOrDefault(name);
		}

		public static void Close()
		{
			Store.FlushAsync().Wait(3000);
		}

		private static readonly HyperspatialIndex<string, Transmission> Index = new HyperspatialIndex<string, Transmission>(Settings.Ttl, StringComparer.Ordinal);
		private static readonly QuantumStore<Transmission> Store = new QuantumStore<Transmission>("data/transmissions.db", transmission => Index.TryAdd(transmission.Name, transmission, transmission.Time));
	}
}