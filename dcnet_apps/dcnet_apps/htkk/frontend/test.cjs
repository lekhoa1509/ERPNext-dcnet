const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({headless: 'new', args: ['--no-sandbox']});
  const page = await browser.newPage();
  
  page.on('console', msg => {
    console.log('[PAGE CONSOLE]', msg.type(), msg.text());
  });
  
  page.on('pageerror', error => {
    console.log('[PAGE ERROR]', error.message);
  });

  await page.goto('http://localhost:5173/?id=HTKK-01/GTGT-Th%C3%A1ng3-2026-0003');
  
  console.log('Waiting 5s for page to load with Univer...');
  await new Promise(r => setTimeout(r, 8000));
  
  await page.screenshot({path: 'htkk_ui.png'});
  console.log('Saved screenshot to htkk_ui.png. Closing...');
  
  await browser.close();
})();
