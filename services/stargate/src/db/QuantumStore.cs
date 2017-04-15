using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using ProtoBuf;
using stargåte.utils;

namespace stargåte.db
{
	class QuantumStore<T>
	{
		public QuantumStore(string filename, Action<T> add)
		{
			var filepath = Path.Combine(Directory.GetCurrentDirectory(), filename);
			Directory.CreateDirectory(Path.GetDirectoryName(filepath));
			stream = new FileStream(filepath, FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.Read, BufferSize, FileOptions.SequentialScan | FileOptions.Asynchronous);
			TryLoad(stream, add);
			new Thread(FlushLoop) {IsBackground = true}.Start();
		}

		public async Task WriteAsync(T item)
		{
			using(await asyncLock.AcquireAsync(CancellationToken.None).ConfigureAwait(false))
				Serializer.SerializeWithLengthPrefix(stream, item, PrefixStyle.Base128, 1);
		}

		public async Task FlushAsync()
		{
			using(await asyncLock.AcquireAsync(CancellationToken.None).ConfigureAwait(false))
				await stream.FlushAsync().ConfigureAwait(false);
		}

		private static void TryLoad(Stream stream, Action<T> load)
		{
			// NOTE: Deserializer moves straight by item boundaries
			long pos = 0L;
			try
			{
				foreach(var item in Serializer.DeserializeItems<T>(stream, PrefixStyle.Base128, 1))
				{
					load(item);
					pos = stream.Position;
				}
			}
			catch
			{
				stream.SetLength(pos);
			}
		}

		private async void FlushLoop()
		{
			while(true)
			{
				await Task.Delay(FlushPeriod).ConfigureAwait(false);
				await FlushAsync();
			}
		}

		private const int FlushPeriod = 3000;
		private const int BufferSize = 512 * 1024;
		private readonly AsyncLockSource asyncLock = new AsyncLockSource();
		private readonly Stream stream;
	}
}