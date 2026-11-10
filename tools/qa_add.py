"""Общий экран добавления: автоопределение сервер/подписка + QR-вход."""
import asyncio
from playwright.async_api import async_playwright

MOCK = """
  window.Native = { available:true, locate:function(){}, ping:function(){}, haptic:function(){},
    vpnState:function(){return JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0});},
    measureDelay:function(){return Promise.resolve(40);},
    fetchText:function(key,url){ setTimeout(function(){ window.__onFetch(key, true, 'vless://11111111-1111-4111-8111-111111111111@sub1.example.com:443?security=tls#%F0%9F%87%A9%F0%9F%87%AA%20Берлин\\nvless://11111111-1111-4111-8111-111111111111@sub2.example.com:443?security=tls#%F0%9F%87%AB%F0%9F%87%B7%20Париж'); }, 60); },
    toast:function(){} };
"""
VLESS = 'vless://11111111-1111-4111-8111-111111111111@fi1.example.com:443?security=tls&type=ws&path=%2Fws#%F0%9F%87%AB%F0%9F%87%AE%20Хельсинки'

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width':412,'height':892}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg = await ctx.new_page()
        errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.add_init_script(MOCK)
        await pg.goto('file:///home/user/app/assets/vpn.html'); await pg.wait_for_timeout(1200)

        await pg.click(".dock-item[data-nav='servers']"); await pg.wait_for_timeout(500)
        print('кнопки в шапке:', await pg.evaluate("Array.from(document.querySelectorAll('.head-actions > *')).map(function(b){return b.id})"))
        await pg.click('#open-add-server'); await pg.wait_for_timeout(400)
        print('экран:', await pg.evaluate("document.body.dataset.view"), '| заголовок:', await pg.text_content('#add-title'))

        await pg.fill('#add-input', VLESS); await pg.wait_for_timeout(250)
        print('чип сервера:', await pg.text_content('#add-kind'), '| кнопка:', await pg.text_content('#add-submit'),
              '| превью:', await pg.get_attribute('#add-preview','hidden'))
        await pg.click('#add-submit'); await pg.wait_for_timeout(900)
        print('после сервера: view =', await pg.evaluate("document.body.dataset.view"),
              '| серверов:', await pg.evaluate("JSON.parse(localStorage.getItem('vpn.servers')||'[]').length"))

        await pg.click(".dock-item[data-nav='servers']"); await pg.wait_for_timeout(400)
        await pg.click('#open-add-server'); await pg.wait_for_timeout(350)
        await pg.fill('#add-input', 'https://panel.example.com/api/sub/abc'); await pg.wait_for_timeout(250)
        print('чип подписки:', await pg.text_content('#add-kind'), '| кнопка:', await pg.text_content('#add-submit'))
        await pg.fill('#add-name', 'Моя подписка')
        await pg.click('#add-submit'); await pg.wait_for_timeout(1600)
        print('подписок:', await pg.evaluate("JSON.parse(localStorage.getItem('vpn.subscriptions')||'[]').length"),
              '| серверов:', await pg.evaluate("JSON.parse(localStorage.getItem('vpn.servers')||'[]').length"))

        await pg.click('#open-scan'); await pg.wait_for_timeout(700)
        print('сканер: view =', await pg.evaluate("document.body.dataset.view"), '| заметка:', await pg.text_content('#scan-note'))
        await pg.click('#scan-manual'); await pg.wait_for_timeout(400)
        print('вручную: view =', await pg.evaluate("document.body.dataset.view"))
        print('ERRORS:', errs[:4] if errs else 'none')
        await b.close()
asyncio.run(main())
