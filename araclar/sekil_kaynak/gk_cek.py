#!/usr/bin/env python3
"""Tek tek şekil önizlemesi: python3 gk_cek.py sekil_10 s10_pat [s10_mest ...]  →  /home/claude/sekil_is/gor/<id>.png"""
import sys, importlib
import sekil_gk; sekil_gk.KOK = 'file:///home/claude/scripts/kalip/'
import sekil_kit
from playwright.sync_api import sync_playwright
mod = importlib.import_module(sys.argv[1]); L = mod.L if hasattr(mod, 'L') else mod.D.L
ist = sys.argv[2:] or [o['id'] for o in L]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1100, 'height': 900}, device_scale_factor=1.25)
    for o in L:
        if o['id'] not in ist: continue
        open('/home/claude/kalip/cek.html', 'w', encoding='utf-8').write(f'<html><body style="margin:0;background:#fff;font-family:Inter,Arial,sans-serif"><div style="width:1080px;padding:6px">{o["svg"]}</div></body></html>')
        pg.goto('file:///home/claude/kalip/cek.html'); pg.wait_for_timeout(250)
        pg.locator('svg').first.screenshot(path=f'/home/claude/sekil_is/gor/{o["id"]}.png'); print(o['id'])
    b.close()
for u in sekil_kit.UYARI: print('UYARI', u)
