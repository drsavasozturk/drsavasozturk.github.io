#!/usr/bin/env python3
"""Nefroloji Ders Serisi: slaytlardaki boş alanı ölçer ve istenirse ekran görüntüsü alır.

Kullanım:
  python3 sekil_olc.py olc 21 09            -> her slayt için boş yükseklik (px, 1280x720 sahnede), punto
  python3 sekil_olc.py cek <çıktı_klasörü> <slayt_id> [...] [--mobil]   -> slayt görüntüleri (PNG)
Çalışma kopyası: /home/claude/sekil_is/index.html
"""
import asyncio, json, sys, subprocess, time, os
from playwright.async_api import async_playwright
ROOT = '/home/claude/sekil_is'; PORT = 8791; B = f'http://localhost:{PORT}/index.html'

GOSTER = """(id)=>{var el=document.getElementById(id); if(!el) return null;
 document.querySelectorAll('#deck .slide.on').forEach(function(x){x.classList.remove('on');});
 el.classList.add('on'); el.querySelectorAll('.frag').forEach(function(x){x.classList.add('vis');}); return true;}"""
OLC = """(id)=>{var s=document.getElementById(id), b=s.querySelector('.body'); if(!b) return null;
 var fit=b.style.fontSize||''; b.style.fontSize='';
 var sc=s.getBoundingClientRect().width/s.offsetWidth, br=b.getBoundingClientRect(), alt=br.top;
 [].forEach.call(b.children,function(c){ if(getComputedStyle(c).position==='absolute') return; var r=c.getBoundingClientRect(); if(r.bottom>alt) alt=r.bottom; });
 var fn=b.querySelector('.fn'), fnTop=fn?fn.getBoundingClientRect().top:br.bottom;
 var o={nom:parseFloat(getComputedStyle(b).fontSize), ch:b.clientHeight, sh:b.scrollHeight,
        bos:Math.round((Math.min(br.bottom,fnTop)-alt)/sc), fit:fit, svg:s.querySelectorAll('svg').length,
        h2:(s.querySelector('h2')||{}).textContent||'', cls:b.className};
 b.style.fontSize=fit; return o;}"""


async def ac(p, w=1366, h=768):
    br = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    ctx = await br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1.5 if w > 600 else 2)
    await ctx.route('**/static.cloudflareinsights.com/**', lambda r: r.fulfill(status=200, content_type='application/javascript', body=''))
    pg = await ctx.new_page(); hata = []
    pg.on('pageerror', lambda e: hata.append(str(e)))
    await pg.goto(B); await pg.wait_for_timeout(1500)
    for k in ('#dk1', '#dk2', '#dk3'): await pg.check(k)
    await pg.click('#dkb'); await pg.wait_for_timeout(600)
    return br, pg, hata


async def main():
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '-d', ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            if sys.argv[1] == 'olc':
                br, pg, hata = await ac(p)
                for no in sys.argv[2:]:
                    ids = await pg.evaluate("(n)=>[].map.call(document.querySelectorAll('#deck .slide[data-ders=\"'+n+'\"]'),function(x){return x.id;})", no)
                    for sid in ids:
                        await pg.evaluate(GOSTER, sid); await pg.wait_for_timeout(60)
                        o = await pg.evaluate(OLC, sid)
                        if o: print(f"{sid:9s} bos={int(o['bos']):4d} nom={o['nom']:.1f} fit={o['fit'] or '-':8s} svg={o['svg']} [{o['cls']}] {o['h2'][:70]}")
                        else: print(f"{sid:9s} (gövde yok)")
                print('JS hatası:', hata)
            else:
                mobil = '--mobil' in sys.argv; out = sys.argv[2]; os.makedirs(out, exist_ok=True)
                br, pg, hata = await ac(p, *((390, 844) if mobil else (1366, 768)))
                for sid in [a for a in sys.argv[3:] if not a.startswith('--')]:
                    if mobil:
                        await pg.evaluate("(id)=>{var e=document.getElementById(id); e.querySelectorAll('.frag').forEach(function(x){x.classList.add('vis');}); e.scrollIntoView();}", sid)
                        await pg.wait_for_timeout(250); el = await pg.query_selector('#' + sid); await el.screenshot(path=f'{out}/{sid}_m.png')
                    else:
                        await pg.evaluate(GOSTER, sid); await pg.wait_for_timeout(700)
                        el = await pg.query_selector('#' + sid); await el.screenshot(path=f'{out}/{sid}.png')
                        o = await pg.evaluate(OLC, sid); print(sid, 'bos=%s fit=%s nom=%s' % (o['bos'], o['fit'] or '-', o['nom']) if o else '')
                print('JS hatası:', hata)
            await br.close()
    finally:
        srv.terminate()

asyncio.run(main())
