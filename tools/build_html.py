#!/usr/bin/env python3
# ВНИМАНИЕ: с v4 источником истины стал app/assets/vpn.html (правится напрямую).
# Этот патчер перезаписывает app/assets/vpn.html из source/vpn.html и откатит правки v4.
# Не запускать без резервной копии.
"""Full patcher: builds app/assets/vpn.html from source/vpn.html with all UI/UX changes."""
import sys

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SRC = 'source/vpn.html'
DST = 'app/assets/vpn.html'
s = open(SRC, encoding='utf-8').read()
done = []


def rep(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# ═══════════════ CSS ═════════════════════════════════════════════════════════
rep("""button, input, textarea { font: inherit; color: inherit; }
button { cursor: pointer; appearance: none; -webkit-appearance: none; }""",
    """button, input, textarea { font: inherit; color: inherit; }
button { cursor: pointer; appearance: none; -webkit-appearance: none; }
button, .srv { -webkit-tap-highlight-color: transparent; -webkit-user-select: none; user-select: none; }
input, textarea { -webkit-user-select: text; user-select: text; }""",
    'css-tap')

rep(""".srv {
  position: absolute;
  left: 0;
  top: 0;
  width: 26px;
  height: 26px;
  padding: 0;
  border: 0;
  background: none;
  pointer-events: auto;
  cursor: pointer;
}

.srv-dot {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 5px;
  height: 5px;
  margin: -2.5px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 0 3px var(--paper);
  transition: width .18s ease, height .18s ease, margin .18s ease;
}

.srv:hover .srv-dot,
.srv:focus-visible .srv-dot {
  width: 7px;
  height: 7px;
  margin: -3.5px;
}

.srv.is-selected .srv-dot {
  width: 9px;
  height: 9px;
  margin: -4.5px;
  box-shadow: 0 0 0 3px var(--paper), 0 0 0 4px var(--accent);
}

.srv.is-selected::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 9px;
  height: 9px;
  border: 1px solid var(--accent);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: ping 2.8s ease-out infinite;
}""",
    """.srv {
  --flag-size: calc(30px * var(--flag-scale, 1));
  position: absolute;
  left: 0;
  top: 0;
  width: 52px;
  height: 52px;
  padding: 0;
  border: 0;
  background: none;
  pointer-events: auto;
  cursor: pointer;
  z-index: 2;
}

.srv.is-selected { z-index: 6; }

.srv-flag {
  position: absolute;
  left: 50%;
  top: 50%;
  display: grid;
  place-items: center;
  width: var(--flag-size);
  height: var(--flag-size);
  overflow: hidden;
  border-radius: 50%;
  background: var(--paper);
  box-shadow: 0 0 0 1px var(--line-strong), 0 6px 16px var(--shadow);
  font-size: calc(var(--flag-size) * .58);
  line-height: 1;
  letter-spacing: 0;
  transform: translate(-50%, -50%) scale(calc(.76 + .24 * var(--depth, 1)));
  opacity: calc(.52 + .48 * var(--depth, 1));
  transition: transform .2s ease, box-shadow .2s ease, opacity .2s ease;
  will-change: transform;
}

.srv-flag.is-unknown {
  font-family: var(--mono);
  font-size: calc(var(--flag-size) * .34);
  font-weight: 500;
  letter-spacing: .02em;
  color: var(--muted);
}

.srv-label {
  position: absolute;
  left: 50%;
  top: calc(50% + var(--flag-size) / 2 + 5px);
  padding: 3px 7px;
  border: 1px solid var(--dock-line);
  border-radius: 999px;
  background: var(--paper);
  box-shadow: 0 6px 16px var(--shadow);
  color: var(--ink);
  font-family: var(--mono);
  font-size: 8.5px;
  letter-spacing: .02em;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transform: translate(-50%, -3px);
  transition: opacity .16s ease, transform .16s ease, visibility 0s linear .16s;
  pointer-events: none;
}

.srv:hover .srv-flag,
.srv:focus-visible .srv-flag {
  opacity: 1;
  transform: translate(-50%, -50%) scale(calc(.88 + .12 * var(--depth, 1)));
  box-shadow: 0 0 0 1px var(--ink), 0 10px 22px var(--shadow);
}

.srv.is-selected .srv-flag {
  opacity: 1;
  transform: translate(-50%, -50%) scale(calc(.9 + .1 * var(--depth, 1)));
  box-shadow: 0 0 0 2px var(--accent), 0 10px 24px var(--shadow);
}

.srv:hover .srv-label,
.srv:focus-visible .srv-label,
.srv.is-selected .srv-label,
body[data-labels="true"] .srv-label {
  opacity: 1;
  visibility: visible;
  transform: translate(-50%, 0);
  transition: opacity .16s ease, transform .16s ease, visibility 0s;
}

.srv.is-selected::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: var(--flag-size);
  height: var(--flag-size);
  border: 1px solid var(--accent);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: ping 2.8s ease-out infinite;
  pointer-events: none;
}""",
    'css-markers')

rep(""".path-to { color: var(--ink); white-space: nowrap; }""",
    """.path-to {
  color: var(--ink);
  max-width: 42vw;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}""",
    'css-path')

rep(""".server-proto {
  font-family: var(--mono);
  font-size: 8.5px;
  letter-spacing: .03em;
  color: var(--muted);
  text-align: right;
  white-space: nowrap;
}""",
    """.server-proto {
  font-family: var(--mono);
  font-size: 8.5px;
  letter-spacing: .03em;
  color: var(--muted);
  text-align: right;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}""",
    'css-proto')

rep(""".reset:hover {
  color: var(--accent);
  border-color: var(--accent);
}

/* ── Тост ──────────────────────────────────────────────── */""",
    """.reset:hover {
  color: var(--accent);
  border-color: var(--accent);
}

/* ── Акцентный цвет ────────────────────────────────────── */

.swatches {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding-top: 2px;
}

.swatch {
  position: relative;
  width: 30px;
  height: 30px;
  flex: 0 0 auto;
  padding: 0;
  border: 1px solid var(--line-strong);
  border-radius: 50%;
  background: var(--swatch, var(--accent));
  box-shadow: inset 0 0 0 3px var(--paper);
  transition: transform .16s ease, box-shadow .16s ease;
}

.swatch:hover { transform: translateY(-1px); }

.swatch[aria-pressed="true"] {
  box-shadow: inset 0 0 0 4px var(--paper), 0 0 0 1px var(--ink);
}

.swatch-custom {
  display: grid;
  place-items: center;
  overflow: hidden;
  border-color: var(--ink);
  background: conic-gradient(from 210deg, #d9584d, #dda63c, #6fae6d, #4f8ecb, #8a6cc0, #d065a4, #d9584d);
}

.swatch-custom input[type="color"] {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  padding: 0;
  border: 0;
  opacity: 0;
  cursor: pointer;
}

.swatch-custom span {
  position: relative;
  font-family: var(--mono);
  font-size: 15px;
  line-height: 1;
  color: #fff;
  text-shadow: 0 1px 3px rgba(0, 0, 0, .5);
  pointer-events: none;
}

.accent-value {
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: .04em;
  text-transform: uppercase;
  color: var(--muted);
}

/* ── Инструменты списка ────────────────────────────────── */

.list-tools {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-top: 16px;
}

.search {
  flex: 1 1 auto;
  min-width: 0;
  height: 36px;
  padding: 0 12px;
  border: 1px solid var(--line-strong);
  border-radius: 0;
  background: transparent;
  font-size: 12px;
  color: var(--ink);
  -webkit-appearance: none;
  appearance: none;
}

.search::placeholder { color: var(--muted); }
.search:focus { outline: none; border-color: var(--accent); }

.ping-all { white-space: nowrap; }

.data-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}

.server-ping {
  font-variant-numeric: tabular-nums;
  letter-spacing: .02em;
}

.server-ping.is-fast { color: var(--accent); }
.server-ping.is-slow { color: var(--danger); }

.server-empty-result {
  margin-top: 18px;
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: .03em;
  color: var(--muted);
}

/* ── Мягкие формы и компактные списки ──────────────────── */

html[data-soft="true"] .primary,
html[data-soft="true"] .toast,
html[data-soft="true"] .segmented,
html[data-soft="true"] .search,
html[data-soft="true"] .preview { border-radius: 12px; }

html[data-soft="true"] .field input,
html[data-soft="true"] .field textarea {
  padding-left: 12px;
  padding-right: 12px;
  border: 1px solid var(--line-strong);
  border-radius: 12px;
}

html[data-soft="true"] .segmented { overflow: hidden; }
html[data-soft="true"] .switch { border-radius: 999px; }
html[data-soft="true"] .switch span { border-radius: 50%; }
html[data-soft="true"] .server-row.is-selected { border-radius: 10px; }
html[data-soft="true"] .sub-refresh,
html[data-soft="true"] .text-action,
html[data-soft="true"] .ghost,
html[data-soft="true"] .reset { border-radius: 8px; padding-left: 6px; padding-right: 6px; }

body[data-compact="true"] .server-row { padding: 9px 0; }
body[data-compact="true"] .sub-row { padding: 10px 0; }
body[data-compact="true"] .server-city { font-size: 13px; }
body[data-compact="true"] .server-flag { font-size: 16px; }
body[data-compact="true"] .screen h1 { font-size: 26px; }
body[data-compact="true"] .group { padding: 14px 0; }
body[data-compact="true"] .row { padding: 10px 0; }

/* ── Тост ──────────────────────────────────────────────── */""",
    'css-accent-tools')

rep("""  .srv {
    width: 34px;
    height: 34px;
  }""",
    """  .srv {
    --flag-size: calc(28px * var(--flag-scale, 1));
    width: 48px;
    height: 48px;
  }

  .srv-label { font-size: 8px; }""",
    'css-mobile-marker')

# ═══════════════ HTML ════════════════════════════════════════════════════════
rep("""      <div class="server-list" id="server-list"></div>

      <section class="subs-block" aria-labelledby="subs-title">""",
    """      <div class="list-tools" id="server-tools">
        <input class="search" id="server-search" type="search" autocomplete="off" spellcheck="false" placeholder="Поиск: город, страна, протокол" aria-label="Поиск серверов">
        <button class="ghost ping-all" type="button" id="ping-all">Задержка</button>
      </div>

      <div class="server-list" id="server-list"></div>
      <p class="server-empty-result" id="server-no-match" hidden>Ничего не найдено.</p>

      <section class="subs-block" aria-labelledby="subs-title">""",
    'html-tools')

rep("""        <div class="row">
          <div class="row-copy">
            <p class="row-label">Уменьшить движение</p>
            <p class="row-note">Отключает вращение, анимацию дуги и пульсацию.</p>
          </div>
          <button class="switch" type="button" role="switch" aria-checked="false" aria-label="Уменьшить движение" data-setting="reduced"><span></span></button>
        </div>
      </section>""",
    """        <div class="row row-stack">
          <div class="row-copy">
            <p class="row-label">Акцентный цвет</p>
            <p class="row-note">Кнопка подключения, маршрут на карте и выделение.</p>
          </div>
          <div class="swatches" role="group" aria-label="Акцентный цвет"></div>
          <p class="accent-value" id="accent-value">Изумруд · #1D5A45</p>
        </div>
        <div class="row">
          <div class="row-copy">
            <p class="row-label">Мягкие формы</p>
            <p class="row-note">Скруглённые кнопки, поля и переключатели.</p>
          </div>
          <button class="switch" type="button" role="switch" aria-checked="false" aria-label="Мягкие формы" data-setting="soft"><span></span></button>
        </div>
        <div class="row">
          <div class="row-copy">
            <p class="row-label">Компактные списки</p>
            <p class="row-note">Больше серверов на экране.</p>
          </div>
          <button class="switch" type="button" role="switch" aria-checked="false" aria-label="Компактные списки" data-setting="compact"><span></span></button>
        </div>
        <div class="row">
          <div class="row-copy">
            <p class="row-label">Уменьшить движение</p>
            <p class="row-note">Отключает вращение, анимацию дуги и пульсацию.</p>
          </div>
          <button class="switch" type="button" role="switch" aria-checked="false" aria-label="Уменьшить движение" data-setting="reduced"><span></span></button>
        </div>
      </section>""",
    'html-accent')

rep("""        <div class="row row-stack">
          <p class="row-label">Размер точек</p>""",
    """        <div class="row row-stack">
          <p class="row-label">Размер флагов</p>
          <div class="segmented" role="group" aria-label="Размер флагов на карте">
            <button type="button" data-group="flags" data-value="0.85" aria-pressed="false">Мелкие</button>
            <button type="button" data-group="flags" data-value="1" aria-pressed="true">Обычные</button>
            <button type="button" data-group="flags" data-value="1.25" aria-pressed="false">Крупные</button>
          </div>
        </div>
        <div class="row">
          <div class="row-copy">
            <p class="row-label">Названия городов</p>
            <p class="row-note">Подписи под флагами на карте.</p>
          </div>
          <button class="switch" type="button" role="switch" aria-checked="false" aria-label="Названия городов на карте" data-setting="labels"><span></span></button>
        </div>
        <div class="row row-stack">
          <p class="row-label">Размер точек</p>""",
    'html-flags')

rep("""          <button class="switch" type="button" role="switch" aria-checked="false" aria-label="Автоподключение" data-setting="autoconnect"><span></span></button>
        </div>
      </section>

      <section class="group">
        <h2>Данные</h2>
        <p class="settings-note">Серверы и подписки хранятся только в этом браузере. Это демонстрационный клиент — туннель не поднимается.</p>
      </section>""",
    """          <button class="switch" type="button" role="switch" aria-checked="false" aria-label="Автоподключение" data-setting="autoconnect"><span></span></button>
        </div>
        <div class="row">
          <div class="row-copy">
            <p class="row-label">Проверять задержку</p>
            <p class="row-note">Измерять отклик серверов при открытии списка.</p>
          </div>
          <button class="switch" type="button" role="switch" aria-checked="true" aria-label="Проверять задержку" data-setting="ping"><span></span></button>
        </div>
      </section>

      <section class="group">
        <h2>Данные</h2>
        <div class="row">
          <div class="row-copy">
            <p class="row-label">Резервная копия</p>
            <p class="row-note">Экспорт и импорт серверов, подписок и настроек.</p>
          </div>
          <div class="data-actions">
            <button class="ghost" type="button" id="export-data">Экспорт</button>
            <button class="ghost" type="button" id="import-data">Импорт</button>
          </div>
        </div>
        <p class="settings-note">Серверы и подписки хранятся только на этом устройстве. Клиент поднимает интерфейс и управление серверами; сам туннель подключается ядром (VLESS / Trojan / Hysteria2), которое ставится отдельно в сборку.</p>
      </section>""",
    'html-data')

# ═══════════════ JS ══════════════════════════════════════════════════════════
rep("""  function normalizeSpeed(value) {
    const n = Number(value);
    return n === 0.5 || n === 2 ? n : 1;
  }
""",
    """  function normalizeSpeed(value) {
    const n = Number(value);
    return n === 0.5 || n === 2 ? n : 1;
  }

  function normalizeFlags(value) {
    const n = Number(value);
    return n === 0.85 || n === 1.25 ? n : 1;
  }

  const ACCENTS = [
    { id: 'emerald', name: 'Изумруд', light: '#1d5a45', dark: '#7db79a' },
    { id: 'ocean', name: 'Океан', light: '#1b5566', dark: '#7cb8cb' },
    { id: 'azure', name: 'Лазурь', light: '#1c5b9b', dark: '#8cb9e8' },
    { id: 'amethyst', name: 'Аметист', light: '#4a3a7c', dark: '#ac9ddb' },
    { id: 'wine', name: 'Вино', light: '#7a2f46', dark: '#de95ab' },
    { id: 'clay', name: 'Терракота', light: '#9a4a2c', dark: '#e5a184' },
    { id: 'sun', name: 'Янтарь', light: '#8a5c14', dark: '#e3b76e' },
    { id: 'olive', name: 'Олива', light: '#4f5b1e', dark: '#b6c283' },
    { id: 'rose', name: 'Роза', light: '#9a3464', dark: '#e69cb9' },
    { id: 'graphite', name: 'Графит', light: '#333537', dark: '#bcc0bd' }
  ];

  function hexToRgb(hex) {
    let value = String(hex || '').trim().replace('#', '');
    if (value.length === 3) {
      value = value.split('').map(function (c) { return c + c; }).join('');
    }
    if (!/^[0-9a-f]{6}$/i.test(value)) return null;
    return {
      r: parseInt(value.slice(0, 2), 16),
      g: parseInt(value.slice(2, 4), 16),
      b: parseInt(value.slice(4, 6), 16)
    };
  }

  function rgbToHsl(rgb) {
    const r = rgb.r / 255;
    const g = rgb.g / 255;
    const b = rgb.b / 255;
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    const l = (max + min) / 2;
    let h = 0;
    let s = 0;
    if (max !== min) {
      const d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      if (max === r) h = ((g - b) / d + (g < b ? 6 : 0)) / 6;
      else if (max === g) h = ((b - r) / d + 2) / 6;
      else h = ((r - g) / d + 4) / 6;
    }
    return { h: h * 360, s: s * 100, l: l * 100 };
  }

  function hslToHex(h, s, l) {
    const hue = (((h % 360) + 360) % 360) / 360;
    const sat = clamp(s, 0, 100) / 100;
    const lum = clamp(l, 0, 100) / 100;
    const q = lum < 0.5 ? lum * (1 + sat) : lum + sat - lum * sat;
    const p = 2 * lum - q;
    const channel = function (t) {
      let temp = t;
      if (temp < 0) temp += 1;
      if (temp > 1) temp -= 1;
      if (temp < 1 / 6) return p + (q - p) * 6 * temp;
      if (temp < 1 / 2) return q;
      if (temp < 2 / 3) return p + (q - p) * (2 / 3 - temp) * 6;
      return p;
    };
    const to = function (value) {
      const v = Math.round(clamp(value, 0, 1) * 255).toString(16);
      return v.length === 1 ? '0' + v : v;
    };
    return '#' + to(channel(hue + 1 / 3)) + to(channel(hue)) + to(channel(hue - 1 / 3));
  }

  function resolveAccent(id, theme) {
    const night = theme === 'night';
    if (typeof id === 'string' && id.charAt(0) === '#') {
      const rgb = hexToRgb(id);
      if (rgb) {
        const hsl = rgbToHsl(rgb);
        const hex = hslToHex(
          hsl.h,
          night ? Math.min(hsl.s, 60) : Math.min(hsl.s, 66),
          night ? clamp(hsl.l, 60, 74) : clamp(hsl.l, 22, 38)
        );
        return { id: 'custom', name: 'Свой цвет', hex: hex, custom: true, source: id };
      }
    }
    const preset = ACCENTS.filter(function (item) { return item.id === id; })[0] || ACCENTS[0];
    return { id: preset.id, name: preset.name, hex: night ? preset.dark : preset.light, custom: false, source: '' };
  }
""",
    'js-settings-helpers')

rep("""    return {
      theme: theme,
      rotate: raw.rotate !== false,
      route: raw.route !== false,
      reduced: raw.reduced == null ? osReduced : raw.reduced === true,
      dots: normalizeDots(raw.dots == null ? 1 : raw.dots),
      speed: normalizeSpeed(raw.speed == null ? 1 : raw.speed),
      autoconnect: raw.autoconnect === true
    };""",
    """    return {
      theme: theme,
      accent: typeof raw.accent === 'string' && raw.accent ? raw.accent : 'emerald',
      rotate: raw.rotate !== false,
      route: raw.route !== false,
      reduced: raw.reduced == null ? osReduced : raw.reduced === true,
      labels: raw.labels === true,
      soft: raw.soft === true,
      compact: raw.compact === true,
      ping: raw.ping !== false,
      dots: normalizeDots(raw.dots == null ? 1 : raw.dots),
      flags: normalizeFlags(raw.flags == null ? 1 : raw.flags),
      speed: normalizeSpeed(raw.speed == null ? 1 : raw.speed),
      autoconnect: raw.autoconnect === true
    };""",
    'js-load-settings')

rep("""  const state = {
    servers: [],
    subs: [],
    selectedId: '',
    connected: false,
    view: 'home'
  };""",
    """  const state = {
    servers: [],
    subs: [],
    selectedId: '',
    connected: false,
    view: 'home',
    query: '',
    latency: {},
    latencyAt: 0
  };

  const native = (window.Native && window.Native.available) ? window.Native : null;

  function haptic() {
    if (!native || typeof native.haptic !== 'function') return;
    try { native.haptic(); } catch (error) { /* не критично */ }
  }

  function copyText(value) {
    if (native && typeof native.copy === 'function') {
      try { native.copy(String(value)); return true; } catch (error) { /* ниже */ }
    }
    if (window.navigator && navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(String(value)).catch(function () {});
      return true;
    }
    return false;
  }""",
    'js-state-native')

rep("""    store.write('vpn.settings', {
      rotate: settings.rotate,
      route: settings.route,
      reduced: settings.reduced,
      dots: settings.dots,
      speed: settings.speed,
      autoconnect: settings.autoconnect
    });""",
    """    store.write('vpn.settings', {
      accent: settings.accent,
      rotate: settings.rotate,
      route: settings.route,
      reduced: settings.reduced,
      labels: settings.labels,
      soft: settings.soft,
      compact: settings.compact,
      ping: settings.ping,
      dots: settings.dots,
      flags: settings.flags,
      speed: settings.speed,
      autoconnect: settings.autoconnect
    });""",
    'js-persist')

rep("""  function applyTheme(theme) {
    settings.theme = theme === 'night' ? 'night' : 'paper';
    document.documentElement.dataset.theme = settings.theme;
    const computed = getComputedStyle(document.documentElement);
    globe.setColors({
      ink: computed.getPropertyValue('--ink').trim(),
      paper: computed.getPropertyValue('--paper').trim(),
      accent: computed.getPropertyValue('--accent').trim()
    });
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', computed.getPropertyValue('--paper').trim());
    $$('[data-theme-value]').forEach(function (button) {
      button.setAttribute('aria-pressed', String(button.dataset.themeValue === settings.theme));
    });
  }

  function applySetting(name) {
    if (name === 'rotate') globe.setAutoRotate(settings.rotate);
    if (name === 'route') globe.setArc(settings.route);
    if (name === 'reduced') {
      document.documentElement.dataset.reduced = String(settings.reduced);
      globe.setReduced(settings.reduced);
    }
    if (name === 'dots') globe.setDotScale(settings.dots);
    if (name === 'speed') globe.setSpin(settings.speed);
  }""",
    """  function applyAccent() {
    const root = document.documentElement;
    const resolved = resolveAccent(settings.accent, settings.theme);
    root.style.setProperty('--accent', resolved.hex);
    const rgb = hexToRgb(resolved.hex);
    if (rgb) {
      root.style.setProperty('--accent-soft', 'rgba(' + rgb.r + ', ' + rgb.g + ', ' + rgb.b + ', .14)');
      root.style.setProperty('--accent-line', 'rgba(' + rgb.r + ', ' + rgb.g + ', ' + rgb.b + ', .40)');
    }
    const label = document.getElementById('accent-value');
    if (label) label.textContent = resolved.name + ' · ' + resolved.hex.toUpperCase();
    $$('[data-accent]').forEach(function (button) {
      const preset = ACCENTS.filter(function (item) { return item.id === button.dataset.accent; })[0];
      if (preset) button.style.setProperty('--swatch', settings.theme === 'night' ? preset.dark : preset.light);
      button.setAttribute('aria-pressed', String(!resolved.custom && button.dataset.accent === resolved.id));
    });
    const custom = $('.swatch-custom input');
    if (custom && resolved.custom && resolved.source) custom.value = resolved.source;
    return resolved;
  }

  function applyTheme(theme) {
    settings.theme = theme === 'night' ? 'night' : 'paper';
    document.documentElement.dataset.theme = settings.theme;
    applyAccent();
    const computed = getComputedStyle(document.documentElement);
    const paper = computed.getPropertyValue('--paper').trim();
    globe.setColors({
      ink: computed.getPropertyValue('--ink').trim(),
      paper: paper,
      accent: computed.getPropertyValue('--accent').trim()
    });
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', paper);
    if (native && typeof native.setChrome === 'function') {
      try { native.setChrome(paper, settings.theme === 'night'); } catch (error) { /* не критично */ }
    }
    $$('[data-theme-value]').forEach(function (button) {
      button.setAttribute('aria-pressed', String(button.dataset.themeValue === settings.theme));
    });
  }

  function applySetting(name) {
    const root = document.documentElement;
    if (name === 'rotate') globe.setAutoRotate(settings.rotate);
    if (name === 'route') globe.setArc(settings.route);
    if (name === 'reduced') {
      root.dataset.reduced = String(settings.reduced);
      globe.setReduced(settings.reduced);
    }
    if (name === 'dots') globe.setDotScale(settings.dots);
    if (name === 'speed') globe.setSpin(settings.speed);
    if (name === 'flags') root.style.setProperty('--flag-scale', String(settings.flags));
    if (name === 'labels') document.body.dataset.labels = String(settings.labels);
    if (name === 'soft') root.dataset.soft = String(settings.soft);
    if (name === 'compact') document.body.dataset.compact = String(settings.compact);
    if (name === 'ping' && settings.ping) {
      state.latencyAt = 0;
      window.setTimeout(function () { pingAll(true); }, 80);
    }
  }""",
    'js-theme')

rep("""  const ui = {
    connect: $('#connect'),""",
    """  function buildSwatches() {
    const box = $('.swatches', $('#view-settings'));
    if (!box || box.childElementCount) return;
    ACCENTS.forEach(function (item) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'swatch';
      button.dataset.accent = item.id;
      button.style.setProperty('--swatch', item.light);
      button.setAttribute('aria-label', 'Акцентный цвет: ' + item.name);
      button.setAttribute('aria-pressed', 'false');
      button.addEventListener('click', function () {
        settings.accent = item.id;
        applyTheme(settings.theme);
        syncSettings();
        persist();
        haptic();
      });
      box.appendChild(button);
    });
    const custom = document.createElement('label');
    custom.className = 'swatch swatch-custom';
    custom.title = 'Свой цвет';
    const input = document.createElement('input');
    input.type = 'color';
    input.value = resolveAccent(settings.accent, settings.theme).hex;
    input.setAttribute('aria-label', 'Свой акцентный цвет');
    const hint = document.createElement('span');
    hint.textContent = '+';
    hint.setAttribute('aria-hidden', 'true');
    custom.appendChild(input);
    custom.appendChild(hint);
    input.addEventListener('input', function () {
      settings.accent = input.value;
      applyTheme(settings.theme);
      syncSettings();
    });
    input.addEventListener('change', function () {
      persist();
      haptic();
    });
    box.appendChild(custom);
  }

  const ui = {
    connect: $('#connect'),""",
    'js-swatches')

rep("""    toast: $('#toast'),
    toastText: $('#toast-text'),
    toastAction: $('#toast-action')
  };""",
    """    toast: $('#toast'),
    toastText: $('#toast-text'),
    toastAction: $('#toast-action'),
    search: $('#server-search'),
    noMatch: $('#server-no-match'),
    pingAll: $('#ping-all'),
    serverTools: $('#server-tools')
  };""",
    'js-ui-refs')

rep("""  function renderServers() {
    const sorted = state.servers.slice().sort(function (a, b) {
      return (a.city || '').localeCompare(b.city || '', 'ru');
    });

    ui.serverList.textContent = '';""",
    """  function matchesQuery(server) {
    const query = normalizeForSearch(state.query);
    if (!query) return true;
    const haystack = normalizeForSearch([
      server.city, server.country, server.protocol, server.subName, server.host, server.code
    ].filter(Boolean).join(' '));
    return query.split(' ').every(function (word) {
      return !word || haystack.indexOf(word) !== -1;
    });
  }

  function latencyText(server) {
    const entry = state.latency[server.id];
    if (!entry) return null;
    if (entry.ms == null) return { text: 'нет ответа', className: ' is-slow' };
    const tone = entry.ms < 220 ? ' is-fast' : (entry.ms > 800 ? ' is-slow' : '');
    return { text: entry.ms + ' мс', className: tone };
  }

  function pingAll(silent) {
    const list = state.servers.filter(function (server) {
      return server.host && server.port;
    }).map(function (server) {
      return { id: server.id, host: server.host, port: server.port };
    });
    if (!list.length) return;
    if (!native || typeof native.ping !== 'function') {
      if (!silent) showToast('Задержка измеряется в приложении');
      return;
    }
    if (ui.pingAll) {
      ui.pingAll.disabled = true;
      ui.pingAll.textContent = 'Проверка…';
    }
    try {
      native.ping(JSON.stringify(list));
    } catch (error) {
      if (ui.pingAll) {
        ui.pingAll.disabled = false;
        ui.pingAll.textContent = 'Задержка';
      }
    }
  }

  window.__onLatency = function (payload) {
    let rows = [];
    try { rows = JSON.parse(payload); } catch (error) { rows = []; }
    if (!Array.isArray(rows)) rows = [];
    rows.forEach(function (row) {
      if (!row || !row.id) return;
      const ms = Number(row.ms);
      state.latency[row.id] = { ms: Number.isFinite(ms) ? ms : null };
    });
    state.latencyAt = Date.now();
    if (ui.pingAll) {
      ui.pingAll.disabled = false;
      ui.pingAll.textContent = 'Задержка';
    }
    renderServers();
  };

  function renderServers() {
    const sorted = state.servers.slice().sort(function (a, b) {
      return (a.city || '').localeCompare(b.city || '', 'ru');
    }).filter(matchesQuery);

    ui.serverList.textContent = '';""",
    'js-ping')

rep("""      const sub = document.createElement('span');
      sub.className = 'server-sub';
      sub.textContent = [server.country || 'Локация не определена', sourceText(server)].filter(Boolean).join(' · ');
      copy.appendChild(city);
      copy.appendChild(sub);""",
    """      const sub = document.createElement('span');
      sub.className = 'server-sub';
      sub.textContent = [server.country || 'Локация не определена', sourceText(server)].filter(Boolean).join(' · ');
      const ping = latencyText(server);
      if (ping) {
        sub.appendChild(document.createTextNode(' · '));
        const pingEl = document.createElement('span');
        pingEl.className = 'server-ping' + ping.className;
        pingEl.textContent = ping.text;
        sub.appendChild(pingEl);
      }
      copy.appendChild(city);
      copy.appendChild(sub);""",
    'js-row-ping')

rep("""    ui.serversEmpty.hidden = state.servers.length !== 0;
    updateMeta();
    markSelectedRow();
  }""",
    """    ui.serversEmpty.hidden = state.servers.length !== 0;
    if (ui.serverTools) ui.serverTools.hidden = state.servers.length === 0;
    if (ui.noMatch) ui.noMatch.hidden = !(state.query && sorted.length === 0 && state.servers.length > 0);
    updateMeta();
    markSelectedRow();
  }""",
    'js-empty')

# ── Globe markers: flag circles ──────────────────────────────────────────────
rep("""    const dot = document.createElement('span');
    dot.className = 'srv-dot';
    button.appendChild(dot);""",
    """    const badge = document.createElement('span');
    badge.className = 'srv-flag' + (server.flag ? '' : ' is-unknown');
    badge.textContent = server.flag || (server.code ? String(server.code).toUpperCase() : '··');
    badge.setAttribute('aria-hidden', 'true');
    button.appendChild(badge);

    const label = document.createElement('span');
    label.className = 'srv-label';
    label.textContent = server.city || server.host || '';
    label.setAttribute('aria-hidden', 'true');
    button.appendChild(label);""",
    'js-globe-flag')

rep("""  DotGlobe.prototype.select = function (id, options) {
    const opts = options || {};
    const server = this.servers.filter(function (s) { return s.id === id; })[0];
    if (!server) return;

    this.selectedId = id;""",
    """  DotGlobe.prototype.select = function (id, options) {
    const opts = options || {};
    const server = this.servers.filter(function (s) { return s.id === id; })[0];
    if (!server) return;
    const alreadySelected = this.selectedId === id;

    this.selectedId = id;""",
    'js-globe-select-guard-a')

rep("""    this.idleUntil = performance.now() + 5000;
    if (opts.notify !== false) this.onSelect(server);""",
    """    this.idleUntil = performance.now() + 5000;
    if (opts.notify !== false && !alreadySelected) this.onSelect(server);""",
    'js-globe-select-guard-b')

# ── Wiring: search, ping, export/import, back, init ─────────────────────────
rep("""  $('#open-add-server').addEventListener('click', openAddServer);""",
    """  if (ui.search) {
    ui.search.addEventListener('input', function () {
      state.query = ui.search.value;
      renderServers();
    });
  }

  if (ui.pingAll) {
    ui.pingAll.addEventListener('click', function () { pingAll(false); });
  }

  function exportData() {
    const payload = {
      app: 'globe-vpn',
      version: 2,
      exportedAt: new Date().toISOString(),
      servers: state.servers,
      subscriptions: state.subs,
      selected: state.selectedId,
      settings: settings
    };
    const text = JSON.stringify(payload, null, 2);
    if (native && typeof native.saveFile === 'function') {
      native.saveFile('globe-vpn-backup.json', text);
      showToast('Резервная копия сохранена');
      return;
    }
    try {
      const blob = new Blob([text], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'globe-vpn-backup.json';
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
      showToast('Резервная копия сохранена');
    } catch (error) {
      if (copyText(text)) showToast('Копия в буфере обмена');
      else showToast('Не удалось сохранить копию');
    }
  }

  function importData() {
    if (native && typeof native.pickFile === 'function') {
      native.pickFile();
      return;
    }
    showToast('Импорт доступен в приложении');
  }

  window.__onImport = function (text) {
    let payload = null;
    try { payload = JSON.parse(String(text || '')); } catch (error) { payload = null; }
    if (!payload || typeof payload !== 'object') {
      showToast('Файл не похож на резервную копию');
      return;
    }
    const servers = Array.isArray(payload.servers) ? payload.servers.map(sanitizeServer).filter(Boolean) : [];
    const subs = Array.isArray(payload.subscriptions) ? payload.subscriptions.map(sanitizeSub).filter(Boolean) : [];
    if (!servers.length && !subs.length) {
      showToast('В файле нет серверов');
      return;
    }
    state.servers.forEach(function (server) { globe.removeServer(server.id); });
    state.servers = [];
    state.subs = subs;
    servers.forEach(function (server) { globe.addServer(server); });
    state.servers = servers;
    state.selectedId = servers.some(function (server) { return server.id === payload.selected; })
      ? payload.selected
      : (servers[0] ? servers[0].id : '');
    if (payload.settings && typeof payload.settings === 'object') {
      Object.keys(payload.settings).forEach(function (key) {
        if (key in settings) settings[key] = payload.settings[key];
      });
      settings.flags = normalizeFlags(settings.flags);
      settings.dots = normalizeDots(settings.dots);
      settings.speed = normalizeSpeed(settings.speed);
      applyTheme(settings.theme);
      ['rotate', 'route', 'reduced', 'dots', 'speed', 'flags', 'labels', 'soft', 'compact', 'ping'].forEach(applySetting);
      syncSettings();
    }
    persist();
    renderServers();
    renderSubs();
    updateHome();
    if (state.selectedId) globe.select(state.selectedId, { notify: false, instant: true });
    showToast('Импортировано: ' + servers.length + ' ' + plural(servers.length, ['сервер', 'сервера', 'серверов']));
  };

  window.__nativeBack = function () {
    if (state.view === 'add-server' || state.view === 'add-sub') {
      showView('servers');
      return true;
    }
    if (state.view !== 'home') {
      showView('home');
      return true;
    }
    return false;
  };

  $('#export-data').addEventListener('click', exportData);
  $('#import-data').addEventListener('click', importData);
  $('#open-add-server').addEventListener('click', openAddServer);""",
    'js-wiring')

rep("""  $('#reset-settings').addEventListener('click', function () {
    settings.rotate = true;
    settings.route = true;
    settings.reduced = osReduced;
    settings.dots = 1;
    settings.speed = 1;
    settings.autoconnect = false;
    applyTheme('paper');
    ['rotate', 'route', 'reduced', 'dots', 'speed'].forEach(applySetting);""",
    """  $('#reset-settings').addEventListener('click', function () {
    settings.accent = 'emerald';
    settings.rotate = true;
    settings.route = true;
    settings.reduced = osReduced;
    settings.labels = false;
    settings.soft = false;
    settings.compact = false;
    settings.ping = true;
    settings.dots = 1;
    settings.flags = 1;
    settings.speed = 1;
    settings.autoconnect = false;
    applyTheme('paper');
    ['rotate', 'route', 'reduced', 'dots', 'speed', 'flags', 'labels', 'soft', 'compact'].forEach(applySetting);""",
    'js-reset')

rep("""  applyTheme(settings.theme);
  ['rotate', 'route', 'reduced', 'dots', 'speed'].forEach(applySetting);
  syncSettings();""",
    """  buildSwatches();
  applyTheme(settings.theme);
  ['rotate', 'route', 'reduced', 'dots', 'speed', 'flags', 'labels', 'soft', 'compact'].forEach(applySetting);
  syncSettings();""",
    'js-init')

# connect: haptic
rep("""    state.connected = !state.connected;
    globe.setConnected(state.connected);
    updateHome();
  });""",
    """    state.connected = !state.connected;
    globe.setConnected(state.connected);
    updateHome();
    haptic();
  });""",
    'js-connect-haptic')

# auto-ping when opening servers view
rep("""    showView(target);
    if (target === 'settings') syncSettings();""",
    """    showView(target);
    if (target === 'settings') syncSettings();
    if (target === 'servers' && settings.ping && Date.now() - state.latencyAt > 60000) pingAll(true);""",
    'js-autoping')

open(DST, 'w', encoding='utf-8').write(s)
print('OK: %d edits applied -> %s' % (len(done), DST))

# ═══════════════ second pass: clipboard paste buttons + native detection ═════
s = open(DST, encoding='utf-8').read()


def rep2(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep2("""      <p class="lead">Вставьте ссылку. Страна и город определятся по флагу и названию.</p>

      <form class="form" id="server-form" novalidate>""",
     """      <p class="lead">Вставьте ссылку. Страна и город определятся по флагу и названию.</p>

      <div class="form-tools">
        <button class="ghost" type="button" data-paste="server-link">Вставить из буфера</button>
      </div>

      <form class="form" id="server-form" novalidate>""",
     'html-paste-server')

rep2("""      <p class="lead">Ссылка или содержимое. Если браузер не может загрузить ссылку, вставьте содержимое вручную.</p>

      <form class="form" id="sub-form" novalidate>""",
     """      <p class="lead">Ссылка или содержимое. Если браузер не может загрузить ссылку, вставьте содержимое вручную.</p>

      <div class="form-tools">
        <button class="ghost" type="button" data-paste="sub-url">Вставить ссылку</button>
        <button class="ghost" type="button" data-paste="sub-content">Вставить содержимое</button>
      </div>

      <form class="form" id="sub-form" novalidate>""",
     'html-paste-sub')

rep2(""".ping-all { white-space: nowrap; }""",
     """.ping-all { white-space: nowrap; }

.form-tools {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 16px;
  margin: -4px 0 18px;
}""",
     'css-form-tools')

rep2("""  const native = (window.Native && window.Native.available) ? window.Native : null;""",
     """  const native = (window.Native && typeof window.Native.ping === 'function') ? window.Native : null;""",
     'js-native-detect')

rep2("""  if (ui.search) {
    ui.search.addEventListener('input', function () {""",
     """  $$('[data-paste]').forEach(function (button) {
    button.addEventListener('click', function () {
      const target = button.dataset.paste;
      if (native && typeof native.readClipboard === 'function') {
        native.readClipboard(target);
        return;
      }
      showToast('Вставка из буфера доступна в приложении');
    });
  });

  window.__onClipboard = function (target, text) {
    const field = document.getElementById(target);
    if (!field) return;
    field.value = String(text || '').trim();
    field.dispatchEvent(new Event('input', { bubbles: true }));
    showToast('Вставлено из буфера');
  };

  if (ui.search) {
    ui.search.addEventListener('input', function () {""",
     'js-paste')

open(DST, 'w', encoding='utf-8').write(s)
print('pass2 OK: %d edits total' % len(done))

# ═══════════════ third pass: polish ══════════════════════════════════════════
s = open(DST, encoding='utf-8').read()


def rep3(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# softer, tighter pulse ring
rep3("""  transform: translate(-50%, -50%);
  animation: ping 2.8s ease-out infinite;
  pointer-events: none;
}""",
     """  transform: translate(-50%, -50%);
  animation: ping 2.6s ease-out infinite;
  pointer-events: none;
}""",
     'polish-ping-ring')

rep3("""@keyframes ping {
  0% { opacity: .55; transform: translate(-50%, -50%) scale(1); }
  70%, 100% { opacity: 0; transform: translate(-50%, -50%) scale(3.8); }
}""",
     """@keyframes ping {
  0% { opacity: .5; transform: translate(-50%, -50%) scale(1); }
  72%, 100% { opacity: 0; transform: translate(-50%, -50%) scale(2.35); }
}""",
     'polish-ping-keyframes')

# switch: clear knob geometry
rep3(""".switch {
  position: relative;
  width: 34px;
  height: 20px;
  flex: 0 0 auto;
  padding: 0;
  border: 1px solid var(--ink);
  border-radius: 0;
  background: transparent;
  transition: background .18s ease, border-color .18s ease;
}

.switch span {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 12px;
  height: 12px;
  background: var(--ink);
  transition: transform .18s ease, background .18s ease;
}""",
     """.switch {
  position: relative;
  width: 36px;
  height: 20px;
  flex: 0 0 auto;
  padding: 0;
  border: 1px solid var(--line-strong);
  border-radius: 0;
  background: transparent;
  transition: background .18s ease, border-color .18s ease;
}

.switch span {
  position: absolute;
  top: 4px;
  left: 4px;
  width: 10px;
  height: 10px;
  background: var(--line-strong);
  transition: transform .18s ease, background .18s ease;
}""",
     'polish-switch')

rep3(""".switch[aria-checked="true"] span {
  background: var(--paper);
  transform: translateX(14px);
}""",
     """.switch[aria-checked="true"] span {
  background: var(--paper);
  transform: translateX(16px);
}""",
     'polish-switch-knob')

# no double divider before the subscriptions block
rep3(""".server-list,
.sub-list { margin-top: 8px; }""",
     """.server-list,
.sub-list { margin-top: 8px; }

.server-item:last-child .server-row { border-bottom: 0; }
.server-list:not(:empty) ~ .server-no-match { display: none; }""",
     'polish-dividers')

# field head with inline paste action
rep3(""".form { margin-top: 6px; }""",
     """.form { margin-top: 6px; }

.field-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 6px;
}

.field-head label { margin-bottom: 0; }

.field-action {
  padding: 0 0 2px;
  border: 0;
  border-bottom: 1px solid var(--line-strong);
  background: none;
  font-family: var(--mono);
  font-size: 8.5px;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--muted);
  transition: color .15s ease, border-color .15s ease;
}

.field-action:hover {
  color: var(--accent);
  border-color: var(--accent);
}""",
     'polish-field-head')

rep3("""      <div class="form-tools">
        <button class="ghost" type="button" data-paste="server-link">Вставить из буфера</button>
      </div>

""",
     """""",
     'polish-drop-tools-server')

rep3("""      <div class="form-tools">
        <button class="ghost" type="button" data-paste="sub-url">Вставить ссылку</button>
        <button class="ghost" type="button" data-paste="sub-content">Вставить содержимое</button>
      </div>

""",
     """""",
     'polish-drop-tools-sub')

rep3("""          <label for="server-link">Ссылка сервера</label>""",
     """          <div class="field-head">
            <label for="server-link">Ссылка сервера</label>
            <button class="field-action" type="button" data-paste="server-link">Вставить</button>
          </div>""",
     'polish-head-link')

rep3("""          <label for="sub-url">Ссылка <span class="optional">необязательно</span></label>""",
     """          <div class="field-head">
            <label for="sub-url">Ссылка <span class="optional">необязательно</span></label>
            <button class="field-action" type="button" data-paste="sub-url">Вставить</button>
          </div>""",
     'polish-head-url')

rep3("""          <label for="sub-content">Содержимое <span class="optional">необязательно</span></label>""",
     """          <div class="field-head">
            <label for="sub-content">Содержимое <span class="optional">необязательно</span></label>
            <button class="field-action" type="button" data-paste="sub-content">Вставить</button>
          </div>""",
     'polish-head-content')

# ping-all shouldn't clip
rep3(""".ping-all { white-space: nowrap; }""",
     """.ping-all {
  flex: 0 0 auto;
  white-space: nowrap;
  padding-right: 2px;
}

.list-tools .search { margin-right: 2px; }""",
     'polish-ping-all')

open(DST, 'w', encoding='utf-8').write(s)
print('pass3 OK: %d edits total' % len(done))

# ═══════════════ fourth pass: deep links from other apps ═════════════════════
s = open(DST, encoding='utf-8').read()


def rep4(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep4("""  window.__nativeBack = function () {""",
     """  window.__importLink = function (link) {
    const value = String(link || '').trim();
    if (!value) return;
    openAddServer();
    ui.serverLink.value = value;
    updateServerPreview();
    showToast('Ссылка получена из другого приложения');
  };

  window.__nativeBack = function () {""",
     'polish-deeplink')

open(DST, 'w', encoding='utf-8').write(s)
print('pass4 OK: %d edits total' % len(done))


# ═══════════════ fifth pass: подписки через нативный HTTP ════════════════════
s = open(DST, encoding='utf-8').read()


def rep5(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep5("""  async function fetchSubscription(url) {
    const controller = new AbortController();""",
     """  const pendingFetches = {};

  function nativeFetch(url) {
    return new Promise(function (resolve, reject) {
      const key = 'f' + Math.random().toString(36).slice(2, 9);
      pendingFetches[key] = { resolve: resolve, reject: reject };
      try {
        native.fetchText(key, url);
      } catch (error) {
        delete pendingFetches[key];
        reject(new Error('нет соединения'));
        return;
      }
      window.setTimeout(function () {
        if (!pendingFetches[key]) return;
        delete pendingFetches[key];
        reject(new Error('таймаут'));
      }, 15000);
    });
  }

  window.__onFetch = function (key, ok, text) {
    const entry = pendingFetches[key];
    if (!entry) return;
    delete pendingFetches[key];
    if (ok) entry.resolve(String(text || ''));
    else entry.reject(new Error('ошибка загрузки'));
  };

  async function fetchSubscription(url) {
    if (native && typeof native.fetchText === 'function') {
      return await nativeFetch(url);
    }
    const controller = new AbortController();""",
     'js-native-fetch')

open(DST, 'w', encoding='utf-8').write(s)
print('pass5 OK: %d edits total' % len(done))

# ═══════════════ sixth pass: подписи без наложений + сохранение акцента ═══════
s = open(DST, encoding='utf-8').read()


def rep6(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep6("""  DotGlobe.prototype.updateMarkers = function () {
    const p = {};
    const self = this;
    this.servers.forEach(function (server) {
      const button = self.markers.get(server.id);
      const vector = self.serverVec[server.id];
      if (!button || !vector) return;
      self.project(vector, p);
      if (p.z <= 0.015) {
        button.style.visibility = 'hidden';
        button.setAttribute('aria-hidden', 'true');
        button.tabIndex = -1;
        return;
      }
      button.style.visibility = 'visible';
      button.removeAttribute('aria-hidden');
      button.tabIndex = 0;
      button.style.transform = 'translate3d(' + p.x.toFixed(1) + 'px,' + p.y.toFixed(1) + 'px,0) translate(-50%,-50%)';
      button.style.setProperty('--depth', String(clamp(p.z, 0, 1)));
    });
""",
     """  DotGlobe.prototype.updateMarkers = function () {
    const p = {};
    const self = this;
    const visible = [];
    this.servers.forEach(function (server) {
      const button = self.markers.get(server.id);
      const vector = self.serverVec[server.id];
      if (!button || !vector) return;
      self.project(vector, p);
      if (p.z <= 0.015) {
        button.style.visibility = 'hidden';
        button.setAttribute('aria-hidden', 'true');
        button.tabIndex = -1;
        return;
      }
      button.style.visibility = 'visible';
      button.removeAttribute('aria-hidden');
      button.tabIndex = 0;
      button.style.transform = 'translate3d(' + p.x.toFixed(1) + 'px,' + p.y.toFixed(1) + 'px,0) translate(-50%,-50%)';
      button.style.setProperty('--depth', String(clamp(p.z, 0, 1)));
      visible.push({ button: button, x: p.x, y: p.y, z: p.z, city: String(server.city || '') });
    });

    // подписи городов: прячем те, что перекрываются с более близкими
    visible.sort(function (a, b) { return b.z - a.z; });
    const placed = [];
    visible.forEach(function (item) {
      const width = Math.min(140, 16 + item.city.length * 5.6);
      const box = {
        x1: item.x - width / 2,
        x2: item.x + width / 2,
        y1: item.y + 14,
        y2: item.y + 38
      };
      const overlap = placed.some(function (other) {
        return !(box.x2 < other.x1 || box.x1 > other.x2 || box.y2 < other.y1 || box.y1 > other.y2);
      });
      item.button.classList.toggle('is-label-hidden', overlap);
      if (!overlap) placed.push(box);
    });
""",
     'polish-label-collision')

rep6(""".srv:hover .srv-label,
.srv:focus-visible .srv-label,
.srv.is-selected .srv-label,
body[data-labels="true"] .srv-label {
  opacity: 1;
  visibility: visible;
  transform: translate(-50%, 0);
  transition: opacity .16s ease, transform .16s ease, visibility 0s;
}""",
     """.srv:hover .srv-label,
.srv:focus-visible .srv-label,
.srv.is-selected .srv-label,
body[data-labels="true"] .srv-label {
  opacity: 1;
  visibility: visible;
  transform: translate(-50%, 0);
  transition: opacity .16s ease, transform .16s ease, visibility 0s;
}

.srv.is-label-hidden:not(.is-selected):not(:hover) .srv-label {
  opacity: 0;
  visibility: hidden;
}""",
     'polish-label-collision-css')

rep6("""    input.addEventListener('input', function () {
      settings.accent = input.value;
      applyTheme(settings.theme);
      syncSettings();
    });
    input.addEventListener('change', function () {
      persist();
      haptic();
    });""",
     """    let saveTimer = null;
    input.addEventListener('input', function () {
      settings.accent = input.value;
      applyTheme(settings.theme);
      syncSettings();
      window.clearTimeout(saveTimer);
      saveTimer = window.setTimeout(persist, 240);
    });
    input.addEventListener('change', function () {
      window.clearTimeout(saveTimer);
      persist();
      haptic();
    });""",
     'polish-accent-persist')

open(DST, 'w', encoding='utf-8').write(s)
print('pass6 OK: %d edits total' % len(done))

# ═══════════════ seventh pass: ландшафтная раскладка ═════════════════════════
s = open(DST, encoding='utf-8').read()


def rep7(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep7("""    const mobile = w < 760;
    const stack = mobile ? 128 : 142;
    const stackOffset = mobile ? 92 : 104;
    const bandTop = mobile ? 20 : 24;
    const gap = mobile ? 28 : 30;
    const bandBottom = Math.max(bandTop + 120, h - stackOffset - stack);
    const byHeight = (bandBottom - bandTop) / 2 - gap;
    const byWidth = w * (mobile ? 0.44 : 0.33);

    this.cx = w * 0.5;
    this.baseR = Math.max(72, Math.min(byHeight, byWidth));
    this.cy = (bandTop + bandBottom) / 2;""",
     """    const mobile = w < 760;
    const wide = w > h * 1.25 && h < 640;

    if (wide) {
      // ландшафт: глобус слева, управление справа
      this.cx = w * 0.31;
      this.cy = h * 0.5;
      this.baseR = Math.max(58, Math.min(h * 0.43, w * 0.26));
      this.dotSize = (mobile ? 1.35 : 1.55) * this.dotScale;
      this.radius = this.baseR * this.zoomLevel;
      return;
    }

    const stack = mobile ? 128 : 142;
    const stackOffset = mobile ? 92 : 104;
    const bandTop = mobile ? 20 : 24;
    const gap = mobile ? 28 : 30;
    const bandBottom = Math.max(bandTop + 120, h - stackOffset - stack);
    const byHeight = (bandBottom - bandTop) / 2 - gap;
    const byWidth = w * (mobile ? 0.44 : 0.33);

    this.cx = w * 0.5;
    this.baseR = Math.max(72, Math.min(byHeight, byWidth));
    this.cy = (bandTop + bandBottom) / 2;""",
     'landscape-globe')

rep7("""/* ── Уменьшенное движение ──────────────────────────────── */""",
     """/* ── Ландшафт ──────────────────────────────────────────── */

@media (orientation: landscape) and (max-height: 640px) {
  .home-ui {
    left: auto;
    right: calc(30px + env(safe-area-inset-right));
    top: 50%;
    bottom: auto;
    align-items: flex-end;
    transform: translateY(-50%);
  }

  .home-ui .connect {
    width: 80px;
    height: 80px;
  }

  .home-ui .connect-icon { width: 26px; height: 26px; }

  .path { width: min(300px, 42vw); }

  .dock {
    bottom: calc(12px + env(safe-area-inset-bottom));
    left: auto;
    right: calc(30px + env(safe-area-inset-right));
    transform: none;
  }

  .toast {
    left: calc(30px + env(safe-area-inset-left));
    right: auto;
    bottom: calc(18px + env(safe-area-inset-bottom));
    transform: translate(0, 8px);
    max-width: 46vw;
  }

  .toast.is-visible { transform: translate(0, 0); }

  body[data-view="home"] .toast {
    top: auto;
    bottom: calc(18px + env(safe-area-inset-bottom));
    transform: translate(0, 8px);
  }

  body[data-view="home"] .toast.is-visible { transform: translate(0, 0); }

  .screen { padding: 20px 28px calc(88px + env(safe-area-inset-bottom)); }
  .screen h1 { font-size: 24px; }
  .lead { margin: 12px 0 16px; }
}

/* ── Уменьшенное движение ──────────────────────────────── */""",
     'landscape-css')

open(DST, 'w', encoding='utf-8').write(s)
print('pass7 OK: %d edits total' % len(done))

# ═══════════════ pass 8: группировка списка как в Happ ═══════════════════════
s = open(DST, encoding='utf-8').read()


def rep8(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# ── HTML: экран серверов ────────────────────────────────────────────────────
rep8("""        <button class="text-action" type="button" id="open-add-server">+ Сервер</button>
      </header>""",
     """        <div class="head-actions">
          <button class="text-action" type="button" id="open-add-sub">+ Подписка</button>
          <button class="text-action" type="button" id="open-add-server">+ Сервер</button>
        </div>
      </header>""",
     'happ-head')

rep8("""      <div class="server-list" id="server-list"></div>
      <p class="server-empty-result" id="server-no-match" hidden>Ничего не найдено.</p>

      <section class="subs-block" aria-labelledby="subs-title">
        <div class="subs-head">
          <h2 id="subs-title">Подписки</h2>
          <button class="text-action" type="button" id="open-add-sub">+ Подписка</button>
        </div>
        <div class="sub-list" id="sub-list"></div>
        <p class="subs-empty" id="subs-empty" hidden>Ни одной подписки.</p>
      </section>""",
     """      <div class="group-list" id="group-list"></div>
      <p class="server-empty-result" id="server-no-match" hidden>Ничего не найдено.</p>""",
     'happ-list')

# ── CSS: карточки групп ─────────────────────────────────────────────────────
rep8("""/* ── Формы ─────────────────────────────────────────────── */""",
     """/* ── Группы: подписки и ручные серверы ─────────────────── */

.head-actions {
  display: flex;
  align-items: center;
  gap: 18px;
}

.group-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
}

.group-card {
  border: 1px solid var(--line);
  background: var(--paper);
  transition: border-color .18s ease, box-shadow .18s ease;
}

.group-card.is-open {
  border-color: var(--line-strong);
  box-shadow: 0 10px 28px rgba(25, 26, 28, .05);
}

[data-theme="night"] .group-card.is-open { box-shadow: 0 10px 28px rgba(0, 0, 0, .28); }

.group-head {
  display: flex;
  align-items: center;
  gap: 4px;
  padding-right: 6px;
}

.group-toggle {
  flex: 1 1 auto;
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
  padding: 13px 2px 13px 14px;
  border: 0;
  background: none;
  text-align: left;
}

.group-flag {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  flex: 0 0 auto;
  border: 1px solid var(--line);
  border-radius: 50%;
  background: var(--paper-2);
  font-size: 15px;
  line-height: 1;
}

.group-flag.is-manual {
  font-size: 14px;
  font-family: var(--mono);
  color: var(--muted);
}

.group-copy {
  display: flex;
  min-width: 0;
  flex-direction: column;
  gap: 3px;
}

.group-name {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.group-meta {
  font-family: var(--mono);
  font-size: 8.5px;
  letter-spacing: .03em;
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.group-count {
  margin-left: auto;
  padding: 2px 7px;
  border: 1px solid var(--line-strong);
  font-family: var(--mono);
  font-size: 8.5px;
  color: var(--muted);
  font-variant-numeric: tabular-nums;
}

.group-chevron {
  width: 7px;
  height: 7px;
  margin: 0 8px 0 10px;
  flex: 0 0 auto;
  border-right: 1px solid var(--muted);
  border-bottom: 1px solid var(--muted);
  transform: rotate(45deg) translateY(-2px);
  transition: transform .2s ease;
}

.group-card.is-open .group-chevron { transform: rotate(225deg) translateY(-2px); }

.group-tools {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 0 0 auto;
}

.group-action {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  padding: 0;
  border: 0;
  background: none;
  color: var(--muted);
  font-family: var(--mono);
  font-size: 13px;
  line-height: 1;
  transition: color .15s ease;
}

.group-action:hover { color: var(--accent); }
.group-action.is-danger:hover { color: var(--danger); }
.group-action[disabled] { opacity: .45; }

.group-body {
  display: none;
  padding: 0 14px;
  border-top: 1px solid var(--line);
}

.group-card.is-open .group-body { display: block; }

.group-body .server-row { padding: 11px 0; }
.group-body .server-item:last-child .server-row { border-bottom: 0; }
.group-body .sub-note {
  padding: 12px 0;
  border-top: 1px solid var(--line);
  font-family: var(--mono);
  font-size: 8.5px;
  line-height: 1.5;
  color: var(--muted);
}

/* ── Формы ─────────────────────────────────────────────── */""",
     'happ-css')

# ── JS: новые рендереры ─────────────────────────────────────────────────────
rep8("""  function renderServers() {
    const sorted = state.servers.slice().sort(function (a, b) {
      return (a.city || '').localeCompare(b.city || '', 'ru');
    }).filter(matchesQuery);""",
     """  function renderServersUnused() {
    const sorted = state.servers.slice().sort(function (a, b) {
      return (a.city || '').localeCompare(b.city || '', 'ru');
    }).filter(matchesQuery);""",
     'happ-dead-render')

rep8("""  function renderSubs() {
    const sorted = state.subs.slice().sort(function (a, b) {
      return a.name.localeCompare(b.name, 'ru');
    });""",
     """  function renderSubsUnused() {
    const sorted = state.subs.slice().sort(function (a, b) {
      return a.name.localeCompare(b.name, 'ru');
    });""",
     'happ-dead-subs')

rep8("""  function selectServer(id, goHome) {""",
     """  function groupKey(sub) {
    return sub ? 'sub:' + sub.id : 'manual';
  }

  function isGroupOpen(key) {
    return state.expanded[key] !== false;
  }

  function toggleGroup(key) {
    state.expanded[key] = !isGroupOpen(key);
    store.write('vpn.expanded', state.expanded);
    renderServers();
  }

  function groupFlag(sub) {
    const list = state.subs.length ? null : null;
    const servers = state.servers.filter(function (server) { return server.subId === (sub ? sub.id : ''); });
    for (let i = 0; i < servers.length; i += 1) {
      if (servers[i].flag) return servers[i].flag;
    }
    return '';
  }

  function groupLatency(servers) {
    let best = null;
    servers.forEach(function (server) {
      const entry = state.latency[server.id];
      if (entry && Number.isFinite(entry.ms) && (best == null || entry.ms < best)) best = entry.ms;
    });
    return best;
  }

  function buildServerRow(server, removable) {
    const item = document.createElement('div');
    item.className = 'server-item';

    const row = document.createElement('button');
    row.type = 'button';
    row.className = 'server-row' + (server.id === state.selectedId ? ' is-selected' : '');
    row.dataset.id = server.id;
    if (server.id === state.selectedId) row.setAttribute('aria-current', 'true');

    const aria = ['Выбрать сервер: ' + server.city];
    if (server.country) aria.push(server.country);
    if (server.protocol) aria.push(server.protocol);
    row.setAttribute('aria-label', aria.join(', '));

    const flag = document.createElement('span');
    flag.className = 'server-flag' + (server.flag ? '' : ' is-unknown');
    flag.textContent = server.flag || '—';
    flag.setAttribute('aria-hidden', 'true');

    const copy = document.createElement('span');
    copy.className = 'server-copy';
    const city = document.createElement('span');
    city.className = 'server-city';
    city.textContent = server.city;
    const sub = document.createElement('span');
    sub.className = 'server-sub';
    sub.textContent = [server.country || 'Локация не определена', sourceText(server)].filter(Boolean).join(' · ');
    const ping = latencyText(server);
    if (ping) {
      sub.appendChild(document.createTextNode(' · '));
      const pingEl = document.createElement('span');
      pingEl.className = 'server-ping' + ping.className;
      pingEl.textContent = ping.text;
      sub.appendChild(pingEl);
    }
    copy.appendChild(city);
    copy.appendChild(sub);

    const proto = document.createElement('span');
    proto.className = 'server-proto';
    proto.textContent = server.protocol || '';

    const action = document.createElement('span');
    action.className = 'server-action';
    action.setAttribute('aria-hidden', 'true');

    row.appendChild(flag);
    row.appendChild(copy);
    row.appendChild(proto);
    row.appendChild(action);

    row.addEventListener('click', function () { selectServer(server.id, true); });
    item.appendChild(row);

    if (removable) {
      const remove = document.createElement('button');
      remove.type = 'button';
      remove.className = 'row-remove';
      remove.setAttribute('aria-label', 'Удалить сервер ' + server.city);
      remove.textContent = '×';
      remove.addEventListener('click', function (event) {
        event.stopPropagation();
        deleteServer(server.id);
      });
      item.appendChild(remove);
    }

    return item;
  }

  function buildGroupCard(options) {
    const key = options.key;
    const open = isGroupOpen(key);
    const servers = options.servers;

    const card = document.createElement('section');
    card.className = 'group-card' + (open ? ' is-open' : '');
    card.dataset.key = key;

    const head = document.createElement('div');
    head.className = 'group-head';

    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'group-toggle';
    toggle.setAttribute('aria-expanded', String(open));

    const flag = document.createElement('span');
    const flagText = options.flag;
    flag.className = 'group-flag' + (flagText ? '' : ' is-manual');
    flag.textContent = flagText || (options.manual ? '✎' : '⌁');
    flag.setAttribute('aria-hidden', 'true');

    const copy = document.createElement('span');
    copy.className = 'group-copy';
    const name = document.createElement('span');
    name.className = 'group-name';
    name.textContent = options.name;

    const meta = document.createElement('span');
    meta.className = 'group-meta';
    const parts = [];
    parts.push(servers.length + ' ' + plural(servers.length, ['сервер', 'сервера', 'серверов']));
    if (options.updatedAt) parts.push(formatUpdated(options.updatedAt));
    const best = groupLatency(servers);
    if (best != null) parts.push(best + ' мс');
    meta.textContent = parts.join(' · ');

    copy.appendChild(name);
    copy.appendChild(meta);

    const count = document.createElement('span');
    count.className = 'group-count';
    count.textContent = String(servers.length);

    const chevron = document.createElement('span');
    chevron.className = 'group-chevron';
    chevron.setAttribute('aria-hidden', 'true');

    toggle.appendChild(flag);
    toggle.appendChild(copy);
    toggle.appendChild(count);
    toggle.appendChild(chevron);
    toggle.addEventListener('click', function () { toggleGroup(key); });

    const tools = document.createElement('div');
    tools.className = 'group-tools';

    if (options.sub) {
      const refresh = document.createElement('button');
      refresh.type = 'button';
      refresh.className = 'group-action';
      refresh.textContent = '⟳';
      refresh.title = 'Обновить подписку';
      refresh.setAttribute('aria-label', 'Обновить подписку ' + options.name);
      refresh.addEventListener('click', function (event) {
        event.stopPropagation();
        refreshSub(options.sub.id, refresh);
      });
      tools.appendChild(refresh);

      const remove = document.createElement('button');
      remove.type = 'button';
      remove.className = 'group-action is-danger';
      remove.textContent = '×';
      remove.title = 'Удалить подписку';
      remove.setAttribute('aria-label', 'Удалить подписку ' + options.name);
      remove.addEventListener('click', function (event) {
        event.stopPropagation();
        deleteSub(options.sub.id);
      });
      tools.appendChild(remove);
    }

    head.appendChild(toggle);
    head.appendChild(tools);
    card.appendChild(head);

    const body = document.createElement('div');
    body.className = 'group-body';
    if (!servers.length) {
      const empty = document.createElement('p');
      empty.className = 'sub-note';
      empty.textContent = options.manual
        ? 'Добавьте ссылку vless://, trojan://, vmess:// или ss:// — сервер появится здесь.'
        : 'В подписке пока нет серверов. Нажмите ⟳, чтобы обновить.';
      body.appendChild(empty);
    } else {
      servers.forEach(function (server) {
        body.appendChild(buildServerRow(server, !!options.manual));
      });
    }
    card.appendChild(body);
    return card;
  }

  function renderServers() {
    const container = document.getElementById('group-list');
    if (!container) return;
    container.textContent = '';

    const key = function (server) { return (server.city || '').toLowerCase(); };
    const query = state.query;
    const cards = [];

    state.subs.forEach(function (sub) {
      const all = state.servers.filter(function (server) { return server.subId === sub.id; });
      const list = all.slice().sort(function (a, b) { return key(a).localeCompare(key(b), 'ru'); }).filter(matchesQuery);
      if (query && !list.length) return;
      cards.push({
        key: groupKey(sub),
        name: sub.name,
        sub: sub,
        servers: list,
        flag: groupFlag(sub),
        updatedAt: sub.updatedAt,
        manual: false
      });
    });

    const manual = state.servers.filter(function (server) { return !server.subId; })
      .sort(function (a, b) { return key(a).localeCompare(key(b), 'ru'); });
    if (manual.length) {
      const list = manual.filter(matchesQuery);
      if (!query || list.length) {
        cards.push({
          key: 'manual',
          name: 'Вручную',
          sub: null,
          servers: list,
          flag: '',
          manual: true
        });
      }
    }

    cards.forEach(function (card) { container.appendChild(buildGroupCard(card)); });

    const found = cards.reduce(function (acc, card) { return acc + card.servers.length; }, 0);
    ui.serversEmpty.hidden = state.servers.length !== 0;
    if (ui.serverTools) ui.serverTools.hidden = state.servers.length === 0;
    if (ui.noMatch) ui.noMatch.hidden = !(query && found === 0 && state.servers.length > 0);
    updateMeta();
    markSelectedRow();
  }

  function renderSubs() {
    // подписки живут внутри общего списка групп
  }

  function selectServer(id, goHome) {""",
     'happ-render')

rep8("""    view: 'home',
    query: '',
    latency: {},
    latencyAt: 0
  };""",
     """    view: 'home',
    query: '',
    latency: {},
    latencyAt: 0,
    expanded: store.read('vpn.expanded', {})
  };""",
     'happ-state')

open(DST, 'w', encoding='utf-8').write(s)
print('pass8 OK: %d edits total' % len(done))

# ═══════════════ pass 9: реальный туннель (Xray core) ════════════════════════
s = open(DST, encoding='utf-8').read()


def rep9(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# ── HTML: строка трафика ────────────────────────────────────────────────────
rep9("""    <p class="conn-status" id="conn-status" role="status" aria-live="polite">Нет сервера</p>""",
     """    <p class="conn-status" id="conn-status" role="status" aria-live="polite">Нет сервера</p>
    <p class="conn-stats" id="conn-stats" hidden></p>""",
     'vpn-stats-html')

# ── CSS: состояния кнопки и трафик ──────────────────────────────────────────
rep9(""".conn-status.is-on { color: var(--accent); }""",
     """.conn-status.is-on { color: var(--accent); }
.conn-status.is-error { color: var(--danger); }

.conn-stats {
  font-family: var(--mono);
  font-size: 8.5px;
  letter-spacing: .04em;
  color: var(--muted);
  font-variant-numeric: tabular-nums;
  text-shadow: 0 0 8px var(--halo), 0 0 2px var(--halo);
  white-space: nowrap;
}

.connect.is-connecting {
  background: var(--paper-2);
  color: var(--ink);
  border: 1px solid var(--accent);
  animation: connect-pulse 1.6s ease-in-out infinite;
}

.connect.is-connecting:hover { background: var(--paper-2); }

.connect.is-error {
  background: var(--paper-2);
  color: var(--danger);
  border: 1px solid var(--danger);
}

@keyframes connect-pulse {
  0%, 100% { box-shadow: 0 12px 30px var(--shadow), 0 0 0 0 var(--accent-soft); }
  50% { box-shadow: 0 12px 30px var(--shadow), 0 0 0 12px transparent; }
}

html[data-reduced="true"] .connect.is-connecting { animation: none; }

.group-body .server-row .row-remove { right: 0; }""",
     'vpn-stats-css')

# ── JS: построение конфигурации Xray ────────────────────────────────────────
rep9("""  function pingAll(silent) {""",
     """  // ── Конфигурация ядра Xray ───────────────────────────────────────────────

  function queryMap(raw) {
    const result = {};
    String(raw || '').split('&').forEach(function (pair) {
      if (!pair) return;
      const index = pair.indexOf('=');
      const key = index < 0 ? pair : pair.slice(0, index);
      const value = index < 0 ? '' : pair.slice(index + 1);
      result[decodeURIComponent(key.replace(/\\+/g, ' '))] = safeDecode(value);
    });
    return result;
  }

  function splitAuthority(rest) {
    const at = rest.lastIndexOf('@');
    const userinfo = at >= 0 ? rest.slice(0, at) : '';
    let hostPort = at >= 0 ? rest.slice(at + 1) : rest;
    hostPort = hostPort.replace(/\\/(?!.*\\/).*$/, '');
    const parsed = splitHostPort(hostPort);
    if (!parsed) return null;
    return { userinfo: userinfo, host: parsed.host, port: parsed.port };
  }

  function cleanObject(value) {
    if (Array.isArray(value)) {
      const list = value.map(cleanObject).filter(function (item) { return item !== undefined; });
      return list.length ? list : undefined;
    }
    if (value && typeof value === 'object') {
      const out = {};
      Object.keys(value).forEach(function (key) {
        const cleaned = cleanObject(value[key]);
        if (cleaned !== undefined && cleaned !== '' && cleaned !== null) out[key] = cleaned;
      });
      return Object.keys(out).length ? out : undefined;
    }
    return value;
  }

  function xrayStream(params, host, security, fallbackSni) {
    const networkRaw = String(params.network || params.type || 'tcp').toLowerCase();
    const network = networkRaw === 'h2' ? 'http' : networkRaw;
    const sec = String(security || params.security || 'none').toLowerCase();
    const sni = params.sni || params.peer || params.host || fallbackSni || host;
    const alpn = params.alpn ? String(params.alpn).split(',').map(function (item) { return item.trim(); }).filter(Boolean) : null;
    const fp = params.fp || params.fingerprint || '';

    const stream = { network: network };

    if (sec === 'tls' || sec === 'xtls') {
      stream.security = 'tls';
      stream.tlsSettings = {
        serverName: sni,
        allowInsecure: params.allowInsecure === '1' || params.insecure === '1' || params.allowinsecure === '1'
      };
      if (fp) stream.tlsSettings.fingerprint = fp;
      if (alpn && alpn.length) stream.tlsSettings.alpn = alpn;
    } else if (sec === 'reality') {
      stream.security = 'reality';
      stream.realitySettings = {
        serverName: sni,
        fingerprint: fp || 'chrome',
        publicKey: params.pbk || '',
        shortId: params.sid || '',
        spiderX: params.spx || '/'
      };
    } else {
      stream.security = 'none';
    }

    if (network === 'ws') {
      stream.wsSettings = { path: params.path ? params.path : '/' };
      if (params.host) stream.wsSettings.headers = { Host: params.host };
    } else if (network === 'grpc') {
      stream.grpcSettings = {
        serviceName: params.serviceName || params.path || '',
        multiMode: params.mode === 'multi'
      };
    } else if (network === 'http') {
      stream.httpSettings = { path: params.path || '/' };
      if (params.host) stream.httpSettings.host = String(params.host).split(',').map(function (h) { return h.trim(); });
    } else if (network === 'tcp') {
      if ((params.headerType || '').toLowerCase() === 'http') {
        stream.tcpSettings = {
          header: {
            type: 'http',
            request: {
              path: [params.path || '/'],
              headers: { Host: [params.host || host] }
            }
          }
        };
      } else {
        stream.tcpSettings = { header: { type: 'none' } };
      }
    } else if (network === 'kcp') {
      stream.kcpSettings = { seed: params.seed || '', header: { type: params.headerType || 'none' } };
    } else if (network === 'quic') {
      stream.quicSettings = {
        security: params.quicSecurity || 'none',
        key: params.key || '',
        header: { type: params.headerType || 'none' }
      };
    } else if (network === 'xhttp' || network === 'splithttp') {
      stream.network = 'xhttp';
      stream.xhttpSettings = { path: params.path || '/', host: params.host || sni, mode: params.mode || 'auto' };
    }

    return stream;
  }

  function buildOutbound(server) {
    const raw = String(server.link || '').trim();
    const match = raw.match(/^([a-z0-9+.-]+):\\/\\//i);
    if (!match) return { ok: false, reason: 'Ссылка сервера не распознана' };
    const scheme = match[1].toLowerCase();
    let rest = raw.slice(match[0].length);

    const hash = rest.indexOf('#');
    if (hash >= 0) rest = rest.slice(0, hash);
    let params = {};
    const q = rest.indexOf('?');
    if (q >= 0) {
      params = queryMap(rest.slice(q + 1));
      rest = rest.slice(0, q);
    }

    if (scheme === 'vmess') {
      let json = null;
      try { json = JSON.parse(decodeBase64(rest)); } catch (error) { json = null; }
      if (!json || !json.add || !json.port || !json.id) {
        return { ok: false, reason: 'VMess-ссылка повреждена' };
      }
      const legacy = {
        network: json.net,
        security: json.tls === 'tls' ? 'tls' : (json.tls === 'reality' ? 'reality' : 'none'),
        sni: json.sni,
        host: json.host,
        path: json.path,
        alpn: json.alpn,
        fp: json.fp,
        headerType: json.type
      };
      return {
        ok: true,
        outbound: {
          tag: 'proxy',
          protocol: 'vmess',
          settings: {
            vnext: [{
              address: String(json.add),
              port: Number(json.port),
              users: [{
                id: String(json.id),
                alterId: Number(json.aid) || 0,
                security: json.scy || 'auto'
              }]
            }]
          },
          streamSettings: xrayStream(legacy, String(json.add), legacy.security, json.host)
        }
      };
    }

    if (scheme === 'ss') {
      let body = rest;
      if (body.indexOf('@') === -1) {
        let decoded = '';
        try { decoded = decodeBase64(body); } catch (error) { decoded = ''; }
        if (!decoded || decoded.indexOf('@') === -1) return { ok: false, reason: 'Shadowsocks-ссылка повреждена' };
        body = decoded;
      }
      const at = body.lastIndexOf('@');
      let credentials = body.slice(0, at);
      const hostPort = body.slice(at + 1);
      if (credentials.indexOf(':') === -1) {
        try { credentials = decodeBase64(credentials); } catch (error) { /* как есть */ }
      }
      const sep = credentials.indexOf(':');
      if (sep < 0) return { ok: false, reason: 'В ссылке нет метода и пароля' };
      const parsed = splitHostPort(hostPort);
      if (!parsed) return { ok: false, reason: 'Не разобрать адрес сервера' };
      return {
        ok: true,
        outbound: {
          tag: 'proxy',
          protocol: 'shadowsocks',
          settings: {
            servers: [{
              address: parsed.host,
              port: parsed.port,
              method: credentials.slice(0, sep),
              password: credentials.slice(sep + 1)
            }]
          },
          streamSettings: { network: 'tcp', security: 'none' }
        }
      };
    }

    const authority = splitAuthority(rest);
    if (!authority) return { ok: false, reason: 'Не разобрать адрес сервера' };

    if (scheme === 'vless') {
      if (!authority.userinfo) return { ok: false, reason: 'В ссылке нет UUID' };
      return {
        ok: true,
        outbound: {
          tag: 'proxy',
          protocol: 'vless',
          settings: {
            vnext: [{
              address: authority.host,
              port: authority.port,
              users: [{
                id: decodeURIComponent(authority.userinfo),
                encryption: params.encryption || 'none',
                flow: params.flow || ''
              }]
            }]
          },
          streamSettings: xrayStream(params, authority.host, params.security, params.sni)
        }
      };
    }

    if (scheme === 'trojan') {
      return {
        ok: true,
        outbound: {
          tag: 'proxy',
          protocol: 'trojan',
          settings: {
            servers: [{
              address: authority.host,
              port: authority.port,
              password: decodeURIComponent(authority.userinfo),
              flow: params.flow || ''
            }]
          },
          streamSettings: xrayStream(params, authority.host, params.security || 'tls', params.sni)
        }
      };
    }

    if (scheme === 'hysteria2' || scheme === 'hy2' || scheme === 'tuic') {
      return { ok: false, reason: 'Ядро Xray не умеет ' + (scheme === 'tuic' ? 'TUIC' : 'Hysteria2') + ' — нужен другой сервер (VLESS, Trojan, VMess или Shadowsocks)' };
    }

    return { ok: false, reason: 'Протокол ' + scheme + ' пока не поддерживается' };
  }

  function buildXrayConfig(server) {
    const built = buildOutbound(server);
    if (!built.ok) return built;

    const config = {
      log: { loglevel: 'warning' },
      stats: {},
      policy: {
        levels: { '8': { handshake: 4, connIdle: 300, uplinkOnly: 1, downlinkOnly: 1 } },
        system: { statsOutboundUplink: true, statsOutboundDownlink: true }
      },
      inbounds: [{
        tag: 'tun',
        protocol: 'tun',
        settings: { name: 'xray0', MTU: 1500, userLevel: 8 },
        sniffing: { enabled: true, destOverride: ['http', 'tls', 'quic'] }
      }],
      outbounds: [
        built.outbound,
        { tag: 'direct', protocol: 'freedom', streamSettings: { sockopt: { domainStrategy: 'UseIP' } } },
        { tag: 'block', protocol: 'blackhole' }
      ],
      routing: {
        domainStrategy: 'AsIs',
        rules: [{
          type: 'field',
          ip: ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '100.64.0.0/10', '127.0.0.0/8', '169.254.0.0/16'],
          outboundTag: 'direct'
        }]
      },
      dns: {
        servers: ['1.1.1.1', '8.8.8.8'],
        queryStrategy: 'UseIPv4'
      }
    };

    const cleaned = cleanObject(config);
    return { ok: true, config: cleaned, protocol: built.outbound.protocol };
  }

  function pingAll(silent) {""",
     'vpn-xray-config')

open(DST, 'w', encoding='utf-8').write(s)
print('pass9 OK: %d edits total' % len(done))

# ═══════════════ pass 10: подключение через Xray ═════════════════════════════
s = open(DST, encoding='utf-8').read()


def rep10(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep10("""    connStatus: $('#conn-status'),""",
      """    connStatus: $('#conn-status'),
    connStats: $('#conn-stats'),""",
      'vpn-ui-ref')

rep10("""  function setHomeClasses() {
    const server = selectedServer();
    const empty = !server;
    ui.connect.classList.toggle('is-empty', empty);
    ui.connect.classList.toggle('is-on', !empty && state.connected);
    ui.connStatus.classList.toggle('is-on', !empty && state.connected);
    if (empty) {
      ui.connStatus.textContent = state.servers.length ? 'Выберите сервер' : 'Нет сервера';
      ui.pathTo.textContent = '—';
      ui.pathTo.classList.add('is-empty');
      ui.path.hidden = true;
      ui.connect.setAttribute('aria-label', state.servers.length ? 'Выбрать сервер' : 'Добавить сервер');
      return;
    }
    ui.connStatus.textContent = state.connected ? 'Защищено' : 'Не подключено';
    const label = server.flag ? server.flag + ' ' + server.city : server.city;
    ui.pathTo.textContent = label;
    ui.pathTo.classList.remove('is-empty');
    ui.path.hidden = false;
    ui.connect.setAttribute('aria-label', state.connected ? 'Отключить' : 'Подключить');
  }""",
      """  function formatBytes(value) {
    const size = Number(value) || 0;
    if (size < 1024) return size + ' Б';
    const units = ['КБ', 'МБ', 'ГБ', 'ТБ'];
    let index = -1;
    let rest = size;
    do {
      rest /= 1024;
      index += 1;
    } while (rest >= 1024 && index < units.length - 1);
    return (rest >= 10 ? rest.toFixed(0) : rest.toFixed(1)) + ' ' + units[index];
  }

  function formatDuration(seconds) {
    const total = Math.max(0, Math.floor(Number(seconds) || 0));
    const h = Math.floor(total / 3600);
    const m = Math.floor((total % 3600) / 60);
    const s = total % 60;
    const two = function (value) { return String(value).padStart(2, '0'); };
    return h > 0 ? h + ':' + two(m) + ':' + two(s) : two(m) + ':' + two(s);
  }

  function vpnStateName() {
    return state.vpn && state.vpn.state ? state.vpn.state : 'idle';
  }

  function setHomeClasses() {
    const server = selectedServer();
    const empty = !server;
    const vpn = vpnStateName();
    const busy = vpn === 'connecting';
    const online = vpn === 'connected';
    const failed = vpn === 'error';

    ui.connect.classList.toggle('is-empty', empty);
    ui.connect.classList.toggle('is-on', !empty && online);
    ui.connect.classList.toggle('is-connecting', !empty && busy);
    ui.connect.classList.toggle('is-error', !empty && failed);
    ui.connStatus.classList.toggle('is-on', !empty && online);
    ui.connStatus.classList.toggle('is-error', !empty && failed);

    if (ui.connStats) {
      if (online) {
        ui.connStats.hidden = false;
        ui.connStats.textContent = '↓ ' + formatBytes(state.vpn.down)
          + '  ↑ ' + formatBytes(state.vpn.up)
          + '  ·  ' + formatDuration(state.vpn.seconds);
      } else {
        ui.connStats.hidden = true;
      }
    }

    if (empty) {
      ui.connStatus.textContent = state.servers.length ? 'Выберите сервер' : 'Нет сервера';
      ui.pathTo.textContent = '—';
      ui.pathTo.classList.add('is-empty');
      ui.path.hidden = true;
      ui.connect.setAttribute('aria-label', state.servers.length ? 'Выбрать сервер' : 'Добавить сервер');
      return;
    }

    if (busy) ui.connStatus.textContent = 'Подключение…';
    else if (online) ui.connStatus.textContent = 'Защищено';
    else if (failed) ui.connStatus.textContent = (state.vpn.error || 'Ошибка').slice(0, 48);
    else ui.connStatus.textContent = 'Не подключено';

    const label = server.flag ? server.flag + ' ' + server.city : server.city;
    ui.pathTo.textContent = label;
    ui.pathTo.classList.remove('is-empty');
    ui.path.hidden = false;
    ui.connect.setAttribute('aria-label', online || busy ? 'Отключить' : 'Подключить');
  }

  function applyVpnState(next) {
    const previous = state.vpn.state;
    state.vpn.state = next.state;
    state.vpn.error = next.error || '';
    state.vpn.up = Number(next.up) || 0;
    state.vpn.down = Number(next.down) || 0;
    state.vpn.seconds = Number(next.seconds) || 0;

    const online = next.state === 'connected';
    state.connected = online;
    globe.setConnected(online);

    if (previous !== next.state) {
      const server = selectedServer();
      const label = server ? (server.flag ? server.flag + ' ' + server.city : server.city) : '';
      if (online) {
        haptic();
        showToast(label ? 'Подключено: ' + label : 'Туннель активен');
      } else if (next.state === 'error') {
        showToast('Ошибка: ' + (next.error || 'соединение не установлено'), { duration: 7000 });
      }
      if (previous === 'connecting' || online || next.state === 'error') renderServers();
    }
    updateHome();
  }

  window.__onVpnState = function (payload) {
    let data = null;
    try { data = JSON.parse(payload); } catch (error) { data = null; }
    if (!data || typeof data !== 'object') return;
    applyVpnState(data);
  };

  function startConnection() {
    const server = selectedServer();
    if (!server) {
      if (!state.servers.length) openAddServer();
      else showView('servers');
      return;
    }
    const built = buildXrayConfig(server);
    if (!built.ok) {
      showToast(built.reason, { duration: 7000 });
      applyVpnState({ state: 'error', error: built.reason });
      return;
    }
    if (!native || typeof native.connect !== 'function') {
      showToast('Туннель включается в приложении для Android', { duration: 6000 });
      return;
    }
    applyVpnState({ state: 'connecting', error: '' });
    try {
      native.connect(JSON.stringify(built.config),
        server.flag ? server.flag + ' ' + server.city : server.city);
    } catch (error) {
      applyVpnState({ state: 'error', error: 'Не удалось запустить ядро' });
      return;
    }
    window.setTimeout(function () {
      if (vpnStateName() === 'connecting') {
        applyVpnState({ state: 'error', error: 'Ядро не ответило за 15 секунд' });
      }
    }, 15000);
  }

  function stopConnection() {
    if (native && typeof native.disconnect === 'function') {
      try { native.disconnect(); } catch (error) { /* уже остановлено */ }
    }
    applyVpnState({ state: 'idle', error: '' });
  }""",
      'vpn-home')

rep10("""  ui.connect.addEventListener('click', function () {
    const server = selectedServer();
    if (!server) {
      if (!state.servers.length) openAddServer();
      else showView('servers');
      return;
    }
    state.connected = !state.connected;
    globe.setConnected(state.connected);
    updateHome();
    haptic();
  });""",
      """  ui.connect.addEventListener('click', function () {
    const server = selectedServer();
    if (!server) {
      if (!state.servers.length) openAddServer();
      else showView('servers');
      return;
    }
    const vpn = vpnStateName();
    if (vpn === 'connected' || vpn === 'connecting' || vpn === 'error') {
      stopConnection();
      return;
    }
    startConnection();
  });""",
      'vpn-click')

rep10("""  if (settings.autoconnect && state.selectedId) {
    window.setTimeout(function () {
      state.connected = true;
      globe.setConnected(true);
      updateHome();
    }, 350);
  }""",
      """  if (native && typeof native.vpnState === 'function') {
    try {
      const initial = native.vpnState();
      if (initial) window.__onVpnState(initial);
    } catch (error) { /* состояние придёт позже */ }
  }

  if (settings.autoconnect && state.selectedId) {
    window.setTimeout(function () {
      if (vpnStateName() === 'idle') startConnection();
    }, 900);
  }""",
      'vpn-autoconnect')

rep10("""    connected: false,
    view: 'home',""",
      """    connected: false,
    vpn: { state: 'idle', error: '', up: 0, down: 0, seconds: 0 },
    view: 'home',""",
      'vpn-state-init')

open(DST, 'w', encoding='utf-8').write(s)
print('pass10 OK: %d edits total' % len(done))

# ═══════════════ pass 11: stats в конфиге + реконнект при смене сервера ══════
s = open(DST, encoding='utf-8').read()


def rep11(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# cleanObject вырезает пустые объекты, а ядру нужен "stats": {} — добавляем после очистки
rep11("""    const cleaned = cleanObject(config);
    return { ok: true, config: cleaned, protocol: built.outbound.protocol };""",
      """    const cleaned = cleanObject(config) || {};
    // "stats": {} обязателен: без него ядро не считает трафик по тегам
    cleaned.stats = {};
    return { ok: true, config: cleaned, protocol: built.outbound.protocol };""",
      'xray-stats')

rep11("""  function selectServer(id, goHome) {""",
      """  function reconnectIfActive() {
    const vpn = vpnStateName();
    if (vpn !== 'connected' && vpn !== 'connecting') return;
    if (!native || typeof native.connect !== 'function') return;
    window.setTimeout(function () { startConnection(); }, 220);
  }

  function selectServer(id, goHome) {""",
      'reconnect-fn')

rep11("""  function selectServer(id, goHome) {
    const server = findServer(id);
    if (!server) return;
    state.selectedId = id;
    persist();
    globe.select(id, { notify: false });
    updateHome();
    markSelectedRow();
    if (goHome) showView('home');
  }""",
      """  function selectServer(id, goHome) {
    const server = findServer(id);
    if (!server) return;
    const changed = state.selectedId !== id;
    state.selectedId = id;
    persist();
    globe.select(id, { notify: false });
    updateHome();
    markSelectedRow();
    if (goHome) showView('home');
    if (changed) reconnectIfActive();
  }""",
      'select-reconnect')

open(DST, 'w', encoding='utf-8').write(s)
print('pass11 OK: %d edits total' % len(done))

# ═══════════════ pass 12: мягкие ошибки валидации ════════════════════════════
s = open(DST, encoding='utf-8').read()


def rep12(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep12("""    const built = buildXrayConfig(server);
    if (!built.ok) {
      showToast(built.reason, { duration: 7000 });
      applyVpnState({ state: 'error', error: built.reason });
      return;
    }""",
      """    const built = buildXrayConfig(server);
    if (!built.ok) {
      showToast(built.reason, { duration: 7000 });
      return;
    }""",
      'soft-error')

rep12("""      return { ok: false, reason: 'Ядро Xray не умеет ' + (scheme === 'tuic' ? 'TUIC' : 'Hysteria2') + ' — нужен другой сервер (VLESS, Trojan, VMess или Shadowsocks)' };""",
      """      return { ok: false, reason: (scheme === 'tuic' ? 'TUIC' : 'Hysteria2') + ' не поддерживается ядром Xray. Нужен VLESS, Trojan, VMess или Shadowsocks.' };""",
      'hy2-msg')

rep12("""    return { ok: false, reason: 'Протокол ' + scheme + ' пока не поддерживается' };""",
      """    return { ok: false, reason: 'Протокол ' + scheme + ' не поддерживается' };""",
      'proto-msg')

open(DST, 'w', encoding='utf-8').write(s)
print('pass12 OK: %d edits total' % len(done))

# ═══════════════ pass 13: шлифовка групп ═════════════════════════════════════
s = open(DST, encoding='utf-8').read()


def rep13(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# поиск уступает место кнопке «Проверка…», чтобы ничего не обрезалось
rep13(""".search {
  flex: 1 1 auto;
  min-width: 0;""",
      """.search {
  flex: 1 1 0;
  min-width: 0;""",
      'search-flex')

rep13(""".conn-stats {
  font-family: var(--mono);""",
      """.conn-stats {
  margin-top: 5px;
  font-family: var(--mono);""",
      'stats-margin')

# в свёрнутой группе видно, какой сервер из неё выбран
rep13("""    const meta = document.createElement('span');
    meta.className = 'group-meta';
    const parts = [];
    parts.push(servers.length + ' ' + plural(servers.length, ['сервер', 'сервера', 'серверов']));
    if (options.updatedAt) parts.push(formatUpdated(options.updatedAt));
    const best = groupLatency(servers);
    if (best != null) parts.push(best + ' мс');
    meta.textContent = parts.join(' · ');""",
      """    const meta = document.createElement('span');
    meta.className = 'group-meta';
    const parts = [];
    if (!open && options.activeCity) {
      parts.push('● ' + options.activeCity);
    } else {
      parts.push(servers.length + ' ' + plural(servers.length, ['сервер', 'сервера', 'серверов']));
      if (options.updatedAt) parts.push(formatUpdated(options.updatedAt));
      const best = groupLatency(servers);
      if (best != null) parts.push(best + ' мс');
    }
    meta.textContent = parts.join(' · ');""",
      'group-active-city')

rep13("""    cards.forEach(function (card) { container.appendChild(buildGroupCard(card)); });""",
      """    const activeServer = selectedServer();
    cards.forEach(function (card) {
      if (activeServer && card.servers.some(function (item) { return item.id === activeServer.id; })) {
        card.activeCity = activeServer.flag ? activeServer.flag + ' ' + activeServer.city : activeServer.city;
      }
      container.appendChild(buildGroupCard(card));
    });""",
      'group-active-pass')

open(DST, 'w', encoding='utf-8').write(s)
print('pass13 OK: %d edits total' % len(done))

# ═══════════════ pass 14: короткий ярлык замера ══════════════════════════════
s = open(DST, encoding='utf-8').read()
if s.count("ui.pingAll.textContent = 'Проверка…';") != 1:
    print('!! ping label'); sys.exit(1)
s = s.replace("ui.pingAll.textContent = 'Проверка…';", "ui.pingAll.textContent = 'Тест…';")
done.append('ping-label')
open(DST, 'w', encoding='utf-8').write(s)
print('pass14 OK: %d edits total' % len(done))

# ═══════════════ pass 15: меньше работы на каждом тике ═══════════════════════
s = open(DST, encoding='utf-8').read()


def rep15(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep15("""    const online = next.state === 'connected';
    state.connected = online;
    globe.setConnected(online);
""",
      """    const online = next.state === 'connected';
    const changed = previous !== next.state;
    state.connected = online;
    if (changed) globe.setConnected(online);
""",
      'vpn-globe-guard')

rep15("""    if (previous !== next.state) {
      const server = selectedServer();""",
      """    if (changed) {
      const server = selectedServer();""",
      'vpn-changed')

open(DST, 'w', encoding='utf-8').write(s)
print('pass15 OK: %d edits total' % len(done))

# ═══════════════ pass 16: SF Pro Rounded + настоящий liquid glass ════════════
import base64, math, struct, zlib

s = open(DST, encoding='utf-8').read()


def rep16(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


def font_face(name, weight, path):
    data = base64.b64encode(open(path, 'rb').read()).decode()
    return ("@font-face{font-family:'SF Pro Rounded';font-style:normal;font-weight:%d;font-display:swap;"
            "src:url(data:font/woff2;base64,%s) format('woff2')}" % (weight, data))


FONTS = ''.join([
    font_face('SF Pro Rounded', 400, ROOT + '/fonts/Regular.woff2'),
    font_face('SF Pro Rounded', 500, ROOT + '/fonts/Medium.woff2'),
    font_face('SF Pro Rounded', 600, ROOT + '/fonts/Semibold.woff2'),
    font_face('SF Pro Rounded', 700, ROOT + '/fonts/Bold.woff2'),
])


def lens_png(w, h, rim):
    """Карта нормалей скруглённого прямоугольника: преломление у кромки."""
    radius = h / 2.0

    def sdf(x, y):
        qx = abs(x - w / 2.0) - (w / 2.0 - radius)
        qy = abs(y - h / 2.0) - (h / 2.0 - radius)
        ax = max(qx, 0.0)
        ay = max(qy, 0.0)
        return math.hypot(ax, ay) + min(max(qx, qy), 0.0)

    rows = bytearray()
    for y in range(h):
        rows.append(0)
        for x in range(w):
            px, py = x + 0.5, y + 0.5
            d = sdf(px, py)
            e = 0.75
            gx = sdf(px + e, py) - sdf(px - e, py)
            gy = sdf(px, py + e) - sdf(px, py - e)
            ln = math.hypot(gx, gy) or 1.0
            nx, ny = gx / ln, gy / ln
            depth = -d
            t = 0.0
            if depth > 0:
                t = max(0.0, 1.0 - depth / rim)
                t = t * t * (3 - 2 * t)
            r = int(max(0, min(255, round((0.5 - 0.5 * nx * t) * 255))))
            g = int(max(0, min(255, round((0.5 - 0.5 * ny * t) * 255))))
            rows += bytes((r, g, 128))

    def chunk(tag, data):
        body = struct.pack('>I', len(data)) + tag + data
        return body + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(bytes(rows), 9))
           + chunk(b'IEND', b''))
    return base64.b64encode(png).decode()


LENS = lens_png(340, 60, 20)

GLASS_SVG = """
<svg class="glass-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>
  <filter id="lg-refract" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
    <feImage href="data:image/png;base64,__LENS__" result="raw" />
    <feGaussianBlur in="raw" stdDeviation="1.1" result="map" />
    <feDisplacementMap in="SourceGraphic" in2="map" scale="26" xChannelSelector="R" yChannelSelector="G" result="dR" />
    <feDisplacementMap in="SourceGraphic" in2="map" scale="21" xChannelSelector="R" yChannelSelector="G" result="dG" />
    <feDisplacementMap in="SourceGraphic" in2="map" scale="16" xChannelSelector="R" yChannelSelector="G" result="dB" />
    <feColorMatrix in="dR" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="mR" />
    <feColorMatrix in="dG" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" result="mG" />
    <feColorMatrix in="dB" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="mB" />
    <feBlend in="mR" in2="mG" mode="screen" result="rg" />
    <feBlend in="rg" in2="mB" mode="screen" />
  </filter>
</defs></svg>
""".replace('__LENS__', LENS)

V2_CSS = """
/* ── Шрифт ─────────────────────────────────────────────── */
__FONTS__

:root {
  --sans: 'SF Pro Rounded', 'Onest', system-ui, -apple-system, sans-serif;
  --r-xs: 10px;
  --r-sm: 14px;
  --r-md: 18px;
  --r-lg: 24px;
  --r-xl: 30px;
  --r-pill: 999px;
  --glass-tint: rgba(255, 255, 255, .10);
  --glass-edge: rgba(255, 255, 255, .55);
  --glass-ink: rgba(255, 255, 255, .30);
}

[data-theme="night"] {
  --glass-tint: rgba(28, 30, 26, .22);
  --glass-edge: rgba(255, 255, 255, .22);
  --glass-ink: rgba(255, 255, 255, .10);
}

body { font-family: var(--sans); }

/* ── Настоящее жидкое стекло в нижней панели ───────────── */

.dock,
.dock * { -webkit-backdrop-filter: none; }

.dock {
  overflow: hidden;
  isolation: isolate;
  border: 0;
  background: transparent;
  box-shadow:
    0 22px 48px rgba(18, 20, 18, .22),
    0 4px 12px rgba(18, 20, 18, .10);
}

.dock::before,
.dock::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
}

/* слой 1: размытие и насыщенность (как у матового стекла) */
.dock::before {
  z-index: 0;
  background: var(--glass-tint);
  -webkit-backdrop-filter: blur(14px) saturate(180%) brightness(1.04);
  backdrop-filter: blur(14px) saturate(180%) brightness(1.04);
}

/* слой 2: настоящее преломление — дисплейсмент карты нормалей + хроматика */
.dock::after {
  z-index: 1;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, .30), rgba(255, 255, 255, 0) 42%),
    radial-gradient(120% 160% at 50% -20%, rgba(255, 255, 255, .22), rgba(255, 255, 255, 0) 60%);
  -webkit-backdrop-filter: url(#lg-refract);
  backdrop-filter: url(#lg-refract);
  box-shadow:
    inset 0 1.5px 0 var(--glass-edge),
    inset 0 -1.5px 0 rgba(0, 0, 0, .10),
    inset 0 0 0 1px var(--glass-ink);
}

.dock > .dock-item { position: relative; z-index: 2; }
.dock > .dock-mark { z-index: 2; }

[data-glass="off"] .dock::after {
  -webkit-backdrop-filter: blur(2px) saturate(160%);
  backdrop-filter: blur(2px) saturate(160%);
}

.dock-mark {
  background: rgba(25, 26, 28, .82);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, .34),
    inset 0 -1px 0 rgba(0, 0, 0, .28),
    0 8px 18px rgba(18, 20, 18, .26);
  -webkit-backdrop-filter: blur(2px);
  backdrop-filter: blur(2px);
}

[data-theme="night"] .dock-mark {
  background: rgba(236, 232, 220, .20);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, .38),
    inset 0 -1px 0 rgba(0, 0, 0, .30),
    0 8px 18px rgba(0, 0, 0, .34);
}

.dock-item.is-active { color: var(--paper); }

[data-theme="night"] .dock-item.is-active { color: var(--ink); }
"""

rep16("</style>\n</head>",
      "</style>\n<style id=\"v2-core\">\n" + V2_CSS.replace('__FONTS__', FONTS) + "\n</style>\n</head>",
      'v2-fonts-glass')

rep16("""  <main class="stage" id="map">""",
      GLASS_SVG + """  <main class="stage" id="map">""",
      'v2-glass-svg')

open(DST, 'w', encoding='utf-8').write(s)
print('pass16 OK: %d edits total' % len(done))

# ═══════════════ pass 17: закругления + редизайн экранов ════════════════════
s = open(DST, encoding='utf-8').read()


def rep17(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# ── разметка: панель сортировки ─────────────────────────────────────────────
rep17("""      <div class="group-list" id="group-list"></div>""",
      """      <div class="sort-bar">
        <span class="sort-label">Порядок</span>
        <div class="segmented segmented-sm" role="group" aria-label="Сортировка серверов" id="sort-bar">
          <button type="button" data-sort="name" aria-pressed="true">Имя</button>
          <button type="button" data-sort="delay" aria-pressed="false">Пинг</button>
          <button type="button" data-sort="country" aria-pressed="false">Страна</button>
          <button type="button" data-sort="added" aria-pressed="false">Новые</button>
        </div>
      </div>

      <div class="group-list" id="group-list"></div>""",
      'sort-markup')

V2_SCREENS = """
/* ══ Закругления и редизайн экранов (главная не меняется) ══ */

.screen {
  background:
    radial-gradient(120% 60% at 50% 0%, rgba(255, 255, 255, .55), rgba(255, 255, 255, 0) 70%),
    var(--paper);
  scrollbar-width: none;
}

.screen::-webkit-scrollbar { width: 0; height: 0; }

[data-theme="night"] .screen {
  background:
    radial-gradient(120% 60% at 50% 0%, rgba(255, 255, 255, .05), rgba(255, 255, 255, 0) 70%),
    var(--paper);
}

.screen h1 {
  font-family: var(--sans);
  font-weight: 600;
  letter-spacing: -.015em;
  font-size: 30px;
}

.eyebrow {
  font-family: var(--sans);
  font-weight: 600;
  font-size: 10px;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--muted);
}

/* кнопки-пилюли */
.primary,
.ghost,
.text-action,
.back,
.form-submit,
.reset {
  border-radius: var(--r-pill);
  font-family: var(--sans);
  font-weight: 500;
}

.primary { padding: 12px 22px; }

.ghost {
  padding: 8px 15px;
  border: 1px solid var(--line-strong);
  background: var(--paper);
  box-shadow: 0 1px 0 rgba(255, 255, 255, .5) inset;
}

.ghost:hover { background: var(--paper-2); }

[data-theme="night"] .ghost { box-shadow: none; }

.text-action { padding: 6px 0; font-size: 12px; }

.back {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px 7px 11px;
  border: 1px solid var(--line-strong);
  background: var(--paper);
  font-size: 12px;
}

/* поиск и тулбар */
.list-tools { gap: 10px; }

.search {
  height: 42px;
  padding: 0 16px;
  border: 1px solid var(--line);
  border-radius: var(--r-pill);
  background: var(--paper-2);
  font-family: var(--sans);
  font-size: 13px;
}

.search:focus {
  border-color: var(--accent);
  background: var(--paper);
  box-shadow: 0 0 0 3px var(--accent-soft);
}

.ping-all {
  height: 42px;
  padding: 0 16px;
  border-radius: var(--r-pill);
  border: 1px solid var(--line);
  background: var(--paper-2);
  font-family: var(--sans);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0;
  text-transform: none;
  color: var(--ink);
}

.ping-all:hover { background: var(--paper); border-color: var(--line-strong); }
.ping-all[disabled] { opacity: .6; }

/* панель сортировки */
.sort-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
}

.sort-label {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 500;
  color: var(--muted);
  flex: 0 0 auto;
}

.segmented {
  display: inline-flex;
  gap: 2px;
  padding: 3px;
  border: 0;
  border-radius: var(--r-pill);
  background: var(--paper-2);
}

.segmented button {
  border: 0;
  border-radius: var(--r-pill);
  padding: 7px 14px;
  background: transparent;
  font-family: var(--sans);
  font-size: 12px;
  font-weight: 500;
  color: var(--muted);
  transition: background .18s ease, color .18s ease, box-shadow .18s ease;
}

.segmented button[aria-pressed="true"] {
  background: var(--paper);
  color: var(--ink);
  box-shadow: 0 1px 3px rgba(20, 22, 20, .14), 0 0 0 1px rgba(20, 22, 20, .05);
}

[data-theme="night"] .segmented button[aria-pressed="true"] {
  background: rgba(255, 255, 255, .12);
  color: var(--ink);
  box-shadow: 0 1px 3px rgba(0, 0, 0, .4);
}

.segmented-sm button {
  padding: 5px 12px;
  font-size: 11.5px;
}

.segmented { flex-wrap: nowrap; overflow-x: auto; scrollbar-width: none; }
.segmented::-webkit-scrollbar { display: none; }
.segmented button { white-space: nowrap; }

/* ── Группы серверов ───────────────────────────────────── */

.group-list { gap: 14px; margin-top: 14px; }

.group-card {
  border: 0;
  border-radius: var(--r-xl);
  background: var(--paper);
  box-shadow:
    0 1px 0 rgba(255, 255, 255, .7) inset,
    0 0 0 1px rgba(25, 26, 28, .07),
    0 10px 26px rgba(25, 26, 28, .06);
  overflow: hidden;
}

[data-theme="night"] .group-card {
  box-shadow:
    0 1px 0 rgba(255, 255, 255, .05) inset,
    0 0 0 1px rgba(255, 255, 255, .07),
    0 14px 30px rgba(0, 0, 0, .30);
}

.group-card.is-open {
  border: 0;
  box-shadow:
    0 1px 0 rgba(255, 255, 255, .7) inset,
    0 0 0 1px rgba(25, 26, 28, .09),
    0 16px 34px rgba(25, 26, 28, .09);
}

.group-head { padding-right: 10px; gap: 2px; }

.group-toggle { padding: 14px 4px 14px 14px; gap: 13px; }

.group-flag {
  width: 40px;
  height: 40px;
  border: 0;
  border-radius: 14px;
  background: var(--paper-2);
  box-shadow: 0 0 0 1px rgba(25, 26, 28, .05) inset;
  font-size: 19px;
}

.group-name {
  font-size: 15px;
  font-weight: 600;
  letter-spacing: -.01em;
}

.group-meta {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0;
  color: var(--muted);
}

.group-count {
  border: 0;
  border-radius: var(--r-pill);
  padding: 3px 9px;
  background: var(--paper-2);
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 600;
  color: var(--muted);
}

.group-chevron {
  width: 8px;
  height: 8px;
  margin: 0 6px 0 10px;
  border-right: 1.6px solid var(--muted);
  border-bottom: 1.6px solid var(--muted);
  border-radius: 1px;
}

.group-tools { gap: 0; }

.group-action {
  width: 34px;
  height: 34px;
  border-radius: var(--r-pill);
  font-family: var(--sans);
  font-size: 15px;
}

.group-action:hover { background: var(--paper-2); }
.group-action.is-danger:hover { background: rgba(155, 61, 47, .10); }

.group-body { padding: 0 10px 10px; border-top: 0; }

.group-card.is-open .group-body { border-top: 1px solid var(--line); margin-top: 0; padding-top: 8px; }

/* ── Строка сервера ────────────────────────────────────── */

.server-item { border-radius: var(--r-md); }

.server-row {
  gap: 12px;
  padding: 10px 12px 10px 6px;
  border-radius: var(--r-md);
  border-bottom: 0;
  transition: background .16s ease;
}

.server-row:hover { background: var(--paper-2); }

.group-body .server-row { padding: 10px 12px 10px 6px; }

.server-item:last-child .server-row,
.group-body .server-item:last-child .server-row { border-bottom: 0; }

.server-row.is-selected {
  background: var(--accent-soft);
  box-shadow: 0 0 0 1px var(--accent-line) inset;
}

.server-row.is-selected::before { display: none; }

.server-flag {
  width: 38px;
  height: 38px;
  flex: 0 0 auto;
  border: 0;
  border-radius: 50%;
  background: var(--paper-2);
  box-shadow: 0 0 0 1px rgba(25, 26, 28, .06) inset;
  font-size: 18px;
}

.server-row.is-selected .server-flag {
  box-shadow: 0 0 0 2px var(--accent) inset, 0 6px 14px rgba(25, 26, 28, .10);
}

.server-copy { gap: 3px; }

.server-city {
  font-size: 14.5px;
  font-weight: 600;
  letter-spacing: -.01em;
}

.server-sub {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0;
  color: var(--muted);
}

.server-ping {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0;
  padding: 1px 6px;
  border-radius: var(--r-pill);
  background: var(--paper-2);
  color: var(--muted);
}

.server-ping.is-fast { color: var(--accent); background: var(--accent-soft); }
.server-ping.is-slow { color: var(--danger); background: rgba(155, 61, 47, .10); }
[data-theme="night"] .server-ping.is-slow { background: rgba(224, 138, 118, .14); }

.server-proto {
  font-family: var(--sans);
  font-size: 9.5px;
  font-weight: 600;
  letter-spacing: .06em;
  text-transform: uppercase;
  color: var(--muted);
  padding: 3px 7px;
  border-radius: var(--r-pill);
  background: var(--paper-2);
  flex: 0 0 auto;
}

.server-action { display: none; }

.row-remove {
  width: 30px;
  height: 30px;
  right: 8px;
  border-radius: var(--r-pill);
  font-family: var(--sans);
  font-size: 16px;
}

.row-remove:hover { background: rgba(155, 61, 47, .10); }

/* ── Настройки ─────────────────────────────────────────── */

.group {
  border: 0;
  border-radius: var(--r-xl);
  margin-top: 18px;
  background: var(--paper);
  box-shadow:
    0 1px 0 rgba(255, 255, 255, .7) inset,
    0 0 0 1px rgba(25, 26, 28, .07),
    0 10px 26px rgba(25, 26, 28, .05);
  overflow: hidden;
}

[data-theme="night"] .group {
  box-shadow:
    0 1px 0 rgba(255, 255, 255, .05) inset,
    0 0 0 1px rgba(255, 255, 255, .07),
    0 14px 30px rgba(0, 0, 0, .30);
}

.group h2 {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .10em;
  text-transform: uppercase;
  color: var(--muted);
  padding: 16px 18px 6px;
  border: 0;
}

.row {
  padding: 13px 18px;
  gap: 14px;
  border-top: 1px solid var(--line);
  border-radius: 0;
}

.row:last-child { border-bottom: 0; border-radius: 0 0 var(--r-xl) var(--r-xl); }

.row-label {
  font-family: var(--sans);
  font-size: 14px;
  font-weight: 500;
  letter-spacing: -.01em;
}

.row-note {
  font-family: var(--sans);
  font-size: 11.5px;
  font-weight: 400;
  letter-spacing: 0;
  color: var(--muted);
  margin-top: 2px;
}

.row-stack { gap: 10px; }

.accent-value {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0;
  color: var(--muted);
}

.switch {
  width: 50px;
  height: 30px;
  border: 0;
  border-radius: var(--r-pill);
  background: var(--line-strong);
  padding: 0;
  transition: background .2s ease;
}

.switch span {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 2px 5px rgba(20, 22, 20, .28);
  transform: translateX(2px);
  transition: transform .2s cubic-bezier(.3, .9, .3, 1);
}

.switch[aria-checked="true"] { background: var(--accent); }
.switch[aria-checked="true"] span { transform: translateX(22px); }

.swatches { gap: 10px; }

.swatch {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 0;
  box-shadow: 0 0 0 1px rgba(25, 26, 28, .10) inset;
}

.swatch[aria-pressed="true"] {
  box-shadow: 0 0 0 2px var(--paper), 0 0 0 3.5px var(--ink);
}

.swatch-custom {
  border-radius: 50%;
  overflow: hidden;
}

.settings-note {
  padding: 14px 18px 16px;
  font-family: var(--sans);
  font-size: 11.5px;
  line-height: 1.5;
  color: var(--muted);
}

.data-actions .ghost { border-radius: var(--r-pill); }

.reset {
  width: 100%;
  padding: 15px;
  border: 0;
  border-radius: var(--r-xl);
  background: var(--paper);
  color: var(--danger);
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 0 0 1px rgba(25, 26, 28, .07), 0 10px 26px rgba(25, 26, 28, .05);
}

/* ── Формы ─────────────────────────────────────────────── */

.field { gap: 7px; }

.field label,
.field-head label {
  font-family: var(--sans);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0;
  text-transform: none;
  color: var(--muted);
}

.field input,
.field textarea {
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  padding: 13px 15px;
  background: var(--paper-2);
  font-family: var(--sans);
  font-size: 14px;
}

.field input:focus,
.field textarea:focus {
  border-color: var(--accent);
  background: var(--paper);
  box-shadow: 0 0 0 3px var(--accent-soft);
}

.form-submit,
.form .primary { border-radius: var(--r-pill); }

.form-foot { gap: 12px; }

.preview {
  border-radius: var(--r-lg);
  border: 1px solid var(--line);
  background: var(--paper-2);
}

/* ── Пустые состояния и тосты ──────────────────────────── */

.empty {
  border-radius: var(--r-xl);
  border: 1px dashed var(--line-strong);
}

.toast {
  border-radius: var(--r-pill);
  border: 1px solid var(--line);
  background: rgba(242, 240, 234, .86);
  -webkit-backdrop-filter: blur(18px) saturate(180%);
  backdrop-filter: blur(18px) saturate(180%);
  box-shadow: 0 18px 40px rgba(20, 22, 20, .18);
  padding: 12px 18px;
}

[data-theme="night"] .toast {
  background: rgba(30, 31, 27, .86);
}

/* ── Таблица стилей «Пилюля» для бейджей ───────────────── */
"""

rep17("</style>\n</head>",
      V2_SCREENS + "</style>\n</head>",
      'v2-screens-css')

open(DST, 'w', encoding='utf-8').write(s)
print('pass17 OK: %d edits total' % len(done))

# ═══════════════ pass 18: список, сортировка, пинг, без демо ════════════════
s = open(DST, encoding='utf-8').read()


def rep18(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# ── без тестовых серверов ──────────────────────────────────────────────────
rep18("""  loadStored();
  if (store.read('vpn.seeded', false) !== true && !state.servers.length && !state.subs.length) {
    seedDemo();
  }""",
      """  loadStored();
  purgeDemoData();""",
      'no-demo')

rep18("""  function persist() {""",
      """  // Демо-данные прошлых сборок больше не нужны: чистим один раз.
  function purgeDemoData() {
    if (store.read('vpn.demoPurged', false) === true) return;
    const demoSubs = state.subs.filter(function (sub) {
      return !sub.url && /^Тестовая подписка$/i.test(sub.name);
    }).map(function (sub) { return sub.id; });
    const before = state.servers.length;
    state.servers = state.servers.filter(function (server) {
      const demoHost = /\\.example\\.(net|com)$/i.test(server.host || '');
      return !demoHost && demoSubs.indexOf(server.subId) === -1;
    });
    state.subs = state.subs.filter(function (sub) { return demoSubs.indexOf(sub.id) === -1; });
    if (state.servers.length !== before) {
      if (!state.servers.some(function (server) { return server.id === state.selectedId; })) {
        state.selectedId = state.servers.length ? state.servers[0].id : '';
      }
      persist();
    }
    store.write('vpn.demoPurged', true);
  }

  function sortValue(server) {
    const entry = state.latency[server.id];
    if (entry && Number.isFinite(entry.ms)) return entry.ms;
    if (entry) return 99999;
    return 50000;
  }

  function sortServers(list) {
    const mode = state.sort || 'name';
    const byName = function (a, b) {
      return String(a.city || '').localeCompare(String(b.city || ''), 'ru');
    };
    const copy = list.slice();
    if (mode === 'delay') {
      copy.sort(function (a, b) {
        const d = sortValue(a) - sortValue(b);
        return d !== 0 ? d : byName(a, b);
      });
    } else if (mode === 'country') {
      copy.sort(function (a, b) {
        const d = String(a.country || '').localeCompare(String(b.country || ''), 'ru');
        return d !== 0 ? d : byName(a, b);
      });
    } else if (mode === 'added') {
      copy.sort(function (a, b) { return (Number(b.created) || 0) - (Number(a.created) || 0); });
    } else {
      copy.sort(byName);
    }
    return copy;
  }

  function setSort(mode) {
    state.sort = mode;
    store.write('vpn.sort', mode);
    Array.prototype.forEach.call(document.querySelectorAll('#sort-bar button'), function (button) {
      button.setAttribute('aria-pressed', String(button.dataset.sort === mode));
    });
    renderServers();
  }

  function persist() {""",
      'sort-logic')

# ── строка сервера: флаг слева, пинг и протокол справа ─────────────────────
rep18("""    const copy = document.createElement('span');
    copy.className = 'server-copy';
    const city = document.createElement('span');
    city.className = 'server-city';
    city.textContent = server.city;
    const sub = document.createElement('span');
    sub.className = 'server-sub';
    sub.textContent = [server.country || 'Локация не определена', sourceText(server)].filter(Boolean).join(' · ');
    const ping = latencyText(server);
    if (ping) {
      sub.appendChild(document.createTextNode(' · '));
      const pingEl = document.createElement('span');
      pingEl.className = 'server-ping' + ping.className;
      pingEl.textContent = ping.text;
      sub.appendChild(pingEl);
    }
    copy.appendChild(city);
    copy.appendChild(sub);

    const proto = document.createElement('span');
    proto.className = 'server-proto';
    proto.textContent = server.protocol || '';

    const action = document.createElement('span');
    action.className = 'server-action';
    action.setAttribute('aria-hidden', 'true');

    row.appendChild(flag);
    row.appendChild(copy);
    row.appendChild(proto);
    row.appendChild(action);

    row.addEventListener('click', function () { selectServer(server.id, true); });""",
      """    const copy = document.createElement('span');
    copy.className = 'server-copy';
    const city = document.createElement('span');
    city.className = 'server-city';
    city.textContent = server.city;
    const sub = document.createElement('span');
    sub.className = 'server-sub';
    sub.textContent = [server.country || 'Локация не определена', sourceText(server)].filter(Boolean).join(' · ');
    copy.appendChild(city);
    copy.appendChild(sub);

    const side = document.createElement('span');
    side.className = 'server-side';
    const ping = latencyText(server);
    const pingEl = document.createElement('span');
    pingEl.className = 'server-ping' + (ping ? ping.className : ' is-idle');
    if (server.id === state.selectedId && state.vpn.state === 'connected') {
      pingEl.classList.add('is-live');
    }
    pingEl.textContent = ping ? ping.text : '— мс';
    const proto = document.createElement('span');
    proto.className = 'server-proto';
    proto.textContent = server.protocol || '—';
    side.appendChild(pingEl);
    side.appendChild(proto);

    row.appendChild(flag);
    row.appendChild(copy);
    row.appendChild(side);

    const openSettings = function (event) {
      if (event) { event.stopPropagation(); event.preventDefault(); }
      openServerSettings(server.id);
    };
    row.addEventListener('click', function () { selectServer(server.id, true); });
    row.addEventListener('contextmenu', openSettings);""",
      'row-markup')

# ── группы: сортировка и настройки сервера ─────────────────────────────────
rep18("""    const key = function (server) { return (server.city || '').toLowerCase(); };
    const query = state.query;
    const cards = [];

    state.subs.forEach(function (sub) {
      const all = state.servers.filter(function (server) { return server.subId === sub.id; });
      const list = all.slice().sort(function (a, b) { return key(a).localeCompare(key(b), 'ru'); }).filter(matchesQuery);""",
      """    const query = state.query;
    const cards = [];

    state.subs.slice().sort(function (a, b) {
      return String(a.name || '').localeCompare(String(b.name || ''), 'ru');
    }).forEach(function (sub) {
      const all = state.servers.filter(function (server) { return server.subId === sub.id; });
      const list = sortServers(all).filter(matchesQuery);""",
      'group-sort')

rep18("""    const manual = state.servers.filter(function (server) { return !server.subId; })
      .sort(function (a, b) { return key(a).localeCompare(key(b), 'ru'); });""",
      """    const manual = sortServers(state.servers.filter(function (server) { return !server.subId; }));""",
      'manual-sort')

rep18("""  function renderSubs() {
    // подписки живут внутри общего списка групп
  }""",
      """  function renderSubs() {
    // подписки живут внутри общего списка групп
  }

  function renderSortBar() {
    Array.prototype.forEach.call(document.querySelectorAll('#sort-bar button'), function (button) {
      button.setAttribute('aria-pressed', String(button.dataset.sort === (state.sort || 'name')));
    });
  }""",
      'render-sort')

# ── состояние: сортировка ──────────────────────────────────────────────────
rep18("""    expanded: store.read('vpn.expanded', {})""",
      """    expanded: store.read('vpn.expanded', {}),
    sort: store.read('vpn.sort', 'name')""",
      'sort-state')

# ── привязка панели сортировки ─────────────────────────────────────────────
rep18("""  $('#open-add-sub').addEventListener('click', openAddSub);""",
      """  Array.prototype.forEach.call(document.querySelectorAll('#sort-bar button'), function (button) {
    button.addEventListener('click', function () {
      haptic();
      setSort(button.dataset.sort);
    });
  });
  renderSortBar();

  $('#open-add-sub').addEventListener('click', openAddSub);""",
      'sort-bind')

# ── пинг рядом с состоянием под кнопкой ────────────────────────────────────
rep18("""    if (busy) ui.connStatus.textContent = 'Подключение…';
    else if (online) ui.connStatus.textContent = 'Защищено';
    else if (failed) ui.connStatus.textContent = (state.vpn.error || 'Ошибка').slice(0, 48);
    else ui.connStatus.textContent = 'Не подключено';""",
      """    const pingEntry = state.latency[server.id];
    const pingText = pingEntry && Number.isFinite(pingEntry.ms) ? pingEntry.ms + ' мс' : '—';

    if (busy) ui.connStatus.textContent = 'Подключение… · ' + pingText;
    else if (online) ui.connStatus.textContent = 'Защищено · ' + pingText;
    else if (failed) ui.connStatus.textContent = (state.vpn.error || 'Ошибка').slice(0, 42);
    else ui.connStatus.textContent = 'Не подключено · ' + pingText;""",
      'home-ping-label')

open(DST, 'w', encoding='utf-8').write(s)
print('pass18 OK: %d edits total' % len(done))

# ═══════════════ pass 19: настройки сервера (лист) ══════════════════════════
s = open(DST, encoding='utf-8').read()


def rep19(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# ── разметка листа ─────────────────────────────────────────────────────────
rep19("""  <div class="toast" id="toast" role="status" aria-live="polite">""",
      """  <div class="sheet-backdrop" id="sheet-backdrop" hidden></div>
  <section class="sheet" id="server-sheet" role="dialog" aria-modal="true" aria-labelledby="sheet-title" hidden>
    <div class="sheet-grip" aria-hidden="true"></div>
    <header class="sheet-head">
      <div class="sheet-head-copy">
        <p class="eyebrow" id="sheet-proto">VLESS</p>
        <h2 id="sheet-title">Настройки сервера</h2>
      </div>
      <button class="sheet-close" type="button" id="sheet-close" aria-label="Закрыть">×</button>
    </header>
    <div class="sheet-body">
      <label class="sheet-field">
        <span>Название</span>
        <input type="text" id="sheet-name" autocomplete="off" spellcheck="false" placeholder="Город или подпись">
      </label>
      <div class="sheet-pair">
        <label class="sheet-field">
          <span>Адрес</span>
          <input type="text" id="sheet-host" autocomplete="off" spellcheck="false" inputmode="url" placeholder="host.example.com">
        </label>
        <label class="sheet-field sheet-field-port">
          <span>Порт</span>
          <input type="text" id="sheet-port" inputmode="numeric" autocomplete="off" placeholder="443">
        </label>
      </div>
      <label class="sheet-field">
        <span>SNI / домен маскировки</span>
        <input type="text" id="sheet-sni" autocomplete="off" spellcheck="false" placeholder="как в ссылке">
      </label>
      <div class="sheet-row">
        <div class="sheet-row-copy">
          <p class="row-label">Не проверять сертификат</p>
          <p class="row-note">allowInsecure — только для своих серверов.</p>
        </div>
        <button class="switch" type="button" role="switch" aria-checked="false" id="sheet-insecure" aria-label="Не проверять сертификат"><span></span></button>
      </div>
      <div class="sheet-row">
        <div class="sheet-row-copy">
          <p class="row-label">Mux</p>
          <p class="row-note">Мультиплексирование соединений ядром.</p>
        </div>
        <button class="switch" type="button" role="switch" aria-checked="false" id="sheet-mux" aria-label="Mux"><span></span></button>
      </div>
      <div class="sheet-meta" id="sheet-meta"></div>
    </div>
    <footer class="sheet-foot">
      <button class="ghost" type="button" id="sheet-ping">Проверить пинг</button>
      <button class="primary" type="button" id="sheet-save">Сохранить</button>
    </footer>
  </section>

  <div class="toast" id="toast" role="status" aria-live="polite">""",
      'sheet-markup')

SHEET_CSS = """
/* ── Строка: сетка под флаг и правую колонку ───────────── */
.server-item {
  display: flex;
  align-items: center;
  gap: 2px;
  border-radius: var(--r-md);
}

.server-row {
  flex: 1 1 auto;
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr) auto;
  align-items: center;
  gap: 12px;
  padding: 9px 6px 9px 6px;
  border-radius: var(--r-md);
  text-align: left;
}

.server-side {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  flex: 0 0 auto;
}

.server-ping {
  font-variant-numeric: tabular-nums;
  min-width: 46px;
  text-align: center;
}

.server-ping.is-idle { opacity: .55; }

.server-ping.is-live {
  color: var(--accent);
  background: var(--accent-soft);
  box-shadow: 0 0 0 1px var(--accent-line) inset;
}

.server-item .row-more,
.server-item .row-remove,
.group-body .server-row .row-remove {
  position: static;
  flex: 0 0 auto;
  width: 30px;
  height: 30px;
  margin-left: -4px;
  border: 0;
  border-radius: var(--r-pill);
  background: none;
  color: var(--muted);
  font-family: var(--sans);
  font-size: 16px;
  line-height: 1;
  display: grid;
  place-items: center;
}

.row-more:hover { background: var(--paper-2); color: var(--ink); }
.row-remove { font-size: 17px; }
.row-remove:hover { background: rgba(155, 61, 47, .12); color: var(--danger); }

/* ── Лист настроек сервера ─────────────────────────────── */

.sheet-backdrop {
  position: fixed;
  inset: 0;
  z-index: 60;
  background: rgba(20, 22, 20, .34);
  -webkit-backdrop-filter: blur(3px);
  backdrop-filter: blur(3px);
  animation: sheet-fade .22s ease;
}

@keyframes sheet-fade { from { opacity: 0; } to { opacity: 1; } }

.sheet {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 61;
  max-height: 88vh;
  display: flex;
  flex-direction: column;
  padding: 8px 18px calc(18px + env(safe-area-inset-bottom));
  border-radius: var(--r-xl) var(--r-xl) 0 0;
  background: var(--paper);
  box-shadow: 0 -18px 48px rgba(20, 22, 20, .22);
  animation: sheet-in .3s cubic-bezier(.22, .9, .26, 1);
}

@keyframes sheet-in { from { transform: translateY(14%); opacity: .6; } to { transform: translateY(0); opacity: 1; } }

.sheet-grip {
  width: 42px;
  height: 4px;
  margin: 2px auto 8px;
  border-radius: var(--r-pill);
  background: var(--line-strong);
  opacity: .7;
}

.sheet-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 2px 0 12px;
}

.sheet-head h2 {
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -.015em;
  margin: 2px 0 0;
}

.sheet-close {
  width: 34px;
  height: 34px;
  border: 0;
  border-radius: var(--r-pill);
  background: var(--paper-2);
  color: var(--ink);
  font-size: 18px;
  line-height: 1;
  display: grid;
  place-items: center;
}

.sheet-body {
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-bottom: 6px;
}

.sheet-field { display: flex; flex-direction: column; gap: 6px; }

.sheet-field span {
  font-size: 11.5px;
  font-weight: 600;
  color: var(--muted);
}

.sheet-field input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--paper-2);
  font-family: var(--sans);
  font-size: 14px;
}

.sheet-field input:focus {
  outline: none;
  border-color: var(--accent);
  background: var(--paper);
  box-shadow: 0 0 0 3px var(--accent-soft);
}

.sheet-pair { display: flex; gap: 10px; }
.sheet-pair .sheet-field { flex: 1 1 auto; }
.sheet-pair .sheet-field-port { flex: 0 0 96px; }

.sheet-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 12px 14px;
  border-radius: var(--r-md);
  background: var(--paper-2);
}

.sheet-meta {
  font-size: 11.5px;
  line-height: 1.5;
  color: var(--muted);
  padding: 2px 2px 0;
  word-break: break-all;
}

.sheet-foot {
  display: flex;
  gap: 10px;
  padding-top: 12px;
  border-top: 1px solid var(--line);
  margin-top: 6px;
}

.sheet-foot .ghost { flex: 0 0 auto; }
.sheet-foot .primary { flex: 1 1 auto; }
"""

rep19("</style>\n</head>", SHEET_CSS + "</style>\n</head>", 'sheet-css')

# ── логика листа ───────────────────────────────────────────────────────────
rep19("""  function selectServer(id, goHome) {""",
      """  let sheetServerId = '';

  function openServerSettings(id) {
    const server = findServer(id);
    if (!server) return;
    sheetServerId = id;
    const params = serverParams(server);
    ui.sheetName.value = server.city || '';
    ui.sheetHost.value = server.host || '';
    ui.sheetPort.value = String(server.port || '');
    ui.sheetSni.value = server.sni || params.sni || '';
    ui.sheetInsecure.setAttribute('aria-checked', String(!!server.allowInsecure));
    ui.sheetMux.setAttribute('aria-checked', String(!!server.mux));
    ui.sheetTitle.textContent = server.city || 'Сервер';
    ui.sheetProto.textContent = (server.protocol || 'Сервер').toUpperCase()
      + (server.subName ? ' · ' + server.subName : '');
    ui.sheetMeta.textContent = 'Ядро: ' + server.host + ':' + server.port
      + (server.sni ? ' · sni ' + server.sni : '')
      + (server.subId ? ' · из подписки' : ' · добавлен вручную');
    ui.sheet.hidden = false;
    ui.sheetBackdrop.hidden = false;
    document.body.classList.add('sheet-open');
  }

  function closeServerSettings() {
    ui.sheet.hidden = true;
    ui.sheetBackdrop.hidden = true;
    document.body.classList.remove('sheet-open');
    sheetServerId = '';
  }

  function saveServerSettings() {
    const server = findServer(sheetServerId);
    if (!server) { closeServerSettings(); return; }
    const name = cleanText(ui.sheetName.value, 80);
    const host = cleanText(ui.sheetHost.value, 120);
    const port = Number(String(ui.sheetPort.value).replace(/[^0-9]/g, ''));
    if (!host) {
      showToast('Укажите адрес сервера');
      return;
    }
    if (!port || port < 1 || port > 65535) {
      showToast('Порт должен быть от 1 до 65535');
      return;
    }
    server.city = name || server.city;
    server.host = host;
    server.port = port;
    server.sni = cleanText(ui.sheetSni.value, 120);
    server.allowInsecure = ui.sheetInsecure.getAttribute('aria-checked') === 'true';
    server.mux = ui.sheetMux.getAttribute('aria-checked') === 'true';
    server.link = patchLink(server.link, { host: host, port: port, sni: server.sni, allowInsecure: server.allowInsecure });
    persist();
    closeServerSettings();
    renderServers();
    updateHome();
    showToast('Сервер обновлён');
  }

  function selectServer(id, goHome) {""",
      'sheet-logic')

open(DST, 'w', encoding='utf-8').write(s)
print('pass19 OK: %d edits total' % len(done))

# ═══════════════ pass 20: связка листа, overrides, ссылки ═══════════════════
s = open(DST, encoding='utf-8').read()


def rep20(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# ── ссылки: разбор параметров и перезапись ─────────────────────────────────
rep20("""  function parseLink(raw) {""",
      """  function serverParams(server) {
    const raw = String(server && server.link ? server.link : '');
    const q = raw.indexOf('?');
    const hashAt = raw.indexOf('#');
    if (q < 0) return {};
    const end = hashAt > q ? hashAt : raw.length;
    return queryMap(raw.slice(q + 1, end));
  }

  function patchLink(link, next) {
    const raw = String(link || '');
    const schemeMatch = raw.match(/^([a-z0-9+.-]+):\\/\\//i);
    if (!schemeMatch) return raw;
    const scheme = schemeMatch[1].toLowerCase();

    if (scheme === 'vmess') {
      try {
        const json = JSON.parse(decodeBase64(raw.slice(schemeMatch[0].length)));
        json.add = next.host;
        json.port = String(next.port);
        if (next.sni) { json.sni = next.sni; json.host = next.host; }
        if (next.allowInsecure) json.allowInsecure = '1';
        return 'vmess://' + btoa(unescape(encodeURIComponent(JSON.stringify(json))));
      } catch (error) {
        return raw;
      }
    }

    const hashAt = raw.indexOf('#');
    const fragment = hashAt >= 0 ? raw.slice(hashAt) : '';
    let body = hashAt >= 0 ? raw.slice(0, hashAt) : raw;
    const q = body.indexOf('?');
    let head = q >= 0 ? body.slice(0, q) : body;
    let params = q >= 0 ? body.slice(q + 1) : '';

    head = head.replace(/\\/\\/[^/@]*@/, function (chunk) { return chunk; });
    const at = head.lastIndexOf('@');
    if (at >= 0) {
      head = head.slice(0, at + 1) + next.host + ':' + next.port;
    } else if (scheme === 'ss') {
      const decoded = (function () {
        try { return decodeBase64(head.slice(schemeMatch[0].length)); } catch (error) { return ''; }
      })();
      if (decoded) {
        const atSs = decoded.lastIndexOf('@');
        head = schemeMatch[0] + decoded.slice(0, atSs + 1) + next.host + ':' + next.port;
      }
    }

    const pairs = params ? params.split('&').filter(Boolean).filter(function (pair) {
      const key = pair.split('=')[0].toLowerCase();
      return key !== 'sni' && key !== 'peer' && key !== 'allowinsecure' && key !== 'insecure';
    }) : [];
    if (next.sni) pairs.push('sni=' + encodeURIComponent(next.sni));
    if (next.allowInsecure) pairs.push('allowInsecure=1');
    params = pairs.join('&');

    return head + (params ? '?' + params : '') + fragment;
  }

  function parseLink(raw) {""",
      'link-utils')

# ── применяем пользовательские настройки к outbound ────────────────────────
rep20("""  function buildXrayConfig(server) {
    const built = buildOutbound(server);
    if (!built.ok) return built;""",
      """  function applyServerOverrides(outbound, server) {
    if (!server) return outbound;
    const stream = outbound.streamSettings || {};
    const sni = cleanText(server.sni, 120);
    if (sni) {
      if (stream.tlsSettings) stream.tlsSettings.serverName = sni;
      if (stream.realitySettings) stream.realitySettings.serverName = sni;
    }
    if (server.allowInsecure && stream.tlsSettings) {
      stream.tlsSettings.allowInsecure = true;
    }
    if (server.mux) {
      outbound.mux = { enabled: true, concurrency: 8 };
    }
    return outbound;
  }

  function buildXrayConfig(server) {
    const built = buildOutbound(server);
    if (!built.ok) return built;
    applyServerOverrides(built.outbound, server);""",
      'overrides')

# ── элементы листа ─────────────────────────────────────────────────────────
rep20("""    connStats: $('#conn-stats'),""",
      """    connStats: $('#conn-stats'),
    sheet: $('#server-sheet'),
    sheetBackdrop: $('#sheet-backdrop'),
    sheetName: $('#sheet-name'),
    sheetHost: $('#sheet-host'),
    sheetPort: $('#sheet-port'),
    sheetSni: $('#sheet-sni'),
    sheetInsecure: $('#sheet-insecure'),
    sheetMux: $('#sheet-mux'),
    sheetMeta: $('#sheet-meta'),
    sheetTitle: $('#sheet-title'),
    sheetProto: $('#sheet-proto'),""",
      'sheet-refs')

# ── привязки листа ─────────────────────────────────────────────────────────
rep20("""  Array.prototype.forEach.call(document.querySelectorAll('#sort-bar button'), function (button) {
    button.addEventListener('click', function () {
      haptic();
      setSort(button.dataset.sort);
    });
  });""",
      """  function bindSwitch(button) {
    if (!button) return;
    button.addEventListener('click', function () {
      const next = button.getAttribute('aria-checked') !== 'true';
      button.setAttribute('aria-checked', String(next));
      haptic();
    });
  }

  if (ui.sheet) {
    ui.sheetBackdrop.addEventListener('click', closeServerSettings);
    document.getElementById('sheet-close').addEventListener('click', closeServerSettings);
    document.getElementById('sheet-save').addEventListener('click', saveServerSettings);
    document.getElementById('sheet-ping').addEventListener('click', function () {
      const server = findServer(sheetServerId);
      if (!server) return;
      if (!native || typeof native.ping !== 'function') return;
      native.ping(JSON.stringify([{ id: server.id, host: server.host, port: server.port }]));
    });
    bindSwitch(ui.sheetInsecure);
    bindSwitch(ui.sheetMux);
  }

  Array.prototype.forEach.call(document.querySelectorAll('#sort-bar button'), function (button) {
    button.addEventListener('click', function () {
      haptic();
      setSort(button.dataset.sort);
    });
  });
  renderSortBar();""",
      'sheet-bind')

# ── кнопка «⋯» в строке ────────────────────────────────────────────────────
rep20("""    const openSettings = function (event) {
      if (event) { event.stopPropagation(); event.preventDefault(); }
      openServerSettings(server.id);
    };
    row.addEventListener('click', function () { selectServer(server.id, true); });
    row.addEventListener('contextmenu', openSettings);""",
      """    row.addEventListener('click', function () { selectServer(server.id, true); });
    row.addEventListener('contextmenu', function (event) {
      event.preventDefault();
      openServerSettings(server.id);
    });""",
      'row-context')

rep20("""    item.appendChild(row);

    if (removable) {""",
      """    item.appendChild(row);

    const more = document.createElement('button');
    more.type = 'button';
    more.className = 'row-more';
    more.textContent = '⋯';
    more.setAttribute('aria-label', 'Настройки сервера ' + server.city);
    more.addEventListener('click', function (event) {
      event.stopPropagation();
      openServerSettings(server.id);
    });
    item.appendChild(more);

    if (removable) {""",
      'row-more')

# ── сохраняем новые поля при чтении из хранилища ──────────────────────────
rep20("""      subId: String(raw.subId || ''),
      subName: cleanText(raw.subName, 60),
      created: Number(raw.created) || Date.now()""",
      """      subId: String(raw.subId || ''),
      subName: cleanText(raw.subName, 60),
      sni: cleanText(raw.sni, 120),
      allowInsecure: raw.allowInsecure === true,
      mux: raw.mux === true,
      created: Number(raw.created) || Date.now()""",
      'sanitize-fields')

open(DST, 'w', encoding='utf-8').write(s)
print('pass20 OK: %d edits total' % len(done))

# ── финальная проверка синтаксиса JS (защита от порчи скрипта) ──────────────
import re as _re, subprocess as _sp, tempfile as _tf
_final = open(DST, encoding='utf-8').read()
_scripts = _re.findall(r'<script>(.*?)</script>', _final, _re.S)
for _i, _sc in enumerate(_scripts):
    _path = '/tmp/_check_%d.js' % _i
    open(_path, 'w', encoding='utf-8').write(_sc)
    _r = _sp.run(['node', '--check', _path], capture_output=True, text=True)
    if _r.returncode != 0:
        print('!! синтаксис скрипта #%d сломан:' % _i)
        print(_r.stderr[:600])
        sys.exit(1)
print('JS: синтаксис %d скриптов в порядке' % len(_scripts))

# ═══════════════ pass 21: слайдер подключения на главной ════════════════════
s = open(DST, encoding='utf-8').read()


def rep21(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# ── разметка: вместо круглой кнопки — слайдер ──────────────────────────────
rep21("""    <button class="connect is-empty" id="connect" type="button" aria-label="Подключить">
      <svg class="connect-icon connect-power" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true">
        <path d="M12 3.5v8" />
        <path d="M6.8 6.9a8 8 0 1 0 10.4 0" />
      </svg>
      <svg class="connect-icon connect-plus" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true">
        <path d="M12 5v14M5 12h14" />
      </svg>
    </button>""",
      """    <div class="slider" id="connect-slider" data-state="empty">
      <span class="slider-track" aria-hidden="true"></span>
      <span class="slider-label" id="slider-label">Добавьте сервер</span>
      <button class="slider-knob" id="slider-knob" type="button" aria-label="Потяните, чтобы подключиться">
        <svg class="slider-icon slider-power" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true">
          <path d="M12 3.5v8" />
          <path d="M6.8 6.9a8 8 0 1 0 10.4 0" />
        </svg>
        <svg class="slider-icon slider-plus" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true">
          <path d="M12 5v14M5 12h14" />
        </svg>
        <svg class="slider-icon slider-stop" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true">
          <rect x="7.4" y="7.4" width="9.2" height="9.2" rx="2.2" />
        </svg>
      </button>
    </div>""",
      'slider-markup')

SLIDER_CSS = """
/* ── Слайдер подключения ───────────────────────────────── */

.home-ui { gap: 10px; }

.slider {
  position: relative;
  width: 268px;
  height: 64px;
  border: 0;
  border-radius: var(--r-pill);
  background: var(--ink);
  overflow: hidden;
  isolation: isolate;
  transition:
    width .46s cubic-bezier(.32, .9, .28, 1),
    background .3s ease,
    box-shadow .3s ease;
  box-shadow: 0 16px 34px var(--shadow);
}

[data-theme="night"] .slider { box-shadow: 0 16px 34px rgba(0, 0, 0, .5); }

.slider-track {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background:
    linear-gradient(100deg, rgba(255, 255, 255, .06), rgba(255, 255, 255, 0) 42%);
  pointer-events: none;
}

.slider-label {
  position: absolute;
  left: 74px;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-family: var(--sans);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: -.01em;
  color: rgba(255, 255, 255, .92);
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  pointer-events: none;
  transition: opacity .24s ease, transform .3s ease;
}

[data-theme="night"] .slider-label { color: var(--paper); }
[data-theme="night"] .slider { background: rgba(236, 232, 220, .14); }

.slider-knob {
  position: absolute;
  left: 6px;
  top: 6px;
  width: 52px;
  height: 52px;
  padding: 0;
  border: 0;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: var(--accent);
  color: #fff;
  box-shadow:
    0 8px 18px rgba(18, 20, 18, .28),
    inset 0 1px 0 rgba(255, 255, 255, .34);
  transition: transform .34s cubic-bezier(.3, .9, .26, 1), background .25s ease, color .25s ease;
  touch-action: none;
  will-change: transform;
}

.slider.is-dragging .slider-knob { transition: none; }

.slider-icon {
  position: absolute;
  width: 24px;
  height: 24px;
  transition: opacity .18s ease, transform .3s ease;
}

.slider-plus,
.slider-stop { opacity: 0; transform: scale(.7); }

.slider[data-state="empty"] .slider-power,
.slider[data-state="empty"] .slider-stop { opacity: 0; transform: scale(.7); }
.slider[data-state="empty"] .slider-plus { opacity: 1; transform: scale(1); }

.slider[data-state="connected"] {
  width: 68px;
  background: var(--accent);
  box-shadow: 0 14px 30px rgba(18, 20, 18, .26), 0 0 0 0 var(--accent-soft);
  animation: slider-halo 3.4s ease-out infinite;
}

.slider[data-state="connected"] .slider-label { opacity: 0; }

.slider[data-state="connected"] .slider-knob {
  left: 6px;
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, .16);
  color: #fff;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .4), inset 0 0 0 1px rgba(255, 255, 255, .22);
}

.slider[data-state="connected"] .slider-power { opacity: 0; transform: scale(.7); }
.slider[data-state="connected"] .slider-stop { opacity: 1; transform: scale(1); }

.slider[data-state="connecting"] { background: var(--paper-2); }
.slider[data-state="connecting"] .slider-label { color: var(--ink); opacity: 1; }
[data-theme="night"] .slider[data-state="connecting"] { background: rgba(236, 232, 220, .10); }
[data-theme="night"] .slider[data-state="connecting"] .slider-label { color: var(--ink); }

.slider[data-state="connecting"] .slider-track::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(100deg, transparent 20%, var(--accent-soft) 50%, transparent 80%);
  animation: slider-sweep 1.5s linear infinite;
}

.slider[data-state="connecting"] .slider-knob { background: var(--accent); }

.slider[data-state="error"] { background: var(--paper-2); }
.slider[data-state="error"] .slider-label { color: var(--danger); }
[data-theme="night"] .slider[data-state="error"] { background: rgba(224, 138, 118, .12); }

.slider.is-empty-hint .slider-knob { animation: knob-nudge 1s ease 1; }

@keyframes slider-sweep {
  from { transform: translateX(-100%); }
  to { transform: translateX(100%); }
}

@keyframes slider-halo {
  0%, 100% { box-shadow: 0 14px 30px rgba(18, 20, 18, .26), 0 0 0 0 rgba(0, 0, 0, 0); }
  50% { box-shadow: 0 14px 30px rgba(18, 20, 18, .26), 0 0 0 10px var(--accent-soft); }
}

@keyframes knob-nudge {
  0%, 100% { transform: translateX(0); }
  40% { transform: translateX(14px); }
  70% { transform: translateX(4px); }
}

html[data-reduced="true"] .slider,
html[data-reduced="true"] .slider-knob { animation: none !important; transition-duration: .001s; }

/* мелкие правки списка */
.server-flag { display: grid; place-items: center; }

.head-actions .text-action {
  padding: 7px 13px;
  border: 1px solid var(--line);
  border-radius: var(--r-pill);
  background: var(--paper-2);
  font-family: var(--sans);
  font-size: 12px;
  font-weight: 500;
  text-transform: none;
  letter-spacing: 0;
  color: var(--ink);
  text-decoration: none;
}

.head-actions .text-action:hover { background: var(--paper); border-color: var(--line-strong); }
.head-actions { gap: 8px; }
"""

rep21("</style>\n</head>", SLIDER_CSS + "</style>\n</head>", 'slider-css')

open(DST, 'w', encoding='utf-8').write(s)
print('pass21 OK: %d edits total' % len(done))

# ═══════════════ pass 22: логика слайдера ═══════════════════════════════════
s = open(DST, encoding='utf-8').read()


def rep22(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep22("""    connect: $('#connect'),""",
      """    slider: $('#connect-slider'),
    sliderKnob: $('#slider-knob'),
    sliderLabel: $('#slider-label'),""",
      'slider-refs')

rep22("""  function setHomeClasses() {
    const server = selectedServer();
    const empty = !server;
    const vpn = vpnStateName();
    const busy = vpn === 'connecting';
    const online = vpn === 'connected';
    const failed = vpn === 'error';

    ui.connect.classList.toggle('is-empty', empty);
    ui.connect.classList.toggle('is-on', !empty && online);
    ui.connect.classList.toggle('is-connecting', !empty && busy);
    ui.connect.classList.toggle('is-error', !empty && failed);
    ui.connStatus.classList.toggle('is-on', !empty && online);
    ui.connStatus.classList.toggle('is-error', !empty && failed);""",
      """  const slider = {
    el: null,
    knob: null,
    label: null,
    offset: 0,
    max: 0,
    dragging: false,
    startX: 0,
    startOffset: 0
  };

  function sliderMax() {
    if (!slider.el || !slider.knob) return 0;
    return Math.max(0, slider.el.clientWidth - slider.knob.offsetWidth - 12);
  }

  function sliderPaint(offset, animate) {
    if (!slider.knob) return;
    slider.offset = offset;
    if (!animate) slider.knob.style.transition = 'none';
    slider.knob.style.transform = 'translateX(' + offset + 'px)';
    if (!animate) {
      void slider.knob.offsetWidth;
      slider.knob.style.transition = '';
    }
  }

  function sliderState(state) {
    if (!slider.el) return;
    slider.el.dataset.state = state;
    if (state === 'connected') {
      sliderPaint(0, true);
      if (slider.label) slider.label.textContent = 'Отключить';
    } else if (state === 'connecting') {
      slider.max = sliderMax();
      sliderPaint(slider.max, true);
      if (slider.label) slider.label.textContent = 'Подключение…';
    } else if (state === 'error') {
      slider.max = sliderMax();
      sliderPaint(0, true);
      if (slider.label) slider.label.textContent = state.vpn.error || 'Повторите попытку';
    } else if (state === 'empty') {
      sliderPaint(0, true);
      if (slider.label) slider.label.textContent = 'Добавьте сервер';
    } else {
      slider.max = sliderMax();
      sliderPaint(0, true);
      if (slider.label) slider.label.textContent = 'Потяните, чтобы подключить';
    }
  }

  function sliderPrimary() {
    const server = selectedServer();
    if (!server) {
      if (!state.servers.length) openAddServer();
      else showView('servers');
      return;
    }
    const vpn = vpnStateName();
    if (vpn === 'connected' || vpn === 'connecting' || vpn === 'error') {
      stopConnection();
      return;
    }
    startConnection();
  }

  function bindSlider() {
    const el = ui.slider;
    const knob = ui.sliderKnob;
    if (!el || !knob) return;
    slider.el = el;
    slider.knob = knob;
    slider.label = ui.sliderLabel;

    knob.addEventListener('pointerdown', function (event) {
      const vpn = vpnStateName();
      if (vpn === 'connected') return;
      if (el.dataset.state === 'empty') return;
      slider.dragging = true;
      slider.startX = event.clientX;
      slider.startOffset = slider.offset;
      slider.max = sliderMax();
      el.classList.add('is-dragging');
      if (knob.setPointerCapture) knob.setPointerCapture(event.pointerId);
      event.preventDefault();
    });

    knob.addEventListener('pointermove', function (event) {
      if (!slider.dragging) return;
      const raw = slider.startOffset + (event.clientX - slider.startX);
      const max = slider.max || sliderMax();
      const eased = Math.max(0, Math.min(max * 1.06, raw));
      sliderPaint(Math.min(max, eased), false);
      if (eased >= max * 0.62) el.classList.add('is-armed');
      else el.classList.remove('is-armed');
    });

    function release() {
      if (!slider.dragging) return;
      slider.dragging = false;
      el.classList.remove('is-dragging');
      const max = slider.max || sliderMax();
      el.classList.remove('is-armed');
      if (slider.offset >= max * 0.62) {
        sliderPaint(max, true);
        haptic();
        sliderPrimary();
      } else {
        sliderPaint(0, true);
      }
    }

    knob.addEventListener('pointerup', release);
    knob.addEventListener('pointercancel', release);
    knob.addEventListener('lostpointercapture', release);

    knob.addEventListener('click', function (event) {
      event.preventDefault();
      const current = vpnStateName();
      if (current === 'connected') { stopConnection(); return; }
      if (el.dataset.state === 'empty') { sliderPrimary(); return; }
      el.classList.add('is-empty-hint');
      window.setTimeout(function () { el.classList.remove('is-empty-hint'); }, 1100);
      if (slider.offset < (slider.max || sliderMax()) * 0.5) {
        showToast('Потяните ползунок вправо, чтобы подключиться');
      }
    });

    window.addEventListener('resize', function () {
      slider.max = sliderMax();
      if (vpnStateName() === 'connecting') sliderPaint(slider.max, true);
    });
  }

  function syncSlider() {
    if (!slider.el) return;
    const server = selectedServer();
    const vpn = vpnStateName();
    if (!server) { sliderState('empty'); return; }
    if (vpn === 'connected') sliderState('connected');
    else if (vpn === 'connecting') sliderState('connecting');
    else if (vpn === 'error') sliderState('error');
    else sliderState('idle');
  }

  function setHomeClasses() {
    const server = selectedServer();
    const empty = !server;
    const vpn = vpnStateName();
    const busy = vpn === 'connecting';
    const online = vpn === 'connected';
    const failed = vpn === 'error';

    ui.connStatus.classList.toggle('is-on', !empty && online);
    ui.connStatus.classList.toggle('is-error', !empty && failed);
    syncSlider();""",
      'slider-logic')

rep22("""  ui.connect.addEventListener('click', function () {
    const server = selectedServer();
    if (!server) {
      if (!state.servers.length) openAddServer();
      else showView('servers');
      return;
    }
    const vpn = vpnStateName();
    if (vpn === 'connected' || vpn === 'connecting' || vpn === 'error') {
      stopConnection();
      return;
    }
    startConnection();
  });""",
      """  bindSlider();""",
      'slider-bind')

open(DST, 'w', encoding='utf-8').write(s)
print('pass22 OK: %d edits total' % len(done))

# ═══════════════ pass 23: остатки старой кнопки ══════════════════════════════
s = open(DST, encoding='utf-8').read()


def rep23(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep23("""      ui.connect.setAttribute('aria-label', state.servers.length ? 'Выбрать сервер' : 'Добавить сервер');""",
      """      if (ui.slider) ui.slider.setAttribute('aria-label', state.servers.length ? 'Выбрать сервер' : 'Добавить сервер');""",
      'drop-connect-1')

rep23("""    ui.connect.setAttribute('aria-label', online || busy ? 'Отключить' : 'Подключить');""",
      """    if (ui.slider) ui.slider.setAttribute('aria-label', online || busy ? 'Отключить' : 'Подключить');""",
      'drop-connect-2')

rep23("""    ui.connect.click();""",
      """    if (ui.sliderKnob) ui.sliderKnob.click();""",
      'drop-connect-3')

open(DST, 'w', encoding='utf-8').write(s)
print('pass23 OK: %d edits total' % len(done))

# ═══════════════ pass 24: косметика слайдера + живой пинг ═══════════════════
s = open(DST, encoding='utf-8').read()


def rep24(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep24(""".slider[data-state="connected"] .slider-knob {
  left: 6px;
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, .16);
  color: #fff;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .4), inset 0 0 0 1px rgba(255, 255, 255, .22);
}""",
      """.slider[data-state="connected"] .slider-knob {
  left: 6px;
  top: 6px;
  width: 56px;
  height: 56px;
  background: transparent;
  color: #fff;
  box-shadow: none;
}

.slider[data-state="connected"] .slider-knob::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 50%;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, .30);
}""",
      'slider-circle')

# пинг выбранного сервера: сразу и после подключения
rep24("""  function pingAll(silent) {""",
      """  function pingSelected() {
    const server = selectedServer();
    if (!server || !native || typeof native.ping !== 'function') return;
    if (!server.host || !server.port) return;
    try {
      native.ping(JSON.stringify([{ id: server.id, host: server.host, port: server.port }]));
    } catch (error) { /* нет моста — останется «—» */ }
  }

  function pingAll(silent) {""",
      'ping-selected')

rep24("""      if (online) {
        haptic();
        showToast(label ? 'Подключено: ' + label : 'Туннель активен');""",
      """      if (online) {
        haptic();
        pingSelected();
        showToast(label ? 'Подключено: ' + label : 'Туннель активен');""",
      'ping-on-connect')

rep24("""    if (goHome) showView('home');
    if (changed) reconnectIfActive();""",
      """    if (goHome) showView('home');
    pingSelected();
    if (changed) reconnectIfActive();""",
      'ping-on-select')

rep24("""  bindSlider();""",
      """  bindSlider();
  window.setTimeout(function () {
    if (settings.ping) pingSelected();
  }, 700);""",
      'ping-on-start')

open(DST, 'w', encoding='utf-8').write(s)
print('pass24 OK: %d edits total' % len(done))

# ═══════════════ pass 25: обновление главной после замера ════════════════════
s = open(DST, encoding='utf-8').read()
if s.count("""    state.latencyAt = Date.now();
    if (ui.pingAll) {
      ui.pingAll.disabled = false;
      ui.pingAll.textContent = 'Задержка';
    }
    renderServers();""") != 1:
    print('!! latency refresh'); sys.exit(1)
s = s.replace("""    state.latencyAt = Date.now();
    if (ui.pingAll) {
      ui.pingAll.disabled = false;
      ui.pingAll.textContent = 'Задержка';
    }
    renderServers();""",
"""    state.latencyAt = Date.now();
    if (ui.pingAll) {
      ui.pingAll.disabled = false;
      ui.pingAll.textContent = 'Задержка';
    }
    renderServers();
    updateHome();""")
done.append('latency-home')
open(DST, 'w', encoding='utf-8').write(s)
print('pass25 OK: %d edits total' % len(done))

# ═══════════════ pass 26: глобус — тап, подписи, глоу ═══════════════════════
s = open(DST, encoding='utf-8').read()


def rep26(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# 1. тап по маркеру = подключиться
rep26("""    button.addEventListener('click', function (event) {
      event.stopPropagation();
      self.select(server.id);
    });""",
      """    button.addEventListener('click', function (event) {
      event.stopPropagation();
      self.select(server.id);
      if (typeof self.onPick === 'function') self.onPick(server);
    });""",
      'globe-tap')

# 2. подписи не «едут» вместе с вращением
rep26("""    this.drawGlobe();
    this.drawArc(now);
    this.updateMarkers();
  };""",
      """    const spinning = this.dragging
      || Math.abs(this.velY) > 0.00012
      || Math.abs(this.velX) > 0.00009
      || (this.autoRotate && !this.paused && !this.hoverHold && !this.reduced
          && now > this.idleUntil && !this.connected);
    if (spinning !== this.spinning) {
      this.spinning = spinning;
      if (this.layer) this.layer.classList.toggle('is-spinning', spinning);
    }

    this.drawGlobe();
    this.drawArc(now);
    this.updateMarkers();
  };""",
      'globe-spin-flag')

# 3. глоу на точках рядом с линией маршрута
rep26("""    ctx.globalAlpha = 1;
  };

  DotGlobe.prototype.drawArc = function (now) {""",
      """    ctx.globalAlpha = 1;

    if (this.arcOn && this.arc && this.colors.accent) {
      this.drawArcGlow(xs, ys, buckets);
    }
  };

  /** Акцентное свечение точек планеты рядом с линией маршрута. */
  DotGlobe.prototype.drawArcGlow = function (xs, ys, buckets) {
    const ctx = this.ctx;
    const points = this.arc.points;
    const screen = [];
    const p = {};
    const step = Math.max(1, Math.floor(points.length / 26));
    for (let i = 0; i < points.length; i += step) {
      this.project(points[i], p);
      if (p.z > 0.03) screen.push({ x: p.x, y: p.y });
    }
    if (screen.length < 2) return;

    const reach = 30;
    let x1 = Infinity;
    let x2 = -Infinity;
    let y1 = Infinity;
    let y2 = -Infinity;
    screen.forEach(function (point) {
      if (point.x < x1) x1 = point.x;
      if (point.x > x2) x2 = point.x;
      if (point.y < y1) y1 = point.y;
      if (point.y > y2) y2 = point.y;
    });
    x1 -= reach; x2 += reach; y1 -= reach; y2 += reach;

    const segments = [];
    for (let i = 1; i < screen.length; i += 1) {
      segments.push([screen[i - 1].x, screen[i - 1].y, screen[i].x, screen[i].y]);
    }

    const size = this.dotSize;
    const pulse = 0.86 + 0.14 * Math.sin((this.arc.began || performance.now()) / 420);
    ctx.globalCompositeOperation = 'lighter';

    for (let i = 0; i < this.count; i += 1) {
      const x = xs[i];
      const y = ys[i];
      if (x < x1 || x > x2 || y < y1 || y > y2) continue;
      let best = Infinity;
      for (let k = 0; k < segments.length; k += 1) {
        const seg = segments[k];
        const vx = seg[2] - seg[0];
        const vy = seg[3] - seg[1];
        const wx = x - seg[0];
        const wy = y - seg[1];
        const len2 = vx * vx + vy * vy || 1;
        let t = (wx * vx + wy * vy) / len2;
        t = t < 0 ? 0 : (t > 1 ? 1 : t);
        const dx = wx - vx * t;
        const dy = wy - vy * t;
        const dist = dx * dx + dy * dy;
        if (dist < best) best = dist;
        if (best < 1) break;
      }
      const dist = Math.sqrt(best);
      if (dist > reach) continue;
      const depth = buckets[i] / 7;
      const energy = Math.pow(1 - dist / reach, 2.1) * (0.30 + 0.70 * depth) * pulse;
      if (energy < 0.03) continue;
      const radius = size * (1.5 + 2.6 * energy);
      ctx.globalAlpha = Math.min(0.9, energy);
      ctx.fillStyle = this.colors.accent;
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.globalCompositeOperation = 'source-over';
    ctx.globalAlpha = 1;
  };

  DotGlobe.prototype.drawArc = function (now) {""",
      'globe-glow')

# 4. перемещение точки «вы» (определение города)
rep26("""  DotGlobe.prototype.removeServer = function (id) {""",
      """  DotGlobe.prototype.setOrigin = function (origin) {
    if (!origin || !Number.isFinite(Number(origin.lat)) || !Number.isFinite(Number(origin.lng))) return;
    this.origin = {
      city: origin.city || this.origin.city,
      country: origin.country || this.origin.country,
      lat: Number(origin.lat),
      lng: Number(origin.lng)
    };
    this.originVec = latLng(this.origin.lat, this.origin.lng, 1.007);
    const selected = this.selectedId;
    const server = this.servers.filter(function (s) { return s.id === selected; })[0];
    if (server) this.makeArc(server, true);
    else this.focusOrigin(true);
  };

  DotGlobe.prototype.removeServer = function (id) {""",
      'globe-origin')

open(DST, 'w', encoding='utf-8').write(s)
print('pass26 OK: %d edits total' % len(done))

# ═══════════════ pass 27: связка глобуса и главной ══════════════════════════
s = open(DST, encoding='utf-8').read()


def rep27(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep27("""      if (state.connected) {
        showToast('Переключено: ' + (server.flag ? server.flag + ' ' + server.city : server.city));
      }
    }
  });""",
      """      if (state.connected) {
        showToast('Переключено: ' + (server.flag ? server.flag + ' ' + server.city : server.city));
      }
    }
  });

  // тап по точке на карте — сразу подключаемся
  globe.onPick = function (server) {
    if (!server) return;
    const vpn = vpnStateName();
    if (vpn === 'connected' && state.selectedId === server.id) return;
    haptic();
    startConnection();
  };""",
      'globe-pick')

rep27("</style>\n</head>",
      """
/* подписи городов не «уезжают» вместе с вращением карты */
#markers.is-spinning .srv-label {
  opacity: 0;
  visibility: hidden;
  transform: translate(-50%, -3px) scale(.96);
  transition: opacity .14s ease, transform .14s ease, visibility 0s linear .14s;
}
</style>
</head>""",
      'label-spin-css')

open(DST, 'w', encoding='utf-8').write(s)
print('pass27 OK: %d edits total' % len(done))

# ═══════════════ pass 28: мягче глоу, чище кнопка ═══════════════════════════
s = open(DST, encoding='utf-8').read()


def rep28(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep28("""    const reach = 30;""", """    const reach = 16;""", 'glow-reach')

rep28("""    const size = this.dotSize;
    const pulse = 0.86 + 0.14 * Math.sin((this.arc.began || performance.now()) / 420);
    ctx.globalCompositeOperation = 'lighter';""",
      """    const size = this.dotSize;
    const pulse = 0.82 + 0.18 * Math.sin((this.arc.began || performance.now()) / 460);""",
      'glow-blend')

rep28("""      const depth = buckets[i] / 7;
      const energy = Math.pow(1 - dist / reach, 2.1) * (0.30 + 0.70 * depth) * pulse;
      if (energy < 0.03) continue;
      const radius = size * (1.5 + 2.6 * energy);
      ctx.globalAlpha = Math.min(0.9, energy);
      ctx.fillStyle = this.colors.accent;
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.globalCompositeOperation = 'source-over';
    ctx.globalAlpha = 1;""",
      """      const depth = buckets[i] / 7;
      const energy = Math.pow(1 - dist / reach, 3.2) * (0.22 + 0.78 * depth) * pulse;
      if (energy < 0.04) continue;
      const radius = size * (1.1 + 1.5 * energy);
      ctx.globalAlpha = Math.min(0.42, energy * 0.5);
      ctx.fillStyle = this.colors.accent;
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.globalAlpha = 1;""",
      'glow-soft')

rep28(""".slider[data-state="connected"] .slider-knob::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 50%;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, .30);
}""",
      """.slider[data-state="connected"] .slider-knob::after {
  content: "";
  position: absolute;
  inset: 8px;
  border-radius: 50%;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, .22);
  opacity: 0;
}""",
      'slider-ring')

open(DST, 'w', encoding='utf-8').write(s)
print('pass28 OK: %d edits total' % len(done))

# ═══════════════ pass 29: города и точное определение локации ════════════════
s = open(DST, encoding='utf-8').read()


def rep29(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# name|iso|lat|lng|aliases|timezone
CITY_ROWS = [
    "Хельсинки|FI|60.1699|24.9384|helsinki,hel,helsinki1|Europe/Helsinki",
    "Тампере|FI|61.4978|23.7610|tampere,tmp|Europe/Helsinki",
    "Турку|FI|60.4518|22.2666|turku,tku|Europe/Helsinki",
    "Стокгольм|SE|59.3293|18.0686|stockholm,sto|Europe/Stockholm",
    "Гётеборг|SE|57.7089|11.9746|gothenburg,goteborg,got|Europe/Stockholm",
    "Мальмё|SE|55.6050|13.0038|malmo,mmx|Europe/Stockholm",
    "Осло|NO|59.9139|10.7522|oslo,osl|Europe/Oslo",
    "Берген|NO|60.3913|5.3221|bergen,bgo|Europe/Oslo",
    "Копенгаген|DK|55.6761|12.5683|copenhagen,kobenhavn,cph|Europe/Copenhagen",
    "Амстердам|NL|52.3676|4.9041|amsterdam,ams|Europe/Amsterdam",
    "Роттердам|NL|51.9244|4.4777|rotterdam,rtm|Europe/Amsterdam",
    "Брюссель|BE|50.8503|4.3517|brussels,bruxelles,bru|Europe/Brussels",
    "Антверпен|BE|51.2194|4.4025|antwerp,anr|Europe/Brussels",
    "Франкфурт|DE|50.1109|8.6821|frankfurt,fra,frankfurt am main|Europe/Berlin",
    "Берлин|DE|52.5200|13.4050|berlin,ber|Europe/Berlin",
    "Мюнхен|DE|48.1351|11.5820|munich,muenchen,muc|Europe/Berlin",
    "Гамбург|DE|53.5511|9.9937|hamburg,ham|Europe/Berlin",
    "Дюссельдорф|DE|51.2277|6.7735|dusseldorf,dus|Europe/Berlin",
    "Кёльн|DE|50.9375|6.9603|cologne,koln,cgn|Europe/Berlin",
    "Штутгарт|DE|48.7758|9.1829|stuttgart,str|Europe/Berlin",
    "Нюрнберг|DE|49.4521|11.0767|nuremberg,nurnberg,nue|Europe/Berlin",
    "Париж|FR|48.8566|2.3522|paris,cdg,ory|Europe/Paris",
    "Марсель|FR|43.2965|5.3698|marseille,mrs|Europe/Paris",
    "Лион|FR|45.7640|4.8357|lyon,lys|Europe/Paris",
    "Страсбург|FR|48.5734|7.7521|strasbourg,sxb|Europe/Paris",
    "Лондон|GB|51.5074|-0.1278|london,lhr,lgw|Europe/London",
    "Манчестер|GB|53.4808|-2.2426|manchester,man|Europe/London",
    "Эдинбург|GB|55.9533|-3.1883|edinburgh,edi|Europe/London",
    "Дублин|IE|53.3498|-6.2603|dublin,dub|Europe/Dublin",
    "Мадрид|ES|40.4168|-3.7038|madrid,mad|Europe/Madrid",
    "Барселона|ES|41.3874|2.1686|barcelona,bcn|Europe/Madrid",
    "Валенсия|ES|39.4699|-0.3763|valencia,vlc|Europe/Madrid",
    "Лиссабон|PT|38.7223|-9.1393|lisbon,lisboa,lis|Europe/Lisbon",
    "Порту|PT|41.1579|-8.6291|porto,opo|Europe/Lisbon",
    "Милан|IT|45.4642|9.1900|milan,milano,mil,lin|Europe/Rome",
    "Рим|IT|41.9028|12.4964|rome,roma,fco|Europe/Rome",
    "Турин|IT|45.0703|7.6869|turin,torino,trn|Europe/Rome",
    "Цюрих|CH|47.3769|8.5417|zurich,zuerich,zrh|Europe/Zurich",
    "Женева|CH|46.2044|6.1432|geneva,genf,gva|Europe/Zurich",
    "Вена|AT|48.2082|16.3738|vienna,wien,vie|Europe/Vienna",
    "Зальцбург|AT|47.8095|13.0550|salzburg,szg|Europe/Vienna",
    "Прага|CZ|50.0755|14.4378|prague,praha,prg|Europe/Prague",
    "Брно|CZ|49.1951|16.6068|brno,brq|Europe/Prague",
    "Братислава|SK|48.1486|17.1077|bratislava,bts|Europe/Bratislava",
    "Варшава|PL|52.2297|21.0122|warsaw,warszawa,waw|Europe/Warsaw",
    "Краков|PL|50.0647|19.9450|krakow,cracow,krk|Europe/Warsaw",
    "Гданьск|PL|54.3520|18.6466|gdansk,gd,dnk|Europe/Warsaw",
    "Будапешт|HU|47.4979|19.0402|budapest,bud|Europe/Budapest",
    "Бухарест|RO|44.4268|26.1025|bucharest,bucuresti,otp|Europe/Bucharest",
    "Клуж|RO|46.7712|23.6236|cluj,cluj-napoca|Europe/Bucharest",
    "София|BG|42.6977|23.3219|sofia,sof|Europe/Sofia",
    "Варна|BG|43.2141|27.9147|varna,var|Europe/Sofia",
    "Афины|GR|37.9838|23.7275|athens,athina,ath|Europe/Athens",
    "Салоники|GR|40.6401|22.9444|thessaloniki,skg|Europe/Athens",
    "Стамбул|TR|41.0082|28.9784|istanbul,ist|Europe/Istanbul",
    "Анкара|TR|39.9334|32.8597|ankara,esb|Europe/Istanbul",
    "Измир|TR|38.4237|27.1428|izmir,adb|Europe/Istanbul",
    "Москва|RU|55.7558|37.6173|moscow,moscow,svo,dme|Europe/Moscow",
    "Санкт-Петербург|RU|59.9311|30.3609|saint petersburg,st petersburg,spb,led|Europe/Moscow",
    "Екатеринбург|RU|56.8389|60.6057|yekaterinburg,ekaterinburg,svx|Asia/Yekaterinburg",
    "Новосибирск|RU|55.0084|82.9357|novosibirsk,ovb|Asia/Novosibirsk",
    "Казань|RU|55.7963|49.1088|kazan,kzn|Europe/Moscow",
    "Сочи|RU|43.6028|39.7342|sochi,aer|Europe/Moscow",
    "Киев|UA|50.4501|30.5234|kyiv,kiev,kbp|Europe/Kiev",
    "Львов|UA|49.8397|24.0297|lviv,lvov,lwo|Europe/Kiev",
    "Одесса|UA|46.4825|30.7233|odesa,odessa,ods|Europe/Kiev",
    "Минск|BY|53.9006|27.5590|minsk,msq|Europe/Minsk",
    "Алматы|KZ|43.2220|76.8512|almaty,ala|Asia/Almaty",
    "Астана|KZ|51.1694|71.4491|astana,nur-sultan,nqz|Asia/Almaty",
    "Тбилиси|GE|41.7151|44.8271|tbilisi,tbs|Asia/Tbilisi",
    "Батуми|GE|41.6168|41.6367|batumi,bus|Asia/Tbilisi",
    "Ереван|AM|40.1792|44.4991|yerevan,evn|Asia/Yerevan",
    "Баку|AZ|40.4093|49.8671|baku,gyd|Asia/Baku",
    "Тель-Авив|IL|32.0853|34.7818|tel aviv,tlv|Asia/Jerusalem",
    "Иерусалим|IL|31.7683|35.2137|jerusalem,jrs|Asia/Jerusalem",
    "Дубай|AE|25.2048|55.2708|dubai,dxb|Asia/Dubai",
    "Абу-Даби|AE|24.4539|54.3773|abu dhabi,auh|Asia/Dubai",
    "Эр-Рияд|SA|24.7136|46.6753|riyadh,ruh|Asia/Riyadh",
    "Джидда|SA|21.4858|39.1925|jeddah,jed|Asia/Riyadh",
    "Доха|QA|25.2854|51.5310|doha,doh|Asia/Qatar",
    "Эль-Кувейт|KW|29.3759|47.9774|kuwait,kwi|Asia/Kuwait",
    "Каир|EG|30.0444|31.2357|cairo,cai|Africa/Cairo",
    "Йоханнесбург|ZA|26.2041|28.0473|johannesburg,jnb|Africa/Johannesburg",
    "Кейптаун|ZA|33.9249|18.4241|cape town,cpt|Africa/Johannesburg",
    "Лагос|NG|6.5244|3.3792|lagos,los|Africa/Lagos",
    "Найроби|KE|-1.2921|36.8219|nairobi,nbo|Africa/Nairobi",
    "Касабланка|MA|33.5731|-7.5898|casablanca,cmn|Africa/Casablanca",
    "Мумбаи|IN|19.0760|72.8777|mumbai,bombay,bom|Asia/Kolkata",
    "Дели|IN|28.6139|77.2090|delhi,new delhi,del|Asia/Kolkata",
    "Бангалор|IN|12.9716|77.5946|bangalore,bengaluru,blr|Asia/Kolkata",
    "Ченнаи|IN|13.0827|80.2707|chennai,madras,maa|Asia/Kolkata",
    "Карачи|PK|24.8607|67.0011|karachi,khi|Asia/Karachi",
    "Лахор|PK|31.5204|74.3587|lahore,lhe|Asia/Karachi",
    "Дакка|BD|23.8103|90.4125|dhaka,dac|Asia/Dhaka",
    "Коломбо|LK|6.9271|79.8612|colombo,cmb|Asia/Colombo",
    "Катманду|NP|27.7172|85.3240|kathmandu,ktm|Asia/Kathmandu",
    "Сингапур|SG|1.3521|103.8198|singapore,sin|Asia/Singapore",
    "Куала-Лумпур|MY|3.1390|101.6869|kuala lumpur,kul|Asia/Kuala_Lumpur",
    "Бангкок|TH|13.7563|100.5018|bangkok,bkk|Asia/Bangkok",
    "Ханой|VN|21.0278|105.8342|hanoi,han|Asia/Bangkok",
    "Хошимин|VN|10.8231|106.6297|ho chi minh,saigon,sgn|Asia/Bangkok",
    "Джакарта|ID|-6.2088|106.8456|jakarta,cgk|Asia/Jakarta",
    "Денпасар|ID|-8.6705|115.2126|bali,denpasar,dps|Asia/Makassar",
    "Манила|PH|14.5995|120.9842|manila,mnl|Asia/Manila",
    "Гонконг|HK|22.3193|114.1694|hong kong,hkg|Asia/Hong_Kong",
    "Тайбэй|TW|25.0330|121.5654|taipei,tpe|Asia/Taipei",
    "Токио|JP|35.6762|139.6503|tokyo,nrt,hnd|Asia/Tokyo",
    "Осака|JP|34.6937|135.5023|osaka,kix|Asia/Tokyo",
    "Сеул|KR|37.5665|126.9780|seoul,icn|Asia/Seoul",
    "Пусан|KR|35.1796|129.0756|busan,pus|Asia/Seoul",
    "Пекин|CN|39.9042|116.4074|beijing,pek|Asia/Shanghai",
    "Шанхай|CN|31.2304|121.4737|shanghai,pvg|Asia/Shanghai",
    "Гуанчжоу|CN|23.1291|113.2644|guangzhou,can|Asia/Shanghai",
    "Улан-Батор|MN|47.8864|106.9057|ulaanbaatar,uln|Asia/Ulaanbaatar",
    "Сидней|AU|-33.8688|151.2093|sydney,syd|Australia/Sydney",
    "Мельбурн|AU|-37.8136|144.9631|melbourne,mel|Australia/Melbourne",
    "Брисбен|AU|-27.4698|153.0251|brisbane,bne|Australia/Brisbane",
    "Перт|AU|-31.9505|115.8605|perth,per|Australia/Perth",
    "Окленд|NZ|-36.8485|174.7633|auckland,akl|Pacific/Auckland",
    "Нью-Йорк|US|40.7128|-74.0060|new york,newyork,nyc,jfk,ewr|America/New_York",
    "Лос-Анджелес|US|34.0522|-118.2437|los angeles,lax|America/Los_Angeles",
    "Чикаго|US|41.8781|-87.6298|chicago,ord|America/Chicago",
    "Даллас|US|32.7767|-96.7970|dallas,dfw|America/Chicago",
    "Майами|US|25.7617|-80.1918|miami,mia|America/New_York",
    "Сиэтл|US|47.6062|-122.3321|seattle,sea|America/Los_Angeles",
    "Сан-Франциско|US|37.7749|-122.4194|san francisco,sfo|America/Los_Angeles",
    "Вашингтон|US|38.9072|-77.0369|washington,washington dc,iad,dca|America/New_York",
    "Бостон|US|42.3601|-71.0589|boston,bos|America/New_York",
    "Атланта|US|33.7490|-84.3880|atlanta,atl|America/New_York",
    "Денвер|US|39.7392|-104.9903|denver,den|America/Denver",
    "Лас-Вегас|US|36.1699|-115.1398|las vegas,vegas,las|America/Los_Angeles",
    "Финикс|US|33.4484|-112.0740|phoenix,phx|America/Phoenix",
    "Хьюстон|US|29.7604|-95.3698|houston,hou|America/Chicago",
    "Торонто|CA|43.6532|-79.3832|toronto,yyz|America/Toronto",
    "Монреаль|CA|45.5017|-73.5673|montreal,yul|America/Toronto",
    "Ванкувер|CA|49.2827|-123.1207|vancouver,yvr|America/Vancouver",
    "Калгари|CA|51.0447|-114.0719|calgary,yyc|America/Edmonton",
    "Мехико|MX|19.4326|-99.1332|mexico city,cdmx,mex|America/Mexico_City",
    "Канкун|MX|21.1619|-86.8515|cancun,cun|America/Cancun",
    "Сан-Паулу|BR|-23.5505|-46.6333|sao paulo,são paulo,gru|America/Sao_Paulo",
    "Рио-де-Жанейро|BR|-22.9068|-43.1729|rio de janeiro,rio,gig|America/Sao_Paulo",
    "Буэнос-Айрес|AR|-34.6037|-58.3816|buenos aires,eze|America/Argentina/Buenos_Aires",
    "Сантьяго|CL|-33.4489|-70.6693|santiago,scl|America/Santiago",
    "Богота|CO|4.7110|-74.0721|bogota,bog|America/Bogota",
    "Лима|PE|-12.0464|-77.0428|lima,lim|America/Lima",
    "Каракас|VE|10.4806|-66.9036|caracas,ccs|America/Caracas",
    "Кито|EC|-0.1807|-78.4678|quito,uio|America/Guayaquil",
    "Монтевидео|UY|-34.9011|-56.1645|montevideo,mvd|America/Montevideo",
]

COUNTRY_ROWS = [
    "UA|Украина|Киев|50.4501|30.5234",
    "BY|Беларусь|Минск|53.9006|27.5590",
    "KZ|Казахстан|Алматы|43.2220|76.8512",
    "GE|Грузия|Тбилиси|41.7151|44.8271",
    "AM|Армения|Ереван|40.1792|44.4991",
    "AZ|Азербайджан|Баку|40.4093|49.8671",
    "IL|Израиль|Тель-Авив|32.0853|34.7818",
    "AE|ОАЭ|Дубай|25.2048|55.2708",
    "SA|Саудовская Арабия|Эр-Рияд|24.7136|46.6753",
    "QA|Катар|Доха|25.2854|51.5310",
    "KW|Кувейт|Эль-Кувейт|29.3759|47.9774",
    "EG|Египет|Каир|30.0444|31.2357",
    "ZA|ЮАР|Йоханнесбург|26.2041|28.0473",
    "NG|Нигерия|Лагос|6.5244|3.3792",
    "KE|Кения|Найроби|-1.2921|36.8219",
    "MA|Марокко|Касабланка|33.5731|-7.5898",
    "IN|Индия|Мумбаи|19.0760|72.8777",
    "PK|Пакистан|Карачи|24.8607|67.0011",
    "BD|Бангладеш|Дакка|23.8103|90.4125",
    "LK|Шри-Ланка|Коломбо|6.9271|79.8612",
    "NP|Непал|Катманду|27.7172|85.3240",
    "SG|Сингапур|Сингапур|1.3521|103.8198",
    "MY|Малайзия|Куала-Лумпур|3.1390|101.6869",
    "TH|Таиланд|Бангкок|13.7563|100.5018",
    "VN|Вьетнам|Ханой|21.0278|105.8342",
    "ID|Индонезия|Джакарта|-6.2088|106.8456",
    "PH|Филиппины|Манила|14.5995|120.9842",
    "HK|Гонконг|Гонконг|22.3193|114.1694",
    "TW|Тайвань|Тайбэй|25.0330|121.5654",
    "JP|Япония|Токио|35.6762|139.6503",
    "KR|Южная Корея|Сеул|37.5665|126.9780",
    "CN|Китай|Пекин|39.9042|116.4074",
    "MN|Монголия|Улан-Батор|47.8864|106.9057",
    "AU|Австралия|Сидней|-33.8688|151.2093",
    "NZ|Новая Зеландия|Окленд|-36.8485|174.7633",
    "US|США|Нью-Йорк|40.7128|-74.0060",
    "CA|Канада|Торонто|43.6532|-79.3832",
    "MX|Мексика|Мехико|19.4326|-99.1332",
    "BR|Бразилия|Сан-Паулу|-23.5505|-46.6333",
    "AR|Аргентина|Буэнос-Айрес|-34.6037|-58.3816",
    "CL|Чили|Сантьяго|-33.4489|-70.6693",
    "CO|Колумбия|Богота|4.7110|-74.0721",
    "PE|Перу|Лима|-12.0464|-77.0428",
    "VE|Венесуэла|Каракас|10.4806|-66.9036",
    "EC|Эквадор|Кито|-0.1807|-78.4678",
    "UY|Уругвай|Монтевидео|-34.9011|-56.1645",
    "IE|Ирландия|Дублин|53.3498|-6.2603",
    "NO|Норвегия|Осло|59.9139|10.7522",
    "DK|Дания|Копенгаген|55.6761|12.5683",
    "BE|Бельгия|Брюссель|50.8503|4.3517",
    "PT|Португалия|Лиссабон|38.7223|-9.1393",
]

EXTRA_JS = """
window.GEO_CITIES_EXTRA = "%s".split(";").filter(Boolean).map(function (row) {
  var f = row.split("|");
  return {
    name: f[0],
    country: f[1],
    lat: Number(f[2]),
    lng: Number(f[3]),
    aliases: f[4] ? f[4].split(",") : [],
    tz: f[5] || ""
  };
});

window.GEO_COUNTRIES_EXTRA = (function () {
  var out = {};
  "%s".split(";").filter(Boolean).forEach(function (row) {
    var f = row.split("|");
    out[f[0]] = { name: f[1], capital: f[2], lat: Number(f[3]), lng: Number(f[4]) };
  });
  return out;
})();
""" % (';'.join(CITY_ROWS), ';'.join(COUNTRY_ROWS))

rep29("""window.GEO_CITIES = [""", EXTRA_JS + """
window.GEO_CITIES = [""", 'geo-extra')

rep29("""  const COUNTRIES = window.GEO_COUNTRIES || {};
  const CITIES = window.GEO_CITIES || [];""",
      """  const COUNTRIES = (function () {
    const out = {};
    const base = window.GEO_COUNTRIES || {};
    Object.keys(base).forEach(function (iso) { out[iso] = base[iso]; });
    const extra = window.GEO_COUNTRIES_EXTRA || {};
    Object.keys(extra).forEach(function (iso) { if (!out[iso]) out[iso] = extra[iso]; });
    return out;
  })();
  const CITIES = (window.GEO_CITIES || []).concat(window.GEO_CITIES_EXTRA || []);""",
      'geo-merge')

# поиск по часовому поясу + аккуратнее совпадения
rep29("""  function detectLocation(fragmentName, explicitName) {""",
      """  function timezoneCity() {
    try {
      const zone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      if (!zone) return null;
      const exact = CITIES.filter(function (city) { return city.tz === zone; })[0];
      if (exact) return exact;
      const region = zone.split('/')[0];
      const cityName = (zone.split('/')[1] || '').replace(/_/g, ' ').toLowerCase();
      if (!cityName) return null;
      const guess = CITIES.filter(function (city) {
        const aliases = [city.name].concat(city.aliases || []).map(function (alias) {
          return String(alias).toLowerCase();
        });
        return aliases.indexOf(cityName) !== -1;
      })[0];
      return guess || null;
    } catch (error) {
      return null;
    }
  }

  function detectLocation(fragmentName, explicitName) {""",
      'tz-city')

open(DST, 'w', encoding='utf-8').write(s)
print('pass29 OK: %d edits total' % len(done))

# ═══════════════ pass 30: определение города пользователя ════════════════════
s = open(DST, encoding='utf-8').read()


def rep30(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep30("""      <span class="path-from">Екатеринбург</span>""",
      """      <span class="path-from" id="path-from">Екатеринбург</span>""",
      'path-from-id')

rep30("""  const globe = new DotGlobe({""",
      """  // ── город пользователя: часовой пояс сразу, IP-геолокация точнее ─────────
  const originState = {
    city: ORIGIN.city || '',
    country: ORIGIN.country || '',
    lat: Number(ORIGIN.lat),
    lng: Number(ORIGIN.lng),
    source: 'default'
  };

  function applyOrigin(next, silent) {
    if (!next) return;
    const lat = Number(next.lat);
    const lng = Number(next.lng);
    const city = cleanText(next.city, 60);
    if (!Number.isFinite(lat) || !Number.isFinite(lng) || !city) return;
    const same = Math.abs(lat - originState.lat) < 0.01
      && Math.abs(lng - originState.lng) < 0.01
      && city === originState.city;
    originState.city = city;
    originState.country = next.country || originState.country;
    originState.lat = lat;
    originState.lng = lng;
    originState.source = next.source || originState.source;
    const label = document.getElementById('path-from');
    if (label) label.textContent = city;
    store.write('vpn.origin', { city: city, country: originState.country, lat: lat, lng: lng, at: Date.now() });
    const current = selectedServer();
    globe.setOrigin({ city: city, country: originState.country, lat: lat, lng: lng });
    if (current) globe.select(current.id, { notify: false, instant: !silent });
    updateHome();
  }

  function nearestCity(lat, lng) {
    let best = null;
    let bestDist = Infinity;
    CITIES.forEach(function (city) {
      const dx = (Number(city.lng) - lng) * Math.cos((lat * Math.PI) / 180);
      const dy = Number(city.lat) - lat;
      const dist = dx * dx + dy * dy;
      if (dist < bestDist) {
        bestDist = dist;
        best = city;
      }
    });
    return best;
  }

  window.__onLocate = function (key, payload) {
    let data = null;
    try { data = typeof payload === 'string' ? JSON.parse(payload) : payload; } catch (error) { data = null; }
    if (!data) return;
    const city = nearestCity(Number(data.lat), Number(data.lng));
    applyOrigin({
      city: city ? city.name : cleanText(data.city, 60),
      country: data.country || (city ? (COUNTRIES[city.country] || {}).name || '' : ''),
      lat: Number(data.lat),
      lng: Number(data.lng),
      source: 'ip'
    }, true);
  };

  function locateUser() {
    const cached = store.read('vpn.origin', null);
    if (cached && cached.city && Number.isFinite(Number(cached.lat))
        && Date.now() - (Number(cached.at) || 0) < 6 * 60 * 60 * 1000) {
      applyOrigin(cached, true);
    } else {
      const guess = timezoneCity();
      if (guess) {
        applyOrigin({
          city: guess.name,
          country: (COUNTRIES[guess.country] || {}).name || '',
          lat: guess.lat,
          lng: guess.lng,
          source: 'tz'
        }, true);
      }
    }
    if (native && typeof native.locate === 'function') {
      try { native.locate('o1'); } catch (error) { /* останется часовой пояс */ }
    }
  }

  const globe = new DotGlobe({""",
      'locate-js')

rep30("""  bindSlider();
  window.setTimeout(function () {
    if (settings.ping) pingSelected();
  }, 700);""",
      """  bindSlider();
  locateUser();
  window.setTimeout(function () {
    if (settings.ping) pingSelected();
  }, 700);""",
      'locate-start')

# сохранённая точка «вы» должна переживать перезапуск: читаем до создания глобуса
rep30("""  const ORIGIN = window.APP_ORIGIN || { city: 'Екатеринбург', lat: 56.8389, lng: 60.6057 };""",
      """  const ORIGIN = (function () {
    const saved = (function () {
      try {
        const raw = window.localStorage.getItem('vpn.origin');
        return raw ? JSON.parse(raw) : null;
      } catch (error) {
        return null;
      }
    })();
    if (saved && Number.isFinite(Number(saved.lat)) && Number.isFinite(Number(saved.lng)) && saved.city) {
      return { city: saved.city, country: saved.country || '', lat: Number(saved.lat), lng: Number(saved.lng) };
    }
    return window.APP_ORIGIN || { city: 'Екатеринбург', lat: 56.8389, lng: 60.6057 };
  })();""",
      'origin-cached')

open(DST, 'w', encoding='utf-8').write(s)
print('pass30 OK: %d edits total' % len(done))

# ═══════════════ pass 31: слайдер — ширина, подпись, клик после драга ═══════
s = open(DST, encoding='utf-8').read()


def rep31(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep31(""".slider {
  position: relative;
  width: 268px;
  height: 64px;""",
      """.slider {
  position: relative;
  width: 100%;
  max-width: 320px;
  height: 64px;""",
      'slider-width')

rep31("""      if (slider.label) slider.label.textContent = 'Потяните, чтобы подключить';""",
      """      if (slider.label) slider.label.textContent = 'Потяните вправо';""",
      'slider-label-text')

rep31("""      if (slider.offset >= max * 0.62) {
        sliderPaint(max, true);
        haptic();
        sliderPrimary();
      } else {
        sliderPaint(0, true);
      }""",
      """      slider.justDragged = true;
      window.setTimeout(function () { slider.justDragged = false; }, 420);
      if (slider.offset >= max * 0.62) {
        sliderPaint(max, true);
        haptic();
        sliderPrimary();
      } else {
        sliderPaint(0, true);
      }""",
      'slider-drag-flag')

rep31("""    knob.addEventListener('click', function (event) {
      event.preventDefault();
      const current = vpnStateName();""",
      """    knob.addEventListener('click', function (event) {
      event.preventDefault();
      if (slider.justDragged) { slider.justDragged = false; return; }
      const current = vpnStateName();""",
      'slider-click-guard')

open(DST, 'w', encoding='utf-8').write(s)
print('pass31 OK: %d edits total' % len(done))

# ═══════════════ pass 32: глоу вдоль линии — тоньше и только на передней части ═
s = open(DST, encoding='utf-8').read()


def rep32(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep32("""    const reach = 16;""", """    const reach = 11;""", 'glow-reach2')

rep32("""      const dist = Math.sqrt(best);
      if (dist > reach) continue;
      const depth = buckets[i] / 7;
      const energy = Math.pow(1 - dist / reach, 3.2) * (0.22 + 0.78 * depth) * pulse;
      if (energy < 0.04) continue;
      const radius = size * (1.1 + 1.5 * energy);
      ctx.globalAlpha = Math.min(0.42, energy * 0.5);""",
      """      const dist = Math.sqrt(best);
      if (dist > reach) continue;
      if (buckets[i] < 5) continue;
      const depth = buckets[i] / 7;
      const energy = Math.pow(1 - dist / reach, 2.8) * (0.3 + 0.7 * depth) * pulse;
      if (energy < 0.05) continue;
      const radius = size * (1 + 0.6 * energy);
      ctx.globalAlpha = Math.min(0.26, energy * 0.3);""",
      'glow-tune')

open(DST, 'w', encoding='utf-8').write(s)
print('pass32 OK: %d edits total' % len(done))

# ═══════════════ pass 33: крестик удаления — только у выбранной строки ═══════
s = open(DST, encoding='utf-8').read()


def rep33(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep33(""".row-more:hover { background: var(--paper-2); color: var(--ink); }
.row-remove { font-size: 17px; }
.row-remove:hover { background: rgba(155, 61, 47, .12); color: var(--danger); }""",
      """.row-more:hover { background: var(--paper-2); color: var(--ink); }
.row-remove { font-size: 17px; }
.row-remove:hover { background: rgba(155, 61, 47, .12); color: var(--danger); }

/* «×» не мусорит в списке: появляется у выбранной строки или при наведении */
.server-item .row-remove,
.group-body .server-row .row-remove {
  opacity: 0;
  visibility: hidden;
  transform: scale(.86);
  transition: opacity .16s ease, transform .16s ease, visibility 0s linear .16s;
}

.server-item.is-selected .row-remove,
.server-item:hover .row-remove,
.group-body .server-row:hover .row-remove,
.group-body .server-row.is-selected .row-remove {
  opacity: 1;
  visibility: visible;
  transform: none;
  transition: opacity .16s ease, transform .16s ease, visibility 0s;
}""",
      'row-remove-reveal')

open(DST, 'w', encoding='utf-8').write(s)
print('pass33 OK: %d edits total' % len(done))

# ═══════════════ pass 34: цвет задержки по качеству канала ═══════════════════
s = open(DST, encoding='utf-8').read()


def rep34(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep34(""".server-ping {
  font-variant-numeric: tabular-nums;
  min-width: 46px;
  text-align: center;
}""",
      """.server-ping {
  font-variant-numeric: tabular-nums;
  min-width: 46px;
  text-align: center;
  color: var(--muted);
}

.server-ping.is-mid { color: #9a6a12; background: rgba(178, 122, 26, .13); }
[data-theme="night"] .server-ping.is-mid { color: #e0b070; background: rgba(224, 176, 112, .14); }""",
      'ping-mid-css')

rep34("""    if (entry.ms == null) return { text: 'нет ответа', className: ' is-slow' };
    const tone = entry.ms < 220 ? ' is-fast' : (entry.ms > 800 ? ' is-slow' : '');
    return { text: entry.ms + ' мс', className: tone };""",
      """    if (entry.ms == null) return { text: 'нет ответа', className: ' is-slow' };
    const tone = entry.ms < 80 ? ' is-fast' : (entry.ms < 200 ? ' is-mid' : ' is-slow');
    return { text: entry.ms + ' мс', className: tone };""",
      'ping-tones')

open(DST, 'w', encoding='utf-8').write(s)
print('pass34 OK: %d edits total' % len(done))

# ═══════════════ pass 35: честная подпись про поддерживаемые протоколы ═══════
s = open(DST, encoding='utf-8').read()


def rep35(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep35("""        <p class="form-foot">Поддерживаются VLESS, Trojan, Shadowsocks, Hysteria2, TUIC и VMess.</p>""",
      """        <p class="form-foot">Ядро Xray: VLESS, VMess, Trojan, Shadowsocks. Hysteria2 и TUIC не поддерживаются.</p>""",
      'form-foot-protocols')

open(DST, 'w', encoding='utf-8').write(s)
print('pass35 OK: %d edits total' % len(done))

# ═══════════════ pass 36: нижняя панель — старая, под чистым блюром ══════════
s = open(DST, encoding='utf-8').read()


def rep36(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep36(""".dock,
.dock * { -webkit-backdrop-filter: none; }

.dock {
  overflow: hidden;
  isolation: isolate;
  border: 0;
  background: transparent;
  box-shadow:
    0 22px 48px rgba(18, 20, 18, .22),
    0 4px 12px rgba(18, 20, 18, .10);
}

.dock::before,
.dock::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
}

/* слой 1: размытие и насыщенность (как у матового стекла) */
.dock::before {
  z-index: 0;
  background: var(--glass-tint);
  -webkit-backdrop-filter: blur(14px) saturate(180%) brightness(1.04);
  backdrop-filter: blur(14px) saturate(180%) brightness(1.04);
}

/* слой 2: настоящее преломление — дисплейсмент карты нормалей + хроматика */
.dock::after {
  z-index: 1;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, .30), rgba(255, 255, 255, 0) 42%),
    radial-gradient(120% 160% at 50% -20%, rgba(255, 255, 255, .22), rgba(255, 255, 255, 0) 60%);
  -webkit-backdrop-filter: url(#lg-refract);
  backdrop-filter: url(#lg-refract);
  box-shadow:
    inset 0 1.5px 0 var(--glass-edge),
    inset 0 -1.5px 0 rgba(0, 0, 0, .10),
    inset 0 0 0 1px var(--glass-ink);
}

.dock > .dock-item { position: relative; z-index: 2; }
.dock > .dock-mark { z-index: 2; }

[data-glass="off"] .dock::after {
  -webkit-backdrop-filter: blur(2px) saturate(160%);
  backdrop-filter: blur(2px) saturate(160%);
}""",
      """.dock,
.dock * { -webkit-backdrop-filter: none; }

/* чистое стекло: один слой блюра, без преломления */
.dock {
  overflow: hidden;
  isolation: isolate;
  border: 0;
  background: transparent;
  box-shadow: 0 16px 38px rgba(18, 20, 18, .16), 0 2px 8px rgba(18, 20, 18, .07);
}

.dock::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 0;
  border-radius: inherit;
  pointer-events: none;
  background: var(--glass-tint);
  -webkit-backdrop-filter: blur(18px) saturate(150%);
  backdrop-filter: blur(18px) saturate(150%);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, .38),
    inset 0 0 0 1px var(--dock-line);
}

.dock > .dock-item { position: relative; z-index: 1; }
.dock > .dock-mark { z-index: 1; }""",
      'dock-clean-blur')

rep36(""".dock-mark {
  background: rgba(25, 26, 28, .82);""",
      """.dock-mark {
  background: rgba(25, 26, 28, .90);""",
      'dock-mark-solid')

# ═══════════════ pass 37: слайдер — ширина, подпись, стрелка ════════════════
rep36(""".slider {
  position: relative;
  width: 100%;
  max-width: 320px;
  height: 64px;""",
      """.slider {
  position: relative;
  width: 100%;
  height: 64px;""",
      'slider-full-width')

rep36(""".slider-label {
  position: absolute;
  left: 74px;
  right: 20px;""",
      """.slider-label {
  position: absolute;
  left: 74px;
  right: 14px;""",
      'slider-label-inset')

rep36("""[data-theme="night"] .slider-label { color: var(--paper); }""",
      """/* пока тянем — подпись уезжает в самый центр дорожки */
.slider.is-dragging .slider-label {
  left: 50%;
  right: auto;
  width: max-content;
  max-width: 62%;
  transform: translate(-50%, -50%);
  opacity: .55;
}

.slider.is-dragging .slider-knob { background: var(--accent); }

/* иконка питания на время драга превращается в стрелку вправо */
.slider-arrow { opacity: 0; transform: scale(.62) translateX(-6px); }

.slider.is-dragging .slider-power {
  opacity: 0;
  transform: scale(.55) translateX(6px);
}

.slider.is-dragging .slider-arrow {
  opacity: 1;
  transform: scale(1) translateX(0);
  transition: opacity .16s ease, transform .26s cubic-bezier(.3, .9, .26, 1);
}

[data-theme="night"] .slider-label { color: var(--paper); }""",
      'slider-drag-label')

rep36("""        <svg class="slider-icon slider-stop" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true">
          <rect x="7.4" y="7.4" width="9.2" height="9.2" rx="2.2" />
        </svg>""",
      """        <svg class="slider-icon slider-stop" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true">
          <rect x="7.4" y="7.4" width="9.2" height="9.2" rx="2.2" />
        </svg>
        <svg class="slider-icon slider-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M5 12h13" />
          <path d="M13.2 6.6 19 12l-5.8 5.4" />
        </svg>""",
      'slider-arrow-svg')

open(DST, 'w', encoding='utf-8').write(s)
print('pass37 OK: %d edits total' % len(done))

# ═══════════════ pass 38: библиотека — «+» и QR, общий экран добавления ══════
s = open(DST, encoding='utf-8').read()


def rep38(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# ── 1. кнопки в шапке библиотеки
rep38("""        <div class="head-actions">
          <button class="text-action" type="button" id="open-add-sub">+ Подписка</button>
          <button class="text-action" type="button" id="open-add-server">+ Сервер</button>
        </div>""",
      """        <div class="head-actions">
          <button class="icon-action" type="button" id="open-scan" aria-label="Сканировать QR-код">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M4 8.4V5.6A1.6 1.6 0 0 1 5.6 4h2.8" />
              <path d="M20 8.4V5.6A1.6 1.6 0 0 0 18.4 4h-2.8" />
              <path d="M4 15.6v2.8A1.6 1.6 0 0 0 5.6 20h2.8" />
              <path d="M20 15.6v2.8A1.6 1.6 0 0 1 18.4 20h-2.8" />
              <path d="M4.6 12h14.8" />
            </svg>
          </button>
          <button class="icon-action is-primary" type="button" id="open-add-server" aria-label="Добавить сервер или подписку">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
              <path d="M12 5.5v13M5.5 12h13" />
            </svg>
          </button>
        </div>""",
      'library-actions')

# ── 2. стили кнопок, экрана добавления и сканера
rep38(""".head-actions .text-action:hover { background: var(--paper); border-color: var(--line-strong); }""",
      """.head-actions .text-action:hover { background: var(--paper); border-color: var(--line-strong); }

.head-actions { gap: 8px; }

.icon-action {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  padding: 0;
  border: 1px solid var(--line);
  border-radius: var(--r-pill);
  background: var(--paper);
  color: var(--ink);
  transition: background .18s ease, border-color .18s ease, transform .18s ease;
}

.icon-action svg { width: 20px; height: 20px; }

.icon-action:hover { border-color: var(--line-strong); }
.icon-action:active { transform: scale(.94); }

.icon-action.is-primary {
  border-color: transparent;
  background: var(--ink);
  color: var(--paper);
}

[data-theme="night"] .icon-action.is-primary { background: var(--paper); color: var(--ink); }

/* ── Общий экран добавления ─────────────────────────────── */

.field-head-actions { display: flex; align-items: center; gap: 12px; }

.add-kind {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 10px;
  padding: 5px 10px;
  border-radius: var(--r-pill);
  background: var(--paper-2);
  color: var(--muted);
  font-family: var(--mono);
  font-size: 9.5px;
  letter-spacing: .04em;
  text-transform: uppercase;
  transition: color .2s ease, background .2s ease;
}

.add-kind::before {
  content: "";
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: currentColor;
  opacity: .7;
}

.add-kind.is-server { color: var(--accent); background: var(--accent-soft); }
.add-kind.is-sub { color: #8a5a12; background: rgba(178, 122, 26, .13); }
[data-theme="night"] .add-kind.is-sub { color: #e0b070; background: rgba(224, 176, 112, .14); }
.add-kind.is-unknown { color: var(--danger); background: rgba(155, 61, 47, .10); }

/* ── Сканер QR ─────────────────────────────────────────── */

.scan-box {
  position: relative;
  margin-top: 18px;
  aspect-ratio: 1 / 1;
  border-radius: var(--r-lg);
  overflow: hidden;
  background: #101210;
  box-shadow: 0 18px 40px var(--shadow);
}

.scan-box video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.scan-frame {
  position: absolute;
  inset: 16%;
  border-radius: 22px;
  box-shadow: 0 0 0 999px rgba(8, 10, 9, .34);
  pointer-events: none;
}

.scan-frame::before,
.scan-frame::after {
  content: "";
  position: absolute;
  width: 26px;
  height: 26px;
  border: 2px solid rgba(255, 255, 255, .9);
}

.scan-frame::before { left: -2px; top: -2px; border-right: 0; border-bottom: 0; border-radius: 14px 0 0 0; }
.scan-frame::after { right: -2px; bottom: -2px; border-left: 0; border-top: 0; border-radius: 0 0 14px 0; }

.scan-box.is-live .scan-line {
  position: absolute;
  left: 16%;
  right: 16%;
  height: 2px;
  border-radius: 2px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  animation: scan-sweep 2.2s ease-in-out infinite;
}

@keyframes scan-sweep {
  0%, 100% { top: 18%; opacity: .2; }
  50% { top: 80%; opacity: 1; }
}""",
      'add-screen-css')

# ── 3. разметка: общий экран добавления + сканер (перед старым «Новый сервер»)
rep38("""  <section class="screen" id="view-add-server" aria-labelledby="add-server-title">""",
      """  <section class="screen" id="view-add" aria-labelledby="add-title">
    <div class="screen-inner narrow">
      <button class="back" type="button" data-nav="servers">← Библиотека</button>
      <header class="screen-head screen-head-form">
        <div>
          <p class="eyebrow" id="add-eyebrow">Добавить</p>
          <h1 id="add-title">Сервер или подписка</h1>
        </div>
      </header>
      <p class="lead">Вставьте ссылку — приложение само поймёт: отдельный сервер это или подписка.</p>

      <form class="form" id="add-form" novalidate>
        <div class="field">
          <div class="field-head">
            <label for="add-input">Ссылка</label>
            <div class="field-head-actions">
              <button class="field-action" type="button" data-paste="add-input">Вставить</button>
              <button class="field-action" type="button" id="add-scan">QR</button>
            </div>
          </div>
          <textarea id="add-input" rows="3" spellcheck="false" autocomplete="off" placeholder="vless://… или https://…/sub" aria-describedby="err-add-input"></textarea>
          <p class="add-kind" id="add-kind">Пока не понятно</p>
          <p class="field-error" id="err-add-input"></p>
        </div>

        <div class="field" id="add-name-field">
          <label for="add-name">Название <span class="optional">необязательно</span></label>
          <input id="add-name" type="text" maxlength="80" autocomplete="off" placeholder="Например, 🇫🇮 Хельсинки или Моя подписка">
          <p class="field-note" id="add-name-note">Для сервера — город с флагом. Для подписки — любое имя.</p>
        </div>

        <div class="preview" id="add-preview" hidden>
          <span class="preview-flag" id="add-preview-flag" aria-hidden="true"></span>
          <span class="preview-copy">
            <span class="preview-city" id="add-preview-city"></span>
            <span class="preview-meta" id="add-preview-meta"></span>
          </span>
          <span class="preview-loc" id="add-preview-loc"></span>
        </div>

        <button class="primary form-submit" type="submit" id="add-submit">Добавить</button>
        <p class="form-foot">Подписка — любая http(s)-ссылка на список. Сервер — vless, vmess, trojan, ss.</p>
        <p class="sr-only" id="add-live" role="status" aria-live="polite"></p>
      </form>
    </div>
  </section>

  <section class="screen" id="view-scan" aria-labelledby="scan-title">
    <div class="screen-inner narrow">
      <button class="back" type="button" data-nav="servers">← Библиотека</button>
      <header class="screen-head screen-head-form">
        <div>
          <p class="eyebrow">QR</p>
          <h1 id="scan-title">Сканировать код</h1>
        </div>
      </header>
      <p class="lead">Наведите камеру на QR-код — сервер или подписка распознаются автоматически.</p>

      <div class="scan-box" id="scan-box">
        <video id="scan-video" playsinline muted autoplay></video>
        <span class="scan-line" aria-hidden="true"></span>
        <span class="scan-frame" aria-hidden="true"></span>
      </div>
      <p class="field-note" id="scan-note">Готовим камеру…</p>
      <button class="primary form-submit" type="button" id="scan-manual">Ввести вручную</button>
    </div>
  </section>

  <section class="screen" id="view-add-server" aria-labelledby="add-server-title">""",
      'add-screen-markup')

open(DST, 'w', encoding='utf-8').write(s)
print('pass38a OK: %d edits total' % len(done))

# ═══════════════ pass 39: логика общего добавления и QR-сканера ══════════════
s = open(DST, encoding='utf-8').read()


def rep39(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# маршрутизация: старые экраны больше не показываем
rep39("""  function showView(name) {
    const home = name === 'home';""",
      """  function showView(name) {
    if (name === 'add-server' || name === 'add-sub') name = 'add';
    const home = name === 'home';""",
      'route-add')

rep39("""    const active = home ? 'home' : (name === 'add-server' || name === 'add-sub' ? 'servers' : name);""",
      """    const active = home ? 'home' : (name === 'add' || name === 'scan' ? 'servers' : name);""",
      'route-add-active')

# открытие общего экрана вместо двух старых
rep39("""  function openAddServer() {
    ui.serverForm.reset();
    clearErrors(['server-link', 'server-name']);
    ui.serverPreview.hidden = true;
    showView('add-server');
    window.setTimeout(function () { ui.serverLink.focus({ preventScroll: true }); }, 80);
  }""",
      """  function openAddServer(prefill) {
    openAdd(prefill);
  }

  // ── Добавление: один экран, тип определяется по содержимому ──────────────
  const SERVER_SCHEME = /^(vless|vmess|trojan|ss|ssr|hysteria2|hy2|tuic|socks|wireguard):\\/\\//i;
  const SUB_SCHEME = /^https?:\\/\\/\\S+$/i;

  function detectAddKind(raw) {
    const text = String(raw || '').trim();
    if (!text) return { kind: 'empty' };
    const link = extractLink(text);
    if (link && SERVER_SCHEME.test(link)) {
      return { kind: 'server', link: link, protocol: link.split('://')[0].toUpperCase() };
    }
    if (SUB_SCHEME.test(text.split(/\\r?\\n/)[0].trim())) {
      return { kind: 'sub', url: text.split(/\\r?\\n/)[0].trim() };
    }
    if (link) return { kind: 'server', link: link, protocol: link.split('://')[0].toUpperCase() };
    if (text.indexOf('://') === -1 && text.replace(/\\s+/g, '').length > 32) {
      return { kind: 'sub', content: text };
    }
    return { kind: 'unknown' };
  }

  function openAdd(prefill) {
    const form = $('#add-form');
    if (form) form.reset();
    clearErrors(['add-input', 'add-name']);
    const input = $('#add-input');
    if (input && typeof prefill === 'string') input.value = prefill;
    updateAddDetection();
    showView('add');
    window.setTimeout(function () {
      if (input) input.focus({ preventScroll: true });
    }, 80);
  }

  function updateAddDetection() {
    const input = $('#add-input');
    const chip = $('#add-kind');
    const submit = $('#add-submit');
    const preview = $('#add-preview');
    if (!input || !chip || !submit) return;
    const kind = detectAddKind(input.value);
    chip.classList.remove('is-server', 'is-sub', 'is-unknown');
    if (preview) preview.hidden = true;

    if (kind.kind === 'server') {
      chip.classList.add('is-server');
      chip.textContent = 'Сервер · ' + (kind.protocol || 'ссылка');
      submit.textContent = 'Добавить сервер';
      const parsed = parseLink(kind.link);
      if (parsed && preview) {
        const location = detectLocation(parsed.name, '');
        preview.hidden = false;
        $('#add-preview-flag').textContent = location.flag || '—';
        $('#add-preview-city').textContent = location.city || parsed.name || parsed.host;
        $('#add-preview-meta').textContent = parsed.protocol + ' · ' + parsed.host + ':' + parsed.port;
        $('#add-preview-loc').textContent = location.located ? 'На карте' : 'Без координат';
      }
      return;
    }
    if (kind.kind === 'sub') {
      chip.classList.add('is-sub');
      chip.textContent = kind.url ? 'Подписка · ссылка' : 'Подписка · содержимое';
      submit.textContent = 'Добавить подписку';
      return;
    }
    if (kind.kind === 'unknown') {
      chip.classList.add('is-unknown');
      chip.textContent = 'Не похоже на ссылку';
      submit.textContent = 'Добавить';
      return;
    }
    chip.textContent = 'Пока не понятно';
    submit.textContent = 'Добавить';
  }

  function submitAdd(event) {
    event.preventDefault();
    clearErrors(['add-input', 'add-name']);
    const input = $('#add-input');
    const nameField = $('#add-name');
    const kind = detectAddKind(input ? input.value : '');
    const name = cleanText(nameField ? nameField.value : '', 80);

    if (kind.kind === 'server') {
      ui.serverLink.value = kind.link;
      ui.serverName.value = name;
      submitServer({ preventDefault: function () {} });
      return;
    }
    if (kind.kind === 'sub') {
      ui.subName.value = name || subNameFromUrl(kind.url || '') || 'Подписка';
      ui.subUrl.value = kind.url || '';
      ui.subContent.value = kind.content || '';
      submitSub({ preventDefault: function () {} });
      return;
    }
    setFieldError('add-input', 'Вставьте ссылку на сервер или на подписку.');
    if (input) input.focus();
  }

  function subNameFromUrl(url) {
    try {
      const host = new Date ? new URL(url).hostname : '';
      return host.replace(/^www\\./, '') || 'Подписка';
    } catch (error) {
      return 'Подписка';
    }
  }

  // ── QR-сканер: камера → canvas → jsQR ────────────────────────────────────
  const scanner = { stream: null, raf: 0, canvas: null, running: false };

  function openScan() {
    showView('scan');
    startScan();
  }

  function stopScan() {
    scanner.running = false;
    if (scanner.raf) {
      cancelAnimationFrame(scanner.raf);
      scanner.raf = 0;
    }
    if (scanner.stream) {
      scanner.stream.getTracks().forEach(function (track) { track.stop(); });
      scanner.stream = null;
    }
    const box = $('#scan-box');
    const video = $('#scan-video');
    if (box) box.classList.remove('is-live');
    if (video) video.srcObject = null;
  }

  function scanNote(text) {
    const note = $('#scan-note');
    if (note) note.textContent = text;
  }

  async function startScan() {
    const video = $('#scan-video');
    const box = $('#scan-box');
    if (!video) return;
    stopScan();
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || typeof jsQR !== 'function') {
      scanNote('Камера недоступна — вставьте ссылку вручную.');
      return;
    }
    scanNote('Готовим камеру…');
    try {
      scanner.stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: 'environment' }, width: { ideal: 1280 }, height: { ideal: 1280 } },
        audio: false
      });
    } catch (error) {
      scanNote('Нет доступа к камере. Разрешите её в настройках Android или вставьте ссылку вручную.');
      return;
    }
    video.srcObject = scanner.stream;
    try { await video.play(); } catch (error) { /* автоплей может быть запрещён */ }
    if (box) box.classList.add('is-live');
    scanNote('Ищем QR-код…');
    scanner.running = true;
    scanFrame();
  }

  function scanFrame() {
    if (!scanner.running) return;
    const video = $('#scan-video');
    if (!video || video.readyState < 2) {
      scanner.raf = requestAnimationFrame(scanFrame);
      return;
    }
    if (!scanner.canvas) scanner.canvas = document.createElement('canvas');
    const canvas = scanner.canvas;
    const size = 480;
    const side = Math.min(video.videoWidth || size, video.videoHeight || size);
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    ctx.drawImage(
      video,
      ((video.videoWidth || side) - side) / 2,
      ((video.videoHeight || side) - side) / 2,
      side,
      side,
      0,
      0,
      size,
      size
    );
    let code = null;
    try {
      const data = ctx.getImageData(0, 0, size, size);
      code = jsQR(data.data, size, size, { inversionAttempts: 'dontInvert' });
    } catch (error) {
      code = null;
    }
    if (code && code.data) {
      const value = String(code.data).trim();
      if (value) {
        stopScan();
        haptic();
        showToast('Код распознан');
        openAdd(value);
        return;
      }
    }
    scanner.raf = requestAnimationFrame(scanFrame);
  }""",
      'add-logic')

rep39("""  function openAddSub() {
    ui.subForm.reset();
    clearErrors(['sub-name', 'sub-url', 'sub-content']);
    showView('add-sub');
    window.setTimeout(function () { ui.subName.focus({ preventScroll: true }); }, 80);
  }""",
      """  function openAddSub(prefill) {
    openAdd(prefill);
  }""",
      'open-add-sub')

# проводка кнопок
rep39("""  $('#open-add-server').addEventListener('click', openAddServer);""",
      """  $('#open-add-server').addEventListener('click', function () { openAddServer(); });
  $('#open-scan').addEventListener('click', openScan);
  $('#add-scan').addEventListener('click', openScan);
  $('#scan-manual').addEventListener('click', function () { stopScan(); openAdd(); });
  $('#add-form').addEventListener('submit', submitAdd);
  $('#add-input').addEventListener('input', updateAddDetection);
  $$('[data-paste="add-input"]').forEach(function (button) {
    button.addEventListener('click', function () {
      window.setTimeout(updateAddDetection, 260);
    });
  });
  document.querySelectorAll('[data-nav="servers"]').forEach(function (element) {
    element.addEventListener('click', stopScan);
  });""",
      'add-wiring')

open(DST, 'w', encoding='utf-8').write(s)
print('pass39 OK: %d edits total' % len(done))

# ═══════════════ pass 40: встраиваем jsQR отдельным скриптом ═════════════════
s = open(DST, encoding='utf-8').read()
if 'function jsQR' not in s and 'jsQR(' not in s.split('<script>(function () {')[0]:
    jsqr_code = open(os.path.join(ROOT, 'vendor', 'jsqr.min.js'), encoding='utf-8').read()
    anchor = """})();
</script>
  <script>(function () {
  'use strict';"""
    assert s.count(anchor) == 1, s.count(anchor)
    s = s.replace(anchor, """})();
</script>
  <script>
""" + jsqr_code + """
  </script>
  <script>(function () {
  'use strict';""")
    done.append('jsqr-embed')
    open(DST, 'w', encoding='utf-8').write(s)
    print('pass40 OK: %d edits total' % len(done))
else:
    print('pass40: jsQR уже встроен (%d edits)' % len(done))

# ═══════════════ pass 41: пустое состояние и остатки старых кнопок ═══════════
s = open(DST, encoding='utf-8').read()


def rep41(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep41("""  renderSortBar();
  renderSortBar();

  $('#open-add-sub').addEventListener('click', openAddSub);
  $('#empty-add-sub').addEventListener('click', openAddSub);""",
      """  renderSortBar();

  $('#empty-scan').addEventListener('click', openScan);""",
      'drop-old-add-actions')

rep41("""          <button class="primary" type="button" id="empty-add-server">Добавить сервер</button>
          <button class="ghost" type="button" id="empty-add-sub">Добавить подписку</button>""",
      """          <button class="primary" type="button" id="empty-add-server">Добавить</button>
          <button class="ghost" type="button" id="empty-scan">Сканировать QR</button>""",
      'empty-state-actions')

open(DST, 'w', encoding='utf-8').write(s)
print('pass41 OK: %d edits total' % len(done))

# ═══════════════ pass 42: зажатие вместо «⋯», заголовок группы, анимации ═════
s = open(DST, encoding='utf-8').read()


def rep42(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# ── 1. «⋯» убираем: меню настроек открывается зажатием строки
rep42("""    row.addEventListener('click', function () { selectServer(server.id, true); });
    row.addEventListener('contextmenu', function (event) {
      event.preventDefault();
      openServerSettings(server.id);
    });
    item.appendChild(row);

    const more = document.createElement('button');
    more.type = 'button';
    more.className = 'row-more';
    more.textContent = '⋯';
    more.setAttribute('aria-label', 'Настройки сервера ' + server.city);
    more.addEventListener('click', function (event) {
      event.stopPropagation();
      openServerSettings(server.id);
    });
    item.appendChild(more);""",
      """    bindLongPress(row, function () { openServerSettings(server.id); }, function () {
      selectServer(server.id, true);
    });
    row.addEventListener('contextmenu', function (event) {
      event.preventDefault();
      openServerSettings(server.id);
    });
    item.appendChild(row);""",
      'row-longpress')

rep42("""  function buildGroupCard(options) {""",
      """  // ── зажатие строки: меню настроек вместо «⋯» ─────────────────────────────
  function bindLongPress(row, onHold, onTap) {
    let timer = 0;
    let startX = 0;
    let startY = 0;
    let fired = false;
    const clear = function () {
      if (timer) {
        window.clearTimeout(timer);
        timer = 0;
      }
    };
    row.addEventListener('pointerdown', function (event) {
      if (event.button) return;
      fired = false;
      startX = event.clientX;
      startY = event.clientY;
      clear();
      timer = window.setTimeout(function () {
        timer = 0;
        fired = true;
        haptic();
        onHold();
      }, 460);
    });
    row.addEventListener('pointermove', function (event) {
      if (!timer) return;
      if (Math.abs(event.clientX - startX) > 9 || Math.abs(event.clientY - startY) > 9) clear();
    });
    ['pointerup', 'pointercancel', 'pointerleave'].forEach(function (name) {
      row.addEventListener(name, clear);
    });
    row.addEventListener('click', function (event) {
      if (fired) {
        fired = false;
        event.preventDefault();
        event.stopPropagation();
        return;
      }
      onTap();
    });
  }

  function buildGroupCard(options) {""",
      'longpress-helper')

# ── 2. в заголовке группы — только название
rep42("""    const meta = document.createElement('span');
    meta.className = 'group-meta';
    const parts = [];
    if (!open && options.activeCity) {
      parts.push('● ' + options.activeCity);
    } else {
      parts.push(servers.length + ' ' + plural(servers.length, ['сервер', 'сервера', 'серверов']));
      if (options.updatedAt) parts.push(formatUpdated(options.updatedAt));
      const best = groupLatency(servers);
      if (best != null) parts.push(best + ' мс');
    }
    meta.textContent = parts.join(' · ');

    copy.appendChild(name);
    copy.appendChild(meta);""",
      """    copy.appendChild(name);""",
      'group-name-only')

# ── 3. анимация раскрытия/закрытия групп без перерисовки
rep42("""  function toggleGroup(key) {
    state.expanded[key] = !isGroupOpen(key);
    store.write('vpn.expanded', state.expanded);
    renderServers();
  }""",
      """  function toggleGroup(key) {
    const open = !isGroupOpen(key);
    state.expanded[key] = open;
    store.write('vpn.expanded', state.expanded);
    const card = document.querySelector('.group-card[data-key="' + key + '"]');
    const body = card ? card.querySelector('.group-body') : null;
    const toggle = card ? card.querySelector('.group-toggle') : null;
    if (!card || !body) {
      renderServers();
      return;
    }
    if (toggle) toggle.setAttribute('aria-expanded', String(open));
    if (open) {
      card.classList.add('is-open');
      body.style.display = 'block';
      body.style.overflow = 'hidden';
      body.style.height = '0px';
      body.style.opacity = '0';
      requestAnimationFrame(function () {
        body.style.height = body.scrollHeight + 'px';
        body.style.opacity = '1';
      });
      body.addEventListener('transitionend', function done(event) {
        if (event.propertyName !== 'height') return;
        body.style.height = '';
        body.style.overflow = '';
        body.removeEventListener('transitionend', done);
      });
    } else {
      body.style.display = 'block';
      body.style.overflow = 'hidden';
      body.style.height = body.scrollHeight + 'px';
      body.style.opacity = '1';
      requestAnimationFrame(function () {
        body.style.height = '0px';
        body.style.opacity = '0';
      });
      body.addEventListener('transitionend', function done(event) {
        if (event.propertyName !== 'height') return;
        card.classList.remove('is-open');
        body.style.cssText = '';
        body.removeEventListener('transitionend', done);
      });
    }
  }""",
      'group-anim')

rep42(""".group-body {
  display: none;
  padding: 0 14px;
  border-top: 1px solid var(--line);
}""",
      """.group-body {
  display: none;
  padding: 0 14px;
  border-top: 1px solid var(--line);
  overflow: hidden;
  transition: height .3s cubic-bezier(.32, .9, .28, 1), opacity .22s ease;
}

html[data-reduced="true"] .group-body { transition: none; }""",
      'group-body-transition')

# ── 4. мягкое появление экранов
rep42(""".screen {
  position: fixed;""",
      """.screen.is-active .screen-inner {
  animation: screen-in .26s cubic-bezier(.32, .9, .28, 1);
}

@keyframes screen-in {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: none; }
}

html[data-reduced="true"] .screen.is-active .screen-inner { animation: none; }

.screen {
  position: fixed;""",
      'screen-anim')

open(DST, 'w', encoding='utf-8').write(s)
print('pass42 OK: %d edits total' % len(done))

# ═══════════════ pass 43: настройки пинга ════════════════════════════════════
s = open(DST, encoding='utf-8').read()


def rep43(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep43("""      <section class="group">
        <h2>Данные</h2>""",
      """      <section class="group">
        <h2>Пинг</h2>
        <div class="row">
          <div class="row-copy">
            <p class="row-label">Мерить автоматически</p>
            <p class="row-note">Проверять отклик серверов при открытии библиотеки.</p>
          </div>
          <button class="switch" type="button" role="switch" aria-checked="true" aria-label="Мерить задержку автоматически" data-setting="ping"><span></span></button>
        </div>
        <div class="row">
          <div class="row-copy">
            <p class="row-label">Только выбранный</p>
            <p class="row-note">Экономит батарею: измеряется один сервер вместо всех.</p>
          </div>
          <button class="switch" type="button" role="switch" aria-checked="false" aria-label="Мерить только выбранный сервер" data-setting="pingOne"><span></span></button>
        </div>
        <div class="row row-stack">
          <p class="row-label">Как часто</p>
          <div class="segmented" role="group" aria-label="Интервал проверки задержки">
            <button type="button" data-group="pingEvery" data-value="60" aria-pressed="true">1 мин</button>
            <button type="button" data-group="pingEvery" data-value="300" aria-pressed="false">5 мин</button>
            <button type="button" data-group="pingEvery" data-value="900" aria-pressed="false">15 мин</button>
          </div>
        </div>
        <div class="row row-stack">
          <p class="row-label">Таймаут</p>
          <div class="segmented" role="group" aria-label="Таймаут проверки задержки">
            <button type="button" data-group="pingTimeout" data-value="1200" aria-pressed="false">1,2 с</button>
            <button type="button" data-group="pingTimeout" data-value="2500" aria-pressed="true">2,5 с</button>
            <button type="button" data-group="pingTimeout" data-value="4000" aria-pressed="false">4 с</button>
          </div>
        </div>
        <div class="row">
          <div class="row-copy">
            <p class="row-label">Проверить сейчас</p>
            <p class="row-note" id="ping-hint">Измерить задержку всех серверов.</p>
          </div>
          <button class="text-action" type="button" id="ping-now">Измерить</button>
        </div>
      </section>

      <section class="group">
        <h2>Данные</h2>""",
      'ping-settings-markup')

rep43("""      autoconnect: raw.autoconnect === true
    };""",
      """      autoconnect: raw.autoconnect === true,
      pingOne: raw.pingOne === true,
      pingEvery: [60, 300, 900].indexOf(Number(raw.pingEvery)) !== -1 ? Number(raw.pingEvery) : 60,
      pingTimeout: [1200, 2500, 4000].indexOf(Number(raw.pingTimeout)) !== -1 ? Number(raw.pingTimeout) : 2500
    };""",
      'ping-settings-defaults')

rep43("""    if (target === 'servers' && settings.ping && Date.now() - state.latencyAt > 60000) pingAll(true);""",
      """    if (target === 'servers' && settings.ping && Date.now() - state.latencyAt > settings.pingEvery * 1000) {
      if (settings.pingOne) pingSelected();
      else pingAll(true);
    }""",
      'ping-settings-interval')

rep43("""  $$('[data-theme-value]', ui.settingsScreen).forEach(function (button) {
    button.addEventListener('click', function () {
      applyTheme(button.dataset.themeValue);""",
      """  $('#ping-now').addEventListener('click', function () {
    const hint = $('#ping-hint');
    if (hint) hint.textContent = 'Измеряем…';
    pingAll(true);
    window.setTimeout(function () {
      if (hint) hint.textContent = 'Измерить задержку всех серверов.';
    }, 2600);
  });

  $$('[data-theme-value]', ui.settingsScreen).forEach(function (button) {
    button.addEventListener('click', function () {
      applyTheme(button.dataset.themeValue);""",
      'ping-now-button')

open(DST, 'w', encoding='utf-8').write(s)
print('pass43 OK: %d edits total' % len(done))

# ═══════════════ pass 44: таймаут пинга доходит до нативного слоя ════════════
s = open(DST, encoding='utf-8').read()


def rep44(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep44("""    }).map(function (server) {
      return { id: server.id, host: server.host, port: server.port };
    });""",
      """    }).map(function (server) {
      return { id: server.id, host: server.host, port: server.port, timeout: settings.pingTimeout };
    });""",
      'ping-timeout-all')

rep44("""      native.ping(JSON.stringify([{ id: server.id, host: server.host, port: server.port }]));
    } catch (error) {""",
      """      native.ping(JSON.stringify([{ id: server.id, host: server.host, port: server.port, timeout: settings.pingTimeout }]));
    } catch (error) {""",
      'ping-timeout-one')

open(DST, 'w', encoding='utf-8').write(s)
print('pass44 OK: %d edits total' % len(done))

# ═══════════════ pass 45: вкладка статистики с календарём активности ═════════
s = open(DST, encoding='utf-8').read()


def rep45(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# ── 1. пункт дока
rep45("""    <button class="dock-item" type="button" data-nav="settings" aria-label="Настройки">""",
      """    <button class="dock-item" type="button" data-nav="stats" aria-label="Статистика">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M4.8 19.2h14.4" />
        <path d="M8 19.2v-5.4" />
        <path d="M12 19.2V8.6" />
        <path d="M16 19.2v-8.2" />
      </svg>
    </button>
    <button class="dock-item" type="button" data-nav="settings" aria-label="Настройки">""",
      'dock-stats-item')

rep45("""    const active = home ? 'home' : (name === 'add' || name === 'scan' ? 'servers' : name);
    const order = ['home', 'servers', 'settings'];""",
      """    const active = home ? 'home' : (name === 'add' || name === 'scan' ? 'servers' : name);
    const order = ['home', 'servers', 'stats', 'settings'];""",
      'dock-stats-order')

# ── 2. экран
rep45("""  <section class="screen" id="view-settings" aria-labelledby="settings-title">""",
      """  <section class="screen" id="view-stats" aria-labelledby="stats-title">
    <div class="screen-inner">
      <header class="screen-head">
        <div>
          <p class="eyebrow">Активность</p>
          <h1 id="stats-title">Статистика</h1>
        </div>
        <div class="head-actions">
          <button class="icon-action" type="button" id="stats-reset" aria-label="Сбросить статистику">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M4.8 7.6h14.4" />
              <path d="M9.6 7.6V5.8h4.8v1.8" />
              <path d="M6.6 7.6l.8 10.6h9.2l.8-10.6" />
            </svg>
          </button>
        </div>
      </header>

      <div class="stats-hero">
        <p class="stats-big" id="stats-total">0 ч</p>
        <p class="stats-sub" id="stats-total-sub">в защищённом режиме за месяц</p>
      </div>

      <div class="stats-cards">
        <div class="stat-card">
          <span class="stat-value" id="stat-today">—</span>
          <span class="stat-label">сегодня</span>
        </div>
        <div class="stat-card">
          <span class="stat-value" id="stat-week">—</span>
          <span class="stat-label">за 7 дней</span>
        </div>
        <div class="stat-card">
          <span class="stat-value" id="stat-streak">—</span>
          <span class="stat-label">дней подряд</span>
        </div>
      </div>

      <section class="group stats-group">
        <h2>Календарь</h2>
        <div class="heat-scroll">
          <div class="heat" id="heat" role="img" aria-label="Календарь активности"></div>
        </div>
        <div class="heat-legend">
          <span>меньше</span>
          <i data-level="0"></i><i data-level="1"></i><i data-level="2"></i><i data-level="3"></i><i data-level="4"></i>
          <span>больше</span>
        </div>
        <p class="row-note">Чем больше часов в VPN за день, тем ярче квадрат.</p>
      </section>

      <section class="group stats-group">
        <h2>Трафик</h2>
        <div class="row">
          <div class="row-copy">
            <p class="row-label">Принято</p>
            <p class="row-note">За всё время</p>
          </div>
          <span class="stats-mono" id="stat-down">—</span>
        </div>
        <div class="row">
          <div class="row-copy">
            <p class="row-label">Отдано</p>
            <p class="row-note">За всё время</p>
          </div>
          <span class="stats-mono" id="stat-up">—</span>
        </div>
        <div class="row">
          <div class="row-copy">
            <p class="row-label">Сессий</p>
            <p class="row-note">Сколько раз поднимали туннель</p>
          </div>
          <span class="stats-mono" id="stat-sessions">—</span>
        </div>
      </section>

      <section class="group stats-group">
        <h2>Последние дни</h2>
        <div class="stats-days" id="stats-days"></div>
      </section>
    </div>
  </section>

  <section class="screen" id="view-settings" aria-labelledby="settings-title">""",
      'stats-markup')

# ── 3. стили
rep45("""/* ── Формы ─────────────────────────────────────────────── */

.form { margin-top: 6px; }""",
      """/* ── Статистика ────────────────────────────────────────── */

.stats-hero {
  margin-top: 18px;
  padding: 22px 22px 20px;
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  background: var(--paper);
}

.stats-big {
  font-family: var(--sans);
  font-size: 44px;
  font-weight: 700;
  letter-spacing: -.03em;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.stats-sub {
  margin-top: 8px;
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: .06em;
  text-transform: uppercase;
  color: var(--muted);
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-top: 10px;
}

.stat-card {
  display: grid;
  gap: 6px;
  padding: 14px 12px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--paper);
  text-align: center;
}

.stat-value {
  font-family: var(--sans);
  font-size: 17px;
  font-weight: 600;
  letter-spacing: -.02em;
  font-variant-numeric: tabular-nums;
}

.stat-label {
  font-family: var(--mono);
  font-size: 8.5px;
  letter-spacing: .05em;
  text-transform: uppercase;
  color: var(--muted);
}

.stats-group { margin-top: 12px; }

.heat-scroll {
  margin-top: 14px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.heat {
  display: grid;
  grid-template-rows: repeat(7, 1fr);
  grid-auto-flow: column;
  gap: 3px;
  width: max-content;
}

.heat i {
  width: 13px;
  height: 13px;
  border-radius: 3.5px;
  background: var(--paper-2);
  box-shadow: inset 0 0 0 1px rgba(25, 26, 28, .05);
}

.heat-legend {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 12px;
  font-family: var(--mono);
  font-size: 8.5px;
  letter-spacing: .04em;
  color: var(--muted);
}

.heat-legend i {
  width: 11px;
  height: 11px;
  border-radius: 3px;
  background: var(--paper-2);
}

.stats-mono {
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: .02em;
  font-variant-numeric: tabular-nums;
}

.stats-days { display: flex; flex-direction: column; }

.stats-day {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 0;
  border-bottom: 1px solid var(--line);
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: .02em;
}

.stats-day:last-child { border-bottom: 0; }

.stats-day-name { flex: 1 1 auto; color: var(--ink); }

.stats-day-bar {
  flex: 0 0 96px;
  height: 4px;
  border-radius: 2px;
  background: var(--paper-2);
  overflow: hidden;
}

.stats-day-bar span {
  display: block;
  height: 100%;
  border-radius: 2px;
  background: var(--accent);
}

.stats-day-value { flex: 0 0 52px; text-align: right; color: var(--muted); }

/* ── Формы ─────────────────────────────────────────────── */

.form { margin-top: 6px; }""",
      'stats-css')

open(DST, 'w', encoding='utf-8').write(s)
print('pass45 OK: %d edits total' % len(done))

# ═══════════════ pass 46: сбор и отрисовка статистики ════════════════════════
s = open(DST, encoding='utf-8').read()


def rep46(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep46("""  function startConnection() {""",
      """  // ── Статистика активности: секунды, трафик и сессии по дням ──────────────
  const usage = {
    data: store.read('vpn.usage', {}) || {},
    tick: 0,
    lastDown: 0,
    lastUp: 0,
    dirtyAt: 0
  };

  function pad2(value) {
    return value < 10 ? '0' + value : String(value);
  }

  function dayKey(date) {
    const d = date || new Date();
    return d.getFullYear() + '-' + pad2(d.getMonth() + 1) + '-' + pad2(d.getDate());
  }

  function usageBucket(key) {
    if (!usage.data[key] || typeof usage.data[key] !== 'object') {
      usage.data[key] = { sec: 0, down: 0, up: 0, sessions: 0 };
    }
    const bucket = usage.data[key];
    bucket.sec = Number(bucket.sec) || 0;
    bucket.down = Number(bucket.down) || 0;
    bucket.up = Number(bucket.up) || 0;
    bucket.sessions = Number(bucket.sessions) || 0;
    return bucket;
  }

  function flushUsage() {
    usage.dirtyAt = Date.now();
    store.write('vpn.usage', usage.data);
  }

  function trackUsage(justConnected) {
    const now = Date.now();
    if (state.vpn.state !== 'connected') {
      if (usage.tick) {
        usage.tick = 0;
        usage.lastDown = 0;
        usage.lastUp = 0;
        flushUsage();
      }
      return;
    }
    const bucket = usageBucket(dayKey());
    if (justConnected) bucket.sessions += 1;
    if (!usage.tick) {
      usage.tick = now;
      usage.lastDown = state.vpn.down;
      usage.lastUp = state.vpn.up;
    } else {
      const delta = Math.max(0, Math.min(15000, now - usage.tick)) / 1000;
      bucket.sec += delta;
      bucket.down += Math.max(0, state.vpn.down - usage.lastDown);
      bucket.up += Math.max(0, state.vpn.up - usage.lastUp);
      usage.tick = now;
      usage.lastDown = state.vpn.down;
      usage.lastUp = state.vpn.up;
    }
    if (now - usage.dirtyAt > 5000) flushUsage();
  }

  function hoursText(seconds) {
    const total = Number(seconds) || 0;
    if (total < 60) return Math.round(total) + ' с';
    const hours = Math.floor(total / 3600);
    const minutes = Math.round((total % 3600) / 60);
    if (!hours) return minutes + ' мин';
    return hours + ' ч' + (minutes ? ' ' + minutes + ' м' : '');
  }

  function accentRgb() {
    const raw = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();
    return hexToRgb(raw) || { r: 29, g: 90, b: 69 };
  }

  function usageLevel(seconds) {
    if (!seconds) return 0;
    const hours = seconds / 3600;
    if (hours < 0.5) return 1;
    if (hours < 1.5) return 2;
    if (hours < 3) return 3;
    return 4;
  }

  function renderStats() {
    const heat = document.getElementById('heat');
    if (!heat) return;
    const rgb = accentRgb();
    const alphas = [0, 0.20, 0.40, 0.62, 1];
    const colors = alphas.map(function (alpha) {
      if (!alpha) return '';
      return alpha >= 1
        ? 'rgb(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ')'
        : 'rgba(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ',' + alpha + ')';
    });

    const weeks = 18;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const start = new Date(today);
    start.setDate(start.getDate() - (weeks * 7 - 1));
    start.setDate(start.getDate() - ((start.getDay() + 6) % 7));

    let total = 0;
    let monthSec = 0;
    let monthStart = new Date(today.getFullYear(), today.getMonth(), 1).getTime();
    Object.keys(usage.data).forEach(function (key) {
      const bucket = usage.data[key];
      const sec = Number(bucket && bucket.sec) || 0;
      total += sec;
      const parts = key.split('-');
      const time = new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2])).getTime();
      if (time >= monthStart) monthSec += sec;
    });

    const cells = [];
    const cursor = new Date(start);
    const labels = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'];
    const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек'];
    while (cursor <= today) {
      const key = dayKey(cursor);
      const sec = Number((usage.data[key] || {}).sec) || 0;
      const level = usageLevel(sec);
      cells.push(
        '<i style="background:' + (level ? colors[level] : 'var(--paper-2)') + '" title="' +
        cursor.getDate() + ' ' + months[cursor.getMonth()] + ', ' + labels[(cursor.getDay() + 6) % 7] +
        ' — ' + (sec ? hoursText(sec) : 'без VPN') + '"></i>'
      );
      cursor.setDate(cursor.getDate() + 1);
    }
    heat.innerHTML = cells.join('');

    const legend = document.querySelectorAll('.heat-legend i');
    Array.prototype.forEach.call(legend, function (cell, index) {
      if (index > 0) cell.style.background = colors[index];
    });

    const totalEl = document.getElementById('stats-total');
    const subEl = document.getElementById('stats-total-sub');
    if (totalEl) totalEl.textContent = hoursText(monthSec);
    if (subEl) subEl.textContent = 'в защищённом режиме за ' + months[today.getMonth()] + ' · всего ' + hoursText(total);

    const todaySec = Number((usage.data[dayKey()] || {}).sec) || 0;
    let weekSec = 0;
    for (let i = 0; i < 7; i += 1) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      weekSec += Number((usage.data[dayKey(d)] || {}).sec) || 0;
    }
    let streak = 0;
    const cursor2 = new Date(today);
    if (!(Number((usage.data[dayKey(cursor2)] || {}).sec) || 0)) cursor2.setDate(cursor2.getDate() - 1);
    while (Number((usage.data[dayKey(cursor2)] || {}).sec) || 0) {
      streak += 1;
      cursor2.setDate(cursor2.getDate() - 1);
    }

    const setText = function (id, value) {
      const node = document.getElementById(id);
      if (node) node.textContent = value;
    };
    setText('stat-today', hoursText(todaySec));
    setText('stat-week', hoursText(weekSec));
    setText('stat-streak', streak ? streak + ' ' + plural(streak, ['день', 'дня', 'дней']) : '—');

    let down = 0;
    let up = 0;
    let sessions = 0;
    Object.keys(usage.data).forEach(function (key) {
      const bucket = usage.data[key] || {};
      down += Number(bucket.down) || 0;
      up += Number(bucket.up) || 0;
      sessions += Number(bucket.sessions) || 0;
    });
    setText('stat-down', down ? formatBytes(down) : '—');
    setText('stat-up', up ? formatBytes(up) : '—');
    setText('stat-sessions', sessions ? String(sessions) : '—');

    const list = document.getElementById('stats-days');
    if (list) {
      const rows = [];
      let maxSec = 1;
      for (let i = 0; i < 7; i += 1) {
        const d = new Date(today);
        d.setDate(d.getDate() - i);
        const sec = Number((usage.data[dayKey(d)] || {}).sec) || 0;
        maxSec = Math.max(maxSec, sec);
        rows.push({ date: d, sec: sec });
      }
      list.innerHTML = rows.map(function (row) {
        const label = i18nDay(row.date);
        const width = row.sec ? Math.max(4, Math.round((row.sec / maxSec) * 100)) : 0;
        return '<div class="stats-day"><span class="stats-day-name">' + label + '</span>' +
          '<span class="stats-day-bar"><span style="width:' + width + '%"></span></span>' +
          '<span class="stats-day-value">' + (row.sec ? hoursText(row.sec) : '—') + '</span></div>';
      }).join('');
    }
  }

  function i18nDay(date) {
    const names = ['воскресенье', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота'];
    const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек'];
    const today = new Date();
    const key = dayKey(date);
    if (key === dayKey(today)) return 'сегодня';
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    if (key === dayKey(yesterday)) return 'вчера';
    return names[date.getDay()] + ', ' + date.getDate() + ' ' + months[date.getMonth()];
  }

  function startConnection() {""",
      'stats-logic')

# включаем трекинг в жизненный цикл состояния VPN
rep46("""    if (changed) {
      const server = selectedServer();
      const label = server ? (server.flag ? server.flag + ' ' + server.city : server.city) : '';
      if (online) {""",
      """    trackUsage(online && changed);
    if (changed) {
      const server = selectedServer();
      const label = server ? (server.flag ? server.flag + ' ' + server.city : server.city) : '';
      if (online) {""",
      'stats-track')

# рисуем при показе вкладки
rep46("""    globe.setPaused(!home);""",
      """    if (name === 'stats') renderStats();
    globe.setPaused(!home);""",
      'stats-render-on-show')

# кнопка сброса
rep46("""  $('#ping-now').addEventListener('click', function () {""",
      """  $('#stats-reset').addEventListener('click', function () {
    const backup = JSON.parse(JSON.stringify(usage.data));
    usage.data = {};
    usage.tick = 0;
    flushUsage();
    renderStats();
    showToast('Статистика очищена', {
      label: 'Вернуть',
      action: function () {
        usage.data = backup;
        flushUsage();
        renderStats();
      }
    });
  });

  $('#ping-now').addEventListener('click', function () {""",
      'stats-reset-button')

open(DST, 'w', encoding='utf-8').write(s)
print('pass46 OK: %d edits total' % len(done))

# ═══════════════ pass 47: статистика — плотнее календарь, аккуратные подписи ══
s = open(DST, encoding='utf-8').read()


def rep47(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep47("""    const weeks = 18;""", """    const weeks = 20;""", 'heat-weeks')

rep47("""    const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек'];
    while (cursor <= today) {""",
      """    const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек'];
    const monthsFull = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль',
      'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь'];
    while (cursor <= today) {""",
      'heat-months-full')

rep47("""    if (subEl) subEl.textContent = 'в защищённом режиме за ' + months[today.getMonth()] + ' · всего ' + hoursText(total);""",
      """    if (subEl) {
      subEl.textContent = 'в защищённом режиме за ' + monthsFull[today.getMonth()] +
        ' · всего ' + hoursText(total);
    }""",
      'heat-sub-text')

open(DST, 'w', encoding='utf-8').write(s)
print('pass47 OK: %d edits total' % len(done))

# ═══════════════ pass 48: подпись на слайдере едет за ползунком к центру ═════
s = open(DST, encoding='utf-8').read()


def rep48(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep48("""    slider.knob.style.transform = 'translateX(' + offset + 'px)';
    if (!animate) {""",
      """    slider.knob.style.transform = 'translateX(' + offset + 'px)';
    if (slider.el) slider.el.style.setProperty('--knob-x', offset + 'px');
    if (!animate) {""",
      'slider-knob-x')

rep48("""/* пока тянем — подпись уезжает в самый центр дорожки */
.slider.is-dragging .slider-label {
  left: 50%;
  right: auto;
  width: max-content;
  max-width: 62%;
  transform: translate(-50%, -50%);
  opacity: .55;
}""",
      """/* пока тянем — подпись едет следом за ползунком и уходит к центру дорожки */
.slider.is-dragging .slider-label {
  left: calc(var(--knob-x, 0px) + 68px);
  right: auto;
  width: max-content;
  max-width: calc(100% - var(--knob-x, 0px) - 84px);
  text-align: left;
  transform: translateY(-50%);
  opacity: .62;
  transition: opacity .2s ease, left .05s linear;
}

.slider.is-dragging.is-armed .slider-label { opacity: 0; }""",
      'slider-label-follow')

open(DST, 'w', encoding='utf-8').write(s)
print('pass48 OK: %d edits total' % len(done))

# ═══════════════ pass 49: мелкие кривости: чип, рамка сканера, дубль тумблера ═
s = open(DST, encoding='utf-8').read()


def rep49(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep49(""".add-kind {
  display: inline-flex;
  align-items: center;""",
      """.add-kind {
  display: inline-flex;
  width: max-content;
  max-width: 100%;
  align-items: center;""",
      'add-kind-width')

rep49(""".scan-frame {
  position: absolute;
  inset: 16%;
  border-radius: 22px;
  box-shadow: 0 0 0 999px rgba(8, 10, 9, .34);
  pointer-events: none;
}""",
      """.scan-frame {
  position: absolute;
  inset: 14%;
  border-radius: 22px;
  background: rgba(255, 255, 255, .02);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, .16);
  pointer-events: none;
}""",
      'scan-frame-fix')

rep49("""        <div class="row">
          <div class="row-copy">
            <p class="row-label">Проверять задержку</p>
            <p class="row-note">Измерять отклик серверов при открытии списка.</p>
          </div>
          <button class="switch" type="button" role="switch" aria-checked="true" aria-label="Проверять задержку" data-setting="ping"><span></span></button>
        </div>
      </section>""",
      """      </section>""",
      'drop-duplicate-ping-toggle')

open(DST, 'w', encoding='utf-8').write(s)
print('pass49 OK: %d edits total' % len(done))

# ═══════════════ pass 50: глоу ещё деликатнее ════════════════════════════════
s = open(DST, encoding='utf-8').read()


def rep50(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep50("""    const reach = 11;""", """    const reach = 9;""", 'glow-reach3')
rep50("""      ctx.globalAlpha = Math.min(0.26, energy * 0.3);""",
      """      ctx.globalAlpha = Math.min(0.17, energy * 0.2);""",
      'glow-alpha3')

open(DST, 'w', encoding='utf-8').write(s)
print('pass50 OK: %d edits total' % len(done))

# ═══════════════ pass 51: сегменты, заголовки, крестик, кнопка «стоп» ════════
s = open(DST, encoding='utf-8').read()


def rep51(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# сегментированные переключатели — пилюля с плавающей плашкой
rep51(""".segmented {
  display: flex;
  width: 100%;
  border: 1px solid var(--line-strong);
}

.segmented button {
  flex: 1 1 0;
  padding: 8px 6px;
  border: 0;
  border-right: 1px solid var(--line-strong);
  border-radius: 0;
  background: transparent;
  font-size: 10.5px;
  color: var(--muted);
  transition: background .15s ease, color .15s ease;
}

.segmented button:last-child { border-right: 0; }
.segmented button:hover { color: var(--ink); }

.segmented button[aria-pressed="true"] {
  background: var(--ink);
  color: var(--paper);
}""",
      """.segmented {
  display: flex;
  width: 100%;
  gap: 2px;
  padding: 3px;
  border: 1px solid var(--line);
  border-radius: var(--r-pill);
  background: var(--paper-2);
}

.segmented button {
  flex: 1 1 0;
  min-height: 34px;
  padding: 0 8px;
  border: 0;
  border-radius: var(--r-pill);
  background: transparent;
  font-family: var(--sans);
  font-size: 11.5px;
  font-weight: 500;
  letter-spacing: -.01em;
  color: var(--muted);
  transition: background .18s ease, color .18s ease, box-shadow .18s ease;
}

.segmented button:hover { color: var(--ink); }

.segmented button[aria-pressed="true"] {
  background: var(--paper);
  color: var(--ink);
  box-shadow:
    0 1px 2px rgba(25, 26, 28, .10),
    0 0 0 1px var(--line) inset;
}

[data-theme="night"] .segmented button[aria-pressed="true"] {
  background: rgba(236, 232, 220, .12);
  color: var(--ink);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, .14) inset;
}""",
      'segmented-pill')

# заголовки: одинаковая плашка у всех экранов, ровные отступы
rep51(""".group h2 {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .10em;
  text-transform: uppercase;
  color: var(--muted);
  padding: 16px 18px 6px;
  border: 0;
}""",
      """.group h2 {
  font-family: var(--sans);
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: .12em;
  line-height: 1.2;
  text-transform: uppercase;
  color: var(--muted);
  padding: 18px 18px 4px;
  border: 0;
}""",
      'group-h2')

rep51(""".screen-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  padding-bottom: 18px;
  border-bottom: 1px solid var(--line);
}""",
      """.screen-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding-bottom: 18px;
  border-bottom: 1px solid var(--line);
}

.screen-head > div:first-child { min-width: 0; }""",
      'screen-head-align')

# «×» в ручных серверах снова видно
rep51(""".server-item .row-remove,
.group-body .server-row .row-remove {
  opacity: 0;
  visibility: hidden;
  transform: scale(.86);
  transition: opacity .16s ease, transform .16s ease, visibility 0s linear .16s;
}

.server-item.is-selected .row-remove,
.server-item:hover .row-remove,
.group-body .server-row:hover .row-remove,
.group-body .server-row.is-selected .row-remove {
  opacity: 1;
  visibility: visible;
  transform: none;
  transition: opacity .16s ease, transform .16s ease, visibility 0s;
}""",
      """.server-item .row-remove,
.group-body .server-row .row-remove {
  opacity: .45;
  visibility: visible;
  transition: opacity .16s ease, color .16s ease;
}

.server-item.is-selected .row-remove,
.server-item:hover .row-remove,
.group-body .server-row:hover .row-remove,
.group-body .server-row.is-selected .row-remove {
  opacity: 1;
}""",
      'row-remove-visible')

# кнопка «стоп»: ползунок ровно по центру круга
rep51(""".slider[data-state="connected"] {
  width: 68px;""",
      """.slider[data-state="connected"] {
  width: 64px;""",
      'slider-connected-size')

open(DST, 'w', encoding='utf-8').write(s)
print('pass51 OK: %d edits total' % len(done))

# ═══════════════ pass 52: карта — линия только в VPN, флаги, коллизии ════════
s = open(DST, encoding='utf-8').read()


def rep52(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# линия маршрута живёт только при включённом VPN
rep52("""  DotGlobe.prototype.drawArc = function (now) {
    if (!this.arc || !this.arcOn) return;""",
      """  DotGlobe.prototype.drawArc = function (now) {
    if (!this.arc || !this.arcOn || !this.connected) return;""",
      'arc-only-connected')

rep52("""    if (this.arcOn && this.arc && this.colors.accent) {
      this.drawArcGlow(xs, ys, buckets);
    }""",
      """    if (this.arcOn && this.arc && this.connected && this.colors.accent) {
      this.drawArcGlow(xs, ys, buckets);
    }""",
      'glow-only-connected')

# пинг и коллизии маркеров
rep52("""    // подписи городов: прячем те, что перекрываются с более близкими
    visible.sort(function (a, b) { return b.z - a.z; });
    const placed = [];""",
      """    // маркеры: убираем перекрытия и «плохие» серверы
    visible.sort(function (a, b) { return b.z - a.z; });
    const occupied = [];
    const MIN_GAP = 30;
    visible.forEach(function (item) {
      const entry = self.latency ? self.latency[item.button.dataset.id] : null;
      const dead = entry && (entry.ms == null || (Number.isFinite(entry.ms) && entry.ms > 200));
      item.button.classList.toggle('is-offline', !!dead);
      if (dead) {
        item.hidden = true;
        item.button.style.visibility = 'hidden';
        item.button.classList.add('is-hidden-map');
        return;
      }
      item.button.classList.remove('is-hidden-map');
      let x = item.x;
      let y = item.y;
      let tries = 0;
      while (tries < 6) {
        const clash = occupied.some(function (other) {
          const dx = other.x - x;
          const dy = other.y - y;
          return dx * dx + dy * dy < MIN_GAP * MIN_GAP;
        });
        if (!clash) break;
        tries += 1;
        const angle = tries * 2.399963;
        x = item.x + Math.cos(angle) * MIN_GAP * (0.6 + tries * 0.22);
        y = item.y + Math.sin(angle) * MIN_GAP * (0.6 + tries * 0.22);
      }
      occupied.push({ x: x, y: y });
      item.button.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0) translate(-50%,-50%)';
      item.button.classList.toggle('is-displaced', tries > 0);
      item.x = x;
      item.y = y;
    });

    // подписи городов: прячем те, что перекрываются с более близкими
    const labels = visible.filter(function (item) { return !item.hidden; });
    labels.sort(function (a, b) { return b.z - a.z; });
    const placed = [];""",
      'markers-collision')

rep52("""    visible.forEach(function (item) {
      const width = Math.min(140, 16 + item.city.length * 5.6);""",
      """    labels.forEach(function (item) {
      const width = Math.min(140, 16 + item.city.length * 5.6);""",
      'markers-labels-loop')

# API для передачи задержек в глобус
rep52("""  DotGlobe.prototype.addServer = function (server) {""",
      """  DotGlobe.prototype.setLatency = function (map) {
    this.latency = map || {};
  };

  DotGlobe.prototype.addServer = function (server) {""",
      'globe-set-latency')

rep52("""    state.latencyAt = Date.now();
    if (ui.pingAll) {""",
      """    state.latencyAt = Date.now();
    globe.setLatency(state.latency);
    if (ui.pingAll) {""",
      'globe-latency-push')

open(DST, 'w', encoding='utf-8').write(s)
print('pass52 OK: %d edits total' % len(done))

# ═══════════════ pass 53: строка маршрута во флагах, бренд smpl ══════════════
s = open(DST, encoding='utf-8').read()


def rep53(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# разметка: флаги вместо названий, «последний сервер» — кнопка
rep53("""      <span class="path-from" id="path-from">Екатеринбург</span>
      <span class="path-line" aria-hidden="true"></span>
      <span class="path-to" id="path-to">—</span>""",
      """      <span class="path-from" id="path-from" aria-hidden="true"></span>
      <span class="path-line" aria-hidden="true"></span>
      <button class="path-to" id="path-to" type="button" aria-label="Последний сервер">—</button>""",
      'path-markup')

rep53(""".path-to {
  color: var(--ink);
  max-width: 42vw;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.path-to.is-empty { color: var(--muted); }
.path-from { white-space: nowrap; }""",
      """.path-to {
  padding: 2px 6px;
  margin: -2px -6px;
  border: 0;
  border-radius: var(--r-pill);
  background: none;
  color: var(--ink);
  max-width: 42vw;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 13px;
  line-height: 1.2;
  transition: background .16s ease;
}

.path-to:hover { background: var(--paper-2); }
.path-to.is-empty { color: var(--muted); }
.path-from { white-space: nowrap; font-size: 13px; line-height: 1.2; }

.path-line { align-self: center; }

/* имя продукта — только мелким текстом над картой */
.brand-mark {
  position: fixed;
  left: 0;
  right: 0;
  top: calc(12px + env(safe-area-inset-top));
  z-index: 30;
  margin: 0;
  text-align: center;
  font-family: var(--mono);
  font-size: 9.5px;
  letter-spacing: .34em;
  text-transform: lowercase;
  color: var(--muted);
  opacity: .75;
  pointer-events: none;
}

body:not([data-view="home"]) .brand-mark { display: none; }""",
      'path-flags-css')

rep53("""  <main class="stage" id="map">""",
      """  <p class="brand-mark" id="brand-mark" aria-label="smpl">smpl</p>
  <main class="stage" id="map">""",
      'brand-markup')

# флаги: «вы» и сервер
rep53("""    const label = server.flag ? server.flag + ' ' + server.city : server.city;
    ui.pathTo.textContent = label;
    ui.pathTo.classList.remove('is-empty');""",
      """    ui.pathTo.textContent = server.flag || (server.code ? codeToFlag(server.code) : '·');
    ui.pathTo.setAttribute('aria-label', 'Последний сервер: ' + server.city);
    ui.pathTo.title = server.city;
    ui.pathTo.classList.remove('is-empty');""",
      'path-flag-server')

rep53("""    const label = document.getElementById('path-from');
    if (label) label.textContent = city;""",
      """    const label = document.getElementById('path-from');
    if (label) {
      const iso = countryCode(next && next.country ? next.country : originState.country);
      label.textContent = iso ? codeToFlag(iso) : '';
      label.setAttribute('title', city);
    }""",
      'path-flag-origin')

rep53("""  function subNameFromUrl(url) {""",
      """  function codeToFlag(code) {
    const iso = String(code || '').trim().toUpperCase();
    if (iso.length !== 2) return '';
    return String.fromCodePoint(0x1f1e6 + iso.charCodeAt(0) - 65)
      + String.fromCodePoint(0x1f1e6 + iso.charCodeAt(1) - 65);
  }

  function countryCode(name) {
    const wanted = normalizeForSearch(String(name || ''));
    if (!wanted) return '';
    const codes = Object.keys(COUNTRIES);
    for (let i = 0; i < codes.length; i += 1) {
      const item = COUNTRIES[codes[i]];
      if (normalizeForSearch(String(item.name || '')) === wanted) return codes[i];
    }
    return wanted.length === 2 ? wanted.toUpperCase() : '';
  }

  function subNameFromUrl(url) {""",
      'flag-helpers')

# тап по последнему серверу — в библиотеку к нему
rep53("""  $('#stats-reset').addEventListener('click', function () {""",
      """  $('#path-to').addEventListener('click', function () {
    const server = selectedServer();
    showView('servers');
    if (!server) return;
    window.setTimeout(function () {
      const row = document.querySelector('.server-row[data-id="' + server.id + '"]');
      if (row) {
        row.scrollIntoView({ block: 'center', behavior: 'smooth' });
        row.classList.add('is-flash');
        window.setTimeout(function () { row.classList.remove('is-flash'); }, 1200);
      }
    }, 260);
  });

  $('#stats-reset').addEventListener('click', function () {""",
      'path-to-click')

open(DST, 'w', encoding='utf-8').write(s)
print('pass53 OK: %d edits total' % len(done))

# ═══════════════ pass 54: настоящие иконки вместо символов ═══════════════════
ICON_CLOSE = """'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M7 7l10 10M17 7 7 17"/></svg>'"""
ICON_REFRESH = """'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12a7 7 0 1 1-2.1-5"/><path d="M19.4 4.6v4.2h-4.2"/></svg>'"""
ICON_PENCIL = """'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 19l.9-3.3 8.4-8.4a1.6 1.6 0 0 1 2.3 0l1.1 1.1a1.6 1.6 0 0 1 0 2.3l-8.4 8.4z"/><path d="M13.2 8.4l2.4 2.4"/></svg>'"""
ICON_LINK = """'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.2 13.8a3.6 3.6 0 0 0 5.1 0l2.4-2.4a3.6 3.6 0 0 0-5.1-5.1l-1 1"/><path d="M13.8 10.2a3.6 3.6 0 0 0-5.1 0l-2.4 2.4a3.6 3.6 0 0 0 5.1 5.1l1-1"/></svg>'"""

s = open(DST, encoding='utf-8').read()


def rep54(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


# иконки в JS
rep54("""    const flag = document.createElement('span');
    const flagText = options.flag;
    flag.className = 'group-flag' + (flagText ? '' : ' is-manual');
    flag.textContent = flagText || (options.manual ? '✎' : '⌁');
    flag.setAttribute('aria-hidden', 'true');""",
      """    const flag = document.createElement('span');
    flag.className = 'group-flag is-icon';
    flag.innerHTML = options.sub ? """ + ICON_LINK + """ : """ + ICON_PENCIL + """;
    flag.setAttribute('aria-hidden', 'true');""",
      'group-icon')

rep54("""      refresh.textContent = '⟳';""",
      """      refresh.innerHTML = """ + ICON_REFRESH + """;""",
      'refresh-icon')

rep54("""      const remove = document.createElement('button');
      remove.type = 'button';
      remove.className = 'group-action is-danger';
      remove.textContent = '×';""",
      """      const remove = document.createElement('button');
      remove.type = 'button';
      remove.className = 'group-action is-danger';
      remove.innerHTML = """ + ICON_CLOSE + """;""",
      'group-remove-icon')

rep54("""        : 'В подписке пока нет серверов. Нажмите ⟳, чтобы обновить.';""",
      """        : 'В подписке пока нет серверов. Нажмите «Обновить», чтобы загрузить заново.';""",
      'sub-note-text')

# крестики в строках серверов (два места)
s = s.replace("""      remove.setAttribute('aria-label', 'Удалить сервер ' + server.city);
      remove.textContent = '×';""",
      """      remove.setAttribute('aria-label', 'Удалить сервер ' + server.city);
      remove.innerHTML = """ + ICON_CLOSE + """;""", 1)
s = s.replace("""        remove.setAttribute('aria-label', 'Удалить сервер ' + server.city);
        remove.textContent = '×';""",
      """        remove.setAttribute('aria-label', 'Удалить сервер ' + server.city);
        remove.innerHTML = """ + ICON_CLOSE + """;""", 1)
done.append('row-remove-icons')

# крестик в листе настроек
rep54("""      <button class="sheet-close" type="button" id="sheet-close" aria-label="Закрыть">×</button>""",
      """      <button class="sheet-close" type="button" id="sheet-close" aria-label="Закрыть">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M7 7l10 10M17 7 7 17"/></svg>
      </button>""",
      'sheet-close-icon')

rep54(""".row-remove { font-size: 17px; }""",
      """.row-remove { font-size: 17px; }
.row-remove svg,
.group-action svg,
.sheet-close svg { display: block; width: 16px; height: 16px; }

.group-flag.is-icon svg { width: 18px; height: 18px; }

.sheet-close { display: grid; place-items: center; }""",
      'icon-sizes')

# подсветка строки, к которой ведёт тап по флагу
rep54(""".server-item.is-selected .row-remove,""",
      """.server-row.is-flash {
  box-shadow: 0 0 0 1.5px var(--accent-line) inset;
  background: var(--accent-soft);
}

.server-item.is-selected .row-remove,""",
      'flash-css')

# город «вы» по умолчанию тоже со флагом
rep54("""  function locateUser() {
    const cached = store.read('vpn.origin', null);""",
      """  function locateUser() {
    applyOrigin({
      city: ORIGIN.city,
      country: ORIGIN.country,
      lat: Number(ORIGIN.lat),
      lng: Number(ORIGIN.lng),
      source: 'default'
    }, true);
    const cached = store.read('vpn.origin', null);""",
      'origin-default')

open(DST, 'w', encoding='utf-8').write(s)
print('pass54 OK: %d edits total' % len(done))

# ═══════════════ pass 55: имя и описание подписки из файла ═══════════════════
s = open(DST, encoding='utf-8').read()


def rep55(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep55("""  function parseSubscriptionContent(text) {""",
      """  // Метаданные подписки: #profile-title / #profile-desc / userinfo
  function parseSubMeta(text) {
    const meta = { title: '', description: '', traffic: '', updateEvery: '' };
    const lines = String(text || '').split(/\\r?\\n/).slice(0, 60);
    const decodeMaybeBase64 = function (value) {
      const raw = String(value || '').trim();
      if (/^base64:/i.test(raw)) {
        try {
          const decoded = atob(raw.replace(/^base64:/i, '').trim());
          if (decoded) return decoded;
        } catch (error) {
          return raw.replace(/^base64:/i, '');
        }
      }
      return raw;
    };
    lines.forEach(function (line) {
      const match = line.match(/^\\s*[#;\\/]{1,2}\\s*([a-z-]+)\\s*[:=]\\s*(.+)$/i);
      if (!match) return;
      const key = match[1].toLowerCase();
      const value = decodeMaybeBase64(match[2]);
      if (key === 'profile-title' && !meta.title) meta.title = cleanText(value, 60);
      if ((key === 'profile-desc' || key === 'description' || key === 'announce') && !meta.description) {
        meta.description = cleanText(value, 160);
      }
      if (key === 'profile-update-interval') meta.updateEvery = cleanText(value, 24);
      if (key === 'subscription-userinfo') meta.traffic = cleanText(value, 120);
    });
    return meta;
  }

  function parseSubscriptionContent(text) {""",
      'sub-meta-parser')

rep55("""      const parsed = parseSubscriptionContent(text);
      if (!parsed.length) throw new Error('В подписке не найдено серверов.');
      replaceSubServers(sub, parsed);""",
      """      const parsed = parseSubscriptionContent(text);
      if (!parsed.length) throw new Error('В подписке не найдено серверов.');
      const meta = parseSubMeta(text);
      if (meta.title && (!sub.name || sub.autoName)) {
        sub.name = meta.title;
        sub.autoName = true;
      }
      if (meta.description) sub.desc = meta.description;
      sub.meta = meta;
      replaceSubServers(sub, parsed);""",
      'sub-meta-refresh')

rep55("""      const sub = {
        id: uid('sub'),
        name: name,
        url: url,
        content: text,
        updatedAt: Date.now()
      };""",
      """      const meta = parseSubMeta(text);
      const finalName = (meta.title && name === subNameFromUrl(url)) ? meta.title : name;
      const sub = {
        id: uid('sub'),
        name: finalName || meta.title || 'Подписка',
        autoName: !name || name === subNameFromUrl(url),
        desc: meta.description || '',
        meta: meta,
        url: url,
        content: text,
        updatedAt: Date.now()
      };""",
      'sub-meta-create')

# описание подписки в карточке группы
rep55("""    copy.appendChild(name);

    const count = document.createElement('span');""",
      """    copy.appendChild(name);
    if (options.sub && options.sub.desc) {
      const desc = document.createElement('span');
      desc.className = 'group-desc';
      desc.textContent = options.sub.desc;
      copy.appendChild(desc);
    }

    const count = document.createElement('span');""",
      'group-desc-render')

rep55(""".group-count {
  border: 0;""",
      """.group-desc {
  display: block;
  margin-top: 2px;
  max-width: 46ch;
  font-family: var(--sans);
  font-size: 11px;
  line-height: 1.35;
  color: var(--muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.group-count {
  border: 0;""",
      'group-desc-css')

open(DST, 'w', encoding='utf-8').write(s)
print('pass55 OK: %d edits total' % len(done))

# ═══════════════ pass 56: 50+ серверов — поиск с задержкой, пинг без перерисовки ═
s = open(DST, encoding='utf-8').read()


def rep56(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep56("""  function renderServers() {
    const container = document.getElementById('group-list');
    if (!container) return;
    container.textContent = '';

    const query = state.query;""",
      """  let renderServersTimer = 0;

  function renderServers(immediate) {
    if (!immediate) {
      window.clearTimeout(renderServersTimer);
      renderServersTimer = window.setTimeout(function () { renderServers(true); }, 60);
      return;
    }
    const container = document.getElementById('group-list');
    if (!container) return;
    container.textContent = '';
    state.queryNorm = normalizeForSearch(state.query);

    const query = state.query;""",
      'render-servers-debounce')

rep56("""  function matchesQuery(server) {
    const query = normalizeForSearch(state.query);
    if (!query) return true;""",
      """  function matchesQuery(server) {
    const query = state.queryNorm != null ? state.queryNorm : normalizeForSearch(state.query);
    if (!query) return true;""",
      'matches-query-cache')

rep56("""  if (ui.search) {
    ui.search.addEventListener('input', function () {
      state.query = ui.search.value;""",
      """  if (ui.search) {
    let searchTimer = 0;
    ui.search.addEventListener('input', function () {
      state.query = ui.search.value;
      window.clearTimeout(searchTimer);
      searchTimer = window.setTimeout(function () { renderServers(true); }, 130);
      return;""",
      'search-debounce')

# пинг обновляем точечно, без полной перерисовки списка
rep56("""    state.latencyAt = Date.now();
    globe.setLatency(state.latency);
    if (ui.pingAll) {
      ui.pingAll.disabled = false;
      ui.pingAll.textContent = 'Задержка';
    }
    renderServers();
    updateHome();""",
      """    state.latencyAt = Date.now();
    globe.setLatency(state.latency);
    if (ui.pingAll) {
      ui.pingAll.disabled = false;
      ui.pingAll.textContent = 'Задержка';
    }
    patchLatency();
    updateHome();""",
      'latency-patch-call')

rep56("""  function markSelectedRow() {""",
      """  // точечное обновление задержек: не перестраиваем весь список
  function patchLatency() {
    const rows = document.querySelectorAll('.server-row[data-id]');
    Array.prototype.forEach.call(rows, function (row) {
      const server = state.servers.filter(function (item) { return item.id === row.dataset.id; })[0];
      if (!server) return;
      const cell = row.querySelector('.server-ping');
      if (!cell) return;
      const ping = latencyText(server);
      cell.className = 'server-ping' + (ping ? ping.className : ' is-idle')
        + (server.id === state.selectedId && state.vpn.state === 'connected' ? ' is-live' : '');
      cell.textContent = ping ? ping.text : '— мс';
    });
    updateMeta();
  }

  function markSelectedRow() {""",
      'patch-latency')

open(DST, 'w', encoding='utf-8').write(s)
print('pass56 OK: %d edits total' % len(done))

# ═══════════════ pass 57: QR — разрешение камеры и повтор, пинг в уведомлении ══
s = open(DST, encoding='utf-8').read()


def rep57(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep57("""  function openScan() {
    showView('scan');
    startScan();
  }""",
      """  function openScan() {
    showView('scan');
    requestCamera();
    window.setTimeout(function () { startScan(); }, 420);
  }

  function requestCamera() {
    if (native && typeof native.requestCamera === 'function') {
      try { native.requestCamera(); } catch (error) { /* мост недоступен */ }
    }
  }""",
      'scan-open-request')

rep57("""    } catch (error) {
      scanNote('Нет доступа к камере. Разрешите её в настройках Android или вставьте ссылку вручную.');
      return;
    }""",
      """    } catch (error) {
      scanNote('Нет доступа к камере. Разрешите её и попробуйте снова.');
      const retry = document.getElementById('scan-retry');
      if (retry) retry.hidden = false;
      return;
    }""",
      'scan-error-retry')

rep57("""  function scanNote(text) {
    const note = $('#scan-note');
    if (note) note.textContent = text;
  }""",
      """  function scanNote(text) {
    const note = $('#scan-note');
    if (note) note.textContent = text;
  }

  window.__onCameraPermission = function (granted) {
    if (state.view !== 'scan') return;
    if (granted) {
      const retry = document.getElementById('scan-retry');
      if (retry) retry.hidden = true;
      startScan();
    } else {
      scanNote('Камера запрещена в настройках Android. Вставьте ссылку вручную.');
    }
  };""",
      'scan-permission-api')

rep57("""      <p class="field-note" id="scan-note">Готовим камеру…</p>
      <button class="primary form-submit" type="button" id="scan-manual">Ввести вручную</button>""",
      """      <p class="field-note" id="scan-note">Готовим камеру…</p>
      <button class="ghost form-submit" type="button" id="scan-retry" hidden>Разрешить камеру и повторить</button>
      <button class="primary form-submit" type="button" id="scan-manual">Ввести вручную</button>""",
      'scan-retry-button')

rep57("""  $('#scan-manual').addEventListener('click', function () { stopScan(); openAdd(); });""",
      """  $('#scan-manual').addEventListener('click', function () { stopScan(); openAdd(); });
  $('#scan-retry').addEventListener('click', function () {
    requestCamera();
    window.setTimeout(function () { startScan(); }, 420);
  });""",
      'scan-retry-wiring')

# в уведомлении — сервер и его пинг
rep57("""    try {
      native.connect(JSON.stringify(built.config),
        server.flag ? server.flag + ' ' + server.city : server.city);""",
      """    try {
      const entry = state.latency[server.id];
      const ms = entry && Number.isFinite(entry.ms) ? ' · ' + entry.ms + ' мс' : '';
      native.connect(JSON.stringify(built.config),
        (server.flag ? server.flag + ' ' + server.city : server.city) + ms);""",
      'notify-label-ping')

open(DST, 'w', encoding='utf-8').write(s)
print('pass57 OK: %d edits total' % len(done))

# ═══════════════ pass 58: сплошная линия маршрута, метка «вы», развод маркеров ══
s = open(DST, encoding='utf-8').read()


def rep58(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


start = s.find('    const opacity = this.connected ? 1 : 0.9;')
end = s.find('    if (this.connected && progress > 0.98) {', start)
assert start > 0 and end > start
old_arc = s[start:end]
new_arc = """    const top = Math.max(2, Math.round(progress * (n - 1)) + 1);
    const screen = [];
    for (let i = 0; i < top; i += 1) {
      const p = this.project(points[i], {});
      p.edge = i === 0 || i === top - 1;
      screen.push(p);
    }

    const strokePath = function (run) {
      ctx.beginPath();
      run.forEach(function (point, index) {
        if (index === 0) ctx.moveTo(point.x, point.y);
        else ctx.lineTo(point.x, point.y);
      });
      ctx.stroke();
    };

    ctx.setLineDash([]);
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    // линия рвётся там, где уходит за горизонт — рисуем сплошными прогонами
    let run = [];
    const flush = function () {
      if (run.length > 1) {
        strokePath(run);
        ctx.strokeStyle = this.colors.paper;
        ctx.lineWidth = 4.6;
        ctx.globalAlpha = 0.92;
        strokePath(run);
        ctx.strokeStyle = this.colors.accent;
        ctx.lineWidth = 1.9;
        ctx.globalAlpha = 1;
        strokePath(run);
      }
      run = [];
    }.bind(this);

    screen.forEach(function (point) {
      if (point.z > 0.02) {
        run.push(point);
      } else {
        flush();
      }
    });
    flush();
"""
s = s[:start] + new_arc + s[end:]
done.append('arc-solid')

rep58("""    const MIN_GAP = 30;""", """    const MIN_GAP = 40;""", 'markers-gap')
rep58("""      while (tries < 6) {""", """      while (tries < 14) {""", 'markers-tries')
rep58("""        const angle = tries * 2.399963;
        x = item.x + Math.cos(angle) * MIN_GAP * (0.6 + tries * 0.22);
        y = item.y + Math.sin(angle) * MIN_GAP * (0.6 + tries * 0.22);""",
      """        const angle = tries * 2.399963;
        const radius = MIN_GAP * (0.55 + tries * 0.3);
        x = item.x + Math.cos(angle) * radius;
        y = item.y + Math.sin(angle) * radius;""",
      'markers-spiral')

# метка «вы» — флаг в кольце, а не точка
rep58("""    this.originEl = document.createElement('div');
    this.originEl.className = 'origin';
    const originDot = document.createElement('span');
    originDot.className = 'origin-dot';
    this.originEl.appendChild(originDot);
    this.layer.appendChild(this.originEl);""",
      """    this.originEl = document.createElement('div');
    this.originEl.className = 'origin';
    const originRing = document.createElement('span');
    originRing.className = 'origin-ring';
    const originDot = document.createElement('span');
    originDot.className = 'origin-dot';
    this.originEl.appendChild(originRing);
    this.originEl.appendChild(originDot);
    this.layer.appendChild(this.originEl);""",
      'origin-markup')

rep58(""".origin-dot {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 6px;
  height: 6px;
  margin: -3px;
  border: 1px solid var(--ink);
  background: var(--paper);""",
      """.origin-ring {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 22px;
  height: 22px;
  margin: -11px;
  border-radius: 50%;
  border: 1px solid var(--accent);
  opacity: .38;
  animation: origin-pulse 2.6s ease-out infinite;
}

@keyframes origin-pulse {
  0% { transform: scale(.72); opacity: .5; }
  70%, 100% { transform: scale(1.5); opacity: 0; }
}

[data-motion="less"] .origin-ring { animation: none; }

.origin-dot {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 22px;
  height: 22px;
  margin: -11px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  line-height: 1;
  border: 1px solid var(--ink);
  background: var(--paper);""",
      'origin-css')

rep58("""    this.origin = {
      city: origin.city || this.origin.city,
      country: origin.country || this.origin.country,
      lat: Number(origin.lat),
      lng: Number(origin.lng)
    };""",
      """    this.origin = {
      city: origin.city || this.origin.city,
      country: origin.country || this.origin.country,
      lat: Number(origin.lat),
      lng: Number(origin.lng)
    };
    if (this.originEl) {
      const dot = this.originEl.querySelector('.origin-dot');
      const iso = countryCode(this.origin.country);
      if (dot) dot.textContent = iso ? codeToFlag(iso) : '';
      this.originEl.setAttribute('title', this.origin.city || '');
    }""",
      'origin-flag')

# исходная точка участвует в разводе, чтобы серверы её не накрывали
rep58("""    this.project(this.originVec, p);
    if (p.z <= 0.015) {
      this.originEl.style.visibility = 'hidden';
    } else {
      this.originEl.style.visibility = 'visible';""",
      """    this.project(this.originVec, p);
    if (p.z <= 0.015) {
      this.originEl.style.visibility = 'hidden';
    } else {
      occupied.push({ x: p.x, y: p.y });
      this.originEl.style.visibility = 'visible';""",
      'origin-collision')

open(DST, 'w', encoding='utf-8').write(s)
print('pass58 OK: %d edits total' % len(done))

# ═══════════════ pass 59: порядок развода метки «вы», редукция движения ════════
s = open(DST, encoding='utf-8').read()


def rep59(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep59('[data-motion="less"] .origin-ring { animation: none; }',
      'html[data-reduced="true"] .origin-ring { animation: none; }',
      'origin-css-reduced')

rep59("""    const occupied = [];""",
      """    const occupied = [];
    const originPoint = this.project(this.originVec, {});
    if (originPoint.z > 0.015) occupied.push({ x: originPoint.x, y: originPoint.y });""",
      'origin-first')

rep59("""      occupied.push({ x: p.x, y: p.y });
      this.originEl.style.visibility = 'visible';""",
      """      this.originEl.style.visibility = 'visible';""",
      'origin-collision-undo')

open(DST, 'w', encoding='utf-8').write(s)
print('pass59 OK: %d edits total' % len(done))

# ═══════════════ pass 60: флаг исходной точки без внешних зависимостей ════════
s = open(DST, encoding='utf-8').read()


def rep60(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        print('!! %s: %d matches' % (label, n))
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label)


rep60("""    if (this.originEl) {
      const dot = this.originEl.querySelector('.origin-dot');
      const iso = countryCode(this.origin.country);
      if (dot) dot.textContent = iso ? codeToFlag(iso) : '';
      this.originEl.setAttribute('title', this.origin.city || '');
    }""",
      """    if (this.originEl) {
      this.originEl.setAttribute('title', this.origin.city || '');
      this.paintOriginFlag(origin.code || origin.countryCode);
    }""",
      'origin-flag-call')

rep60("""  DotGlobe.prototype.setOrigin = function (origin) {""",
      """  DotGlobe.prototype.paintOriginFlag = function (code) {
    if (!this.originEl) return;
    const dot = this.originEl.querySelector('.origin-dot');
    if (!dot) return;
    const iso = String(code || '').toUpperCase();
    if (!/^[A-Z]{2}$/.test(iso)) return;
    dot.textContent = String.fromCodePoint(
      0x1F1E6 + iso.charCodeAt(0) - 65,
      0x1F1E6 + iso.charCodeAt(1) - 65
    );
  };

  DotGlobe.prototype.setOrigin = function (origin) {""",
      'origin-flag-helper')

rep60("""    this.originVec = latLng(this.origin.lat, this.origin.lng, 1.007);
    this.originEl = document.createElement('div');""",
      """    this.originVec = latLng(this.origin.lat, this.origin.lng, 1.007);
    this.originEl = document.createElement('div');""",
      'origin-noop') if False else None

rep60("""    globe.setOrigin({ city: city, country: originState.country, lat: lat, lng: lng });""",
      """    globe.setOrigin({ city: city, country: originState.country, lat: lat, lng: lng, code: isoOf(city) });""",
      'origin-pass-code')

rep60("""    const current = selectedServer();
    globe.setOrigin""",
      """    const current = selectedServer();
    globe.setOrigin""",
      'origin-noop2') if False else None

rep60("""  function applyOrigin(next, silent) {""",
      """  function isoOf(cityName) {
    const clean = String(cityName || '').trim();
    if (!clean) return '';
    const record = originState.country;
    return countryCode(record);
  }

  function applyOrigin(next, silent) {""",
      'iso-helper')

# ═══════════════ v3: флаги, слайдеры, карта, подписки, QR, иконки ══════════════
import base64 as _b64
_FLAGS_B64 = _b64.b64encode(open(os.path.join(ROOT, 'fonts', 'smpl-flags.woff2'), 'rb').read()).decode('ascii')

def rep_all(old, new, label):
    global s
    n = s.count(old)
    if n < 1:
        print('!! %s: 0 matches' % label)
        sys.exit(1)
    s = s.replace(old, new)
    done.append(label + ' x%d' % n)


# ── CSS: шрифт флагов (флаги рисуются одинаково в любом браузере) и единые фонты
rep(r"""</head>""",
    r"""  <style>/* v3: флаги и единые шрифты */
@font-face {
  font-family: 'smpl Flags';
  font-style: normal;
  font-weight: 400 600;
  font-display: block;
  src: url(data:font/woff2;base64,__FLAGS_B64__) format('woff2');
  unicode-range: U+1F1E6-1F1FF;
}
:root {
  --sans: 'smpl Flags', 'Onest', system-ui, -apple-system, sans-serif;
  --mono: 'smpl Flags', 'IBM Plex Mono', ui-monospace, 'SF Mono', monospace;
}
</style>
</head>""".replace('__FLAGS_B64__', _FLAGS_B64), 'css-v3-flags')

# ── CSS: переключатели (слайдеры настроек) — ровные кнопки, текст не переносится
rep(r"""</head>""",
    r"""  <style>/* v3: сегментированные переключатели */
.segmented { display: flex; width: 100%; max-width: 100%; }
.segmented button {
  flex: 1 1 0;
  min-width: 0;
  padding: 8px 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: center;
  letter-spacing: 0;
  line-height: 1.2;
}
.segmented-sm { width: 100%; }
.segmented-sm button { flex: 1 1 0; padding: 6px 4px; font-size: 11.5px; }
.row-stack .segmented { margin-top: 8px; }
</style>
</head>""", 'css-v3-segmented')

# ── CSS: крестик у ручных серверов всегда виден; «←» и стрелки — SVG
rep(r"""</head>""",
    r"""  <style>/* v3: видимые действия и иконки */
.row-remove,
.server-item .row-remove,
.group-body .server-row .row-remove {
  opacity: 1 !important;
  color: var(--ink) !important;
  width: 36px;
  height: 36px;
  display: grid;
  place-items: center;
}
.row-remove svg { width: 18px; height: 18px; }
.back-ico { width: 15px; height: 15px; vertical-align: -2px; margin-right: 4px; }
</style>
</head>""", 'css-v3-remove')

# ── CSS: линия маршрута скрыта, пока VPN отключён; режим «много серверов»
rep(r"""</head>""",
    r"""  <style>/* v3: маршрут и оптимизация при 50+ серверах */
body[data-link="off"] .path-line { visibility: hidden; }
body[data-many="true"] .srv-label { display: none; }
body[data-many="true"] .srv-flag { box-shadow: none; transition: none; }
body[data-many="true"] .server-item,
body[data-many="true"] .server-row { content-visibility: auto; contain-intrinsic-size: 64px; }
body[data-many="true"] * { -webkit-backdrop-filter: none !important; backdrop-filter: none !important; }
body[data-many="true"] .srv { transition: none; }
</style>
</head>""", 'css-v3-perf')

# ── Заголовок вкладки: smpl
rep('  <title>VPN</title>', '  <title>smpl</title>', 'title-smpl')

# ── Стрелки «← …» в шапках экранов → SVG
rep_all('>← Библиотека</button>',
        '><svg class="back-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>Библиотека</button>',
        'back-lib')
rep_all('>← Серверы</button>',
        '><svg class="back-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>Серверы</button>',
        'back-srv')

# ── JS: состояние VPN на body (для линии маршрута) + уведомление с пингом
rep("    ui.connStatus.classList.toggle('is-on', !empty && online);",
    "    ui.connStatus.classList.toggle('is-on', !empty && online);\n"
    "    document.body.dataset.link = (!empty && (online || busy)) ? 'on' : 'off';",
    'js-link-state')

rep("    ui.path.hidden = false;\n    if (ui.slider) ui.slider.setAttribute('aria-label', online || busy ? 'Отключить' : 'Подключить');",
    "    ui.path.hidden = false;\n"
    "    if (online && native && typeof native.setNotice === 'function') {\n"
    "      try { native.setNotice(String(server.city || ''), pingEntry && Number.isFinite(pingEntry.ms) ? pingEntry.ms : -1); } catch (error) { /* мост недоступен */ }\n"
    "    }\n"
    "    if (ui.slider) ui.slider.setAttribute('aria-label', online || busy ? 'Отключить' : 'Подключить');",
    'js-notice')

# ── Карта: порядок разрешения наложений стабильный (серверы не прыгают друг на друга)
rep("    visible.sort(function (a, b) { return b.z - a.z; });\n    const occupied = [];",
    "    visible.sort(function (a, b) { return String(a.button.dataset.id).localeCompare(String(b.button.dataset.id)); });\n    const occupied = [];",
    'map-stable-order')

# ── Карта: при 50+ серверах подписи городов не рисуем
rep("      item.button.classList.toggle('is-label-hidden', overlap);",
    "      item.button.classList.toggle('is-label-hidden', overlap || document.body.dataset.many === 'true');",
    'map-many-labels')

# ── Список: признак «много серверов»
rep_all("    ui.serversEmpty.hidden = state.servers.length !== 0;",
    "    ui.serversEmpty.hidden = state.servers.length !== 0;\n    document.body.dataset.many = String(state.servers.length >= 50);",
    'list-many')

# ── Подписки в списке: без значка-флага
rep("    flag.setAttribute('aria-hidden', 'true');\n\n    const copy = document.createElement('span');\n    copy.className = 'group-copy';",
    "    flag.setAttribute('aria-hidden', 'true');\n    if (options.sub) flag.hidden = true;\n\n    const copy = document.createElement('span');\n    copy.className = 'group-copy';",
    'group-no-flag')

# ── Удаление подписки: настоящий крестик вместо символа
rep("      remove.textContent = '×';",
    "      remove.innerHTML = '<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.7\" stroke-linecap=\"round\"><path d=\"M7 7l10 10M17 7 7 17\"/></svg>';",
    'sub-remove-svg')

# ── Подписка: название и описание из заголовков и из декодированного содержимого
rep(r"""    const lines = String(text || '').split(/\r?\n/).slice(0, 60);""",
    r"""    let source = String(text || '');
    if (source.indexOf('://') === -1) {
      try { source = decodeBase64(source.trim()) + '\n' + source; } catch (error) { /* не base64 */ }
    }
    const lines = source.split(/\r?\n/).slice(0, 80);""", 'submeta-decode')

rep("      if ((key === 'profile-desc' || key === 'description' || key === 'announce') && !meta.description) {",
    "      if ((key === 'profile-desc' || key === 'profile-description' || key === 'description' || key === 'announce' || key === 'desc') && !meta.description) {",
    'submeta-desc-keys')

# ── QR: сначала выдаём доступ к камере, и только потом открываем поток
rep("  const scanner = { stream: null, raf: 0, canvas: null, running: false };",
    "  const scanner = { stream: null, raf: 0, canvas: null, running: false, permitted: false };",
    'scanner-permitted')

rep("    scanNote('Готовим камеру…');",
    "    if (native && typeof native.requestCamera === 'function' && !scanner.permitted) {\n"
    "      scanNote('Запрашиваем доступ к камере…');\n"
    "      requestCamera();\n"
    "      return;\n"
    "    }\n"
    "    scanNote('Готовим камеру…');",
    'scan-gate')

rep("  window.__onCameraPermission = function (granted) {\n    if (state.view !== 'scan') return;\n    if (granted) {",
    "  window.__onCameraPermission = function (granted) {\n    if (state.view !== 'scan') return;\n    if (granted) {\n      scanner.permitted = true;",
    'camera-permitted')

# ── Заголовок приложения
rep("<meta name=\"description\" content=\"Демонстрационный VPN-клиент: серверы и подписки, карта, подключение.\">",
    "<meta name=\"description\" content=\"smpl: серверы и подписки, карта, подключение.\">",
    'meta-desc')


open(DST, 'w', encoding='utf-8').write(s)
print('pass60 OK: %d edits total' % len(done))
