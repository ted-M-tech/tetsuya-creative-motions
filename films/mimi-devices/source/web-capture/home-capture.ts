// Film capture (mimi-devices): the real Web Home with the daily-home fixture (GET-only, every /api mocked by the fixture).
import {chromium} from '@playwright/test';
const base=process.env.BASE||'http://127.0.0.1:21990', out=process.env.OUT!, state=(process.env.STATE||'habits') as any;
const sizes:[string,number,number][]=JSON.parse(process.env.SIZES||'[["laptop",1440,900]]');
const fixtureNow=Date.UTC(2026,9,21,3); // 2026-10-21 12:00 JST
const browser=await chromium.launch();
for(const [name,width,height] of sizes){
 const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:2,reducedMotion:'reduce',locale:'ja',timezoneId:'Asia/Tokyo'});
 page.on('pageerror',e=>console.error('pageerror',e.message));
 await page.clock.setFixedTime(fixtureNow);
 await page.route('**/*',route=>new URL(route.request().url()).origin===base?route.continue():route.abort());
 await page.route('**/api/**',route=>route.abort());
 await page.route('**/src/account/client.ts*',route=>route.fulfill({contentType:'text/javascript',body:'export function getAccountClient(){return null}'}));
 await page.goto(base+'/dev/onboarding');
 await page.evaluate(async args=>{const path='/tests/daily-home-fixture.tsx';const fixture=await import(path);fixture.mount(args)},{ui:'ja',state,now:fixtureNow});
 await page.waitForTimeout(2500);
 await page.screenshot({path:`${out}/${name}-${state}.png`});
 await page.screenshot({path:`${out}/${name}-${state}-full.png`,fullPage:true});
 await page.close();
}
await browser.close();
