using System;
using System.Security.Cryptography;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using stargåte.db;
using stargåte.utils;

namespace stargåte.handlers
{
	static class TransmissionInfoHandler
	{
		public static async Task<HttpResult> ProcessRequest(HttpContext context)
		{
			var name = context.Request.Headers["X-SG1-Name"];
			if(string.IsNullOrEmpty(name))
				return new HttpResult {StatusCode = 404, Message = "Substance Not Found"};

			var key = context.Request.Headers["X-SG1-Key"];
			if(string.IsNullOrEmpty(key))
				return new HttpResult {StatusCode = 403, Message = "Access Denied"};

			using(var hmac = new HMACSHA256(Settings.Key))
			if(!hmac.ComputeHash(Convert.FromBase64String(name)).FastTimingSecureEquals(Convert.FromBase64String(key)))
				return new HttpResult {StatusCode = 403, Message = "Access Denied"};

			Transmission info;
			if((info = TransmissionsDb.Find(name)) == null)
				return new HttpResult {StatusCode = 404, Message = "Substance Not Found"};

			context.Response.ContentType = "application/protobuf";

			using(var pooled = await ResponsePool.AcquireAsync().ConfigureAwait(false))
			{
				var buffer = pooled.Item;
				var length = ProtoBufHelper.Serialize(buffer, info);

				context.Response.ContentLength = length;
				if(!await context.Response.Body.WriteAsync(buffer, 0, length, context.RequestAborted).Wrap().WithTimeout(Settings.ReadWriteTimeout).ConfigureAwait(false))
				{
					context.TryAbort();
					return HttpResult.Cancelled;
				}
			}

			return HttpResult.OK;
		}

		private static readonly ReusableObjectPool<byte[]> ResponsePool = new ReusableObjectPool<byte[]>(() => new byte[Settings.MaxTransmissionInfoSize], buffer => Array.Clear(buffer, 0, buffer.Length), 64);
	}
}