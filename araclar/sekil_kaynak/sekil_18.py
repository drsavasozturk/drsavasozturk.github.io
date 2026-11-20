#!/usr/bin/env python3
"""Ders 18 · Amiloidoz ve fibriler hastalıklar — şekil tanımları (20 Kasım 2026)."""
import random
from sekil_ortak import *
from sekil_glom import etk

D = Ders('18')

# ============================================================================================== 1 · fibril oluşumu ve doku tanısı
F = Fig('fib', 392, 'Çözünür öncül proteinden amiloid fibriline: yanlış katlanma, beta tabaka, çekirdeklenme; Kongo kırmızısı ve elektron mikroskopisi', w=1080)
serit(F, 6, 6, 1068, 'Çözünür proteinden dallanmayan fibrile', BRANDD); zemin(F, 6, 42, 1068, 184)
xs = (90, 290, 490, 690, 920)
# 1 çözünür öncül
F.el(xs[0], 120, 34, 30, '#e8f6ff', BRAND, 1.6)
F.yol(f'M{xs[0] - 22},120 c6,-14 10,14 16,0 c6,-14 10,14 16,0 c6,-14 10,14 16,0', BRAND, 2.2)
# 2 yanlış katlanma
F.yol(f'M{xs[1] - 40},132 C{xs[1] - 24},92 {xs[1] - 10},150 {xs[1]},112 C{xs[1] + 10},82 {xs[1] + 24},148 {xs[1] + 40},104', GOLD, 2.6)
# 3 beta tabaka oligomeri
for i in range(4):
    y = 98 + i * 14; F.ok(xs[2] - 34, y, xs[2] + 34, y, RED, 3)
# 4 protofilament
for i in range(2):
    F.yol(f'M{xs[3] - 50},{112 + i * 14} q12,-10 25,0 q12,10 25,0 q12,-10 25,0 q12,10 25,0', PUR, 5, op=.85)
# 5 fibril + SAP, GAG
for i in range(3):
    F.yol(f'M{xs[4] - 80},{106 + i * 12} C{xs[4] - 40},{94 + i * 12} {xs[4] + 20},{118 + i * 12} {xs[4] + 80},{106 + i * 12}', PUR, 5.4, op=.85)
for (u, v) in ((-46, 90), (30, 140)):
    for k in range(5):
        a = 2 * math.pi * k / 5; F.el(xs[4] + u + 8 * math.cos(a), v + 8 * math.sin(a), 3.6, 3.6, '#7ec8a0', GREEN, 1)
F.yol(f'M{xs[4] + 52},86 q6,-8 12,0 q6,8 12,0 q6,-8 12,0', '#a07a00', 2.2)
for a, b in zip(xs, xs[1:]): F.ok(a + 50, 120, 832 if b == xs[4] else b - 58, 120, INK2, 2.2)
YZ = [('Çözünür öncül', 'katlanmış, işlevsel'), ('Yanlış katlanma', 'konformasyon değişir'), ('Çapraz-β oligomer', 'zincirler eksene dik'),
      ('Protofilament', 'çekirdeklenme ile uzar'), ('Fibril 8–12 nm', 'düz, dallanmayan')]
for x, (a, b) in zip(xs, YZ):
    F.t(x, 186, a, 12.8, 800, INK, 'middle'); F.t(x, 204, b, 11.6, None, INK2, 'middle')
F.yol(f'M{xs[4] - 10},80 C{xs[4] - 60},52 {xs[2] + 40},52 {xs[2] + 4},84', RED, 1.8, ok=True, dash='5 4'); F.t((xs[2] + xs[4]) / 2 + 10, 50, 'tohumlama (seeding) hızlandırır', 11.6, 700, RED, 'middle')
F.t(1014, 82, 'GAG', 11, 800, '#7a5a00'); F.t(xs[4] - 70, 78, 'SAP', 11, 800, GREEN, 'end')
serit(F, 6, 236, 1068, 'Doku tanısı', PUR); zemin(F, 6, 272, 1068, 114)
rg = random.Random(4)
def doku(cx, zem, renk, bas, alt):
    F.el(cx, 328, 46, 46, zem, '#8a9aa8', 1.4)
    for k in range(7):
        a = rg.uniform(0, 6.28); r = rg.uniform(4, 30)
        F.el(cx + r * math.cos(a), 328 + r * math.sin(a) * .8, rg.uniform(7, 13), rg.uniform(4, 8), renk, None, op=.9)
    F.t(cx + 60, 318, bas, 12.8, 800, INK); F.t(cx + 60, 336, alt, 11.6, None, INK2)
doku(70, '#fbf1f3', '#e58aa0', 'Kongo kırmızısı', 'ışık mikroskobu: pembe-kırmızı')
doku(430, '#1d2430', '#9fe08a', 'Polarize ışık', 'elma yeşili birefrenjans')
F.el(790, 328, 46, 46, '#f2f5f8', '#8a9aa8', 1.4)
for gx in range(-30, 31, 15):
    for gy in range(-30, 31, 15):
        if gx * gx + gy * gy > 36 * 36: continue
        a = rg.uniform(0, 3.14); x, y = 790 + gx + rg.uniform(-1.5, 1.5), 328 + gy + rg.uniform(-1.5, 1.5)
        F.ln(x - 6 * math.cos(a), y - 6 * math.sin(a), x + 6 * math.cos(a), y + 6 * math.sin(a), '#4a5b6b', 1.5)
F.t(850, 318, 'Elektron mikroskopisi', 12.8, 800, INK); F.t(850, 336, 'rastgele dizilimli, 8–12 nm', 11.6, None, INK2)
D.yeni('s18_fib', 'x18_9', 'Moleküler Çerçeve · Şekil', 'Amiloid Fibrili Nasıl Oluşur, Nasıl Görülür?', F,
       '<b>Okuma:</b> Çözünür öncül protein konformasyon değiştirir, zincirleri fibril eksenine dik dizilen çapraz-β oligomerler çekirdek oluşturur ve tohumlama ile 8–12 nm çaplı, dallanmayan fibriller uzar; SAP, apolipoprotein E ve glikozaminoglikanlar yapıya katılır. '
       'Dokuda Kongo kırmızısı ile boyanır, polarize ışıkta elma yeşili birefrenjans verir; elektron mikroskopisinde rastgele dizilimli fibriller görülür.',
       'Şekil: üstte soldan sağa beş adım: katlanmış çözünür öncül protein, yanlış katlanmış zincir, zincirleri fibril eksenine dik dizilmiş çapraz beta oligomeri, uzayan protofilament ve sekiz ile on iki nanometre çaplı düz fibril; '
       'fibrile beşli halka biçimli serum amiloid P ve glikozaminoglikan zinciri bağlı. Fibrilden oligomere dönen kesikli ok tohumlamayı gösteriyor. '
       'Altta üç doku görüntüsü: Kongo kırmızısıyla pembe birikim, polarize ışıkta koyu zeminde elma yeşili parlama, elektron mikroskopisinde rastgele dizilimli fibriller.')
