using System;
using System.Net.WebSockets;
using System.Threading;
using System.Threading.Tasks;

namespace checker.net
{
	internal class AsyncWebSocketClient : IDisposable
	{
		private AsyncWebSocketClient(ClientWebSocket client, int maxMsgSize)
		{
			this.client = client;
			this.maxMsgSize = maxMsgSize;
		}

		public static async Task<AsyncWebSocketClient> TryConnectAsync(Uri uri, int maxMsgSize, int timeout)
		{
			ClientWebSocket client = null;
			try
			{
				client = new ClientWebSocket();
				using(var source = new CancellationTokenSource(timeout))
				{
					await client.ConnectAsync(uri, source.Token).ConfigureAwait(false);
					return new AsyncWebSocketClient(client, maxMsgSize);
				}
			}
			catch(Exception e)
			{
				await Console.Error.WriteLineAsync($"ws connect error: {e}").ConfigureAwait(false);
				client?.Dispose();
				return null;
			}
		}

		public async Task<T> TryWaitMessageAsync<T>(Func<ArraySegment<byte>, Tuple<bool, T>> filter, int timeout)
		{
			var buffer = new ArraySegment<byte>(new byte[maxMsgSize]);
			using(var source = new CancellationTokenSource(timeout))
			{
				try
				{
					while(!source.IsCancellationRequested)
					{
						while(client.State == WebSocketState.Open)
						{
							var result = await client.ReceiveAsync(buffer, source.Token).ConfigureAwait(false);
							await Console.Error.WriteLineAsync($"ws {result.MessageType.ToString().ToLowerInvariant()} type, got {result.Count} bytes, {(result.EndOfMessage ? "complete" : "partial")} msg").ConfigureAwait(false);

							var offset = buffer.Offset + result.Count;
							if(result.EndOfMessage || offset == buffer.Array.Length)
							{
								buffer = new ArraySegment<byte>(buffer.Array, 0, offset);
								break;
							}

							buffer = new ArraySegment<byte>(buffer.Array, offset, buffer.Array.Length - offset);
						}

						var tuple = filter(buffer);
						if(tuple.Item1)
							return tuple.Item2;
					}
				}
				catch(Exception e)
				{
					if(!(e is OperationCanceledException || e is ObjectDisposedException))
						await Console.Error.WriteLineAsync($"ws receive error: {e}").ConfigureAwait(false);
				}
			}

			return default(T);
		}

		public void Dispose()
		{
			try { client.Dispose(); } catch { /* ignored */ }
		}

		private readonly int maxMsgSize;
		private readonly ClientWebSocket client;
	}
}