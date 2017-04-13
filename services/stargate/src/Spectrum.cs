using System;
using System.Drawing;
using System.Runtime.CompilerServices;
using ProtoBuf;
using stargåte.utils;

namespace stargåte
{
	[ProtoContract]
	public class Spectrum
	{
		public Spectrum() => Components = new[] {R, G, B, A, H, S, L};

		[MethodImpl(MethodImplOptions.AggressiveInlining)]
		public void Update(Color color)
		{
			R[color.R]++;
			G[color.G]++;
			B[color.B]++;
			A[color.A]++;
			var (h, s, l) = color.ToHSL();
			H[h]++;
			S[s]++;
			L[l]++;
		}

		public void Zero()
		{
			for(int i = 0; i < Components.Length; i++)
			{
				var comp = Components[i];
				Array.Clear(comp, 0, comp.Length);
			}
		}

		public void Write()
		{
			for(int i = 0; i < LEN; i++)
			{
				if(R[i] + G[i] + B[i] + A[i] > 0)
					Console.WriteLine($"{i:X2} - {R[i]};{G[i]};{B[i]};{A[i]}");
			}
		}

		[ProtoMember(1, IsPacked = true)] public readonly int[] R = new int[LEN];
		[ProtoMember(2, IsPacked = true)] public readonly int[] G = new int[LEN];
		[ProtoMember(3, IsPacked = true)] public readonly int[] B = new int[LEN];
		[ProtoMember(4, IsPacked = true)] public readonly int[] A = new int[LEN];
		[ProtoMember(5, IsPacked = true)] public readonly int[] H = new int[LEN];
		[ProtoMember(6, IsPacked = true)] public readonly int[] S = new int[LEN];
		[ProtoMember(7, IsPacked = true)] public readonly int[] L = new int[LEN];

		private readonly int[][] Components;

		private const int LEN = byte.MaxValue + 1;
	}
}