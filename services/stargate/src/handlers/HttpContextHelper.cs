using Microsoft.AspNetCore.Http;

namespace stargåte.handlers
{
	static class HttpContextHelper
	{
		public static void TryAbort(this HttpContext context)
		{
			try { context.Abort(); } catch { /* ignored */ }
		}
	}
}