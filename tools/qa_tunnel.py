"""Проверка генерации Xray-конфига и моста подключения через mock Native."""
import asyncio, json, base64, sys
from playwright.async_api import async_playwright

HTML = 'file:///home/user/app/assets/vpn.html'

def b64(s):
    return base64.b64encode(s.encode()).decode().rstrip('=')

VMESS = 'vmess://' + b64(json.dumps({
    "v": "2", "ps": "Frankfurt", "add": "de1.example.com", "port": "443",
    "id": "b831381d-6324-4d53-ad4f-8cda48b30811", "aid": "0", "scy": "auto",
    "net": "ws", "type": "none", "host": "cdn.example.com", "path": "/ray", "tls": "tls",
    "sni": "cdn.example.com", "alpn": "h2,http/1.1"
}))

CASES = [
    ("vless+reality+grpc", "vless://b831381d-6324-4d53-ad4f-8cda48b30811@fi1.example.com:443?encryption=none&security=reality&sni=www.microsoft.com&fp=chrome&pbk=WAm6ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefg&sid=ab12&type=grpc&serviceName=grpcsvc&mode=gun#Helsinki"),
    ("vless+tls+ws", "vless://b831381d-6324-4d53-ad4f-8cda48b30811@nl1.example.com:443?encryption=none&security=tls&sni=nl1.example.com&type=ws&host=nl1.example.com&path=%2Fws%3Fed%3D2048#Amsterdam"),
    ("trojan+tls", "trojan://secretpass@sg1.example.com:443?sni=sg1.example.com&type=tcp&headerType=none#Singapore"),
    ("vmess+ws", VMESS),
    ("shadowsocks", "ss://" + b64("aes-256-gcm:secretpass") + "@jp1.example.com:8388#Tokyo"),
    ("hysteria2", "hysteria2://pass@se1.example.com:443?sni=se1.example.com#Stockholm"),
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 412, 'height': 892})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append('console:' + m.text) if m.type == 'error' else None)
        await page.add_init_script("""
          window.__captured = [];
          window.__vpn = { state: 'idle', error: '', up: 0, down: 0, seconds: 0, name: '' };
          window.Native = {
            available: true,
            ping: function (url) { return Promise.resolve(-1); },
            haptic: function () {},
            copy: function (t) { return Promise.resolve(true); },
            setChrome: function () {},
            readClipboard: function () { return Promise.resolve(null); },
            saveFile: function () { return Promise.resolve(true); },
            pickFile: function () { return Promise.resolve(null); },
            share: function () { return Promise.resolve(true); },
            fetchText: function () { return Promise.reject(new Error('no')); },
            toast: function () {},
            connect: function (config, name) {
              var parsed = null, err = null;
              try { parsed = JSON.parse(config); } catch (e) { err = String(e); }
              window.__captured.push({ raw: config, config: parsed, name: name, error: err });
              window.__vpn.state = 'connected';
              setTimeout(function () {
                window.__onVpnState(JSON.stringify({ state: 'connected', error: '', name: name, up: 2048, down: 3145728, seconds: 75 }));
              }, 120);
            },
            disconnect: function () {
              window.__captured.push({ disconnect: true });
              window.__vpn.state = 'idle';
              window.__onVpnState(JSON.stringify({ state: 'idle', error: '', up: 0, down: 0, seconds: 0 }));
            },
            vpnState: function () { return JSON.stringify(window.__vpn); },
            measureDelay: function () { return Promise.resolve(42); }
          };
        """)
        await page.goto(HTML)
        await page.wait_for_timeout(700)

        results = []
        for label, link in CASES:
            await page.evaluate("""(link) => {
              document.querySelector('.dock-item[data-nav="servers"]').click();
            }""", link)
            await page.wait_for_timeout(150)
            await page.click('#open-add-server')
            await page.wait_for_timeout(200)
            await page.fill('#server-link', link)
            await page.click('#server-form button[type="submit"]')
            await page.wait_for_timeout(350)
            await page.click('.dock-item[data-nav="home"]')
            await page.wait_for_timeout(200)
            st = await page.evaluate("window.__vpn.state")
            if st == 'connected':
                await page.click('#connect')
                await page.wait_for_timeout(250)
                await page.evaluate("window.__vpn.state = 'idle'")
            await page.evaluate("window.__captured.length = 0")
            await page.click('#connect')
            await page.wait_for_timeout(500)
            captured = await page.evaluate("window.__captured.slice()")
            last = captured[-1] if captured else {}
            results.append((label, last))

        # состояние UI после ошибки/успеха
        state_text = await page.text_content('#conn-status')
        stats = await page.text_content('#conn-stats')
        stats_hidden = await page.get_attribute('#conn-stats', 'hidden')
        cls = await page.get_attribute('#connect', 'class')

        for label, last in results:
            cfg = last.get('config') or {}
            out = [o for o in cfg.get('outbounds', []) if o.get('tag') == 'proxy']
            print('── %-20s name=%-14s err=%s' % (label, last.get('name'), last.get('error')))
            if out:
                o = out[0]
                print('   protocol=%s keys=%s' % (o.get('protocol'), sorted(o.keys())))
                print('   settings=%s' % json.dumps(o.get('settings'), ensure_ascii=False))
                print('   stream=%s' % json.dumps(o.get('streamSettings'), ensure_ascii=False))
            elif last.get('config'):
                print('   proxy outbound отсутствует')
            if cfg:
                print('   inbound=%s routing=%s dns=%s stats=%s' % (
                    json.dumps(cfg.get('inbounds'), ensure_ascii=False)[:120],
                    json.dumps(cfg.get('routing'), ensure_ascii=False)[:110],
                    json.dumps(cfg.get('dns'), ensure_ascii=False),
                    json.dumps(cfg.get('stats'), ensure_ascii=False)))
            print()
        print('status:', state_text, '| stats:', stats, '| hidden:', stats_hidden)
        print('connect class:', cls)
        print('ERRORS:', errors if errors else 'none')
        await browser.close()

asyncio.run(main())
