#!/usr/bin/env python3
"""Ders 11 · MPGN ve C3 Glomerülopati — şekiller."""
from sekil_ortak import *
D = Ders('11'); L = D.L

# ---------------------------------------------------------------- 1 · çift kontur
F = Fig('kon', 436, 'MPGN paterninde lobüler glomerül ve çift konturun oluşumu: mezangiyal interpozisyon ve yeni bazal membran', w=1080, mh=410)
serit(F, 6, 6, 400, 'Işık mikroskopisi: lobüler görünüm', BRAND); zemin(F, 6, 42, 400, 388)
G = Glomerul(F, 206, 214, 112, vp=-90, up=90, tubul_boy=.45, arteriyol_boy=.3, mez_genis=1.9, mez_cekirdek=.95, gbm_kalin=True)
etk(F, G.p_yumak(-150, .78), 98, 120, ['Belirgin', 'lobülasyon'], False, fs=11.5)
etk(F, G.p_yumak(20, .35), 400, 396, ['Mezangiyal hücre', 've matriks artışı'], False, fs=11.5)
etk(F, G.p_yumak(160, .75), 98, 330, ['Kalın kapiller', 'duvar'], False, fs=11.5)
serit(F, 418, 6, 656, 'Elektron mikroskopisi: çift kontur nasıl oluşur?', BRAND); zemin(F, 418, 42, 656, 388)
mg = mini_glomerul(F, 482, 112, 34, vp=-90, up=128, fs=9.5); yakinlastir(F, mg, (760, 236), 140, kutu_a=-10)
k = 1.0
A = Lobul(F, 760, 236, k, cift=True, subendo=[(0, -90, 64, 5), (1, 30, 64, 5), (2, 150, 64, 5)], mez=2, mez_hiper=4, acik=1.08)
etk(F, A.p_gbm(-90), 904, 70, ['Eski GBM'], True)
etk(F, A.p_ic(0, -125, 9 * k), 904, 110, ['Yeni GBM', '(çift kontur)'], True)
etk(F, A.p_ic(0, -28, 4.5 * k), 904, 160, ['Mezangiyal', 'interpozisyon'], True)
etk(F, A.yakin('subendo', 860, 280), 904, 330, ['Subendotelyal', 'birikim'], True)
etk(F, A.p_ic(2, 205, 14 * k), 600, 300, ['Endotel: yeni GBM’nin', 'lümen tarafında'], False)
etk(F, A.p_mezm(1), 600, 398, ['Mezangiyal artış'], False)
F.t(904, 400, 'Gümüş boyasında', 11.6, 800, BRANDD); F.t(904, 415, '“tramvay rayı”', 11.6, None, INK)
D.yeni('s11_kon', 'x11_9', 'Temel Bilgiler · 5 · Şekil', 'Çift Kontur — Eski GBM, Araya Giren Hücre, Yeni GBM', F,
       '<b>Okuma:</b> Subendotelyal birikimler ve mezangiyal hücre uzantıları endotel ile bazal membran arasına girer; endotel bunun lümen tarafına yeni bir bazal membran döşer. '
       'Gümüş boyasında iki paralel çizgi, eski ve yeni GBM’dir. Işıkta glomerül lobüler, mezangiyum genişlemiş, kapiller duvar kalındır.',
       'Şekil: solda ışık mikroskopisinde lobüler glomerül; mezangiyum genişlemiş, kapiller duvarlar kalın. Sağda kapiller ilmekte çift konturun oluşumu: '
       'eski bazal membran, araya giren mezangiyal hücre ve subendotelyal birikim, lümen tarafında yeni bazal membran ve endotel.')

# ---------------------------------------------------------------- 2 · DDD ve C3GN
F = Fig('ddd', 450, 'Yoğun birikim hastalığı ile C3 glomerülonefritinde elektron mikroskopi bulguları', w=1080, mh=410)
for (x, bas, c) in ((6, 'Yoğun birikim hastalığı (DDD)', '#3a4a5a'), (546, 'C3 glomerülonefriti (C3GN)', PUR)):
    serit(F, x, 6, 528, bas, c); zemin(F, x, 42, 528, 318)
