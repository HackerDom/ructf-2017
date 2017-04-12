using System.Threading;
using System.Threading.Tasks;

namespace stargåte.utils
{
	internal static class TaskUtils
	{
		public static Task<bool> Wrap(this Task task)
		{
			return task.ContinueWith(t => t.IsCompleted);
		}

		public static Task<T> WithTimeout<T>(this Task<T> task, int timeout)
		{
			if(task.IsCompleted || timeout == Timeout.Infinite)
				return task;

			var source = new TaskCompletionSource<T>();

			if(timeout == 0)
			{
				source.SetResult(default(T));
				return source.Task;
			}

			var timer = new Timer(state => ((TaskCompletionSource<T>)state).TrySetResult(default(T)), source, timeout, Timeout.Infinite);

			task.ContinueWith(t =>
			{
				timer.Dispose();
				switch(task.Status)
				{
					case TaskStatus.Faulted:
						source.TrySetException(task.Exception);
						break;
					case TaskStatus.Canceled:
						source.TrySetCanceled();
						break;
					case TaskStatus.RanToCompletion:
						source.TrySetResult(task.Result);
						break;
				}
			}, TaskContinuationOptions.ExecuteSynchronously);

			return source.Task;
		}
	}
}