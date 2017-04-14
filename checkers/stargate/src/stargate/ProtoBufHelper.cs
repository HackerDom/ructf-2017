using System;
using System.IO;
using ProtoBuf;

namespace checker.stargate
{
	internal static class ProtoBufHelper
	{
		public static bool TryDeserialize<T>(Stream stream, out T item)
		{
			try
			{
				item = Serializer.Deserialize<T>(stream);
				return true;
			}
			catch
			{
				item = default(T);
				return false;
			}
		}

		public static T Deserialize<T>(ArraySegment<byte> segment)
		{
			using(var ms = new MemoryStream(segment.Array, segment.Offset, segment.Count))
				return Serializer.Deserialize<T>(ms);
		}

		public static bool TryDeserialize<T>(ArraySegment<byte> segment, out T item)
		{
			using(var ms = new MemoryStream(segment.Array, segment.Offset, segment.Count))
				return TryDeserialize(ms, out item);
		}
	}
}