"""Скриншоты для README: главная, слайдер, серверы, группы, настройки, ночная тема."""
import asyncio, os
from playwright.async_api import async_playwright

URL = 'file:///home/user/app/assets/vpn.html'
OUT = '/home/user/release/screenshots'

MOCK = """
  window.Native = {
    available: true,
    locate: function (key) {
      setTimeout(function () {
        window.__onLocate(key, JSON.stringify({city:'Helsinki', country:'Finland', lat:60.19, lng:24.95}));
      }, 150);
    },
    ping: function (json) {
      var rows = [];
      try { rows = JSON.parse(json); } catch (e) { rows = []; }
      var out = rows.map(function (r, i) { return { id: r.id, ms: 34 + (i * 47) % 260 }; });
      setTimeout(function () { window.__onLatency(JSON.stringify(out)); }, 260);
    },
    haptic: function () {}, copy: function () { return Promise.resolve(true); },
    setChrome: function () {}, readClipboard: function () { return Promise.resolve(null); },
    saveFile: function () { return Promise.resolve(true); },
    pickFile: function () { return Promise.resolve(null); },
    share: function () { return Promise.resolve(true); },
    fetchText: function () { return Promise.reject(new Error('offline')); },
    toast: function () {},
    connect: function () {
      setTimeout(function () { window.__onVpnState(JSON.stringify({ state: 'connecting', error: '', up: 0, down: 0, seconds: 0 })); }, 40);
      setTimeout(function () { window.__onVpnState(JSON.stringify({ state: 'connected', error: '', up: 1269760, down: 634388480, seconds: 5471 })); }, 700);
    },
    disconnect: function () { window.__onVpnState(JSON.stringify({ state: 'idle', error: '', up: 0, down: 0, seconds: 0 })); },
    vpnState: function () { return JSON.stringify({ state: 'idle', error: '', up: 0, down: 0, seconds: 0 }); },
    measureDelay: function () { return Promise.resolve(48); }
  };
"""


LINKS = [('🇫🇮 Хельсинки', 'vless://11111111-1111-4111-8111-111111111111@fi1.globe.net:443?security=tls&sni=fi1.globe.net&type=ws&path=%2Fws#%F0%9F%87%AB%F0%9F%87%AE%20Хельсинки'), ('🇸🇪 Стокгольм', 'vless://11111111-1111-4111-8111-111111111111@se1.globe.net:443?security=tls&sni=se1.globe.net&type=tcp#%F0%9F%87%B8%F0%9F%87%AA%20Стокгольм'), ('🇳🇱 Амстердам', 'vless://11111111-1111-4111-8111-111111111111@nl1.globe.net:443?security=tls&sni=nl1.globe.net&type=ws&path=%2Fv2#%F0%9F%87%B3%F0%9F%87%B1%20Амстердам'), ('🇺🇸 Нью-Йорк', 'vless://11111111-1111-4111-8111-111111111111@us1.globe.net:443?security=tls&sni=us1.globe.net&type=grpc&serviceName=svc#%F0%9F%87%BA%F0%9F%87%B8%20Нью-Йорк'), ('🇯🇵 Токио', 'vless://11111111-1111-4111-8111-111111111111@jp1.globe.net:443?security=tls&sni=jp1.globe.net&type=tcp#%F0%9F%87%AF%F0%9F%87%B5%20Токио')]


async def seed_servers(page):
    """Добавляем серверы как пользователь — через форму, чтобы данные были каноническими."""
    for index, (label, link) in enumerate(LINKS):
        if index:
            if await page.evaluate("document.body.dataset.view") != 'servers':
                await page.click(".dock-item[data-nav='servers']")
                await page.wait_for_timeout(300)
            await page.click('#open-add-server' if index else '#empty-add-server')
        else:
            await page.click('#slider-knob')
        await page.wait_for_timeout(350)
        await page.fill('#add-input', link)
        await page.click('#add-submit')
        await page.wait_for_timeout(650)
    view = await page.evaluate("document.body.dataset.view")
    if view != 'home':
        await page.click(".dock-item[data-nav='home']")
        await page.wait_for_timeout(700)


