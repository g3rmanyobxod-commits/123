import asyncio, json
from playwright.async_api import async_playwright

URL = 'file:///home/user/app/assets/vpn.html'
OUT = '/home/user/qa'

BRIDGE = """
window.__jsCalls = [];
window.Native = {
  ping: function (json) {
    const list = JSON.parse(json);
    const out = list.map((row, i) => ({ id: row.id, ms: 40 + i * 90 }));
    window.__jsCalls.push('ping:' + list.length);
    setTimeout(function () { window.__onLatency(JSON.stringify(out)); }, 120);
  },
  readClipboard: function (target) {
    window.__jsCalls.push('clip:' + target);
    setTimeout(function () {
      window.__onClipboard(target, 'vless://abc@de1.example.net:443?security=tls#🇩🇪 Берлин');
    }, 80);
  },
  haptic: function () { window.__jsCalls.push('haptic'); },
  setChrome: function (color, dark) { window.__jsCalls.push('chrome:' + color + ':' + dark); },
  copy: function (t) { window.__jsCalls.push('copy'); },
  saveFile: function (n, c) { window.__jsCalls.push('save:' + n + ':' + c.length); },
  pickFile: function () { window.__jsCalls.push('pick'); },
  fetchText: function (key, url) {
    setTimeout(function () {
      window.__onFetch(key, true, 'vless://x@fi9.example.net:443#🇫🇮 Хельсинки');
    }, 60);
  }
};
"""


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={'width': 412, 'height': 892},
                                        device_scale_factor=2, is_mobile=True, has_touch=True)
        page = await ctx.new_page()
        errors = []
        page.on('console', lambda m: errors.append('CONSOLE %s: %s' % (m.type, m.text)) if m.type in ('error', 'warning') else None)
        page.on('pageerror', lambda e: errors.append('PAGEERROR: %s' % e))
        await page.add_init_script(BRIDGE)
        await page.goto(URL)
        await page.wait_for_timeout(1200)

        # 1. latency
        await page.click(".dock-item[data-nav='servers']")
        await page.wait_for_timeout(1400)
        await page.screenshot(path=OUT + '/t-latency.png')
        pings = await page.eval_on_selector_all('.server-ping', 'els => els.map(e => e.textContent)')
        print('latency cells:', pings)

        # 2. clipboard paste into a new server form
        await page.click('#open-add-server')
        await page.wait_for_timeout(400)
        await page.click("[data-paste='server-link']")
        await page.wait_for_timeout(500)
        val = await page.input_value('#server-link')
        preview = await page.text_content('#preview-city')
        print('paste ->', val, '| preview city:', preview)
        await page.screenshot(path=OUT + '/t-paste.png')

        # 3. deep link import
        await page.evaluate("window.__importLink('vless://z@us5.example.net:8443?security=tls#🇺🇸 Нью-Йорк')")
        await page.wait_for_timeout(400)
        print('deeplink value:', await page.input_value('#server-link'))

        # 4. back navigation
        handled = await page.evaluate('window.__nativeBack()')
        print('back handled (from add-server):', handled)
        print('view after back:', await page.evaluate("document.body.dataset.view"))

        # 5. native fetch for subscription
        await page.evaluate("""
          (async () => {
            document.getElementById('sub-name').value = 'Нативная подписка';
            document.getElementById('sub-url').value = 'https://example.com/sub';
            document.getElementById('sub-form').dispatchEvent(new Event('submit', {cancelable: true, bubbles: true}));
          })()
        """)
        await page.wait_for_timeout(900)
        subs = await page.eval_on_selector_all('.sub-name', 'els => els.map(e => e.textContent)')
        print('subscriptions:', subs)

        # 6. export
        await page.click(".dock-item[data-nav='settings']")
        await page.wait_for_timeout(400)
        await page.click('#export-data')
        await page.wait_for_timeout(300)
        print('calls:', await page.evaluate('window.__jsCalls'))

        # 7. import round-trip
        payload = await page.evaluate("""() => JSON.stringify({servers:[{id:'srv-x',city:'Осло',country:'Норвегия',code:'NO',flag:'🇳🇴',lat:59.91,lng:10.75,protocol:'VLESS',host:'no1.example.net',port:443,link:'vless://n@no1.example.net:443#🇳🇴 Осло',subId:'',subName:'',created:1}],subscriptions:[],selected:'srv-x',settings:{theme:'night'}})""")
        await page.evaluate("t => window.__onImport(t)", payload)
        await page.wait_for_timeout(800)
        await page.screenshot(path=OUT + '/t-import.png')
        rows = await page.eval_on_selector_all('.server-city', 'els => els.map(e => e.textContent)')
        print('after import rows:', rows)

        # 8. labels + flags size + soft + compact
        await page.click(".dock-item[data-nav='settings']")
        await page.wait_for_timeout(300)
        await page.click("[data-setting='labels']")
        await page.click("[data-setting='soft']")
        await page.click("[data-setting='compact']")
        await page.click("[data-group='flags'][data-value='1.25']")
        await page.wait_for_timeout(400)
        await page.screenshot(path=OUT + '/t-soft-settings.png')
        await page.click(".dock-item[data-nav='home']")
        await page.wait_for_timeout(1600)
        await page.screenshot(path=OUT + '/t-labels.png')
        print('labels on:', await page.evaluate("document.body.dataset.labels"))
        print('flag scale:', await page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--flag-scale')"))

        # 9. custom accent colour
        await page.evaluate("""() => {
          const input = document.querySelector('.swatch-custom input');
          input.value = '#1e88e5';
          input.dispatchEvent(new Event('input', {bubbles: true}));
        }""")
        await page.wait_for_timeout(500)
        print('accent:', await page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--accent')"))
        await page.screenshot(path=OUT + '/t-accent-custom.png')

        # 10. persistence check
        await page.reload()
        await page.wait_for_timeout(1200)
        print('persisted accent:', await page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--accent')"))
        print('persisted rows:', await page.eval_on_selector_all('.server-city', 'els => els.map(e => e.textContent)'))
        await page.screenshot(path=OUT + '/t-reload.png')

        print('ERRORS:', errors[:10] if errors else 'none')
        await browser.close()

asyncio.run(main())