for (x0, cx) in ((6, 290), (546, 830)):
    mg = mini_glomerul(F, x0 + 64, 112, 32, vp=-90, up=128, fs=9.5); yakinlastir(F, mg, (cx, 204), 112, kutu_a=-10)
A = Lobul(F, 290, 204, .86, yogun=True, mez=2, mez_boy=7, efase=[(-100, 40)])
etk(F, A.p_gbm(-40), 404, 76, ['GBM’nin şeritsel,', 'çok yoğun dönüşümü', '(intramembranöz)'], True)
etk(F, A.yakin('mez', 290, 260), 404, 300, ['Mezangiyumda', 'büyük yoğun birikimler'], True)
F.t(20, 334, 'Bowman kapsülü ve tübüler bazal', 11.4, None, INK2); F.t(20, 349, 'membranda da benzer değişiklik', 11.4, None, INK2)
B = Lobul(F, 830, 204, .86, mez=3, subendo=[(0, -90, 40, 4), (1, 30, 36, 4), (2, 150, 40, 4)], hump=[-30, 210], mez_hiper=3, subendo_renk='#6f7d89', mez_dep_renk='#6f7d89')
etk(F, B.yakin('mez', 830, 260), 958, 300, ['Mezangiyal', 'birikimler'], True)
etk(F, B.yakin('subendo', 760, 110), 690, 200, ['Subendotelyal', 'birikimler'], False)
etk(F, B.dep['hump'][0], 958, 76, ['Ara sıra', 'subepitelyal hörgüç'], True)
F.t(6, 384, 'DDD’de histolojik patern', 12.6, 800, BRANDD)
segs = [(45, '#7fb3d5', 'mezangiyal proliferatif %45'), (25, PUR, 'membranoproliferatif %25'), (18, RED, 'kresentik %18'), (12, GOLD, 'akut proliferatif-eksüdatif %12')]
xx = 200
for (v, c, ad) in segs:
    w = v * 3.4; F.r(xx, 372, w, 18, c, '#fff', 1.2, 3); xx += w
