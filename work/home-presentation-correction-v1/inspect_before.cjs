const {chromium}=require('C:/Users/DELL/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs');const path=require('node:path');
const OUT=__dirname;const ids=['echoes-of-the-past','the-cursed-quest','the-book-of-shadows','fastest-finger-first','words-of-the-feast','the-phantom-order','door-to-darkness','build-the-haunted-banquet','hotel-transylvania'];
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1920,height:1080},reducedMotion:'reduce'});
 await page.goto('http://127.0.0.1:4173/');await page.locator('.protected-title').waitFor();
 await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))));
 const metrics=await page.evaluate(()=>({height:innerHeight,width:innerWidth,documentHeight:document.documentElement.scrollHeight,documentWidth:document.documentElement.scrollWidth,scrollY,title:document.querySelector('.protected-title').getBoundingClientRect().toJSON()}));
 await page.screenshot({path:path.join(OUT,'before-home-projector.png')});
 await page.locator('.activities-control').click();
 const menuOpened=await page.evaluate(()=>({hash:location.hash,scrollY,expanded:document.querySelector('.activities-control').getAttribute('aria-expanded'),drawerVisible:!document.querySelector('.activity-drawer').hidden}));
 await page.mouse.move(700,600);await page.mouse.wheel(0,500);await page.waitForTimeout(200);
 const backgroundWheel=await page.evaluate(()=>({hash:location.hash,scrollY}));
 await page.keyboard.press('Escape');
 const menuClosed=await page.evaluate(()=>({hash:location.hash,scrollY}));
 const rails=[];
 for(const width of [1920,1366]){
  await page.setViewportSize({width,height:width===1920?1080:768});
  for(const id of ids){
   await page.goto('http://127.0.0.1:4173/#/activities/'+id);await page.locator('h1').waitFor();
   await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))));
   await page.mouse.move(width-50,500);
   await page.locator('.activity-drawer').screenshot({path:path.join(OUT,`before-rail-${width}-${id}.png`)});
   rails.push({width,id,...await page.locator('.activity-drawer').evaluate(e=>({box:e.getBoundingClientRect().toJSON(),listScroll:e.querySelector('.destination-list').scrollTop,selected:e.querySelector('[aria-current="page"]').dataset.destination}))});
  }
 }
 const result={metrics,menuOpened,backgroundWheel,menuClosed,rails};
 fs.writeFileSync(path.join(OUT,'before-browser-measurements.json'),JSON.stringify(result,null,2));
 console.log(JSON.stringify({metrics,menuOpened,backgroundWheel,menuClosed,railsRecorded:rails.length},null,2));await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
