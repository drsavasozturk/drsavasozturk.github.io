#!/usr/bin/env python3
"""Şekil tanımlarından paketi (araclar/sekiller.json) üretir.  Kullanım: python3 araclar/sekil_kaynak/sekil_paket.py [çıktı.json]"""
import sys, os, json, importlib
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
P = []
for m in ('sekil_07', 'sekil_08', 'sekil_09', 'sekil_10', 'sekil_11', 'sekil_12', 'sekil_13', 'sekil_14', 'sekil_15', 'sekil_17', 'sekil_18', 'sekil_19', 'sekil_20', 'sekil_21', 'sekil_22', 'sekil_23', 'sekil_26', 'sekil_27'):
    mod = importlib.import_module(m); P += mod.L if hasattr(mod, 'L') else mod.D.L
ids = [o['id'] for o in P]; assert len(ids) == len(set(ids)), 'yinelenen kimlik'
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, '..', 'sekiller.json')
json.dump(P, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(P), 'şekil ->', out, '| toplam SVG', sum(len(o['svg']) for o in P) // 1024, 'KB')
import sekil_kit
for u in sekil_kit.UYARI: print('UYARI', u)
