"""Browser smoke test. Serve the repo locally; requires Playwright and Chromium."""
import asyncio, json, os, struct, wave
from pathlib import Path
from playwright.async_api import async_playwright

BASE_URL = os.environ.get('MAESTRO_BASE_URL', 'http://127.0.0.1:8000').rstrip('/')
OUTPUT = Path(os.environ.get('MAESTRO_TEST_OUTPUT', '/tmp/maestro-browser-check'))
OUTPUT.mkdir(parents=True, exist_ok=True)

async def main():
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True, executable_path=os.environ.get('MAESTRO_CHROMIUM_PATH'), args=['--no-sandbox','--disable-dev-shm-usage'])
    page = await browser.new_page(viewport={'width':1440,'height':1000}, device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    await page.goto(BASE_URL + '/studio/')
    print(await page.evaluate('JSON.stringify({title:document.title,w:document.documentElement.scrollWidth,h:document.documentElement.scrollHeight})'))
    await page.screenshot(path=str(OUTPUT / 'maestro-studio-desktop.png'),full_page=True)
    initial=json.loads(await page.evaluate("localStorage.getItem('maestro-music-kitchen-v1')"))
    await page.get_by_role('button',name='↗ Rise',exact=True).click()
    await page.locator('#apply').click()
    await page.wait_for_timeout(500)
    changed=json.loads(await page.evaluate("localStorage.getItem('maestro-music-kitchen-v1')"))
    assert changed['tracks'][0]==initial['tracks'][0], 'Piano must remain identical'
    assert changed['tracks'][2:]==initial['tracks'][2:], 'Other instruments must remain identical'
    for i in [0,1,3]: assert changed['tracks'][1]['phrases'][i]==initial['tracks'][1]['phrases'][i]
    assert changed['tracks'][1]['phrases'][2]!=initial['tracks'][1]['phrases'][2]
    assert await page.locator('#play').get_attribute('aria-label')=='Pause arrangement'
    await page.locator('#before').click()
    assert await page.locator('#before').get_attribute('aria-pressed')=='true'
    await page.locator('#after').click()
    await page.locator('#stop').click()
    await page.locator('#undo').click()
    assert json.loads(await page.evaluate("localStorage.getItem('maestro-music-kitchen-v1')"))==initial
    await page.get_by_role('button',name='Select drums, bars 3 to 4',exact=True).click()
    await page.locator('#tap').click();await page.wait_for_timeout(180)
    await page.locator('#tap').click();await page.wait_for_timeout(360)
    await page.locator('#tap').click()
    await page.locator('#use-rhythm').click()
    await page.locator('#apply').click();await page.locator('#stop').click()
    tapped=json.loads(await page.evaluate("localStorage.getItem('maestro-music-kitchen-v1')"))
    assert len(tapped['tracks'][2]['phrases'][1]['rhythm'])>=2
    await page.locator('.recipe-details summary').click()
    await page.locator('#recipe').fill('phrase piano [1:2] {\n density 0.5\n contour [0,0,0,0,0,0,0,0]\n rhythm auto\n}')
    await page.locator('#run-recipe').click()
    assert 'pinned' in await page.locator('#announcement').inner_text()
    assert json.loads(await page.evaluate("localStorage.getItem('maestro-music-kitchen-v1')"))==tapped
    await page.locator('#recipe').fill('phrase bass [7:8] {\n density 0.3\n contour [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]\n rhythm [0,8,16,24]\n}')
    await page.locator('#run-recipe').click(); await page.locator('#stop').click()
    assert 'Bass · bars 7–8' in await page.locator('#selected-name').inner_text()
    await page.locator('#direction').fill('Make a symphony about the ocean')
    await page.locator('#direction-form button').click()
    assert 'not connected' in await page.locator('#announcement').inner_text()
    await page.locator('#project-name').fill('Browser verified sketch'); await page.locator('#project-name').press('Tab')
    async with page.expect_download() as d:
      await page.locator('#export-project').click()
    project_download=await d.value; await project_download.save_as(str(OUTPUT / 'maestro-test.kitchen.json'))
    assert json.loads(Path(str(OUTPUT / 'maestro-test.kitchen.json')).read_text())['name']=='Browser verified sketch'
    async with page.expect_download(timeout=30000) as d:
      await page.locator('#export-audio').click()
    audio_download=await d.value; await audio_download.save_as(str(OUTPUT / 'maestro-test.wav'))
    with wave.open(str(OUTPUT / 'maestro-test.wav')) as w:
      assert w.getnchannels()==1 and w.getframerate()==44100 and w.getnframes()>44100*20
      samples=struct.unpack('<'+'h'*w.getnframes(),w.readframes(w.getnframes()))
      assert max(abs(s) for s in samples)>1000
      print('WAV:',len(samples),'samples; peak',max(abs(s) for s in samples))
    await page.reload()
    assert await page.locator('#project-name').input_value()=='Browser verified sketch'
    await page.locator('#reset').click()
    await page.set_viewport_size({'width':390,'height':844})
    await page.screenshot(path=str(OUTPUT / 'maestro-studio-mobile.png'),full_page=True)
    assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Studio mobile overflow'
    for url in ['','journal/','journal/2026-09-10.html','artifacts/music-kitchen-product.html','journal/snapshots/2026-09-10/music-kitchen-product.html']:
      response=await page.goto(BASE_URL + '/'+url)
      assert response.status==200
      assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Mobile overflow: {url}'
    await page.goto(BASE_URL + '/')
    await page.screenshot(path=str(OUTPUT / 'maestro-home-mobile.png'),full_page=True)
    await page.set_viewport_size({'width':1440,'height':1000})
    await page.screenshot(path=str(OUTPUT / 'maestro-home-desktop.png'),full_page=True)
    assert not errors, errors
    print('PASS: scoped edits, protected piano, A/B, undo, taps, recipe validation/execution, honest prompt fallback, persistence, project/WAV export, page loading, and mobile layout.')
    print(f'Browser artifacts: {OUTPUT}')
    await browser.close()

asyncio.run(main())
