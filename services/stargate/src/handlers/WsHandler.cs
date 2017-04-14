using System;
using System.Collections.Concurrent;
using System.Linq;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using stargåte.utils;

namespace stargåte.handlers
{
	static class WsHandler
	{
		public static async Task TryProcessWebSocketRequest(HttpContext context)
		{
			using(var ws = await context.WebSockets.AcceptWebSocketAsync().ConfigureAwait(false))
			{
				await ws.SendAsync(new ArraySegment<byte>(HelloMessage), WebSocketMessageType.Text, true, context.RequestAborted).Wrap().WithTimeout(Settings.ReadWriteTimeout).ConfigureAwait(false);
				var semaphore = new SemaphoreSlim(0, 1);
				Clients.TryAdd(ws, semaphore);
				await semaphore.WaitAsync(context.RequestAborted).ConfigureAwait(false);
			}
		}

		public static async Task BroadcastAsync<T>(T msg, CancellationToken token)
		{
			using(var pooled = await ResponsePool.AcquireAsync().ConfigureAwait(false))
			{
				var buffer = ProtoBufHelper.SerializeAsArraySegment(pooled.Item, msg);
				await Task.WhenAll(Clients.Select(pair => Task.Run(() => TrySendAsync(pair.Key, buffer, token), token))).ConfigureAwait(false);
			}
		}

		private static async Task TrySendAsync(WebSocket ws, ArraySegment<byte> buffer, CancellationToken token)
		{
			try
			{
				if(ws.State == WebSocketState.Open && await ws.SendAsync(buffer, WebSocketMessageType.Binary, true, token).Wrap().WithTimeout(Settings.ReadWriteTimeout).ConfigureAwait(false))
					return;
			}
			catch { /* ignored */ }
			Unregister(ws);
		}

		private static void Unregister(WebSocket ws)
		{
			if(Clients.TryRemove(ws, out var sem))
				sem.Dispose();
		}

		private static readonly byte[] HelloMessage = Encoding.ASCII.GetBytes("hi");
		private static readonly ConcurrentDictionary<WebSocket, SemaphoreSlim> Clients = new ConcurrentDictionary<WebSocket, SemaphoreSlim>();
		private static readonly ReusableObjectPool<byte[]> ResponsePool = new ReusableObjectPool<byte[]>(() => new byte[Settings.MaxTransmissionInfoSize], null, 512);
	}
}