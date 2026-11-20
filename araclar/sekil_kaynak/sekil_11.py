#!/usr/bin/env python3
"""Ders 11 · MPGN ve C3 Glomerülopati — şekiller."""
from sekil_ortak import *
from sekil_gk import *
D = Ders('11'); L = D.L

# ---------------------------------------------------------------- 1 · çift kontur
F = Fig('kon', 436, 'MPGN paterninde lobüler glomerül ve çift konturun oluşumu: mezangiyal interpozisyon ve yeni bazal membran', w=1080, mh=410)
serit(F, 6, 6, 400, 'Işık mikroskopisi: lobüler görünüm', BRAND); zemin(F, 6, 42, 400, 388)
G = GK(F, 'yumak', 112, 50, 286, kirp=(0, 20, 680, 800)); G.mez_agac(); G.lobuler(); G.cekirdekler(40)
G.etiket((G.kc[0] + G.tr(205) * .9 * math.cos(math.radians(205)), G.kc[1] + G.tr(205) * .9 * math.sin(math.radians(205))), 104, 140, ['Belirgin', 'lobülasyon'], sag=False, fs=11.5)
G.etiket((G.kc[0] + G.tr(150) * .93 * math.cos(math.radians(150)), G.kc[1] + G.tr(150) * .93 * math.sin(math.radians(150))), 104, 250, ['Kalın', 'kapiller', 'duvar'], sag=False, fs=11.5)
G.etiket((G.kc[0] + G.tr(80) * .45, G.kc[1] + G.tr(80) * .2), 120, 414, ['Mezangiyal hücre ve matriks artışı'], fs=11.5)
serit(F, 418, 6, 656, 'Elektron mikroskopisi: çift kontur nasıl oluşur?', BRAND); zemin(F, 418, 42, 656, 388)
A = GK(F, 'lobul', 426, 50, 370, cerceve=LINE); A.kose(54)
A.cift_kontur(0, 165, 262); A.cift_kontur(0, 300, 30); A.cift_kontur(1, 280, 40); A.cift_kontur(2, 200, 290)
A.subendotelyal(0, [345, 10], gen=10); A.subendotelyal(2, [240], gen=10); MH = A.mez_hucre(4)
A.etiket(A.duvar(0, 315, 'gbm'), 808, 70, ['Eski GBM'])
A.etiket(A.cift_nokta(0, 320, 'yeni_gbm'), 808, 116, ['Yeni GBM', '(çift kontur)'])
A.etiket(A.cift_nokta(0, 330, 'interpoz'), 808, 172, ['Mezangiyal', 'interpozisyon'])
A.etiket(A.duvar(0, 10, 'subendo'), 808, 230, ['Subendotelyal', 'birikim'])
A.etiket(A.cift_nokta(0, 20, 'endotel'), 808, 290, ['Endotel: yeni GBM’nin', 'lümen tarafında'])
A.etiket(max(MH, key=lambda q: q[0]), 808, 350, ['Mezangiyal artış'])
F.t(808, 398, 'Gümüş boyasında', 11.6, 800, BRANDD); F.t(808, 413, '“tramvay rayı”', 11.6, None, INK)
D.yeni('s11_kon', 'x11_9', 'Temel Bilgiler · 5 · Şekil', 'Çift Kontur — Eski GBM, Araya Giren Hücre, Yeni GBM', F,
       '<b>Okuma:</b> Subendotelyal birikimler ve mezangiyal hücre uzantıları endotel ile bazal membran arasına girer; endotel bunun lümen tarafına yeni bir bazal membran döşer. '
       'Gümüş boyasında iki paralel çizgi, eski ve yeni GBM’dir. Işıkta glomerül lobüler, mezangiyum genişlemiş, kapiller duvar kalındır.',
       'Şekil: solda ışık mikroskopisinde lobüler glomerül; mezangiyum genişlemiş, kapiller duvarlar kalın. Sağda kapiller ilmekte çift konturun oluşumu: '
       'eski bazal membran, araya giren mezangiyal hücre ve subendotelyal birikim, lümen tarafında yeni bazal membran ve endotel.')

# ---------------------------------------------------------------- 2 · DDD ve C3GN
F = Fig('ddd', 450, 'Yoğun birikim hastalığı ile C3 glomerülonefritinde elektron mikroskopi bulguları', w=1080, mh=410)
for (x, bas, c) in ((6, 'Yoğun birikim hastalığı (DDD)', '#3a4a5a'), (546, 'C3 glomerülonefriti (C3GN)', PUR)):
    serit(F, x, 6, 528, bas, c); zemin(F, x, 42, 528, 318)
A = GK(F, 'lobul', 14, 50, 296, cerceve=LINE); A.kose(44)
A.intramembranoz(0, 158, 36); A.intramembranoz(1, 272, 80); A.intramembranoz(2, 176, 303); MD = A.mezangiyal(5, 30)
A.etiket(A.duvar(0, 340, 'gbm'), 324, 76, ['GBM’nin şeritsel,', 'çok yoğun dönüşümü', '(intramembranöz)'])
A.etiket(min(MD, key=lambda q: math.hypot(q[0] - 450, q[1] - 700)), 324, 220, ['Mezangiyumda', 'büyük yoğun birikimler'])
F.tl(324, 300, ['Bowman kapsülü ve', 'tübüler bazal membranda', 'da benzer değişiklik'], 11.4, 15, fill=INK2)
B = GK(F, 'lobul', 554, 50, 296, cerceve=LINE); B.kose(44)
MB = B.mezangiyal(7, 13, renk='#56616b', kenar='#2f3840'); B.mez_hucre(3)
B.subendotelyal(0, [5, 330], gen=12, renk='#56616b', kenar='#2f3840'); B.subendotelyal(2, [250], gen=12, renk='#56616b', kenar='#2f3840')
B.hump(0, [300], renk='#56616b', kenar='#2f3840'); B.hump(2, [205], renk='#56616b', kenar='#2f3840')
B.etiket(B.duvar(0, 300, 'ayak'), 864, 76, ['Ara sıra', 'subepitelyal hörgüç'])
B.etiket(B.duvar(0, 5, 'subendo'), 864, 160, ['Subendotelyal', 'birikimler'])
B.etiket(max(MB, key=lambda q: q[0] - q[1] * .3), 864, 250, ['Mezangiyal', 'birikimler'])
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
