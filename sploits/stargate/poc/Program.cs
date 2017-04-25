using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Threading;
using System.Threading.Tasks;
using ProtoBuf;

namespace starbrute
{
	static partial class Program
	{
		private const int ff = 138; // Spectrums taken for 24bpp BMP with 138 white pixels

		// Known HMAC value from some uploaded image
		private static readonly byte[] Sample = Convert.FromBase64String("ODAw");
		private static readonly byte[] Hash = Convert.FromBase64String("61XLCKqsTi/0yi1gSCCEZDKkgoo+9olIhiZzorugVo4=");

		static void Main()
		{
			var (vH, vS, vL) = Color.FromArgb(0xff, 0xff, 0xff, 0xff).ToHSL();

			var result = GetAvgSpectrum(
				Directory.EnumerateFiles("spectrums"),
				spectrum =>
				{
					spectrum.A[0xff] -= ff;
					spectrum.R[0xff] -= ff;
					spectrum.G[0xff] -= ff;
					spectrum.B[0xff] -= ff;
					spectrum.H[vH] -= ff;
					spectrum.S[vS] -= ff;
					spectrum.L[vL] -= ff;
					return spectrum;
				},
				spectrum => // Some statistics filter
					spectrum.A[0x00] >= 29 && spectrum.A[0x00] <= 34 &&
					spectrum.R[0x00] >= 29 && spectrum.R[0x00] <= 34 &&
					spectrum.G[0x00] >= 29 && spectrum.G[0x00] <= 34 &&
					spectrum.B[0x00] >= 29 && spectrum.B[0x00] <= 34 &&
					spectrum.A[0xff] >= 0 && spectrum.A[0xff] <= 4 &&
					spectrum.R[0xff] >= 0 && spectrum.R[0xff] <= 4 &&
					spectrum.G[0xff] >= 0 && spectrum.G[0xff] <= 4 &&
					spectrum.B[0xff] >= 0 && spectrum.B[0xff] <= 4 &&
					spectrum.A.Skip(1).Take(254).Any(c => c >= 3) &&
					spectrum.R.Skip(1).Take(254).Any(c => c >= 3) &&
					spectrum.G.Skip(1).Take(254).Any(c => c >= 3) &&
					spectrum.B.Skip(1).Take(254).Any(c => c >= 3));

			result.Write();

			var A = new HashSet<byte>(Spectrum.GetNonZeroIndices(result.A));
			var R = new HashSet<byte>(Spectrum.GetNonZeroIndices(result.R));
			var G = new HashSet<byte>(Spectrum.GetNonZeroIndices(result.G));
			var B = new HashSet<byte>(Spectrum.GetNonZeroIndices(result.B));
			var H = new HashSet<byte>(Spectrum.GetNonZeroIndices(result.H));
			var S = new HashSet<byte>(Spectrum.GetNonZeroIndices(result.S));
			var L = new HashSet<byte>(Spectrum.GetNonZeroIndices(result.L));

			var colors = new HashSet<Color>();

			foreach(var a in A)
			foreach(var r in R)
			foreach(var g in G)
			foreach(var b in B)
			{
				var color = Color.FromArgb(a, r, g, b);
				var (h, s, l) = color.ToHSL();
				if(H.Contains(h) && S.Contains(s) && L.Contains(l) && colors.Add(color))
					Console.WriteLine(color);
			}

			var total = colors.Count * colors.Count * colors.Count * colors.Count;

			Console.WriteLine("=====");

			Console.WriteLine("Possible number colors: {0}", colors.Count);
			Console.WriteLine("Total number of checks: {0}", total);
			Console.WriteLine("Brute-force em all...");

			var sw = Stopwatch.StartNew();

			int count = 0;
			Parallel.ForEach(colors, c1 =>
			{
				Parallel.ForEach(colors, c2 =>
				{
					Parallel.ForEach(colors, c3 =>
					{
						Parallel.ForEach(colors, c4 =>
						{
							if(Interlocked.Increment(ref count) % 100000 == 0)
								Console.WriteLine("Done {0} - {1:P2}", count, (double)count / total);

							var key = new[] {c1.B, c1.G, c1.R, c1.A, c2.B, c2.G, c2.R, c2.A, c3.B, c3.G, c3.R, c3.A, c4.B, c4.G, c4.R, c4.A};
							if(IsValidKey(key))
							{
								Console.WriteLine($"Key found: {BitConverter.ToString(key)}, elapsed {sw.Elapsed}");
								Environment.Exit(0);
							}
						});
					});
				});
			});
		}

