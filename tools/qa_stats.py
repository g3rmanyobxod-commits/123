"""Статистика: трекинг времени, календарь по яркости, сброс."""
import asyncio
from playwright.async_api import async_playwright

MOCK = """
  window.Native = { available:true, locate:function(){}, ping:function(){}, haptic:function(){},
    toast:function(){}, measureDelay:function(){return Promise.resolve(38);},
    connect:function(){ setTimeout(function(){ window.__onVpnState(JSON.stringify({state:'connected',error:'',up:4096,down:81920,seconds:12})); }, 120); },
    disconnect:function(){ window.__onVpnState(JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0})); },
    vpnState:function(){ return JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0}); } };
"""
SEED_USAGE = """
  (function () {
    const out = {};
    const today = new Date();
    for (let i = 0; i < 120; i += 1) {
      if (Math.random() < 0.45) continue;
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const key = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
      out[key] = { sec: Math.round(Math.random() * 5 * 3600), down: 1024 * 1024 * (5 + i), up: 1024 * 300 * (1 + i % 7), sessions: 1 + (i % 3) };
    }
    const t = new Date();
    const tk = t.getFullYear() + '-' + String(t.getMonth() + 1).padStart(2, '0') + '-' + String(t.getDate()).padStart(2, '0');
    out[tk] = { sec: 2 * 3600 + 900, down: 1024 * 1024 * 40, up: 1024 * 512, sessions: 2 };
    localStorage.setItem('vpn.usage', JSON.stringify(out));
  })();
"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width':412,'height':892}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg = await ctx.new_page()
        errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.add_init_script(MOCK)
        await pg.add_init_script(SEED_USAGE)
        await pg.goto('file:///home/user/app/assets/vpn.html'); await pg.wait_for_timeout(1000)
        await pg.click(".dock-item[data-nav='stats']"); await pg.wait_for_timeout(700)
        print('вкладка:', await pg.evaluate("document.body.dataset.view"))
        cells = await pg.evaluate("document.querySelectorAll('#heat i').length")
        print('квадратов в календаре:', cells)
        print('месяц:', await pg.text_content('#stats-total'), '|', await pg.text_content('#stats-total-sub'))
        print('сегодня:', await pg.text_content('#stat-today'), '| неделя:', await pg.text_content('#stat-week'),
              '| серия:', await pg.text_content('#stat-streak'))
        print('трафик:', await pg.text_content('#stat-down'), await pg.text_content('#stat-up'),
              '| сессий:', await pg.text_content('#stat-sessions'))
        levels = await pg.evaluate("Array.from(document.querySelectorAll('#heat i')).map(function(c){return c.style.background}).filter(Boolean).slice(0,6)")
        print('примеры цветов:', levels)
        await pg.screenshot(path='qa/stats.png')
        # трекинг: подключаемся и ждём роста секунд
        await pg.click(".dock-item[data-nav='home']"); await pg.wait_for_timeout(400)
        before = await pg.evaluate("JSON.parse(localStorage.getItem('vpn.usage')||'{}')[Object.keys(JSON.parse(localStorage.getItem('vpn.usage')||'{}')).sort().pop()].sec")
        await pg.evaluate("window.__onVpnState(JSON.stringify({state:'connected',error:'',up:4096,down:81920,seconds:12}))")
        for i in range(6):
            await pg.wait_for_timeout(1000)
            await pg.evaluate("window.__onVpnState(JSON.stringify({state:'connected',error:'',up:4096,down:81920,seconds:%d}))" % (12+i))
        await pg.wait_for_timeout(500)
        after = await pg.evaluate("JSON.parse(localStorage.getItem('vpn.usage')||'{}')[Object.keys(JSON.parse(localStorage.getItem('vpn.usage')||'{}')).sort().pop()].sec")
        print('секунды выросли:', round(before), '→', round(after))
        print('ERRORS:', errs[:3] if errs else 'none')
        await b.close()
asyncio.run(main())
