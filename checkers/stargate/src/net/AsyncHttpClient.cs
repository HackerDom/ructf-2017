using System;
using System.Collections.Specialized;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Threading.Tasks;

namespace checker.net
{
	internal class AsyncHttpClient
	{
		public AsyncHttpClient(Uri baseUri, bool shareCookies = false)
		{
			this.baseUri = baseUri;
			cookies = shareCookies ? new CookieContainer(10, 10, 32768) : null;
		}

		public async Task<HttpResult> DoRequestAsync(string method, string relative, NameValueCollection headers = null, byte[] data = null, int timeout = 10000, int maxBodySize = 1024 * 1024, bool keepAlive = true)
		{
			HttpResult result;
			var stopwatch = new Stopwatch();
			try
			{
				var request = CreateWebRequest(method, relative, keepAlive, headers);

				await Console.Error.WriteLineAsync($"{method.ToLowerInvariant()} {relative}, send {data?.Length ?? 0} bytes").ConfigureAwait(false);

				stopwatch.Start();
				var task = DoRequestAsync(request, data, maxBodySize);
				if(ReferenceEquals(task, await Task.WhenAny(task, Task.Delay(timeout)).ConfigureAwait(false)))
					result = task.Result;
				else
				{
					try { request.Abort(); } catch { }
					result = HttpResult.Timeout;
				}
			}
			catch(Exception e)
			{
				result = HttpResult.Unknown;
				result.Exception = e;
			}

			stopwatch.Stop();
			result.Elapsed = stopwatch.Elapsed;

			await Console.Error.WriteLineAsync($"http {(int)result.StatusCode} {result.StatusDescription ?? "Unknown"}, recv {result.Body?.Length ?? 0} bytes, {stopwatch.ElapsedMilliseconds} ms").ConfigureAwait(false);

			return result;
		}

		private async Task<HttpResult> DoRequestAsync(HttpWebRequest request, byte[] data, int maxBodySize)
		{
			if(data == null)
				request.ContentLength = 0L;
			else
			{
				request.ContentLength = data.Length;
				if(data.Length > 0)
				{
					using(var stream = await request.GetRequestStreamAsync().ConfigureAwait(false))
						await stream.WriteAsync(data, 0, data.Length).ConfigureAwait(false);
				}
			}

			using(var response = await TryGetResponseAsync(request).ConfigureAwait(false) as HttpWebResponse)
			{
				if(response == null)
					return HttpResult.Unknown;

				var result = new HttpResult {StatusCode = response.StatusCode, StatusDescription = response.StatusDescription, Headers = response.Headers};
				var stream = response.GetResponseStream();

				var ms = new MemoryStream(new byte[maxBodySize], 0, maxBodySize, true, true);
				ms.SetLength(0);

				if(stream != null)
					await stream.CopyToAsync(ms).ConfigureAwait(false);

				ms.Seek(0, SeekOrigin.Begin);
				result.Body = ms;

				return result;
			}
		}

		private static async Task<WebResponse> TryGetResponseAsync(WebRequest request)
		{
			try
			{
				return await request.GetResponseAsync().ConfigureAwait(false);
			}
			catch(WebException we) when (we.Status == WebExceptionStatus.ProtocolError)
			{
				return we.Response;
			}
		}

		private HttpWebRequest CreateWebRequest(string method, string relative, bool keepAlive, NameValueCollection headers = null)
		{
			var request = WebRequest.CreateHttp(new Uri(baseUri, relative));
			request.Method = method;
			request.Proxy = null;
			request.ServicePoint.UseNagleAlgorithm = false;
			request.ServicePoint.ConnectionLimit = 1024;
			request.AllowReadStreamBuffering = false;
			request.AllowWriteStreamBuffering = false;
			request.KeepAlive = keepAlive;
			request.ServicePoint.Expect100Continue = false;
			if(cookies != null)
				request.CookieContainer = cookies;
			if(headers != null && headers.Count > 0)
				request.Headers.Add(headers);
			return request;
		}

		private readonly Uri baseUri;
		private readonly CookieContainer cookies;
	}

	internal struct HttpResult
	{
		public HttpStatusCode StatusCode;
		public string StatusDescription;
		public WebHeaderCollection Headers;

		public MemoryStream Body;
		public TimeSpan Elapsed;

		public Exception Exception;

		public static readonly HttpResult Timeout = new HttpResult {StatusCode = (HttpStatusCode)499};
		public static readonly HttpResult Unknown = new HttpResult();
	}
}