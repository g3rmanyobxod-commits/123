"""Слайдер: перетаскивание, подключение, превращение в кнопку отключения."""
import asyncio, json
from playwright.async_api import async_playwright

URL = 'file:///home/user/app/assets/vpn.html'
MOCK = """
  window.Native = {
    available: true,
    ping: function (json) { var r = JSON.parse(json||'[]'); setTimeout(function(){ window.__onLatency(JSON.stringify(r.map(function(x,i){return {id:x.id, ms:38+i*20};}))); },120); },
    haptic: function () { window.__haptic = (window.__haptic||0)+1; }, copy: function(){return Promise.resolve(true);},
    setChrome: function(){}, readClipboard: function(){return Promise.resolve(null);},
    saveFile: function(){return Promise.resolve(true);}, pickFile: function(){return Promise.resolve(null);},
    share: function(){return Promise.resolve(true);}, fetchText: function(k){setTimeout(function(){window.__onFetch(k,false,'');},30);},
    toast: function(t){ window.__toast=t; }, locate: function(){ return ''; },
    connect: function(c,n){ window.__cfg=c; window.__name=n; setTimeout(function(){ window.__onVpnState(JSON.stringify({state:'connected',error:'',up:2048,down:8192,seconds:9})); }, 400); },
    disconnect: function(){ window.__onVpnState(JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0})); },
    vpnState: function(){ return JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0}); },
    measureDelay: function(){ return Promise.resolve(38); }
  };
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
        await pg.goto(URL); await pg.wait_for_timeout(800)

        # добавить сервер
        await pg.click('#slider-knob'); await pg.wait_for_timeout(500)
        await pg.fill('#add-input', 'vless://11111111-2222-3333-4444-555555555555@fi1.example.com:443?security=tls&type=ws&path=%2Fws#Хельсинки')
        await pg.click('#add-submit'); await pg.wait_for_timeout(900)
        print('состояние слайдера:', await pg.get_attribute('#connect-slider', 'data-state'),
              '| подпись:', await pg.text_content('#slider-label'))
        await pg.screenshot(path='qa/s-idle.png')

        # тянем ползунок
        knob = await pg.query_selector('#slider-knob')
        box = await knob.bounding_box()
        slider_box = await pg.query_selector('#connect-slider')
        sbox = await slider_box.bounding_box()
        start = (box['x'] + box['width']/2, box['y'] + box['height']/2)
        await pg.mouse.move(*start)
        await pg.mouse.down()
        for step in range(1, 12):
            await pg.mouse.move(start[0] + (sbox['width'] - box['width'] - 10) * step / 11, start[1])
            await pg.wait_for_timeout(16)
        await pg.screenshot(path='qa/s-drag.png')
        await pg.mouse.up()
        await pg.wait_for_timeout(300)
        print('после драга:', await pg.get_attribute('#connect-slider', 'data-state'))
        await pg.wait_for_timeout(900)
        print('после подключения:', await pg.get_attribute('#connect-slider', 'data-state'),
              '| подпись:', await pg.text_content('#conn-status'), '| stats:', await pg.text_content('#conn-stats'))
        await pg.screenshot(path='qa/s-connected.png')

        # отключение тапом
        await pg.click('#slider-knob'); await pg.wait_for_timeout(700)
        print('после тапа:', await pg.get_attribute('#connect-slider', 'data-state'))
        print('ERRORS:', errs[:4] if errs else 'none')
        await b.close()

asyncio.run(main())