		private static Spectrum GetAvgSpectrum(IEnumerable<string> files, Func<Spectrum, Spectrum> patch, Func<Spectrum, bool> filter)
		{
			return
				files
					.Select(GetSpectrums)
					.Select(patch)
					.Where(filter)
					.Take(3)
					.Aggregate(Spectrum.Intersect);
		}

		private static Spectrum GetSpectrums(string filepath)
		{
			using(var file = File.OpenRead(filepath))
				return Serializer.Deserialize<Spectrum>(file);
		}

		public static bool IsValidKey(byte[] key)
		{
			using(var md5 = new HMACSHA256(key))
			{
				if(md5.ComputeHash(Sample).ByteEquals(Hash))
					return true;
			}
			return false;
		}
	}

	public static class Utils
	{
		public static bool ByteEquals(this byte[] a1, byte[] a2)
		{
			if(a1.Length != a2.Length)
				return false;
			for(int i = 0; i < a1.Length; i++)
			{
				if(a1[i] != a2[i])
					return false;
			}
			return true;
		}
	}

	static partial class Program
	{
		[ProtoContract]
		public class Spectrum
		{
			public static Spectrum Create() => new Spectrum {A = new int[256], R = new int[256], G = new int[256], B = new int[256], H = new int[256], S = new int[256], L = new int[256]};

			public static Spectrum Intersect(Spectrum hist1, Spectrum hist2)
			{
				var result = Create();
				for(int i = 0; i < 256; i++)
				{
					result.A[i] = Math.Min(hist1.A[i], hist2.A[i]);
					result.R[i] = Math.Min(hist1.R[i], hist2.R[i]);
					result.G[i] = Math.Min(hist1.G[i], hist2.G[i]);
					result.B[i] = Math.Min(hist1.B[i], hist2.B[i]);
					result.H[i] = Math.Min(hist1.H[i], hist2.H[i]);
					result.S[i] = Math.Min(hist1.S[i], hist2.S[i]);
					result.L[i] = Math.Min(hist1.L[i], hist2.L[i]);
				}
				return result;
			}

			public void Write()
			{
				for(int i = 0; i < 256; i++)
				{
					if(A[i] + R[i] + G[i] + B[i] > 0)
						Console.WriteLine($"{i:X2} - {A[i]};{R[i]};{G[i]};{B[i]}");
				}
			}

			public static IEnumerable<byte> GetNonZeroIndices(int[] array)
			{
				for(int i = 0; i < array.Length; i++)
				{
					for(int c = 0; c < array[i]; c++)
						yield return (byte)i;
				}
			}

			[ProtoMember(1, IsPacked = true)] public int[] R;
			[ProtoMember(2, IsPacked = true)] public int[] G;
			[ProtoMember(3, IsPacked = true)] public int[] B;
			[ProtoMember(4, IsPacked = true)] public int[] A;
			[ProtoMember(5, IsPacked = true)] public int[] H;
			[ProtoMember(6, IsPacked = true)] public int[] S;
			[ProtoMember(7, IsPacked = true)] public int[] L;
		}
	}

	static class ColorSpace
	{
		public static (byte H, byte S, byte L) ToHSL(this Color color)
		{
			int r = color.R, g = color.G, b = color.B;

			var max = Math.Max(Math.Max(r, g), b);
			var min = Math.Min(Math.Min(r, g), b);

			var l = (max + min) >> 1;

			int sum = max + min;
			int delta = max - min;

			int s;
			if(delta == 0)
				s = 0;
			else
			{
				if(sum > MAX)
					sum = 510 - sum;
				s = MAX * delta / sum;
			}

			int h = 0;
			if(r == g && g == b)
				h = 0;
			else
			{
				if(r == max)
					h = (g < b ? MAX : 0) + MAXdiv3 * (g - b) / (delta << 1);
				else if(g == max)
					h = MAXdiv3 + (b - r) * MAXdiv3 / (delta << 1);
				else if(b == max)
					h = MAXdiv3mul2 + (r - g) * MAXdiv3 / (delta << 1);
			}

			return ((byte)h, (byte)s, (byte)l);
		}

		private const int MAX = byte.MaxValue;
		private const int MAXdiv3 = MAX / 3;
		private const int MAXdiv3mul2 = MAXdiv3 * 2;
	}
}