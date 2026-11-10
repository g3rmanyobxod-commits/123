"""Локация: часовой пояс → IP-геолокация → ближайший город и точка «вы» на глобусе."""
import asyncio
from playwright.async_api import async_playwright

URL = 'file:///home/user/app/assets/vpn.html'
MOCK = """
  window.Native = {
    available: true,
    ping: function (j) { setTimeout(function(){ window.__onLatency(j); },80); },
    locate: function (key) {
      setTimeout(function () {
        window.__onLocate(key, JSON.stringify({city:'Helsinki', country:'Finland', lat:60.19, lng:24.95}));
      }, 120);
    },
    vpnState: function(){ return JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0}); },
    measureDelay: function(){ return Promise.resolve(38); },
    haptic: function(){}, toast: function(){}, setChrome: function(){}
  };
"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 412, 'height': 892}, device_scale_factor=2,
                                  is_mobile=True, has_touch=True, timezone_id='Europe/Helsinki',
                                  locale='ru-RU')
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.add_init_script(MOCK)
        await pg.goto(URL); await pg.wait_for_timeout(1500)
        label = await pg.inner_text('#path-from')
        print('подпись города:', label)
        stored = await pg.evaluate("localStorage.getItem('vpn.origin')")
        print('localStorage vpn.origin:', stored)
        stats = await pg.evaluate("({cities: (window.GEO_CITIES||[]).length + (window.GEO_CITIES_EXTRA||[]).length, countries: Object.keys(window.GEO_COUNTRIES_EXTRA||{}).length})")
        print('справочник:', stats)
        await pg.screenshot(path='qa/l-home.png')
        print('ERRORS:', errs[:3] if errs else 'none')
        await b.close()

asyncio.run(main())
