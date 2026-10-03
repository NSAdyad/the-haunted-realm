const { chromium } = require('C:/Users/DELL/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('node:fs');
const path = require('node:path');
const RUN = process.argv[2] || 'presentation-run-1';
const onlyTest = process.argv.find(a=>a.startsWith('--only='))?.slice(7);
const onlyViewport = process.argv.find(a=>a.startsWith('--viewport='))?.slice(11);
const OUT = path.join(__dirname, RUN);
fs.mkdirSync(OUT, { recursive: true });
const BASE = 'http://127.0.0.1:4173/';
const names = ['Echoes of the Past', 'The Cursed Quest', 'The Book of Shadows', 'Fastest Finger First', 'Words of the Feast', 'The Phantom Order', 'Door to Darkness', 'Build the Haunted Banquet', 'Hotel Transylvania'];
const ids = ['echoes-of-the-past', 'the-cursed-quest', 'the-book-of-shadows', 'fastest-finger-first', 'words-of-the-feast', 'the-phantom-order', 'door-to-darkness', 'build-the-haunted-banquet', 'hotel-transylvania'];
const viewports = [['projector',1920,1080],['desktop',1600,900],['laptop',1366,768],['tablet',768,1024],['mobile',390,844],['mobile-narrow',320,812]];
const tests = [], metrics = [], errors = [], badRequests = [];
const auditNotes = [{event:'Read-only lookup failure',expected:'Read historical testing helper',actual:'The guessed test_local_shell.cjs filename did not exist',cause:'Guessed a filename instead of using an inventory',correction:'Read the existing test_normal.cjs and inspect_before.cjs after inventory',prevention:'List actual filenames before reading a historical helper',effect:'No runtime, image, Git or source mutation'}];
auditNotes.push({event:'Preserved presentation-run-1 harness failures',expected:'Compare equivalent states and numeric offset; install early fullscreen fixtures',actual:'CSS zero serialized as0px; Playwright auto-centered clicked Build row to180 vs archived direct-load90; aborted aggregate caused later tests to remain on activity route; early documentElement override did not install',cause:'Audit assumptions/preconditions and early DOM fixture target',correction:'Numeric top comparison, direct-load baseline reproduction, explicit Home setup before independent drawer tests, Element.prototype fixture overrides',prevention:'Assert equivalent starting state and fixture installation before classifying runtime failures',effect:'Only this test runner changed; runtime/protected sources unchanged; run1 remains preserved'});
let label = '';
const check = (condition,message,detail) => {if(!condition)throw new Error(message+' '+JSON.stringify(detail ?? ''));};
function persist(final=false) {const result={tests,metrics,errors,badRequests,auditNotes,summary:{passed:tests.filter(t=>t.status==='PASS').length,failed:tests.filter(t=>t.status==='FAIL').length}};fs.writeFileSync(path.join(OUT,final?'results.json':'partial-results.json'),JSON.stringify(result,null,2));return result;}
async function test(name,fn) {
  if(onlyTest && name!==onlyTest) return;
  try {tests.push({viewport:label,test:name,status:'PASS',evidence:await fn()});}
  catch(e) {tests.push({viewport:label,test:name,status:'FAIL',actual:String(e)});console.log('TEST FAILURE',label,name,String(e));}
  persist();
}
async function settle(page) {await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))));await page.waitForTimeout(90);}
async function state(page) {return page.evaluate(()=>({hash:location.hash,active:document.body.classList.contains('presentation-mode'),pressed:document.querySelector('.presentation-toggle').getAttribute('aria-pressed'),fullscreen:document.querySelector('.presentation-controls').dataset.fullscreen,nativeElement:document.fullscreenElement?.tagName || null,fullscreenEnabled:document.fullscreenEnabled,selected:document.querySelector('.destination-link[aria-current="page"]')?.dataset.destination || null,width:innerWidth,height:innerHeight,documentWidth:document.documentElement.scrollWidth,documentHeight:document.documentElement.scrollHeight,scrollY,navCount:document.querySelectorAll('.global-navigation').length,modeCount:document.querySelectorAll('.presentation-toggle').length}));}
async function mode(page,want=true,keyboard=false) {
  const before=await state(page);
  if(before.active!==want) {
    const button=page.locator('.presentation-toggle');
    if(keyboard){await button.focus();await page.keyboard.press('Enter');}else await button.click();
  }
  await page.waitForFunction(expected=>document.body.classList.contains('presentation-mode')===expected,want);
  if(want)await page.waitForFunction(()=>document.querySelector('.presentation-controls').dataset.fullscreen!=='requesting');
  else await page.waitForFunction(()=>!document.fullscreenElement);
  await settle(page);
  return state(page);
}
async function route(page,id,index) {
  await page.waitForURL(url=>url.hash==='#/activities/'+id);
  await page.locator('h1').filter({hasText:names[index]}).waitFor();
  check(await page.locator('h1').innerText()===names[index],'Wrong exact activity name');
  check(await page.locator('.destination-link[aria-current="page"]').getAttribute('data-destination')===id,'Wrong selected activity');
  check(await page.locator('.content-space').innerText()==='Activity content area\n\nContent and interactions will be developed after separate approval.','Unexpected activity content');
}
async function openDrawer(page,width) {
  if(width<=900 || await page.locator('body').evaluate(b=>b.classList.contains('home-view')))await page.locator('.activities-control').click();
  await page.locator('.activity-drawer').waitFor({state:'visible'});
}
async function home(page,width) {
  await page.locator(width>900?'.rail-home':'.home-control').click();
  await page.waitForURL(url=>url.hash==='#/');await page.locator('.protected-title').waitFor();await settle(page);
}
async function controls(page) {
  const geometry=await page.evaluate(()=>{
    const list=[...document.querySelectorAll('.home-control,.activities-control,.presentation-toggle,.close-drawer')].filter(e=>e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden');
    return {width:innerWidth,height:innerHeight,controls:list.map(e=>({name:e.className,...e.getBoundingClientRect().toJSON()}))};
  });
  for(const b of geometry.controls)check(b.left>=0&&b.top>=0&&b.right<=geometry.width+.5&&b.bottom<=geometry.height+.5,'Control clipped',b);
  for(let i=0;i<geometry.controls.length;i++)for(let j=i+1;j<geometry.controls.length;j++) {
    const a=geometry.controls[i],b=geometry.controls[j];
    check(Math.min(a.right,b.right)<=Math.max(a.left,b.left)||Math.min(a.bottom,b.bottom)<=Math.max(a.top,b.top),'Controls overlap',{a,b});
  }
  return geometry;
}
async function assertHome(page,width,height,phase) {
  const data=await page.evaluate(()=>({width:innerWidth,height:innerHeight,documentHeight:document.documentElement.scrollHeight,documentWidth:document.documentElement.scrollWidth,scrollY,title:document.querySelector('.protected-title').getBoundingClientRect().toJSON(),cards:[...document.querySelectorAll('.scene-destination')].map(e=>({id:e.dataset.homeDestination,hit:e.getBoundingClientRect().toJSON(),scene:e.querySelector('.activity-scene').getBoundingClientRect().toJSON(),space:e.querySelector('.scene-space').getBoundingClientRect().toJSON(),name:e.querySelector('.scene-name').getBoundingClientRect().toJSON(),source:e.querySelector('.activity-scene').getAttribute('src'),lettering:e.querySelector('.name-rest').getAttribute('src')}))}));
  check(data.documentWidth===width,'Home horizontal overflow',data);
  const tw=width<650?width-32:650;
  check(Math.abs(data.title.width-tw)<.2&&Math.abs(data.title.height-tw*215/650)<.2,'Title dimensions',data.title);
  check(data.title.y===65&&Math.abs(data.title.x+data.title.width/2-width/2)<.2,'Title positioning',data.title);
  check(data.cards.length===9,'Wrong Home destination count');
  if(width===1920&&height===1080) {
    check(data.documentHeight<=height,'Projector Home ordinary document scrolling still required',data);
    for(const card of data.cards)for(const key of ['hit','scene','space','name']) {
      const b=card[key];check(b.left>=0&&b.top>=0&&b.right<=width+.5&&b.bottom<=height+.5,'Projector Home element clipped',{id:card.id,type:key,b});
    }
    for(const card of data.cards)check(card.space.height===178&&card.name.width===440,'Scene/lettering scale changed',card);
    await page.mouse.move(700,650);await page.mouse.wheel(0,1200);await page.waitForTimeout(130);
    check(await page.evaluate(()=>scrollY)===0,'Projector Home wheel reveals hidden choices');
  }
  metrics.push({viewport:label,phase,...data});return data;
}
function listen(page,phase) {
  page.on('pageerror',e=>errors.push({phase,error:String(e)}));
  page.on('console',m=>{if(m.type()==='error')errors.push({phase,error:m.text()});});
  page.on('requestfailed',r=>badRequests.push({phase,url:r.url(),failure:r.failure()}));
  page.on('response',r=>{if(r.status()>=400)badRequests.push({phase,url:r.url(),status:r.status()});});
}
(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  const baseline=JSON.parse(fs.readFileSync(path.join(__dirname,'before-browser-measurements.json'),'utf8'));
  for(const [name,width,height] of viewports) {
    if(onlyViewport && name!==onlyViewport)continue;
    label=name;
    const context=await browser.newContext({viewport:{width,height},hasTouch:width<=900,isMobile:width<=649,reducedMotion:'reduce'});
    const page=await context.newPage();page.setDefaultTimeout(6500);listen(page,name);
    await page.goto(BASE+'#/');await page.locator('.protected-title').waitFor();await settle(page);
    await test('Normal Home bounds, exact names and protected title',async()=>{
      check(JSON.stringify(await page.locator('.scene-destination').evaluateAll(a=>a.map(e=>e.getAttribute('aria-label'))))===JSON.stringify(names),'Wrong exact Home names');
      check(JSON.stringify(await page.locator('.destination-link span').allTextContents())===JSON.stringify(names),'Wrong exact navigation names');
      const data=await assertHome(page,width,height,'normal');await controls(page);await page.screenshot({path:path.join(OUT,name+'-home-normal.png')});return data;
    });
    await test('Mouse presentation entry and native fullscreen observation',async()=>{
      const before=await state(page);const after=await mode(page,true);
      check(after.hash===before.hash&&after.navCount===1&&after.modeCount===1,'Presentation changed route or duplicated controls',{before,after});
      check(after.pressed==='true','Presentation pressed state');check(['native','fallback'].includes(after.fullscreen),'Invalid settled fullscreen state',after);
      if(after.fullscreen==='native')check(after.nativeElement==='HTML','Native fullscreen claim has no fullscreenElement',after);
      await controls(page);const data=await assertHome(page,width,height,'presentation');await page.screenshot({path:path.join(OUT,name+'-home-presentation.png')});return {entry:after,bounds:data};
    });
    await test('Mouse presentation exit restores normal state and same route',async()=>{
      const before=await state(page),after=await mode(page,false);check(after.hash===before.hash,'Exit reset destination');check(after.fullscreen==='inactive'&&after.nativeElement===null,'Native fullscreen not exited',after);return after;
    });
    await test('Keyboard presentation entry and Escape exit',async()=>{
      const before=await state(page),entered=await mode(page,true,true);await page.keyboard.press('Escape');await page.waitForFunction(()=>!document.body.classList.contains('presentation-mode'));await page.waitForFunction(()=>!document.fullscreenElement);
      const exited=await state(page);check(exited.hash===before.hash&&exited.pressed==='false','Keyboard escape state mismatch',{before,entered,exited});return {entered,exited};
    });
    await test('Presentation Home image choices open all nine exact shells',async()=>{
      await mode(page,true);
      for(let i=0;i<ids.length;i++) {
        const card=page.locator('[data-home-destination="'+ids[i]+'"]');await card.scrollIntoViewIfNeeded();
        if(width<=900)await card.tap();else await card.click();await route(page,ids[i],i);
        check((await state(page)).active,'Route lost presentation state');await controls(page);await home(page,width);check((await state(page)).active,'Home return lost presentation state');
      }
      await mode(page,false);return {destinations:9,input:width<=900?'emulated touch taps':'mouse clicks'};
    });
    await test('All nine shells preserve selection and shared nav through mode and cross-navigation',async()=>{
      for(let i=0;i<ids.length;i++) {
        await openDrawer(page,width);const link=page.locator('[data-destination="'+ids[i]+'"]');await link.scrollIntoViewIfNeeded();await link.click();await route(page,ids[i],i);
        await page.evaluate(()=>{window.__navIdentity=document.querySelector('.global-navigation');});
        const before=await state(page),entered=await mode(page,true,i%2===0);await controls(page);
        check(entered.hash===before.hash&&entered.selected===ids[i],'Mode changed shell/selection',{before,entered});
        check(await page.evaluate(()=>window.__navIdentity===document.querySelector('.global-navigation')),'Mode replaced navigation');
        check(entered.documentWidth===width,'Activity horizontal overflow',entered);
        const background=await page.locator('.realm-background').evaluate(e=>getComputedStyle(e).backgroundImage);
        check(background.includes('the-haunted-realm-background-corrected-review-v3.png'),'Background changed');
        const exited=await mode(page,false);check(exited.hash===before.hash&&exited.selected===ids[i],'Exit changed shell/selection',{before,exited});
        if(width===1920||width===1366) {
          // Archived rail evidence used a direct load, not Playwright's link
          // auto-centering. Reproduce that state before the pixel comparison.
          await page.reload();await page.locator('h1').waitFor();await settle(page);
          await page.mouse.move(width-50,500);await settle(page);
          const rail=await page.locator('.activity-drawer').evaluate(e=>({box:e.getBoundingClientRect().toJSON(),listScroll:e.querySelector('.destination-list').scrollTop,selected:e.querySelector('[aria-current="page"]').dataset.destination,sources:[...e.querySelectorAll('img')].map(i=>i.getAttribute('src'))}));
          const old=baseline.rails.find(r=>r.width===width&&r.id===ids[i]);check(JSON.stringify(rail.box)===JSON.stringify(old.box)&&rail.listScroll===old.listScroll,'Successful rail geometry/scroll changed',{old,rail});
          await page.locator('.activity-drawer').screenshot({path:path.join(OUT,`after-rail-${width}-${ids[i]}.png`)});metrics.push({viewport:name,id:ids[i],rail});
        }
      }
      await page.screenshot({path:path.join(OUT,name+'-hotel-normal.png')});await home(page,width);return {destinations:9};
    });
    await test('Open drawer retains accessible presentation control, Hotel access, and focus trap',async()=>{
      await page.goto(BASE+'#/');await page.locator('.protected-title').waitFor();await settle(page);
      await openDrawer(page,width);const geometry=await controls(page);
      if(width<=600)check(await page.locator('.presentation-toggle').evaluate(e=>e.closest('.drawer-heading')!==null),'Mobile presentation control not inside drawer header');
      let reached=false,escaped=false;
      await page.locator('.close-drawer').focus();
      for(let i=0;i<18;i++) {await page.keyboard.press('Tab');const active=await page.evaluate(()=>({inside:document.querySelector('#navigation-region').contains(document.activeElement),presentation:document.activeElement.classList.contains('presentation-toggle')}));reached ||= active.presentation;escaped ||= !active.inside;}
      check(reached&&!escaped,'Drawer focus trap excludes presentation or escapes',{reached,escaped});
      await page.locator('.presentation-toggle').click();await page.waitForFunction(()=>document.body.classList.contains('presentation-mode'));await page.waitForFunction(()=>document.querySelector('.presentation-controls').dataset.fullscreen!=='requesting');
      check(await page.locator('.activity-drawer').isVisible(),'Entering mode unexpectedly closes drawer');
      const hotel=page.locator('[data-destination="hotel-transylvania"]');await hotel.scrollIntoViewIfNeeded();const b=await hotel.boundingBox(),list=await page.locator('.destination-list').boundingBox();check(b.y>=list.y-.5&&b.y+b.height<=list.y+list.height+.5,'Hotel entry clipped',b);
      check(await page.locator('.presentation-toggle').isVisible(),'Presentation exit inaccessible in drawer');
      await page.keyboard.press('Escape');check((await state(page)).active,'Drawer Escape prematurely exited presentation');check(await page.locator('.activity-drawer').isHidden(),'Escape did not close drawer');
      await page.keyboard.press('Escape');await page.waitForFunction(()=>!document.body.classList.contains('presentation-mode'));await page.waitForFunction(()=>!document.fullscreenElement);return geometry;
    });
    await test('Home Activities opens navigation without changing route or document offset',async()=>{
      await page.goto(BASE+'#/');await page.locator('.protected-title').waitFor();await settle(page);
      await page.evaluate(()=>scrollTo(0,400));await page.waitForTimeout(90);const original=await page.evaluate(()=>scrollY),hash=await page.evaluate(()=>location.hash);await openDrawer(page,width);
      const locked=await page.evaluate(()=>({hash:location.hash,position:getComputedStyle(document.body).position,top:document.body.style.top,scrollY}));check(locked.hash===hash&&locked.position==='fixed'&&parseFloat(locked.top)===-original,'Drawer changes route/does not lock original offset',locked);
      await page.mouse.move(width-25,height-100);await page.mouse.wheel(0,500);await page.waitForTimeout(120);check(await page.evaluate(()=>scrollY)===locked.scrollY,'Outside drawer wheel moves document');
      await page.locator('.close-drawer').click();check(await page.evaluate(()=>scrollY)===original,'Closing drawer does not restore document offset');await page.evaluate(()=>scrollTo(0,0));return {original,locked};
    });
    await test('No broken loaded images or emojis after presentation flows',async()=>{
      const broken=await page.evaluate(()=>[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src));check(broken.length===0,'Broken loaded images',broken);check(!await page.locator('body').evaluate(e=>/\p{Extended_Pictographic}/u.test(e.textContent)),'Emoji in interface');return {broken};
    });
    await context.close();
  }
  for(const fixture of ['absent','denied','delayed']) {
    if(onlyViewport)continue;
    label='fixture-'+fixture;const context=await browser.newContext({viewport:{width:1920,height:1080},reducedMotion:'reduce'});
    await context.addInitScript(kind=>{
      if(kind==='absent')Object.defineProperty(Element.prototype,'requestFullscreen',{configurable:true,value:undefined});
      if(kind==='denied')Object.defineProperty(Element.prototype,'requestFullscreen',{configurable:true,value:()=>Promise.reject(new DOMException('Test fixture denied fullscreen','NotAllowedError'))});
      if(kind==='delayed')Object.defineProperty(Element.prototype,'requestFullscreen',{configurable:true,value:()=>new Promise(resolve=>setTimeout(resolve,350))});
    },fixture);
    const page=await context.newPage();page.setDefaultTimeout(6500);listen(page,label);await page.goto(BASE+'#/activities/hotel-transylvania');await page.locator('h1').waitFor();await settle(page);
    await test('Fullscreen fixture installed before interaction',async()=>{
      const actual=await page.evaluate(()=>({type:typeof document.documentElement.requestFullscreen,source:String(document.documentElement.requestFullscreen)}));
      check(fixture==='absent'?actual.type==='undefined':actual.source.includes(fixture==='denied'?'Test fixture denied fullscreen':'setTimeout'),'Fullscreen fixture not installed',actual);return actual;
    });
    await test('Fullscreen '+fixture+' fixture preserves route and provides graceful exit',async()=>{
      const before=await state(page);
      if(fixture==='delayed') {
        await page.locator('.presentation-toggle').click();await page.locator('.presentation-toggle').click();await page.locator('.presentation-toggle').click();await page.waitForTimeout(500);
        const active=await state(page);check(active.active&&active.fullscreen==='fallback'&&active.nativeElement===null&&active.hash===before.hash,'Late fullscreen promise overrides current mode/route',{before,active});
        await page.keyboard.press('Escape');await page.waitForFunction(()=>!document.body.classList.contains('presentation-mode'));await page.waitForTimeout(100);
      } else {
        const active=await mode(page,true,true);check(active.active&&active.fullscreen==='fallback'&&active.nativeElement===null&&active.hash===before.hash,'Unavailable/denied fullscreen breaks layout',{before,active});await controls(page);await mode(page,false,true);
      }
      const after=await state(page);check(!after.active&&after.nativeElement===null&&after.hash===before.hash&&after.selected==='hotel-transylvania','Fallback exit lost route/state',{before,after});return {before,after};
    });
    await test('Fullscreen '+fixture+' fallback Home projector fit remains valid',async()=>{
      await home(page,1920);await mode(page,true);const bounds=await assertHome(page,1920,1080,'fallback-'+fixture);await page.screenshot({path:path.join(OUT,'fallback-'+fixture+'-home.png')});await mode(page,false);return bounds;
    });
    await context.close();
  }
  label='suite';await test('Console/runtime and local-network error audit',async()=>{check(errors.length===0,'Console/runtime errors',errors);check(badRequests.length===0,'Request errors',badRequests);return {errors,badRequests};});
  await browser.close();const result=persist(true);console.log(JSON.stringify({run:RUN,...result.summary,errors:errors.length,badRequests:badRequests.length,native:tests.filter(t=>t.test.includes('Mouse presentation entry')).map(t=>({viewport:t.viewport,...t.evidence?.entry})),failures:tests.filter(t=>t.status==='FAIL')},null,2));process.exitCode=result.summary.failed?1:0;
})().catch(e=>{auditNotes.push({event:'Runner fatal error',actual:String(e)});persist(true);console.error('RUNNER FAILURE',e);process.exitCode=1;});
