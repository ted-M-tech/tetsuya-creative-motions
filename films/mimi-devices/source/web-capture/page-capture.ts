// Film capture (mimi-devices): guest Web pages with every /api mocked (as web-parity-shell-browser.ts), GET-only.
import {chromium} from '@playwright/test';
const base=process.env.BASE||'http://127.0.0.1:21990', out=process.env.OUT!;
const shots:[string,string,number,number][]=JSON.parse(process.env.SHOTS!);
const browser=await chromium.launch();
for(const [name,path,width,height] of shots){
 const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:2,reducedMotion:'reduce',locale:'ja',timezoneId:'Asia/Tokyo'});
 page.on('pageerror',e=>console.error('pageerror',e.message));
 await page.clock.setFixedTime(Date.UTC(2026,9,21,3));
 await page.addInitScript(()=>{localStorage.setItem('koe-simple-ui','ja');localStorage.setItem('koe-simple-language','en');localStorage.setItem('voicetwin-onboarding','done')});
 await page.route('**/*',route=>new URL(route.request().url()).origin===base?route.continue():route.abort());
 await page.route('**/api/**',route=>{const p=new URL(route.request().url()).pathname;return route.fulfill({json:p==='/api/voice'?{enrolled:true,session:true}:{stories:[]}})});
 await page.goto(base+path);
 await page.waitForTimeout(3000);
 await page.screenshot({path:`${out}/${name}.png`});
 await page.close();
}
await browser.close();
