// Legacy gallery routes now share the MaePace site shell. Media still supports byte ranges.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/$/, '') || '/';
    const english = path === '/en' || path.startsWith('/en/');
    const route = english ? (path.slice(3) || '/') : path;
    const redirects = {'/':'/works', '/works/lanclo-lp':'/works/lanclo-lp', '/films/lanclo-daily':'/works/lanclo-film', '/slides/lanclo-making':'/works/lanclo-lp#making'};
    if (redirects[route] && ['GET','HEAD'].includes(request.method)) {
      const target = new URL(redirects[route], 'https://maepace.com');
      target.searchParams.set('lang', english ? 'en' : 'ja');
      return Response.redirect(target.href, 302);
    }
    const headers = new Headers(request.headers);
    const range = headers.get('range');
    headers.delete('range');
    const response = await env.ASSETS.fetch(new Request(request, { headers }));
    if (response.status !== 200 || !['GET', 'HEAD'].includes(request.method)) return response;
    const outputHeaders = new Headers(response.headers);
    outputHeaders.set('Accept-Ranges', 'bytes');
    const ifRange = request.headers.get('if-range');
    const matches = !ifRange || ifRange === response.headers.get('etag') || ifRange === response.headers.get('last-modified');
    const match = range?.match(/^bytes=(\d*)-(\d*)$/);
    if (request.method !== 'GET' || !match || !matches) {
      return new Response(response.body, { status: 200, headers: outputHeaders });
    }
    // Asset bindings may omit Content-Length until the response reaches the edge.
    const bytes = await response.arrayBuffer();
    const length = bytes.byteLength;
    const start = match[1] ? Number(match[1]) : Math.max(0, length - Number(match[2]));
    const end = match[1] && match[2] ? Math.min(length - 1, Number(match[2])) : length - 1;
    if ((!match[1] && !match[2]) || !Number.isSafeInteger(start) || !Number.isSafeInteger(end) || start > end || start >= length) {
      outputHeaders.set('Content-Range', `bytes */${length}`);
      outputHeaders.set('Content-Length', '0');
      return new Response(null, { status: 416, headers: outputHeaders });
    }
    // Current films are ~12 MB; Workers assets cap individual files at 25 MiB.
    outputHeaders.set('Content-Range', `bytes ${start}-${end}/${length}`);
    outputHeaders.set('Content-Length', String(end - start + 1));
    return new Response(bytes.slice(start, end + 1), { status: 206, headers: outputHeaders });
  },
};
