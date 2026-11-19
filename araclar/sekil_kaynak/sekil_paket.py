#!/usr/bin/env python3
"""Şekil tanımlarından paketi (sekiller.json) üretir.  Kullanım: python3 sekil_paket.py [çıktı.json]"""
import sys, json, importlib
sys.path.insert(0, '/home/claude/scripts')
P = []
for m in ('sekil_21', 'sekil_09'):
    try: P += importlib.import_module(m).L
    except ModuleNotFoundError: pass
ids = [o['id'] for o in P]; assert len(ids) == len(set(ids)), 'yinelenen kimlik'
out = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/sekil_is/sekiller.json'
json.dump(P, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(P), 'şekil ->', out, '| toplam SVG', sum(len(o['svg']) for o in P) // 1024, 'KB')
