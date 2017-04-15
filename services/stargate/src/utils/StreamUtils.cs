using System.IO;
using System.Threading;
using System.Threading.Tasks;

namespace stargåte.utils
{
	static class StreamUtils
	{
		public static async Task<int> ReadAllAsync(this Stream source, byte[] buffer, CancellationToken token)
		{
			int bytesRead, total = 0;
			while((bytesRead = await source.ReadAsync(buffer, total, buffer.Length - total, token).ConfigureAwait(false)) > 0)
				total += bytesRead;
			return total;
		}
	}
}