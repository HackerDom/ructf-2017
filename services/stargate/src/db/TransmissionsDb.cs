using System;
using System.Collections.Concurrent;
using System.Threading.Tasks;

namespace stargåte.db
{
	static class TransmissionsDb
	{
		public static async Task<bool> TryAdd(Transmission item)
		{
			if(!Dict.TryAdd(item.Name, item))
				return false;
			await Store.WriteAsync(item).ConfigureAwait(false);
			return true;
		}

		public static Transmission Find(string name)
		{
			return Dict.TryGetValue(name, out Transmission item) ? item : null;
		}

		public static void Close()
		{
			Store.FlushAsync().Wait(3000);
		}

		private static readonly ConcurrentDictionary<string, Transmission> Dict = new ConcurrentDictionary<string, Transmission>(StringComparer.Ordinal);
		private static readonly QuantumStore<Transmission> Store = new QuantumStore<Transmission>("data/transmissions.db", transmission => Dict[transmission.Name] = transmission);
	}
}