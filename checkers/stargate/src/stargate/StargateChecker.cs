using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using checker.net;
using checker.rnd;

namespace checker.stargate
{
	internal class StargateChecker : IChecker
	{
		public async Task<string> Info()
		{
			var vulns = "vulns: 1:2";
			await Console.Out.WriteLineAsync(vulns).ConfigureAwait(false);

			return vulns;
		}

		public async Task Check(string host)
		{
			var httpClient = new AsyncHttpClient(GetBaseHttpUri(host));

			var result = await httpClient.DoRequestAsync(WebRequestMethods.Http.Get, "/", null, null, NetworkOpTimeout, MaxHttpBodySize).ConfigureAwait(false);
			if(result.StatusCode != HttpStatusCode.OK)
				throw new CheckerException(result.StatusCode.ToExitCode(), "get / failed");
		}

		public async Task<string> Put(string host, string id, string flag, int vuln)
		{
			var len = vuln == 1 ? RndUtil.Choice(11, 14) : RndUtil.Choice(12, 15);
			var name = RndText.RandomWord(len);

			var b64Name = Convert.ToBase64String(Encoding.ASCII.GetBytes(name));
			var b64Entropy = Convert.ToBase64String(Encoding.ASCII.GetBytes(flag));

			await Console.Error.WriteLineAsync($"name '{name}', b64name '{b64Name}', entropy '{b64Entropy}'").ConfigureAwait(false);

			using(var bmp = RndBitmap.RndBmp(RndUtil.ThreadStaticRnd.Next(32) + 96, RndUtil.ThreadStaticRnd.Next(32) + 96))
			using(var wsClient = await AsyncWebSocketClient.TryConnectAsync(GetBaseWsUri(host), MaxWsMsgSize, NetworkOpTimeout).ConfigureAwait(false))
			{
				if(wsClient == null)
					throw new CheckerException(ExitCode.DOWN, "ws connect failed");

				await Console.Error.WriteLineAsync("ws connected").ConfigureAwait(false);

				if(await wsClient.TryWaitMessageAsync(buffer => Tuple.Create(buffer.Count == 2 && buffer.Array[0] == (byte)'h' && buffer.Array[1] == (byte)'i', buffer), NetworkOpTimeout).ConfigureAwait(false) == default(ArraySegment<byte>))
					throw new CheckerException(ExitCode.MUMBLE, "await hello failed");

				await Console.Error.WriteLineAsync("ws hello received").ConfigureAwait(false);

				// ReSharper disable once AccessToDisposedClosure
				var wsTask = Task.Run(() => wsClient.TryWaitMessageAsync(buffer =>
				{
					if(!ProtoBufHelper.TryDeserialize<Transmission>(buffer, out var transmission))
						throw new CheckerException(ExitCode.MUMBLE, "invalid ws data");
					return Tuple.Create(transmission.Name == b64Name, transmission);
				}, NetworkOpTimeout));

				await RndUtil.RndDelay(MaxDelay).ConfigureAwait(false);

				var httpClient = new AsyncHttpClient(GetBaseHttpUri(host));

				var result = await httpClient.DoRequestAsync(WebRequestMethods.Http.Put, PutRelative, new WebHeaderCollection {{"X-SG1-Name", b64Name}, {"X-SG1-Entropy", b64Entropy}}, bmp.ToByteArray(), NetworkOpTimeout, MaxHttpBodySize).ConfigureAwait(false);
				if(result.StatusCode != HttpStatusCode.OK)
					throw new CheckerException(result.StatusCode.ToExitCode(), $"put {PutRelative} failed");

				var key = result.Headers?["X-SG1-Key"];
				if(string.IsNullOrEmpty(key))
					throw new CheckerException(ExitCode.MUMBLE, $"put {PutRelative} failed, no key");

				if(!ProtoBufHelper.TryDeserialize(result.Body, out Spectrum spectrum))
					throw new CheckerException(ExitCode.MUMBLE, $"invalid {PutRelative} response");

				var expectedSpectrum = bmp.CalcSpectrum();

				if(!spectrum.ComponentEquals(expectedSpectrum))
					throw new CheckerException(ExitCode.MUMBLE, $"invalid {PutRelative} response");

				await RndUtil.RndDelay(MaxDelay).ConfigureAwait(false);

				var msg = await wsTask.ConfigureAwait(false);
				if(msg == null || msg.Name != b64Name)
					throw new CheckerException(ExitCode.MUMBLE, "await msg failed");

				var flagid = $"{b64Name}:{key}";
				await Console.Out.WriteLineAsync(flagid).ConfigureAwait(false);

				return flagid;
			}
		}

		public async Task Get(string host, string id, string flag, int vuln)
		{
			var httpClient = new AsyncHttpClient(GetBaseHttpUri(host));

			var parts = id.Split(new[] {':'}, 2);

			var b64Name = parts[0];
			var key = parts[1];

			var result = await httpClient.DoRequestAsync(WebRequestMethods.Http.Get, GetRelative, new WebHeaderCollection {{"X-SG1-Name", b64Name}, {"X-SG1-Key", key}}, null, NetworkOpTimeout, MaxHttpBodySize).ConfigureAwait(false);
			if(result.StatusCode != HttpStatusCode.OK)
				throw new CheckerException(result.StatusCode.ToExitCode(), $"get {GetRelative} failed");

			if(!ProtoBufHelper.TryDeserialize(result.Body, out Transmission transmission))
				throw new CheckerException(ExitCode.MUMBLE, $"invalid {GetRelative} response");

			if(transmission.Name != b64Name)
				throw new CheckerException(ExitCode.MUMBLE, $"invalid {GetRelative} response");

			if(ConvertHelper.TryFromBase64String(transmission.Entropy) != flag)
				throw new CheckerException(ExitCode.CORRUPT, "no entropy found");
		}

		private const int WsPort = 5001;
		private const int HttpPort = 5000;

		private static Uri GetBaseWsUri(string host) => new Uri($"ws://{host}:{WsPort}/");
		private static Uri GetBaseHttpUri(string host) => new Uri($"http://{host}:{HttpPort}/");

		private const string GetRelative = "/find/";
		private const string PutRelative = "/send/";

		private const int MaxWsMsgSize = 65536;
		private const int MaxHttpBodySize = 512 * 1024;

		private const int NetworkOpTimeout = 5000;

		private const int MaxDelay = 500;
	}
}