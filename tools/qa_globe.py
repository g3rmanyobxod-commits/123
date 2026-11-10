"""Глобус: глоу у линии, подписи во время вращения, тап по точке = подключение."""
import asyncio
from playwright.async_api import async_playwright

URL = 'file:///home/user/app/assets/vpn.html'
MOCK = """
  window.Native = {
    available: true,
    ping: function (json) { var r = JSON.parse(json||'[]'); setTimeout(function(){ window.__onLatency(JSON.stringify(r.map(function(x,i){return {id:x.id, ms:36+i*18};}))); },100); },
    haptic: function(){}, copy: function(){return Promise.resolve(true);}, setChrome: function(){},
    readClipboard: function(){return Promise.resolve(null);}, saveFile: function(){return Promise.resolve(true);},
    pickFile: function(){return Promise.resolve(null);}, share: function(){return Promise.resolve(true);},
    fetchText: function(k){setTimeout(function(){window.__onFetch(k,false,'');},30);}, toast: function(t){window.__toast=t;},
    locate: function(){ return ''; },
    connect: function(c,n){ window.__cfg=c; window.__name=n; setTimeout(function(){window.__onVpnState(JSON.stringify({state:'connected',error:'',up:1,down:2,seconds:3}));},200); },
    disconnect: function(){ window.__onVpnState(JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0})); },
    vpnState: function(){ return JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0}); },
    measureDelay: function(){ return Promise.resolve(36); }
  };
"""
LINKS = [
 "vless://11111111-2222-3333-4444-555555555555@fi1.example.com:443?security=tls#%F0%9F%87%AB%F0%9F%87%AE Хельсинки",
 "vless://11111111-2222-3333-4444-555555555555@us1.example.com:443?security=tls#%F0%9F%87%BA%F0%9F%87%B8 New York",
 "trojan://p@sg1.example.com:443#%F0%9F%87%B8%F0%9F%87%AC Singapore",
]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 412, 'height': 892}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.add_init_script(MOCK)
        await pg.goto(URL); await pg.wait_for_timeout(700)
        for link in LINKS:
            await pg.evaluate("""(link) => {
              const ev = new CustomEvent('x');
              document.querySelector('.dock-item[data-nav="servers"]').click();
            }""", link)
            await pg.wait_for_timeout(300)
            await pg.click('#open-add-server'); await pg.wait_for_timeout(200)
            await pg.fill('#add-input', link)
            await pg.click('#add-submit'); await pg.wait_for_timeout(500)
        await pg.click('.dock-item[data-nav="home"]'); await pg.wait_for_timeout(900)

        # выбираем сервер, чтобы появилась дуга
        markers = await pg.query_selector_all('.srv')
        print('маркеров:', len(markers))
        await markers[0].click(); await pg.wait_for_timeout(1400)
        await pg.screenshot(path='qa/g-glow.png')
        print('после тапа по точке: слайдер', await pg.get_attribute('#connect-slider','data-state'),
              '| cfg?', bool(await pg.evaluate("window.__cfg||null")))

        # вращение: подпись должна скрыться
        await pg.evaluate("window.__onVpnState(JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0}))")
        await pg.wait_for_timeout(600)
        box = await pg.evaluate("() => { const c = document.querySelector('#globe').getBoundingClientRect(); return {x:c.x+c.width/2, y:c.y+c.height/2}; }")
        await pg.mouse.move(box['x'], box['y'])
        await pg.mouse.down()
        for i in range(1, 14):
            await pg.mouse.move(box['x'] + i * 14, box['y'])
            await pg.wait_for_timeout(16)
        spinning = await pg.evaluate("document.querySelector('#markers').classList.contains('is-spinning')")
        label_op = await pg.evaluate("(() => { const l = document.querySelector('.srv.is-selected .srv-label'); return l ? getComputedStyle(l).opacity : 'none'; })()")
        await pg.mouse.up()
        print('во время вращения: is-spinning =', spinning, ', подпись opacity =', label_op)
        await pg.wait_for_timeout(1200)
        label_after = await pg.evaluate("(() => { const l = document.querySelector('.srv.is-selected .srv-label'); return l ? getComputedStyle(l).opacity : 'none'; })()")
        print('после остановки: opacity =', label_after)
        print('ERRORS:', errs[:4] if errs else 'none')
        await b.close()

asyncio.run(main())
