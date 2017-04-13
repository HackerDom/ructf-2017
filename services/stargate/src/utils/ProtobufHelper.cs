using System;
using System.IO;
using ProtoBuf;

namespace stargåte.utils
{
	static class ProtoBufHelper
	{
		public static int Serialize<T>(byte[] buffer, T item)
		{
			using(var ms = new MemoryStream(buffer, 0, buffer.Length, true, true))
			{
				Serializer.Serialize(ms, item);
				return (int)ms.Position;
			}
		}

		public static ArraySegment<byte> SerializeAsArraySegment<T>(byte[] buffer, T item) => new ArraySegment<byte>(buffer, 0, Serialize(buffer, item));
	}
}