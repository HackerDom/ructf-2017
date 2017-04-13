using System;
using System.Drawing;
using System.Linq;
using System.Security.Cryptography;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using ProtoBuf;
using stargåte.db;
using stargåte.utils;

namespace stargåte.handlers
{
	static class IncomingCallHandler
	{
		public static async Task<HttpResult> ProcessRequest(HttpContext context)
		{
			context.Response.ContentType = "text/plain; charset=utf-8";

			var name = context.Request.Headers["X-SG1-Name"].FirstOrDefault();
			if(string.IsNullOrEmpty(name))
				return new HttpResult {StatusCode = 400, Message = "Substance Without Name"};

			var secret = context.Request.Headers["X-SG1-Entropy"].FirstOrDefault();
			if(name.Length > Settings.MaxFieldLength || secret?.Length > Settings.MaxFieldLength)
				return new HttpResult {StatusCode = 400, Message = "Too Long"};

			if(context.Request.ContentLength == null)
				return new HttpResult {StatusCode = 411, Message = "Substance With Unknown Size"};

			if(context.Request.ContentLength > Settings.MaxMatterSize)
				return new HttpResult {StatusCode = 413, Message = "Substance Too Large"};

			if(context.RequestAborted.IsCancellationRequested)
				return HttpResult.Cancelled;

			Bitmap bmp;
			using(var pooled = await InputBuffer.AcquireAsync().ConfigureAwait(false))
			{
				var length = await context.Request.Body.ReadAllAsync(pooled.Item, context.RequestAborted).WithTimeout(Settings.ReadWriteTimeout).ConfigureAwait(false);

				if(length == default(int))
				{
					context.TryAbort();
					return HttpResult.Cancelled;
				}

				bmp = BitmapHelper.TryFromBuffer(pooled.Item, length);
			}

			if(context.RequestAborted.IsCancellationRequested)
				return HttpResult.Cancelled;

			if(bmp == null)
				return new HttpResult {StatusCode = 400, Message = "Invalid Substance"};

			if(bmp.Width * bmp.Height > Settings.MaxMatterDimensions)
				return new HttpResult {StatusCode = 413, Message = "Substance Too Large"};

			var info = new Transmission {Name = name, Entropy = secret, Timestamp = DateTime.UtcNow.ToTimestamp()};
			if(!await TransmissionsDb.TryAdd(info))
				return new HttpResult {StatusCode = 409, Message = "Substance Conflict"};

			info = Serializer.DeepClone(info); //NOTE: remove secrets from broadcast
			info.Entropy = null;

			await WsHandler.BroadcastAsync(info, CancellationToken.None);

			context.Response.ContentType = "application/protobuf";

			using(var dbmp = new DirectBitmap(bmp))
				return await ProcessRequestInternal(context, name, dbmp).ConfigureAwait(false);
		}

		private static async Task<HttpResult> ProcessRequestInternal(HttpContext context, string name, DirectBitmap dbmp)
		{
			using(var hmac = new HMACSHA256(Settings.Key))
			using(var pooled = await OutputBuffer.AcquireAsync())
			{
				var (hist, buffer) = pooled.Item;
				hist.CalcSpectrum(dbmp);

				var length = ProtoBufHelper.Serialize(buffer, hist);

				var hash = hmac.ComputeHash(Convert.FromBase64String(name));
				context.Response.Headers["X-SG1-Key"] = Convert.ToBase64String(hash);
				context.Response.ContentLength = length;

				if(!await context.Response.Body.WriteAsync(buffer, 0, length, context.RequestAborted).Wrap().WithTimeout(Settings.ReadWriteTimeout).ConfigureAwait(false))
				{
					context.TryAbort();
					return HttpResult.Cancelled;
				}
			}

			return HttpResult.OK;
		}

		private static void CalcSpectrum(this Spectrum spectrum, DirectBitmap bmp)
		{
			for(int y = 0; y < bmp.Height; y++)
			for(int x = 0; x < bmp.Width; x++)
				spectrum.Update(bmp.FastGetPixel(x, y));
		}

		private static readonly ReusableObjectPool<byte[]> InputBuffer = new ReusableObjectPool<byte[]>(() => new byte[Settings.MaxMatterSize], buffer => Array.Clear(buffer, 0, buffer.Length), 64);
		private static readonly ReusableObjectPool<(Spectrum spectrum, byte[] buffer)> OutputBuffer = new ReusableObjectPool<(Spectrum spectrum, byte[] buffer)>(() => (new Spectrum(), new byte[Settings.MaxSpectrumSize]), item => item.spectrum.Zero(), 64);
	}
}