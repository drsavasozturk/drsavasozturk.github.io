#!/usr/bin/env python3
"""Nefroloji Ders Serisi — etkileşimli şekil betiğini (araclar/etk/etk.js) sayfaya ekler (kullanıcı onayı 20 Kasım 2026).
Kullanım: python3 -I araclar/etk_ekle.py dersler/nefroloji-ders-serisi/index.html
Önceki ekleme varsa söker ve yeniden ekler (tekrar çalıştırmak güvenlidir). Sıra: sekil_ekle → metin_duzelt → svg_duzelt → etk_ekle → imza_ekle."""
import os, re, sys
JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etk', 'etk.js'), encoding='utf-8').read()
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
s = re.sub(r'<script id="etk-js">.*?</script>\n?', '', s, flags=re.S)
assert '</script>' not in JS.replace('<\\/', '')
i = s.rfind('</body>'); assert i > 0
s = s[:i] + '<script id="etk-js">' + JS + '</script>\n' + s[i:]
open(p, 'w', encoding='utf-8').write(s)
print(f'{p}: etkileşimli şekil betiği eklendi ({len(JS) // 1024} KB)')
