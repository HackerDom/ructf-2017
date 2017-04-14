using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;
using Microsoft.Extensions.DependencyInjection;
using stargåte.handlers;

namespace stargåte
{
	internal class Startup : IStartup
	{
		IServiceProvider IStartup.ConfigureServices(IServiceCollection services)
		{
			return services.AddRouting().BuildServiceProvider();
		}

		public void Configure(IApplicationBuilder app)
		{
			app
				.UseWebSockets(new WebSocketOptions {KeepAliveInterval = Settings.WsPingInterval})
				.Use((ctx, next) => ctx.WebSockets.IsWebSocketRequest ? WsHandler.TryProcessWebSocketRequest(ctx) : next())
				.UseDefaultFiles(new DefaultFilesOptions {DefaultFileNames = new List<string>(1) {"index.html"}})
				.UseStaticFiles(new StaticFileOptions {OnPrepareResponse = ctx => ctx.Context.Response.Headers.Append("Cache-Control", "public, max-age=600")})
				.UseRouter(
					new RouteBuilder(app)
						.MapPut("put", ctx => ProcessRequest(ctx, IncomingCallHandler.ProcessRequest))
						.MapGet("get", ctx => ProcessRequest(ctx, TransmissionInfoHandler.ProcessRequest))
						.Build())
				.Run(ctx =>
				{
					ctx.Response.StatusCode = 404;
					return ctx.Response.WriteAsync("File Not Found");
				});
		}

		private async Task ProcessRequest(HttpContext context, Func<HttpContext, Task<HttpResult>> handler)
		{
			var result = await TryProcessRequest(context, handler).ConfigureAwait(false);
			if(result.Equals(HttpResult.OK) || result.Equals(HttpResult.Cancelled) || context.RequestAborted.IsCancellationRequested)
				return;
			if(context.Response.HasStarted)
				context.TryAbort();
			else
			{
				try
				{
					context.Response.Clear();
					context.Response.StatusCode = result.StatusCode;
					if(result.Message != null)
						await context.Response.WriteAsync(result.Message).ConfigureAwait(false);
				} catch { /* ignored */ }
			}
		}

		private async Task<HttpResult> TryProcessRequest(HttpContext context, Func<HttpContext, Task<HttpResult>> handler)
		{
			try { return await handler(context).ConfigureAwait(false); } catch { return HttpResult.ServerError; }
		}
	}

	public struct HttpResult
	{
		public int StatusCode;
		public string Message;

		public static HttpResult OK = new HttpResult {StatusCode = 200};
		public static HttpResult Cancelled = new HttpResult {StatusCode = 499};
		public static HttpResult ServerError = new HttpResult {StatusCode = 500, Message = "Internal Stargåte Error"};
	}
}