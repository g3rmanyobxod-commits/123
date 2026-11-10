"""Быстрый визуальный прогон: главная, серверы, настройки (светлая/ночная)."""
import asyncio, sys
from playwright.async_api import async_playwright

URL = 'file:///home/user/app/assets/vpn.html'
MOCK = """
  window.Native = {
    available: true,
    ping: function (json) {
      var rows = JSON.parse(json || '[]');
      setTimeout(function () { window.__onLatency(JSON.stringify(rows.map(function (r, i) { return { id: r.id, ms: 32 + (i * 44) % 240 }; }))); }, 200);
    },
    haptic: function () {}, copy: function () { return Promise.resolve(true); },
    setChrome: function () {}, readClipboard: function () { return Promise.resolve(null); },
    saveFile: function () { return Promise.resolve(true); }, pickFile: function () { return Promise.resolve(null); },
    share: function () { return Promise.resolve(true); },
    fetchText: function (key) { setTimeout(function () { window.__onFetch(key, false, ''); }, 50); },
    toast: function () {}, locate: function () { return ''; },
    connect: function () { setTimeout(function () { window.__onVpnState(JSON.stringify({ state: 'connected', error: '', up: 1269760, down: 634388480, seconds: 5471 })); }, 200); },
    disconnect: function () { window.__onVpnState(JSON.stringify({ state: 'idle', error: '', up: 0, down: 0, seconds: 0 })); },
    vpnState: function () { return JSON.stringify({ state: 'idle', error: '', up: 0, down: 0, seconds: 0 }); },
    measureDelay: function () { return Promise.resolve(48); }
  };
"""

SEED = """
  localStorage.setItem('vpn.seeded', '1');
"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 412, 'height': 892}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('c:' + m.text) if m.type == 'error' else None)
        await pg.add_init_script(MOCK)
        await pg.goto(URL)
        await pg.wait_for_timeout(1200)
        for name, sel in [('q-home', None), ('q-servers', ".dock-item[data-nav='servers']"), ('q-settings', ".dock-item[data-nav='settings']")]:
            if sel:
                await pg.click(sel); await pg.wait_for_timeout(600)
            await pg.screenshot(path='qa/%s.png' % name)
        print('ERRORS:', errs[:6] if errs else 'none')
        await b.close()

asyncio.run(main())