for j, (v, c, ad) in enumerate(segs):
    lx = 200 + (j % 2) * 175; ly = 408 + (j // 2) * 19
    F.r(lx, ly - 10, 12, 12, c, None, rx=2); F.t(lx + 16, ly, ad, 11.2, None, INK2)
haplar(F, 570, 382, 504, ['DDD: C3 düşük ~%80, C3NeF çoğunda', 'C3GN: C3 düşük ~%50, C3NeF %40–60', 'İF: ikisinde baskın C3'], PUR, 11.2)
D.yeni('s11_ddd', 'x11_11', 'Temel Bilgiler · 7 · Şekil', 'DDD ve C3GN — Ayrımı Elektron Mikroskopisi Yapar', F,
       '<b>Okuma:</b> DDD’de birikim GBM’nin kendisidir: bazal membran sürekli, çok yoğun bir şeride dönüşür; mezangiyumda büyük yoğunluklar vardır. '
       'C3GN’de birikimler ayrı ayrıdır ve daha az yoğundur: mezangiyal, subendotelyal, ara sıra subepitelyal. İkisinde de immünfloresanda baskın C3 görülür.',
       'Şekil: solda yoğun birikim hastalığı; glomerüler bazal membran sürekli, koyu bir şeride dönüşmüş, mezangiyumda büyük yoğun birikimler. '
       'Sağda C3 glomerülonefriti; ayrı ayrı mezangiyal ve subendotelyal birikimler ve ara sıra subepitelyal hörgüç. Altta yoğun birikim hastalığında histolojik paternlerin dağılımı.')

# ---------------------------------------------------------------- 3 · iptakopan ve pegsetakoplan
F = Fig('c3t', 320, 'Alternatif kompleman yolunda faktör B ve C3 inhibisyonu ile APPEAR-C3G ve VALIANT sonuçları', w=1080)
zemin(F, 6, 6, 430, 308)
F.t(20, 26, 'Alternatif yol ve iki hedef', 13, 800, BRANDD)
hap(F, 30, 80, 'C3', MUT); hap(F, 200, 80, 'C3b', MUT)
F.ok(76, 80, 196, 80, INK2, 2.4)
F.r(120, 140, 200, 56, TINT[PUR], PUR, 1.6, 10); F.t(220, 162, 'C3 konvertaz (C3bBb)', 12.4, 800, PUR, 'middle'); F.t(220, 182, 'C3b + faktör B (faktör D ile)', 11.2, None, INK2, 'middle')
F.ok(228, 94, 228, 138, INK2, 2); F.yol('M122,168 C60,168 50,96 60,92', PUR, 2.2, ok=True); F.t(74, 122, 'amplifikasyon', 11, None, PUR); F.t(74, 136, 'döngüsü', 11, None, PUR)
F.ok(320, 168, 360, 168, INK2, 2.2); hap(F, 364, 168, 'C5 → C5b-9', MUT, 11.4)
F.engel(300, 230, 260, 198, RED, 2.6); F.t(304, 246, 'İptakopan', 12.4, 800, RED); F.t(304, 262, 'faktör B’yi engeller (oral)', 11.2, None, INK2)
F.engel(296, 56, 252, 74, GREEN, 2.6); F.t(300, 52, 'Pegsetakoplan', 12.4, 800, GREEN); F.t(300, 67, 'C3 ve C3b’yi bağlar', 11.2, None, INK2)
F.t(20, 300, 'Kapsüllü bakterilere karşı aşılama her ikisinde de gereklidir.', 11.4, None, INK2)
F.t(462, 26, 'UPCR değişimi · başlangıca göre (%)', 13, 800, BRANDD)
ZX = 760; sc = 3.2
for v in (-80, -60, -40, -20, 0, 20):
    x = ZX + v * sc; F.ln(x, 44, x, 206, LINE if v else INK2, 1 if v else 1.8, '3 4' if v else None); F.t(x, 222, f'{v}'.replace('-', '−'), 11, None, MUT, 'middle')
GR = [('APPEAR-C3G · 6. ay', [('İptakopan', -30.2, RED), ('Plasebo', 7.6, MUT)]), ('VALIANT · 26. hafta', [('Pegsetakoplan', -67.2, GREEN), ('Plasebo', 2.9, MUT)])]
for g, (bas, sat) in enumerate(GR):
    y0 = 46 + g * 84; F.t(462, y0 + 12, bas, 11.8, 800, INK)
    for j, (ad, v, c) in enumerate(sat):
        y = y0 + 20 + j * 24
        F.t(ZX + (8 if v < 0 else -8), y + 12, ad, 11.4, None, INK2, 'start' if v < 0 else 'end')
        x0 = ZX + min(v, 0) * sc; F.r(x0, y, abs(v) * sc, 16, c, None, rx=3)
        F.t(ZX + v * sc + (-6 if v < 0 else 6), y + 12, ('−' if v < 0 else '+') + '%' + f'{abs(v):.1f}'.replace('.', ','), 11.6, 800, c, 'end' if v < 0 else 'start')
F.t(462, 262, 'Plaseboya göre göreli azalma: iptakopan %35,1 (13,8–51,1) · pegsetakoplan %68,1 (57,3–76,2)', 11.6, 800, INK)
F.t(462, 282, 'VALIANT: bileşik böbrek sonlanımı %49 ile %3; histolojik aktivite skorunda fark yok.', 11.4, None, INK2)
F.t(462, 302, 'Popülasyonlar, süreler ve tasarım farklı; çubuklar baş başa karşılaştırma değildir.', 11.4, 800, RED)
D.yeni('s11_c3t', 'x11_25', 'Pegsetakoplan · Şekil', 'Faktör B mi, C3 mü? — İki Hedef, İki Faz 3', F,
       '<b>Okuma:</b> İptakopan C3 konvertazın kurulması için gereken faktör B’yi, pegsetakoplan doğrudan C3 ve C3b’yi hedefler. Her iki çalışmada proteinüri plaseboya göre belirgin azaldı; '
       'VALIANT’ta histolojik aktivite skoru değişmedi.',
       'Şekil: solda alternatif kompleman yolu; iptakopan faktör B’yi, pegsetakoplan C3 ve C3b’yi engeller. Sağda proteinürideki değişim: APPEAR-C3G’de iptakopanla eksi otuz virgül iki, '
       'plaseboyla artı yedi virgül altı; VALIANT’ta pegsetakoplanla eksi altmış yedi virgül iki, plaseboyla artı iki virgül dokuz.', oz=OZGUN_G)
