interface Environment { DEMO_ASSETS: {fetch(request: Request): Promise<Response>} }
/** Retire only the product demo entrypoints; retain the original asset service. */
export default {
 async fetch(request: Request, env: Environment): Promise<Response> {
  const url=new URL(request.url);
  if(url.hostname==='videos.maepace.com'&&['/demos/lanclo-lp','/demos/lanclo-lp/','/demos/lanclo-lp/index.html'].includes(url.pathname)){
   return new Response(null,{status:301,headers:{Location:'https://lanclo.app/lp/'+url.search}});
  }
  return env.DEMO_ASSETS.fetch(request);
 }
};
