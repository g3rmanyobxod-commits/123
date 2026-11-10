"""Быстрый снимок глобуса с линией маршрута (для подбора глоу)."""
import asyncio, sys
from playwright.async_api import async_playwright

MOCK = """
  window.Native = { available:true, locate:function(){}, ping:function(){}, haptic:function(){},
    vpnState:function(){return JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0});},
    measureDelay:function(){return Promise.resolve(40);} };
"""
LINKS = [
 "vless://11111111-1111-4111-8111-111111111111@fi.globe.net:443?security=tls&sni=fi.globe.net&type=ws&path=%2Fws#%F0%9F%87%AB%F0%9F%87%AE%20Хельсинки",
 "vless://11111111-1111-4111-8111-111111111111@jp.globe.net:443?security=tls&sni=jp.globe.net&type=tcp#%F0%9F%87%AF%F0%9F%87%B5%20Токио",
]

async def main():
    out = sys.argv[1] if len(sys.argv) > 1 else 'qa/arc.png'
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width':412,'height':892}, device_scale_factor=2, is_mobile=True, has_touch=True, locale='ru-RU')
        pg = await ctx.new_page()
        await pg.add_init_script(MOCK)
        await pg.goto('file:///home/user/app/assets/vpn.html'); await pg.wait_for_timeout(1200)
        for i, link in enumerate(LINKS):
            await pg.click(".dock-item[data-nav='servers']"); await pg.wait_for_timeout(300)
            await pg.click('#open-add-server')
            await pg.wait_for_timeout(350)
            await pg.fill('#add-input', link)
            await pg.wait_for_timeout(250)
            await pg.click('#add-form button[type="submit"]')
            await pg.wait_for_timeout(600)
        await pg.click(".dock-item[data-nav='servers']"); await pg.wait_for_timeout(400)
        await pg.locator('.server-item').nth(1).click(); await pg.wait_for_timeout(300)
        await pg.click(".dock-item[data-nav='home']"); await pg.wait_for_timeout(2200)
        await pg.screenshot(path=out)
        print('снято:', out)
        await b.close()
asyncio.run(main())
