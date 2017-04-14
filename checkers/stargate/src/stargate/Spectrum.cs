using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Runtime.CompilerServices;
using ProtoBuf;

namespace checker.stargate
{
	[ProtoContract]
	public class Spectrum
	{
		public bool ComponentEquals(Spectrum other)
		{
			return R.SequenceEqual(other.R) && G.SequenceEqual(other.G) && B.SequenceEqual(other.B) && A.SequenceEqual(other.A) && H.SequenceEqual(other.H) && S.SequenceEqual(other.S) && L.SequenceEqual(other.L);
		}

		public static Spectrum Create()
		{
			return new Spectrum
			{
				R = new int[LEN],
				G = new int[LEN],
				B = new int[LEN],
				A = new int[LEN],
				H = new int[LEN],
				S = new int[LEN],
				L = new int[LEN]
			};
		}

		[MethodImpl(MethodImplOptions.AggressiveInlining)]
		public void Update(Color color)
		{
			R[color.R]++;
			G[color.G]++;
			B[color.B]++;
			A[color.A]++;
			var hsl = color.ToHSL();
			H[hsl.H]++;
			S[hsl.S]++;
			L[hsl.L]++;
		}

		public void Zero()
		{
			for(int i = 0; i < Components.Length; i++)
			{
				var comp = Components[i];
				Array.Clear(comp, 0, comp.Length);
			}
		}

		public string ToText()
		{
			return string.Join("", NonZeroStrings());
		}

		private IEnumerable<string> NonZeroStrings()
		{
			for(int i = 0; i < LEN; i++)
			{
				if(R[i] + G[i] + B[i] + A[i] > 0)
					yield return $"[{i:X2}|{R[i]};{G[i]};{B[i]};{A[i]}]";
			}
		}

		[ProtoMember(1, IsPacked = true)] public int[] R;
		[ProtoMember(2, IsPacked = true)] public int[] G;
		[ProtoMember(3, IsPacked = true)] public int[] B;
		[ProtoMember(4, IsPacked = true)] public int[] A;
		[ProtoMember(5, IsPacked = true)] public int[] H;
		[ProtoMember(6, IsPacked = true)] public int[] S;
		[ProtoMember(7, IsPacked = true)] public int[] L;

		private int[][] Components => new[] {R, G, B, A, H, S, L};

		private const int LEN = byte.MaxValue + 1;
	}
}