"""Скриншоты экрана серверов с группами (как в Happ) и состояний подключения."""
import asyncio, json
from playwright.async_api import async_playwright

HTML = 'file:///home/user/app/assets/vpn.html'

SERVERS = [
    dict(id='s1', city='Хельсинки', country='Финляндия', code='FI', flag='🇫🇮', lat=60.17, lng=24.94, protocol='vless', host='fi.example.com', port=443, link='vless://a@fi.example.com:443#Helsinki', subId='sub1', subName='Happ Cloud'),
    dict(id='s2', city='Амстердам', country='Нидерланды', code='NL', flag='🇳🇱', lat=52.37, lng=4.9, protocol='trojan', host='nl.example.com', port=443, link='trojan://p@nl.example.com:443#Amsterdam', subId='sub1', subName='Happ Cloud'),
    dict(id='s3', city='Франкфурт', country='Германия', code='DE', flag='🇩🇪', lat=50.11, lng=8.68, protocol='vmess', host='de.example.com', port=443, link='vmess://eyJhZGQiOiJkZSJ9', subId='sub1', subName='Happ Cloud'),
    dict(id='s4', city='Токио', country='Япония', code='JP', flag='🇯🇵', lat=35.68, lng=139.69, protocol='shadowsocks', host='jp.example.com', port=8388, link='ss://YWVzLTI1Ni1nY206cA==@jp.example.com:8388#Tokyo', subId='sub2', subName='Резерв'),
    dict(id='s5', city='Сингапур', country='Сингапур', code='SG', flag='🇸🇬', lat=1.35, lng=103.82, protocol='vless', host='sg.example.com', port=443, link='vless://b@sg.example.com:443#Singapore', subId='sub2', subName='Резерв'),
    dict(id='s6', city='Лондон', country='Великобритания', code='GB', flag='🇬🇧', lat=51.5, lng=-0.12, protocol='trojan', host='uk.example.com', port=443, link='trojan://p@uk.example.com:443#London', subId='', subName=''),
]
SUBS = [
    dict(id='sub1', name='Happ Cloud', url='https://example.com/sub1', updatedAt=1770000000000),
    dict(id='sub2', name='Резерв', url='https://example.com/sub2', updatedAt=1770100000000),
]

INIT = """
  window.Native = {
    available: true,
    ping: function () { return Promise.resolve(38); },
    haptic: function () {}, copy: function () { return Promise.resolve(true); },
    setChrome: function () {}, readClipboard: function () { return Promise.resolve(null); },
    saveFile: function () { return Promise.resolve(true); }, pickFile: function () { return Promise.resolve(null); },
    share: function () { return Promise.resolve(true); }, fetchText: function () { return Promise.reject(new Error('x')); },
    toast: function () {},
    connect: function () { setTimeout(function () { window.__onVpnState(JSON.stringify({state:'connecting',error:'',up:0,down:0,seconds:0})); }, 30);
                         setTimeout(function () { window.__onVpnState(JSON.stringify({state:'connected',error:'',up:2411724,down:1073741824,seconds:3725})); }, 400); },
    disconnect: function () { window.__onVpnState(JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0})); },
    vpnState: function () { return JSON.stringify({state:'idle',error:'',up:0,down:0,seconds:0}); },
    measureDelay: function () { return Promise.resolve(38); }
  };
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={'width': 412, 'height': 892}, device_scale_factor=2)
        page = await ctx.new_page()
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append('console:' + m.text) if m.type == 'error' else None)
        await page.add_init_script(INIT)
        await page.add_init_script("""
          localStorage.setItem('vpn.servers', %s);
          localStorage.setItem('vpn.subscriptions', %s);
          localStorage.setItem('vpn.selected', '"s1"');
          localStorage.setItem('vpn.seeded', '1');
          localStorage.setItem('vpn.latency', %s);
        """ % (json.dumps(json.dumps(SERVERS)), json.dumps(json.dumps(SUBS)),
               json.dumps(json.dumps({'s1': {'ms': 42}, 's2': {'ms': 61}, 's3': {'ms': 88}, 's4': {'ms': 145}, 's5': {'ms': 210}}))))
        await page.goto(HTML)
        await page.wait_for_timeout(900)

        await page.click('.dock-item[data-nav="servers"]')
        await page.wait_for_timeout(500)
        await page.screenshot(path='qa/g-groups.png')

        # свернуть первую группу
        await page.click('.group-card[data-key="sub:sub1"] .group-toggle')
        await page.wait_for_timeout(400)
        await page.screenshot(path='qa/g-collapsed.png')

        await page.click('.group-card[data-key="sub:sub1"] .group-toggle')
        await page.wait_for_timeout(300)

        # домашний экран в состоянии connecting/connected
        await page.click('.dock-item[data-nav="home"]')
        await page.wait_for_timeout(300)
        await page.click('#connect')
        await page.wait_for_timeout(150)
        await page.screenshot(path='qa/g-connecting.png')
        await page.wait_for_timeout(900)
        await page.screenshot(path='qa/g-connected.png')

        status = await page.text_content('#conn-status')
        stats = await page.text_content('#conn-stats')
        print('status:', status, '| stats:', stats)
        print('ERRORS:', errors if errors else 'none')
        await browser.close()

asyncio.run(main())
