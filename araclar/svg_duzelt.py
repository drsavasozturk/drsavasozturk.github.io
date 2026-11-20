#!/usr/bin/env python3
"""Nefroloji Ders Serisi — desteden gelen (özgün) şekillerde yerleşim düzeltmeleri (20 Kasım 2026, kullanıcı onayı).
Kullanım: python3 -I araclar/svg_duzelt.py dersler/nefroloji-ders-serisi/index.html
araclar/svg_duzelt/<slayt>.svg dosyası o slayttaki ilk SVG'nin yerine geçer (<slayt>__<k>.svg: k. SVG).
Yalnız hedef slaytın içinde çalışır; tekrar çalıştırmak güvenlidir. Seri yeniden üretilirse sekil_ekle.py ve metin_duzelt.py'den sonra çalıştırın."""
import os, re, sys
K = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svg_duzelt')
p = sys.argv[1]; s = open(p, encoding='utf-8').read(); n = z = 0
for ad in sorted(os.listdir(K)):
    if not ad.endswith('.svg'): continue
    sid, _, k = ad[:-4].partition('__'); k = int(k or 0)
    yeni = open(os.path.join(K, ad), encoding='utf-8').read().strip()
    i = s.find('<section id="%s"' % sid); assert i >= 0, sid
    j = s.find('</section>', i); blok = s[i:j]
    m = list(re.finditer(r'<svg\b.*?</svg>', blok, re.S)); assert len(m) > k, (sid, k)
    if m[k].group(0) == yeni: z += 1; continue
    blok = blok[:m[k].start()] + yeni + blok[m[k].end():]
    s = s[:i] + blok + s[j:]; n += 1
open(p, 'w', encoding='utf-8').write(s)
print(f'{p}: {n} şekil düzeltildi ({z} zaten düzeltilmiş)')
