"""Подписка: добавление по ссылке → группа с серверами → обновление и удаление."""
import asyncio, base64, json
from playwright.async_api import async_playwright

SUB = "\n".join([
    "vless://11111111-2222-3333-4444-555555555555@fi.example.com:443?security=tls&sni=fi.example.com&type=ws&path=%2Fws#%F0%9F%87%AB%F0%9F%87%AE Хельсинки",
    "trojan://pass@nl.example.com:443?sni=nl.example.com#%F0%9F%87%B3%F0%9F%87%B1 Амстердам",
    "ss://YWVzLTI1Ni1nY206cGFzcw==@jp.example.com:8388#%F0%9F%87%AF%F0%9F%87%B5 Токио",
])
B64 = base64.b64encode(SUB.encode()).decode()

MOCK = """
  window.__fetchCalls = 0;
  window.Native = {
    available: true,
    ping: function (json) {
      var rows = JSON.parse(json || '[]');
      setTimeout(function () {
        window.__onLatency(JSON.stringify(rows.map(function (r, i) { return { id: r.id, ms: 50 + i * 30 }; })));
      }, 120);
    },
    haptic: function () {}, copy: function () { return Promise.resolve(true); },
    setChrome: function () {}, readClipboard: function () { return Promise.resolve(null); },
    saveFile: function () { return Promise.resolve(true); }, pickFile: function () { return Promise.resolve(null); },
    share: function () { return Promise.resolve(true); },
    fetchText: function (key, url) {
      window.__fetchCalls += 1;
      setTimeout(function () { window.__onFetch(key, true, %s); }, 100);
    },
    toast: function (t) { window.__lastToast = t; },
    connect: function (c, n) { window.__cfg = c; window.__cfgName = n; window.__onVpnState(JSON.stringify({state:'connected',error:'',up:1024,down:2048,seconds:3})); },
    disconnect: function () { window.__onVpnState(JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0})); },
    vpnState: function () { return JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0}); },
    measureDelay: function () { return Promise.resolve(50); }
  };
""" % json.dumps(B64)


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 412, 'height': 892})
        errors = []
        pg.on('pageerror', lambda e: errors.append(str(e)))
        pg.on('console', lambda m: errors.append('console:' + m.text) if m.type == 'error' else None)
        await pg.add_init_script(MOCK)
        await pg.goto('file:///home/user/app/assets/vpn.html')
        await pg.wait_for_timeout(900)
        await pg.click('.dock-item[data-nav="servers"]')
        await pg.wait_for_timeout(400)
        await pg.click('#open-add-sub')
        await pg.wait_for_timeout(400)
        await pg.fill('#sub-url', 'https://example.com/sub.txt')
        await pg.fill('#sub-name', 'Happ Cloud')
        await pg.click('#sub-form button[type="submit"]')
        await pg.wait_for_timeout(1500)

        groups = await pg.eval_on_selector_all('.group-card', "els => els.map(e => ({key: e.dataset.key, name: e.querySelector('.group-name').textContent, meta: e.querySelector('.group-meta').textContent, rows: [...e.querySelectorAll('.server-city')].map(x => x.textContent)}))")
        print('groups:', json.dumps(groups, ensure_ascii=False))

        # выбрать сервер из подписки и подключиться
        await pg.click('.group-card[data-key^="sub:"] .server-row')
        await pg.wait_for_timeout(400)
        await pg.click('#connect')
        await pg.wait_for_timeout(500)
        cfg = await pg.evaluate("window.__cfg ? JSON.parse(window.__cfg) : null")
        print('connect name:', await pg.evaluate("window.__cfgName"))
        print('proxy outbound:', json.dumps([o for o in (cfg or {}).get('outbounds', []) if o.get('tag') == 'proxy'], ensure_ascii=False))
        print('status:', await pg.text_content('#conn-status'))

        # обновление подписки кнопкой ⟳
        await pg.click('.dock-item[data-nav="servers"]')
        await pg.wait_for_timeout(300)
        before = await pg.evaluate("window.__fetchCalls")
        await pg.click('.group-card[data-key^="sub:"] .group-action')
        await pg.wait_for_timeout(1200)
        after = await pg.evaluate("window.__fetchCalls")
        print('refresh fetched:', before, '->', after)

        # удаление подписки
        await pg.click('.group-card[data-key^="sub:"] .group-action.is-danger')
        await pg.wait_for_timeout(600)
        left = await pg.eval_on_selector_all('.group-card', "els => els.length")
        toast = await pg.evaluate("window.__lastToast || ''")
        print('groups after delete:', left, '| toast:', toast)
        print('ERRORS:', errors if errors else 'none')
        await b.close()

asyncio.run(main())
