const {chromium}=require('C:/Users/DELL/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const WORK=__dirname,OUT=path.join(WORK,process.argv[2]||'rail-rendering-replay-v1');
if(fs.existsSync(OUT))throw Error('Do not overwrite a rendering replay');fs.mkdirSync(OUT);
const baseline=JSON.parse(fs.readFileSync(path.join(WORK,'before-snapshot.json'),'utf8'));
const hash=text=>crypto.createHash('sha256').update(text).digest('hex').toUpperCase();
const sourceVerification=Object.fromEntries(Object.entries(baseline.source_before).map(([file,text])=>{
 const candidate=hash(text)===baseline.files[file]?text:text.replace(/\r?\n/g,'\r\n');
 return [file,{expected:baseline.files[file],actual:hash(candidate),matches:hash(candidate)===baseline.files[file],snapshotTextNewlines:hash(text)===baseline.files[file]?'already byte exact':'CRLF restored only in verification memory'}];
}));
if(Object.values(sourceVerification).some(v=>!v.matches))throw Error('Baseline source hash mismatch');
const ids=['echoes-of-the-past','the-cursed-quest','the-book-of-shadows','fastest-finger-first','words-of-the-feast','the-phantom-order','door-to-darkness','build-the-haunted-banquet','hotel-transylvania'];
const names=['Echoes of the Past','The Cursed Quest','The Book of Shadows','Fastest Finger First','Words of the Feast','The Phantom Order','Door to Darkness','Build the Haunted Banquet','Hotel Transylvania'];
const measurements=[],errors=[],badRequests=[];
async function decode(page){await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))));}
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 for(const variant of ['original-memory-replay','current-memory-replay']){
  const page=await browser.newPage({viewport:{width:1920,height:1080},reducedMotion:'reduce'});
  if(variant==='original-memory-replay'){
   await page.route('**/src/app.js',route=>route.fulfill({status:200,contentType:'text/javascript',body:baseline.source_before['src/app.js']}));
   await page.route('**/src/styles.css',route=>route.fulfill({status:200,contentType:'text/css',body:baseline.source_before['src/styles.css']}));
  }
  page.on('pageerror',e=>errors.push({variant,error:String(e)}));page.on('console',m=>{if(m.type()==='error')errors.push({variant,error:m.text()});});
  page.on('requestfailed',r=>badRequests.push({variant,url:r.url(),failure:r.failure()}));
  await page.goto('http://127.0.0.1:4173/');await page.locator('.protected-title').waitFor();await decode(page);
  await page.screenshot({path:path.join(OUT,variant+'-home.png')});
  await page.locator('.activities-control').click();await page.mouse.move(700,600);await page.mouse.wheel(0,500);await page.waitForTimeout(200);await page.keyboard.press('Escape');
  for(const width of [1920,1366]){
   await page.setViewportSize({width,height:width===1920?1080:768});
   for(let i=0;i<ids.length;i++){
    await page.goto('http://127.0.0.1:4173/#/activities/'+ids[i]);await page.locator('h1').filter({hasText:names[i]}).waitFor();await decode(page);await page.mouse.move(width-50,500);
    await page.locator('.activity-drawer').screenshot({path:path.join(OUT,`${variant}-rail-${width}-${ids[i]}.png`)});
    measurements.push({variant,width,id:ids[i],...await page.locator('.activity-drawer').evaluate(e=>({box:e.getBoundingClientRect().toJSON(),listScroll:e.querySelector('.destination-list').scrollTop,selected:e.querySelector('[aria-current="page"]').dataset.destination,sources:[...e.querySelectorAll('img')].map(i=>i.getAttribute('src')),rowMaterials:[...e.querySelectorAll('.destination-link')].map(e=>getComputedStyle(e).backgroundImage),dpr:devicePixelRatio}))});
   }
  }
  await page.close();
 }
 await browser.close();const result={method:'Original app/styles served only in browser memory from verified pre-change snapshot. Original/current captures use the same browser, context options, reduced-motion setting, viewport sequence and prior Home/menu interaction; no runtime or archived image mutation.',sourceVerification,measurements,errors,badRequests};
 fs.writeFileSync(path.join(OUT,'browser-evidence.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({captures:measurements.length,sourceHashesVerified:Object.keys(sourceVerification).length,errors:errors.length,badRequests:badRequests.length}));
})().catch(e=>{console.error(e);process.exitCode=1});
