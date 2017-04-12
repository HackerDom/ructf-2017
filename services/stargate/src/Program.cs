using System;
using System.IO;
using Microsoft.AspNetCore.Hosting;
using stargåte.db;

namespace stargåte
{
	static class Program
	{
		static void Main(string[] args)
		{
			var dir = Directory.GetCurrentDirectory();
			new WebHostBuilder()
				.UseKestrel(options =>
				{
					options.ThreadCount = Environment.ProcessorCount;
					options.AddServerHeader = false;
					//options.NoDelay = true;
					options.Limits.KeepAliveTimeout = TimeSpan.FromSeconds(5);
					options.Limits.MaxRequestLineSize = 512;
					options.Limits.MaxRequestHeaderCount = 32;
					options.Limits.MaxRequestHeadersTotalSize = 8192;
					options.Limits.RequestHeadersTimeout = TimeSpan.FromSeconds(3);
					options.ShutdownTimeout = TimeSpan.FromSeconds(1);
				})
				.UseUrls("http://*:5000/")
				.UseStartup<Startup>()
				.UseContentRoot(dir)
				.UseWebRoot(Path.Combine(dir, "static"))
				.Build()
				.Run();

			TransmissionsDb.Close();
		}
	}
}