SEED_USAGE = """
  (function () {
    const out = {};
    const today = new Date();
    for (let i = 1; i < 150; i += 1) {
      if (Math.random() < 0.42) continue;
      const d = new Date(today); d.setDate(d.getDate() - i);
      const key = d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
      out[key] = { sec: Math.round((0.2 + Math.random() * 5) * 3600), down: 1048576 * (5 + i), up: 307200 * (1 + i % 7), sessions: 1 + (i % 3) };
    }
    const t = new Date();
    const tk = t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0');
    out[tk] = { sec: 2 * 3600 + 900, down: 41943040, up: 524288, sessions: 2 };
    localStorage.setItem('vpn.usage', JSON.stringify(out));
  })();
"""


async def drag_slider(page, hold=False):
    box = await page.locator('#slider-knob').bounding_box()
    track = await page.locator('#connect-slider').bounding_box()
    y = box['y'] + box['height'] / 2
    await page.mouse.move(box['x'] + box['width'] / 2, y)
    await page.mouse.down()
    steps = 14 if not hold else 7
    total = track['width'] - box['width'] - 8
    for i in range(1, steps + 1):
        await page.mouse.move(box['x'] + box['width'] / 2 + total * i / 14, y)
        await page.wait_for_timeout(18)
    if not hold:
        await page.mouse.up()


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={'width': 412, 'height': 892},
                                        device_scale_factor=2, is_mobile=True, has_touch=True,
                                        timezone_id='Europe/Helsinki', locale='ru-RU')
        page = await ctx.new_page()
        errors = []
        page.on('pageerror', lambda e: errors.append('PAGEERROR: %s' % e))
        await page.add_init_script(MOCK)
        await page.add_init_script(SEED_USAGE)
        await page.goto(URL)
        await page.wait_for_timeout(1600)
        await seed_servers(page)
        await page.wait_for_timeout(1200)

        async def shot(name):
            await page.evaluate("(() => { const t = document.querySelector('#toast'); if (t) t.classList.remove('is-visible'); })()")
            await page.wait_for_timeout(120)
            await page.screenshot(path='%s/%s.png' % (OUT, name))
            print('  ✓', name)

        print('снимаем:')
        await shot('home-idle')
        await drag_slider(page, hold=True)
        await shot('home-drag')
        box = await page.locator('#slider-knob').bounding_box()
        track = await page.locator('#connect-slider').bounding_box()
        y = box['y'] + box['height'] / 2
        for i in range(8, 15):
            await page.mouse.move(box['x'] + box['width'] / 2 + (track['width'] - box['width'] - 8) * i / 14, y)
            await page.wait_for_timeout(18)
        await page.mouse.up()
        await page.wait_for_timeout(1600)
        await page.wait_for_timeout(1800)
        await shot('home-connected')

        await page.click(".dock-item[data-nav='servers']")
        await page.wait_for_timeout(900)
        # измеряем задержки у всех серверов — иначе в списке «— мс»
        await page.click('#ping-all')
        await page.wait_for_timeout(1400)
        await shot('servers')

        await page.click(".dock-item[data-nav='stats']")
        await page.wait_for_timeout(900)
        await shot('stats')
        await page.click(".dock-item[data-nav='servers']")
        await page.wait_for_timeout(500)

        # открыть лист настроек клиента — зажатием строки
        try:
            box = await page.locator('.server-row').first.bounding_box()
            await page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
            await page.mouse.down()
            await page.wait_for_timeout(560)
            await page.mouse.up()
            await page.wait_for_timeout(700)
            await shot('client-settings')
            await page.click('#sheet-close')
            await page.wait_for_timeout(600)
        except Exception as error:
            print('  ! лист настроек:', error)

        await page.click(".dock-item[data-nav='settings']")
        await page.wait_for_timeout(900)
        await shot('settings')
        await page.click("[data-theme-value='night']")
        await page.wait_for_timeout(800)
        await shot('settings-night')
        await page.click(".dock-item[data-nav='home']")
        await page.wait_for_timeout(1600)
        await shot('home-night')
        await page.click(".dock-item[data-nav='servers']")
        await page.wait_for_timeout(900)
        await shot('servers-night')
        await page.click('#open-add-server')
        await page.wait_for_timeout(700)
        await page.fill('#add-input', LINKS[2][1])
        await page.wait_for_timeout(300)
        await shot('add')

        await page.click(".back[data-nav='servers']")
        await page.wait_for_timeout(500)
        await page.click('#open-scan')
        await page.wait_for_timeout(900)
        await shot('scan')
        await page.click('#scan-manual')
        await page.wait_for_timeout(400)

        print('ERRORS:', errors[:8] if errors else 'none')
        await browser.close()

asyncio.run(main())
