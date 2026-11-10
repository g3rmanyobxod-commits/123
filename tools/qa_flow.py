"""Проверка: без демо-данных, добавление сервера, сортировка, лист настроек, подключение."""
import asyncio, json
from playwright.async_api import async_playwright

URL = 'file:///home/user/app/assets/vpn.html'
MOCK = """
  window.Native = {
    available: true,
    ping: function (json) {
      var rows = JSON.parse(json || '[]');
      setTimeout(function () { window.__onLatency(JSON.stringify(rows.map(function (r, i) { return { id: r.id, ms: 40 + (i * 43) % 200 }; }))); }, 150);
    },
    haptic: function () {}, copy: function () { return Promise.resolve(true); },
    setChrome: function () {}, readClipboard: function () { return Promise.resolve(null); },
    saveFile: function () { return Promise.resolve(true); }, pickFile: function () { return Promise.resolve(null); },
    share: function () { return Promise.resolve(true); },
    fetchText: function (k) { setTimeout(function () { window.__onFetch(k, false, ''); }, 40); },
    toast: function (t) { window.__toast = t; }, locate: function () { return ''; },
    connect: function (c, n) { window.__cfg = c; setTimeout(function () { window.__onVpnState(JSON.stringify({state:'connected',error:'',up:1024,down:2048,seconds:12})); }, 120); },
    disconnect: function () { window.__onVpnState(JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0})); },
    vpnState: function () { return JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0}); },
    measureDelay: function () { return Promise.resolve(40); }
  };
"""

LINKS = [
 "vless://11111111-2222-3333-4444-555555555555@fi1.example.com:443?security=tls&sni=fi1.example.com&type=ws&path=%2Fws#Хельсинки",
 "trojan://pass@nl1.example.com:443?sni=nl1.example.com#Амстердам",
 "vless://11111111-2222-3333-4444-555555555555@de1.example.com:443?security=tls#Берлин",
]

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
        await pg.wait_for_timeout(900)

        empty = await pg.evaluate("[...document.querySelectorAll('.group-card')].length")
        print('групп после старта (без демо):', empty)

        await pg.click(".dock-item[data-nav='servers']")
        await pg.wait_for_timeout(400)
        for link in LINKS:
            if await pg.evaluate("document.body.dataset.view") != 'servers':
                await pg.click(".dock-item[data-nav='servers']")
                await pg.wait_for_timeout(350)
            await pg.click('#open-add-server')
            await pg.wait_for_timeout(250)
            await pg.fill('#add-input', link)
            await pg.click('#add-submit')
            await pg.wait_for_timeout(450)
        await pg.click(".dock-item[data-nav='servers']")
        await pg.wait_for_timeout(500)
        rows = await pg.eval_on_selector_all('.server-row', "els => els.map(e => ({city: e.querySelector('.server-city').textContent, ping: e.querySelector('.server-ping').textContent, proto: e.querySelector('.server-proto').textContent}))")
        print('строки:', json.dumps(rows, ensure_ascii=False))

        # сортировка по имени / пингу
        await pg.click("#sort-bar button[data-sort='name']"); await pg.wait_for_timeout(300)
        by_name = await pg.eval_on_selector_all('.server-city', "els => els.map(e => e.textContent)")
        await pg.click("#sort-bar button[data-sort='delay']"); await pg.wait_for_timeout(300)
        by_ping = await pg.eval_on_selector_all('.server-city', "els => els.map(e => e.textContent)")
        print('имя:', by_name)
        print('пинг:', by_ping)

        await pg.screenshot(path='qa/q-list.png')

        # лист настроек — зажатие строки вместо «⋯»
        box = await pg.locator('.server-row').first.bounding_box()
        await pg.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
        await pg.mouse.down()
        await pg.wait_for_timeout(560)
        await pg.mouse.up()
        await pg.wait_for_timeout(400)
        print('лист открыт:', await pg.is_visible('#server-sheet'))
        await pg.screenshot(path='qa/q-sheet.png')
        await pg.fill('#sheet-name', 'Хельсинки 2')
        await pg.fill('#sheet-sni', 'www.microsoft.com')
        await pg.click('#sheet-insecure')
        await pg.click('#sheet-mux')
        await pg.click('#sheet-save')
        await pg.wait_for_timeout(500)
        saved = await pg.evaluate("JSON.parse(localStorage.getItem('vpn.servers'))[0]")
        print('сохранено:', json.dumps({k: saved.get(k) for k in ['city','host','port','sni','allowInsecure','mux']}, ensure_ascii=False))

        # подключение и конфиг с overrides
        await pg.click('.dock-item[data-nav="home"]'); await pg.wait_for_timeout(300)
        # слайдер: тянем ползунок вправо
        knob = await pg.query_selector('#slider-knob')
        box = await knob.bounding_box()
        sbox = await (await pg.query_selector('#connect-slider')).bounding_box()
        start = (box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
        await pg.mouse.move(*start)
        await pg.mouse.down()
        for step in range(1, 12):
            await pg.mouse.move(start[0] + (sbox['width'] - box['width'] - 10) * step / 11, start[1])
            await pg.wait_for_timeout(16)
        await pg.mouse.up()
        await pg.wait_for_timeout(900)
        cfg = await pg.evaluate("window.__cfg ? JSON.parse(window.__cfg) : null")
        proxy = [o for o in (cfg or {}).get('outbounds', []) if o.get('tag') == 'proxy']
        print('proxy:', json.dumps(proxy, ensure_ascii=False))
        print('статус:', await pg.text_content('#conn-status'))
        print('ERRORS:', errs[:5] if errs else 'none')
        await b.close()

asyncio.run(main())
