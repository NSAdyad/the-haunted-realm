const { chromium } = require('C:/Users/DELL/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('node:fs');
const path = require('node:path');
const RUN = process.argv[2] || 'run-1';
const OUT = path.join(__dirname,RUN);
fs.mkdirSync(OUT,{recursive:true});
const BASE = 'http://127.0.0.1:4173/';
const names = ['Echoes of the Past','The Cursed Quest','The Book of Shadows','Fastest Finger First','Words of the Feast','The Phantom Order','Door to Darkness','Build the Haunted Banquet','Hotel Transylvania'];
const ids = ['echoes-of-the-past','the-cursed-quest','the-book-of-shadows','fastest-finger-first','words-of-the-feast','the-phantom-order','door-to-darkness','build-the-haunted-banquet','hotel-transylvania'];
const viewports = [
  ['projector',1920,1080], ['desktop',1600,900], ['laptop',1366,768],
  ['tablet',768,1024], ['mobile',390,844], ['mobile-narrow',320,812]
];
const tests = [], metrics = [], errors = [], badRequests = [];
let label = '';
function check(condition,message,detail) { if(!condition)throw new Error(message+' '+JSON.stringify(detail??'')); }
async function test(name,fn) {
  try { const evidence = await fn(); tests.push({viewport:label,test:name,status:'PASS',evidence}); }
  catch(e) { tests.push({viewport:label,test:name,status:'FAIL',actual:String(e)}); console.log('TEST FAILURE',label,name,String(e)); }
  fs.writeFileSync(path.join(OUT,'partial-results.json'),JSON.stringify({tests,metrics,errors,badRequests},null,2));
}
async function images(page) {
  await page.evaluate(()=>Promise.all([...document.images].map(img=>img.decode().catch(()=>{}))));
  return page.evaluate(()=>[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src));
}
async function route(page,id,expected) {
  await page.waitForURL(url=>url.hash==='#/activities/'+id);
  await page.locator('h1').filter({hasText:expected}).waitFor();
  check(await page.locator('h1').innerText()===expected,'Exact page name mismatch');
  check(await page.locator('.destination-link[aria-current="page"]').count()===1,'Current destination count');
  check(await page.locator('.destination-link[aria-current="page"]').getAttribute('data-destination')===id,'Wrong selected activity');
  check(await page.locator('.content-space h2').innerText()==='Activity content area','Shell content label');
  check((await page.locator('.content-space').innerText()).replace(/\s+/g,' ').trim()==='Activity content area Content and interactions will be developed after separate approval.','Unexpected educational content');
}
async function goHome(page,width) {
  await page.locator(width>900?'.rail-home':'.home-control').click();
  await page.waitForURL(url=>url.hash==='#/');
  await page.locator('.protected-title').waitFor();
}
async function openMenu(page,width) {
  if(width<=900 || await page.locator('body').evaluate(e=>e.classList.contains('home-view')))await page.locator('.activities-control').click();
  await page.locator('.activity-drawer').waitFor({state:'visible'});
}
async function swipe(page,x,fromY,toY) {
  const client = await page.context().newCDPSession(page);
  await client.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y:fromY}]});
  for(let step=1;step<=8;step++)await client.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x,y:fromY+(toY-fromY)*step/8}]});
  await client.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
  await client.detach();
  await page.waitForTimeout(150);
}
(async () => {
  const browser = await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  for(const [name,width,height] of viewports) {
    label = name;
    const context = await browser.newContext({viewport:{width,height},hasTouch:width<=900,isMobile:width<=649,reducedMotion:'reduce'});
    const page = await context.newPage();
    page.setDefaultTimeout(7000);
    page.on('pageerror',e=>errors.push({viewport:name,error:String(e)}));
    page.on('console',m=>{if(m.type()==='error')errors.push({viewport:name,error:m.text()})});
    page.on('requestfailed',r=>badRequests.push({viewport:name,url:r.url(),failure:r.failure()}));
    page.on('response',r=>{if(r.status()>=400)badRequests.push({viewport:name,status:r.status(),url:r.url()})});
    await page.goto(BASE);
    await page.locator('.protected-title').waitFor();
    await test('Home, exact nine names, approved images and no emojis',async()=>{
      check(await page.locator('.scene-destination').count()===9,'Card count');
      check(JSON.stringify(await page.locator('.scene-destination').evaluateAll(a=>a.map(e=>e.getAttribute('aria-label'))))===JSON.stringify(names),'Card names');
      check(JSON.stringify(await page.locator('.destination-link span').allTextContents())===JSON.stringify(names),'Navigation names');
      check((await images(page)).length===0,'Broken images',await images(page));
      check(!await page.locator('body').evaluate(e=>/\p{Extended_Pictographic}/u.test(e.textContent)),'Emoji in visible UI');
      const title = await page.locator('.protected-title').boundingBox();
      const intendedWidth = width<650?width-32:650;
      check(Math.abs(title.width-intendedWidth)<.1,'Title width',title);
      check(Math.abs(title.height-intendedWidth*215/650)<.1,'Title proportions',title);
      check(title.y===65 && Math.abs(title.x+title.width/2-width/2)<.1,'Title placement',title);
      check(await page.locator('.protected-title').getAttribute('src')==='outputs/the-haunted-realm-title-approved.png','Title source');
      return {title};
    });
    await page.screenshot({path:path.join(OUT,name+'-home-top.png')});
    await test('Home bottom card and document scrolling are reachable',async()=>{
      const bottom = page.locator('.scene-destination').last();
      if(width>900){await page.mouse.move(width/2,height/2);await page.mouse.wheel(0,5000);await page.waitForTimeout(250);}
      else {for(let i=0;i<12;i++)await swipe(page,width-35,height-120,150);}
      const box = await bottom.boundingBox();
      check(box.y>=60 && box.y+box.height<=height+.5,'Last Home scene/name not fully accessible',box);
      check(await bottom.isVisible(),'Last card visibility');
      const data=await page.evaluate(()=>({scrollY,scrollHeight:document.documentElement.scrollHeight,innerHeight,scrollWidth:document.documentElement.scrollWidth,innerWidth}));
      check(data.scrollWidth===width,'Horizontal overflow',data);
      await page.screenshot({path:path.join(OUT,name+'-home-bottom.png')});
      return data;
    });
    await page.evaluate(()=>scrollTo(0,0));
    await test('Home drawer only conceals content temporarily; close restores exact title',async()=>{
      const before = await page.locator('.protected-title').boundingBox();
      await openMenu(page,width);
      check(await page.locator('main').evaluate(e=>getComputedStyle(e).visibility)==='hidden','Overlay did not conceal main content');
      check(await page.locator('.realm-background').evaluate(e=>getComputedStyle(e).visibility)==='visible','Background concealed');
      await page.screenshot({path:path.join(OUT,name+'-home-menu.png')});
      await page.keyboard.press('Escape');
      check(await page.locator('.activities-control').evaluate(e=>e===document.activeElement),'Escape focus restoration');
      check(await page.locator('main').evaluate(e=>getComputedStyle(e).visibility)==='visible','Content not restored');
      check(JSON.stringify(await page.locator('.protected-title').boundingBox())===JSON.stringify(before),'Title moved after overlay');
      return before;
    });
    await test('Every Home scene opens its exact shell and returns Home',async()=>{
      await page.goto(BASE+'#/');await page.locator('.protected-title').waitFor();
      for(let i=0;i<ids.length;i++){
        const link=page.locator('[data-home-destination="'+ids[i]+'"]');
        await link.scrollIntoViewIfNeeded();
        if(width<=900)await link.tap();else await link.click();
        await route(page,ids[i],names[i]);
        await goHome(page,width);
      }
      return {destinations:9,input:width<=900?'emulated touch taps':'mouse clicks'};
    });
    await test('Home menu reaches every activity; activity navigation transitions through all nine',async()=>{
      await page.goto(BASE+'#/');await page.locator('.protected-title').waitFor();
      for(let i=0;i<ids.length;i++){
        await openMenu(page,width);
        const link=page.locator('[data-destination="'+ids[i]+'"]');
        await link.scrollIntoViewIfNeeded();
        if(width<=900)await link.tap();else await link.click();
        await route(page,ids[i],names[i]);
        if(width<=900)check(await page.locator('.activity-drawer').isHidden(),'Drawer failed to close on route');
        else check(await page.locator('main').evaluate(e=>getComputedStyle(e).visibility)==='visible','Permanent rail hides main');
        const background=await page.locator('.realm-background').evaluate(e=>getComputedStyle(e).backgroundImage);
        check(background.endsWith('/outputs/the-haunted-realm-background-corrected-review-v3.png")'),'Wrong global background',background);
        check(await page.evaluate(()=>document.documentElement.scrollWidth)===width,'Activity horizontal overflow');
        check((await images(page)).length===0,'Activity missing image');
        if(width>900 && i===0){
          const frame=await page.locator('.activity-drawer').boundingBox();
          check(frame.x===16 && frame.width===(width>=1800?460:430),'Desktop rail geometry',frame);
          const content=await page.locator('.content-space').boundingBox();
          check(content.x>frame.x+frame.width && content.x+content.width<=width,'Content/rail overlap',content);
          metrics.push({viewport:name,rail:frame,content});
        }
      }
      await page.screenshot({path:path.join(OUT,name+'-hotel-shell.png')});
      return {destinations:9};
    });
    await test('Last Hotel entry: actual navigation scroll, complete label and 34/38px image',async()=>{
      await page.goto(BASE+'#/activities/hotel-transylvania');await route(page,ids[8],names[8]);
      await openMenu(page,width);
      const list=page.locator('.destination-list');
      await list.evaluate(e=>e.scrollTop=0);
      const dimensions=await list.evaluate(e=>({clientHeight:e.clientHeight,scrollHeight:e.scrollHeight}));
      if(dimensions.scrollHeight>dimensions.clientHeight){
        const box=await list.boundingBox();
        if(width<=900)await swipe(page,box.x+box.width/2,box.y+box.height-25,box.y+40);
        else{await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.wheel(0,2000);await page.waitForTimeout(200);}
        check(await list.evaluate(e=>e.scrollTop)>0,'List did not scroll with tested input');
      }
      const last=page.locator('.destination-link').last();
      const box=await last.boundingBox(), container=await list.boundingBox();
      check(box.y>=container.y-.5 && box.y+box.height<=container.y+container.height+.5,'Hotel row clipped', {box,container});
      check(await last.innerText()==='Hotel Transylvania','Hotel name');
      const img=await last.locator('img').boundingBox();
      check(img.width===(width<=900?34:38) && img.height===img.width,'Navigation image size',img);
      const colour=await last.evaluate(e=>getComputedStyle(e).color);
      check(colour==='rgb(255, 218, 143)','Hotel selected colour',colour);
      await page.screenshot({path:path.join(OUT,name+'-navigation-bottom.png')});
      if(width<=900)await page.locator('.close-drawer').tap();
      return {...dimensions,row:box,image:img,selectedColour:colour};
    });
    await test('Direct destination URL, reload, back/forward preserve exact route/current state',async()=>{
      await page.goto(BASE+'#/activities/the-book-of-shadows');
      await route(page,ids[2],names[2]);
      await page.reload();await route(page,ids[2],names[2]);
      await openMenu(page,width);await page.locator('[data-destination="hotel-transylvania"]').click();await route(page,ids[8],names[8]);
      await page.goBack();await route(page,ids[2],names[2]);
      await page.goForward();await route(page,ids[8],names[8]);
      await goHome(page,width);
      return {direct:'the-book-of-shadows',history:'Hotel -> back Book -> forward Hotel -> Home'};
    });
    await test('Keyboard opens menu, traps focus, reaches final entry and activates it',async()=>{
      await page.goto(BASE+'?test=keyboard#/');await page.locator('.protected-title').waitFor();
      await page.locator('.activities-control').focus();
      await page.keyboard.press('Enter');
      check(await page.locator('.close-drawer').evaluate(e=>e===document.activeElement),'Open focus');
      const focusable=await page.locator('#navigation-region').evaluate(e=>[...e.querySelectorAll('a,button')].filter(n=>n.getClientRects().length).map(n=>n.textContent.trim()));
      const visible=page.locator('#navigation-region a, #navigation-region button');
      await page.locator('.home-control').focus();
      await page.keyboard.press('Shift+Tab');
      check(await page.locator('#navigation-region').evaluate(e=>e.contains(document.activeElement)),'Backward focus escaped modal');
      await page.keyboard.press('Tab');
      check(await page.locator('.home-control').evaluate(e=>e===document.activeElement),'Focus trap wrapping');
      await page.locator('.close-drawer').focus();
      for(let i=0;i<9;i++)await page.keyboard.press('Tab');
      check(await page.locator('.destination-link').last().evaluate(e=>e===document.activeElement),'Final keyboard focus');
      const final=await page.locator('.destination-link').last().boundingBox(),list=await page.locator('.destination-list').boundingBox();
      check(final.y+final.height<=list.y+list.height+.5,'Keyboard final row clipped');
      await page.keyboard.press('Enter');await route(page,ids[8],names[8]);
      check(await page.locator('h1').evaluate(e=>e===document.activeElement),'Activity route focus');
      await goHome(page,width);
      return {focusableCount:focusable.length,lastDestination:names[8]};
    });
    await test('Home route restores a programmatically focusable heading',async()=>{
      await page.goto(BASE+'?test=focus#/');await page.locator('.protected-title').waitFor();
      await page.locator('[data-home-destination="echoes-of-the-past"]').click();await route(page,ids[0],names[0]);
      await goHome(page,width);
      check(await page.locator('h1').evaluate(e=>e===document.activeElement),'Home heading did not receive route focus');
    });
    await test('Skip link focuses content without changing the Home route',async()=>{
      await page.goto(BASE+'?test=skip#/');await page.locator('.protected-title').waitFor();
      await page.keyboard.press('Tab');
      check(await page.locator('.skip-link').evaluate(e=>e===document.activeElement),'Skip link not first');
      await page.keyboard.press('Enter');
      await page.waitForTimeout(100);
      check(await page.locator('.protected-title').count()===1,'Skip link replaced Home');
      check(await page.locator('main').evaluate(e=>e===document.activeElement),'Skip link focus');
      check(new URL(page.url()).hash==='#/','Skip changed hash');
    });
    await test('No local console/runtime/network errors',async()=>{
      check(errors.filter(e=>e.viewport===name).length===0,'Console/runtime errors',errors.filter(e=>e.viewport===name));
      check(badRequests.filter(e=>e.viewport===name).length===0,'Failed requests',badRequests.filter(e=>e.viewport===name));
    });
    await context.close();
    console.log(name+' completed');
  }
  label='additional-routing';
  const context=await browser.newContext({viewport:{width:1366,height:768}});
  const page=await context.newPage();page.setDefaultTimeout(7000);
  page.on('pageerror',e=>errors.push({viewport:label,error:String(e)}));
  await test('Pages project-prefix entry/assets and every direct route reload',async()=>{
    const prefix=BASE+'the-haunted-realm/';
    await page.goto(prefix);await page.locator('.protected-title').waitFor();
    check((await images(page)).length===0,'Prefix assets missing');
    for(let i=0;i<ids.length;i++){
      await page.goto(prefix+'#/activities/'+ids[i]);await route(page,ids[i],names[i]);
      await page.reload();await route(page,ids[i],names[i]);
      check((await images(page)).length===0,'Reload asset failure');
    }
    return {prefix,routeReloads:9};
  });
  await test('Title exception boundary at 649 and 650px; resize preserves routing',async()=>{
    await page.goto(BASE+'#/');
    for(const width of [649,650]){
      await page.setViewportSize({width,height:812});
      const box=await page.locator('.protected-title').boundingBox();
      check(Math.abs(box.width-(width===650?650:617))<.1,'Title boundary',box);
    }
    await page.goto(BASE+'#/activities/hotel-transylvania');await route(page,ids[8],names[8]);
    await page.setViewportSize({width:1366,height:768});
    check(await page.locator('.activity-drawer').isVisible(),'Resize desktop rail');
    await page.setViewportSize({width:390,height:844});
    check(await page.locator('.activity-drawer').isHidden(),'Resize mobile drawer');
    await openMenu(page,390);
    await page.setViewportSize({width:1920,height:1080});
    check(await page.locator('.activity-drawer').isVisible(),'Resize rail visibility');
    check(await page.locator('main').evaluate(e=>!e.inert&&getComputedStyle(e).visibility==='visible'),'Resize content state');
  });
  await test('Unknown route handled without incorrect activity',async()=>{
    await page.goto(BASE+'#/activities/no-such-activity');
    await page.getByRole('heading',{name:'Destination not found'}).waitFor();
    check(await page.locator('.destination-link[aria-current="page"]').count()===0,'Unknown selected entry');
    await page.getByRole('link',{name:'Return Home'}).click();await page.locator('.protected-title').waitFor();
  });
  await test('Malformed encoded route handled without runtime exception',async()=>{
    await page.goto(BASE+'#/activities/%zz');
    await page.getByRole('heading',{name:'Destination not found'}).waitFor();
  });
  await context.close();await browser.close();
  const result={run:RUN,engine:'Installed Microsoft Edge (Chromium), headless Playwright',viewports,tests,metrics,errors,badRequests,passed:tests.filter(t=>t.status==='PASS').length,failed:tests.filter(t=>t.status==='FAIL').length};
  fs.writeFileSync(path.join(OUT,'results.json'),JSON.stringify(result,null,2));
  console.log(JSON.stringify({run:RUN,passed:result.passed,failed:result.failed,failures:tests.filter(t=>t.status==='FAIL'),errors,badRequests},null,2));
  process.exitCode=result.failed?1:0;
})().catch(e=>{console.error(e);process.exitCode=1});
