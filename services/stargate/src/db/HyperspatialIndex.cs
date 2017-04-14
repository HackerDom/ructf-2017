using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Threading;

namespace stargåte.db
{
	class HyperspatialIndex<TKey, TValue>
	{
		public HyperspatialIndex(TimeSpan ttl, IEqualityComparer<TKey> comparer = null)
		{
			this.ttl = ttl;
			queue = new ConcurrentQueue<(TKey, DateTime)>();
			dict = new ConcurrentDictionary<TKey, TValue>(comparer ?? EqualityComparer<TKey>.Default);
			if(ttl != TimeSpan.MaxValue) timer = new Timer(RemoveExpired, null, ttl, TimeSpan.FromSeconds(Math.Max(1L, (long)ttl.TotalSeconds >> 3)));
		}

		[MethodImpl(MethodImplOptions.AggressiveInlining)]
		public TValue GetOrDefault(TKey key) => dict.TryGetValue(key, out var item) ? item : default(TValue);

		[MethodImpl(MethodImplOptions.AggressiveInlining)]
		public bool TryAdd(TKey key, TValue value) => TryAdd(key, value, DateTime.UtcNow);

		public bool TryAdd(TKey key, TValue value, DateTime time)
		{
			if(!dict.TryAdd(key, value))
				return false;
			queue.Enqueue((key, time));
			return true;
		}

		private void RemoveExpired(object state)
		{
			var expire = GetExpireTime();
			while(queue.TryPeek(out (TKey key, DateTime added) item) && item.added < expire)
			{
				queue.TryDequeue(out item);
				dict.TryRemove(item.key, out _);
			}
		}

		[MethodImpl(MethodImplOptions.AggressiveInlining)]
		private DateTime GetExpireTime() => DateTime.UtcNow.Add(-ttl);

		private readonly ConcurrentQueue<(TKey, DateTime)> queue;
		private readonly ConcurrentDictionary<TKey, TValue> dict;
		private readonly TimeSpan ttl;
		private readonly Timer timer;
	}
}