const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const { chromium } = require('C:/Users/DELL/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const out = path.join(__dirname, process.argv[2] || 'drawer-input-run-1');
fs.mkdirSync(out, { recursive: true });
const result = { tests: [], errors: [], badRequests: [] };
function save() {
  result.passed = result.tests.filter(t => t.status === 'PASS').length;
  result.failed = result.tests.filter(t => t.status === 'FAIL').length;
  fs.writeFileSync(path.join(out, 'results.json'), JSON.stringify(result, null, 2));
}
(async () => {
  const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true });
  for (const [name, width, height] of [['projector',1920,1080],['desktop',1600,900],['laptop',1366,768],['tablet',768,1024],['mobile',390,844],['mobile-narrow',320,812]]) {
    const context = await browser.newContext({ viewport: { width, height }, hasTouch: width < 600 });
    const page = await context.newPage();
    page.on('pageerror', e => result.errors.push(String(e)));
    page.on('console', m => { if (m.type() === 'error') result.errors.push(m.text()); });
    page.on('requestfailed', r => result.badRequests.push({url:r.url(), error:r.failure()?.errorText}));
    page.on('response', r => { if (r.status() >= 400) result.badRequests.push({url:r.url(),status:r.status()}); });
    try {
      await page.goto('http://127.0.0.1:4173/?drawerInput='+name+'#/');
      await page.locator('.activity-scene').last().waitFor();
      await page.evaluate(() => window.scrollTo(0, 600));
      const original = await page.evaluate(() => window.scrollY);
      await page.locator('.activities-control').click();
      const open = await page.evaluate(() => ({fixed:getComputedStyle(document.body).position,top:parseFloat(document.body.style.top),y:window.scrollY,hash:location.hash}));
      assert.equal(open.fixed,'fixed'); assert.ok(open.top===-original); assert.equal(open.y,0); assert.equal(open.hash,'#/');
      const list = page.locator('.destination-list');
      const box = await list.boundingBox();
      const first = await list.evaluate(e => e.scrollTop);
      await page.mouse.move(box.x+box.width/2, box.y+box.height/2);
      await page.mouse.wheel(0,450);
      await page.waitForTimeout(250);
      const wheel = await list.evaluate(e => ({scroll:e.scrollTop,max:e.scrollHeight-e.clientHeight}));
      if (wheel.max>0) assert.ok(wheel.scroll>first,'Real wheel must scroll an overflowing inner list');
      else {
        assert.equal(wheel.scroll,0);
        const last = await page.locator('.destination-link').last().boundingBox();
        assert.ok(last.y+last.height<=box.y+box.height,'Non-overflowing list must show its final row');
      }
      await page.mouse.move(width-2,height-2);
      await page.mouse.wheel(0,450);
      await page.waitForTimeout(200);
      assert.equal(await page.evaluate(() => window.scrollY),0);
      assert.ok(await page.evaluate(() => parseFloat(document.body.style.top))===-original);
      if (width < 600) {
        await list.evaluate(e => e.scrollTop=0);
        const cdp = await context.newCDPSession(page);
        const x=box.x+box.width/2, start=box.y+box.height-50, end=box.y+60;
        await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y:start}]});
        for (let i=1;i<=10;i++) {
          await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x,y:start+(end-start)*i/10}]});
          await page.waitForTimeout(20);
        }
        await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
        await page.waitForTimeout(200);
        assert.ok(await list.evaluate(e => e.scrollTop)>0,'Emulated touch swipe must scroll inner list');
        assert.equal(await page.evaluate(() => window.scrollY),0);
        await cdp.detach();
      }
      await page.keyboard.press('Escape');
      assert.equal(await page.evaluate(() => window.scrollY),original);
      assert.equal(await page.evaluate(() => location.hash),'#/');
      assert.equal(await page.evaluate(() => document.body.style.top),'');
      result.tests.push({test:name+' real wheel/inner list, outside lock and exact restoration'+(width<600?' + emulated touch swipe':''),status:'PASS',evidence:{originalScroll:original,innerScrollAfterWheel:wheel.scroll,innerMax:wheel.max,physicalDevice:false}});
    } catch(e) {result.tests.push({test:name+' drawer input',status:'FAIL',error:e.stack});}
    save(); await context.close();
  }
  await browser.close(); save();
  process.stdout.write(JSON.stringify(result,null,2));
  process.exitCode = result.failed || result.errors.length || result.badRequests.length ? 1 : 0;
})().catch(e => {result.errors.push(e.stack);save();console.error(e);process.exitCode=1;});
