#!/usr/bin/env python3
"""Ders 10 · IgA Nefropatisi — şekiller."""
from sekil_ortak import *
from sekil_gk import *
D = Ders('10'); L = D.L

# ---------------------------------------------------------------- 1 · patoloji: lobül + immünfloresan
F = Fig('igap', 436, 'IgA nefropatisinde mezangiyal birikim ve hiperselülarite ile immünfloresan bulguları', w=1080, mh=410)
serit(F, 6, 6, 600, 'Işık ve elektron mikroskopisi', BRAND); zemin(F, 6, 42, 600, 388)
A = GK(F, 'lobul', 16, 50, 356, cerceve=LINE); A.kose(52)
A.matriks_artisi(.32); A.mezangiyal(10); PA = A.paramezangiyal(0, 3); A.mez_hucre(4)
A.etiket(A.duvar(0, 330, 'gbm'), 386, 78, ['Kapiller duvar', 'çoğu kez korunmuş'])
A.etiket(A.duvar(0, PA[len(PA) // 2], 'subepi'), 386, 152, ['Mezangiyal ve', 'paramezangiyal', 'birikim'])
A.etiket(A.duvar(0, 20, 'endotel'), 386, 238, ['Pencereli endotel'])
A.etiket('mez_hucre2', 386, 300, ['Mezangiyal hücre', 've matriks artışı'])
A.etiket(A.duvar(2, 300, 'podosit'), 386, 380, ['Podosit'])
serit(F, 620, 6, 454, 'İmmünfloresan', BRAND)
if_patern(F, 690, 112, 52, 'mez', baslik='IgA', alt=['baskın / eş baskın', 'mezangiyal'], fs=11.5)
if_patern(F, 847, 112, 52, 'mez', renk='#a6f0b0', baslik='C3', alt=['olguların %90’ına', 'kadar'], fs=11.5)
if_patern(F, 1004, 112, 52, 'negatif', baslik='C1q', alt=['tipik olarak yok:', 'klasik yol değil'], fs=11.5)
F.t(626, 264, 'Kompleman yolu ipuçları', 12.6, 800, BRANDD)
haplar(F, 626, 290, 448, ['Properdin %75–100', 'Faktör H %30–90 → alternatif yol', 'MBL %17–25 ve C4d → lektin yolu, daha ağır hasar', 'Kapiller duvarda IgA: kötü prognoz'], BRAND, 11.6)
D.yeni('s10_pat', 'x10_9', 'Temel Bilgiler · 5 · Şekil', 'IgA Nefropatisi — Birikim Mezangiyumda, Tanı İmmünfloresanda', F,
       '<b>Okuma:</b> Lobülün ortasındaki mezangiyal alan genişlemiş, hücreleri çoğalmış ve birikimler burada toplanmıştır; kapiller duvarlar çoğu kez korunur. '
       'Işık mikroskopisi tanı koydurmaz; tanımlayıcı bulgu immünfloresanda baskın ya da eş baskın mezangiyal IgA’dır. C1q’nun olmaması klasik yolun değil, alternatif ve lektin yollarının etkin olduğunu gösterir.',
       'Şekil: solda IgA nefropatisinde glomerül lobülü; mezangiyal alan genişlemiş, mezangiyal hücreler çoğalmış, birikimler mezangiyumda. '
       'Sağda immünfloresan: mezangiyal IgA, olguların çoğunda C3, C1q ise tipik olarak yok.')

# ---------------------------------------------------------------- 2 · Oxford MEST-C
F = Fig('mest', 400, 'Oxford MEST-C sınıflamasının beş lezyonu', w=1080)
MS = [('M', 'Mezangiyal hiperselülarite', 'M', ['M0 ≤ %50 · M1 > %50 glomerülde', 'mezangiyal alanda > 3 hücre']),
      ('E', 'Endokapiller hiperselülarite', 'E', ['E0 yok · E1 var', 'tedaviyle geri döner']),
      ('S', 'Segmental skleroz', 'S', ['S0 yok · S1 var', 'podositopatik alt grup olabilir']),
      ('T', 'Tübüler atrofi / interstisyel fibroz', None, ['T0 %0–25 · T1 %26–50 · T2 > %50', 'en güçlü prognostik belirteç']),
      ('C', 'Kresent (hücresel/fibroselüler)', 'C', ['C0 yok · C1 < %25 · C2 ≥ %25', 'glomerülde'])]
for i, (h, ad, op, sat) in enumerate(MS):
    x = 6 + i * 216; cx = x + 104
    F.r(x, 6, 208, 30, TINT[BRAND], None, rx=8); F.t(x + 14, 28, h, 17, 800, BRAND); F.t(x + 34, 27, ad, 11.6 if len(ad) < 28 else 10.6, 800, BRANDD)
    zemin(F, x, 42, 208, 240)
    if op is not None:
        G = GK(F, 'yumak', cx - 98, 48, 196, kirp=(0, 20, 680, 800))
        if op == 'M': G.mez_agac(kalin=22, op=.38, cek=0); G.cekirdekler(34, 0, 359, r=11) if False else None; [elips(F, *G.xy(q), 11 * G.k, 8 * G.k, 30, CEK, CEK_K, .8) for q in G._sac(G.tuft.intersection(Point(G.kc[0], G.kc[1] - 40).buffer(120)).difference(Point(G.HILUS).buffer(40)), 20, 4)[:30]]
        elif op == 'E': G.lokosit(26, r=15)
        elif op == 'S': G.skleroz(150, 215, derin=.4)
        else: G.kresent(100, 215, 'hucresel')
    else:
        F.r(x + 104, 50, 98, 224, '#e8eef1', None, rx=8)
        for j in range(6): F.yol('M' + ' L'.join('%.1f,%.1f' % (x + 108 + t * 3.2, 56 + j * 38 + 3 * math.sin(t * .7)) for t in range(30)), '#b9c9d1', 1)
        for (yy, a) in ((92, False), (160, False), (228, False)): tubul_kesit(F, x + 54, yy, 26, a)
        for (yy, a) in ((92, True), (160, True), (228, True)): tubul_kesit(F, x + 153, yy, 26, a)
        F.t(x + 54, 270, 'normal', 11, 700, INK2, 'middle'); F.t(x + 153, 270, 'atrofi + fibroz', 11, 700, INK2, 'middle')
    F.tl(cx, 304, sat, 11.8, 16, fill=INK, a='middle')
F.r(6, 352, 1068, 42, TINT[GOLD], GOLD, 1.3, 10)
F.t(540, 378, 'Geçerlilik koşulu: biyopside en az 8 glomerül. Rapor MEST-C olarak verilir (C 2016’da eklendi).', 13, 800, '#6b4a00', 'middle')
D.yeni('s10_mest', 'x10_10', 'Temel Bilgiler · 6 · Şekil', 'Oxford MEST-C — Beş Harf, Beş Lezyon', F,
       '<b>Okuma:</b> M, E, S ve C glomerül lezyonlarıdır; T tübülointerstisyumu değerlendirir ve en güçlü prognostik belirteçtir. E ve C aktif, tedaviye yanıt verebilen lezyonlardır; '
       'S ve T kronik, geri dönmeyen hasarı gösterir.',
       'Şekil: Oxford MEST-C sınıflamasının beş lezyonu. M mezangiyal hiperselülarite, E endokapiller hiperselülarite, S segmental skleroz, T tübüler atrofi ve interstisyel fibroz, C kresent. '
       'Skorun geçerli olması için biyopside en az sekiz glomerül olmalıdır.')

# ---------------------------------------------------------------- 3 · STOP-IgAN ve TESTING
F = Fig('stp', 310, 'STOP-IgAN ve TESTING çalışmalarının temel sonuçları', w=1080)
F.t(6, 22, 'STOP-IgAN (n = 162) · 3 yıl', 13.5, 800, BRANDD); F.t(6, 40, 'destek + immünsüpresyona karşı yalnız destek', 11.6, None, INK2)
cubuk(F, 50, 84, 420, 150, [(['Tam klinik', 'remisyon'], [17, 5], ['%17', '%5']), (['eGFR’de ≥ 15', 'mL/dk düşüş'], [26, 28], ['%26', '%28'])],
      [('İmmünsüpresyon', BRAND), ('Yalnız destek', MUT)], ymax=50, adim=10, fs=12.4, bw=56)
F.t(260, 304, 'Remisyon arttı, eGFR kaybı değişmedi; 10 yıla kadar izlemde de fark yok.', 11.8, 800, RED, 'middle')
F.ln(540, 10, 540, 292, LINE, 1.5)
F.t(566, 22, 'TESTING (n = 503) · ortalama 4,2 yıl', 13.5, 800, BRANDD); F.t(566, 40, 'oral metilprednizolona karşı plasebo', 11.6, None, INK2)
cubuk(F, 610, 84, 450, 150, [(['Birincil sonlanım*'], [28.8, 43.1], ['%28,8', '%43,1']), (['Böbrek', 'yetmezliği'], [19.5, 27.2], ['%19,5', '%27,2']), (['Ciddi advers', 'olay'], [10.9, 2.8], ['%10,9', '%2,8'])],
      [('Metilprednizolon', BRAND), ('Plasebo', MUT)], ymax=50, adim=10, fs=12.4, bw=46)
F.t(566, 286, '* eGFR’de %40 düşüş, böbrek yetmezliği ya da böbrek kaynaklı ölüm · HR 0,53 (0,39–0,72)', 11.2, None, INK2)
F.t(566, 304, 'Ciddi advers olay esas olarak tam doz kolunda; önerilen: azaltılmış doz + profilaksi.', 11.8, 800, RED)
D.yeni('s10_stp', 'x10_19', 'Kortikosteroid · Şekil', 'STOP-IgAN ve TESTING — Aynı Soru, İki Cevap', F,
       '<b>Okuma:</b> STOP-IgAN’da immünsüpresyon remisyonu artırdı ama eGFR kaybını değiştirmedi; TESTING’de birincil böbrek sonlanımı azaldı, bedeli ciddi advers olaylardı. '
       'Popülasyon, başlangıç proteinürisi ve destek tedavisinin optimizasyonu farklıdır; iki çalışma doğrudan karşılaştırılamaz.',
       'Şekil: solda STOP-IgAN: tam klinik remisyon immünsüpresyonla yüzde on yedi, yalnız destekle yüzde beş; eGFR düşüşünde fark yok. '
       'Sağda TESTING: birincil sonlanım metilprednizolonla yüzde yirmi sekiz virgül sekiz, plaseboyla yüzde kırk üç virgül bir; ciddi advers olay yüzde on virgül dokuz ile yüzde iki virgül sekiz.', oz=OZGUN_G)

# ---------------------------------------------------------------- 4 · Nefecon: mukozal kaynak
F = Fig('nef', 330, 'Hedefli salınımlı budesonidin distal ileumda Peyer plaklarında etkisi ve NefIgArd sonuçları', w=1080)
zemin(F, 6, 6, 680, 318)
# ileum
F.yol('M30,130 C150,90 300,90 420,130 C470,146 520,150 560,140', '#c98a7a', 34); F.yol('M30,130 C150,90 300,90 420,130 C470,146 520,150 560,140', '#f6d6cc', 26)
for t in range(0, 26):
    x = 40 + t * 20; y = 112 + 18 * math.sin((x - 30) / 170 * math.pi) * -.9 + (0 if x < 420 else (x - 420) * .05)
    F.ln(x, y + 26, x, y + 36, '#e8a898', 3)
for (x, y) in ((300, 150), (322, 148), (344, 152)):
    F.el(x, y, 11, 9, '#d9ccef', PUR, 1.2); F.el(x, y, 4.5, 4, PUR)
F.t(322, 182, 'Peyer plakları (distal ileum)', 12, 800, PUR, 'middle')
F.t(30, 80, 'İnce bağırsak', 12, 800, '#9a5a4a')
F.r(150, 92, 34, 16, GOLD, '#8a5a00', 1.2, 8); F.r(167, 92, 17, 16, '#fff2cc', '#8a5a00', 1.2, 8)
F.t(150, 82, 'Nefecon kapsülü', 11.6, 800, GOLD)
F.ok(200, 104, 286, 136, GOLD, 2.4, '6 4'); F.t(236, 104, 'ilaç burada açılır', 11.2, None, GOLD)
# B hücresi → Gd-IgA1
F.ok(332, 196, 332, 232, PUR, 2.4)
F.el(332, 252, 16, 16, '#e3dbf5', PUR, 1.4); F.el(332, 252, 7, 6, PUR)
F.t(356, 248, 'Mukozal B hücresi', 11.6, 800, PUR); F.t(356, 264, 'galaktozdan yoksun IgA1 (Gd-IgA1)', 11.4, None, INK2)
F.ok(350, 274, 420, 290, PUR, 2.2); F.t(426, 294, '→ dolaşım → immün kompleks', 11.4, 800, INK); F.t(426, 308, '→ böbrekte mezangiyum', 11.4, 800, INK)
# karaciğer
F.yol('M560,214 q40,-30 96,-6 q10,30 -26,42 q-44,10 -70,-6 z', '#8a4a3a', 1.4, '#c98370')
F.t(610, 272, 'Karaciğer', 11.6, 800, '#6a3426', 'middle')
F.ok(560, 156, 590, 196, GOLD, 2.2, '5 4'); F.t(552, 196, 'emilen ilacın >%90’ı', 11.2, 800, GOLD, 'end'); F.t(552, 211, 'ilk geçişte yıkılır', 11.2, None, GOLD, 'end')
F.tl(20, 298, ['Yüksek lokal doz, sınırlı sistemik maruziyet;', 'ödem, hipertansiyon, akne gibi steroid etkileri yine de görülebilir.'], 11.4, 15, fill=INK2)
F.t(708, 22, 'NefIgArd · 2 yıl (9 ay ilaç + 15 ay izlem)', 13, 800, BRANDD)
cubuk(F, 760, 70, 300, 150, [(['eGFR değişimi', '2 yıl, zaman ağırlıklı ort.'], [2.47, 7.52], ['−2,47', '−7,52'])], [('Nefecon', BRAND), ('Plasebo', MUT)], ymax=10, adim=2, birim='azalma', fs=12.4, bw=64)
F.t(708, 258, 'Zaman ağırlıklı ortalama eGFR farkı', 12, 700, INK)
F.t(708, 276, '+5,05 mL/dk/1,73 m² (%95 GA 3,24–7,38); p < 0,0001', 12, 800, GREEN)
F.t(708, 296, 'Proteinürideki azalma ilaç kesildikten sonra da sürdü.', 11.6, None, INK2)
D.yeni('s10_nef', 'x10_21', 'Hedefli Tedavi · Şekil', 'Nefecon — Sorunu Kaynağında, Bağırsakta Hedeflemek', F,
       '<b>Okuma:</b> Hedefli salınımlı budesonid distal ileumda, Peyer plaklarının olduğu bölgede açılır; galaktozdan yoksun IgA1 üreten mukozal B hücrelerine yüksek lokal doz ulaşır, '
       'emilen ilacın çoğu karaciğerde ilk geçişte yıkılır. Sağda NefIgArd’ın iki yıllık eGFR sonucu.',
       'Şekil: solda hedefli salınımlı budesonidin etki yeri. İlaç distal ileumda Peyer plaklarına yakın açılır, mukozal B hücrelerini etkiler; emilen kısmın yüzde doksanından fazlası karaciğerde yıkılır. '
       'Sağda NefIgArd: iki yıllık zaman ağırlıklı ortalama eGFR değişimi Nefecon ile eksi iki virgül kırk yedi, plaseboyla eksi yedi virgül elli iki.')

# ---------------------------------------------------------------- 5 · APRIL/BAFF ve kompleman hedefleri
F = Fig('apr', 360, 'IgA nefropatisinde B hücresi, APRIL ve BAFF yolu ile kompleman hedefleri ve ilgili ilaçlar', w=1080)
zemin(F, 6, 6, 700, 348)
F.el(150, 150, 46, 46, '#dbe8f5', BRANDD, 1.8); F.el(150, 150, 18, 16, BRANDD); F.t(150, 214, 'B hücresi', 12.6, 800, BRANDD, 'middle')
F.el(470, 150, 52, 44, '#ece2f7', PUR, 1.8); elips(F, 486, 146, 16, 14, 0, PUR); F.t(470, 214, 'Plazma hücresi', 12.6, 800, PUR, 'middle')
F.ok(200, 150, 412, 150, INK2, 2.6); F.t(306, 140, 'olgunlaşma ve sağkalım', 11.4, None, INK2, 'middle')
for (x, ad) in ((108, 'BAFF-R'), (150, 'TACI'), (192, 'BCMA')):
    F.r(x - 4, 102, 8, 14, '#2f6f9a', None, rx=2); F.t(x, 96, ad, 9.8, 700, '#2f6f9a', 'middle')
for (x, ad) in ((452, 'TACI'), (488, 'BCMA')):
    F.r(x - 4, 100, 8, 14, '#2f6f9a', None, rx=2); F.t(x, 94, ad, 10.2, 700, '#2f6f9a', 'middle')
for (x, y, ad, c) in ((236, 64, 'APRIL', GOLD), (300, 64, 'BAFF', GREEN)):
    for j in range(3): F.el(x - 8 + j * 8, y, 5, 5, c, '#fff', 1)
    F.t(x, y - 12, ad, 11.6, 800, c, 'middle')
F.ok(228, 72, 154, 84, GOLD, 1.8, '4 3'); F.ok(292, 72, 112, 84, GREEN, 1.8, '4 3'); F.ok(250, 72, 446, 82, GOLD, 1.8, '4 3')
for (x, y) in ((560, 112), (590, 124), (575, 146)):
    F.yol(f'M{x},{y} l0,10 m0,-10 l-5,-7 m5,7 l5,-7', PUR, 2)
F.t(606, 108, 'Gd-IgA1 ve', 11.4, 800, PUR); F.t(606, 122, 'anti-glikan', 11.4, 800, PUR); F.t(606, 136, 'otoantikor', 11.4, 800, PUR)
F.r(464, 104, 24, 10, '#c05a2a', None, rx=3); F.t(476, 128, 'CD38', 10.2, 800, '#c05a2a', 'middle')
# kompleman kutusu
F.r(30, 246, 650, 96, '#fff', LINE, 1.4, 10)
F.t(44, 268, 'Glomerülde kompleman: alternatif ve lektin yolu', 12.4, 800, BRANDD)
for (x, ad) in ((50, 'C3'), (150, 'C3 konvertaz'), (330, 'C5'), (420, 'C5b-9 · inflamasyon')):
    w = hap(F, x, 300, ad, MUT, 11.8)
F.ok(86, 300, 146, 300, INK2, 2); F.ok(278, 300, 326, 300, INK2, 2); F.ok(372, 300, 416, 300, INK2, 2)
# ilaç etiketleri
for (x, ad, h, c) in ((150, 'Sibeprenlimab', 'yalnız APRIL', GOLD), (390, 'Atasisept · telitasisept', 'APRIL + BAFF (TACI-Fc)', GREEN)):
    F.t(x, 24, ad, 12, 800, c, 'middle'); F.t(x, 38, h, 10.6, None, INK2, 'middle')
F.t(560, 62, 'Felzartamab', 12, 800, '#c05a2a', 'middle'); F.t(560, 76, 'anti-CD38', 10.6, None, INK2, 'middle')
F.t(214, 332, 'faktör B gerekir · İptakopan faktör B’yi engeller', 11.2, 800, RED, 'middle')
SON = [('İptakopan · APPLAUSE-IgAN', '9. ayda UPCR plaseboya göre %38,3 daha düşük', RED),
       ('Atasisept · ORIGIN 3', '36. haftada UPCR azalması %45,7 ile %6,8', GREEN),
       ('Sibeprenlimab · VISIONARY', '9. ayda UPCR plaseboya göre %51,2 daha düşük', GOLD),
       ('Felzartamab · IGNAZ (faz 2)', '9 doz: 9. ayda UPCR −%29,5 (plasebo −%5,7)', '#c05a2a')]
F.t(724, 22, 'Faz 3 ara analizleri ve faz 2 · proteinüri', 12.6, 800, BRANDD)
for i, (ad, tx, c) in enumerate(SON):
    y = 40 + i * 64
    F.r(724, y, 350, 56, TINT.get(c, '#fbeee6'), None, rx=8); F.r(724, y, 5, 56, c, None, rx=2)
    F.t(738, y + 22, ad, 12.2, 800, c); F.t(738, y + 42, tx, 11.6, None, INK)
F.r(724, 300, 350, 54, TINT[GOLD], GOLD, 1.2, 8)
F.tl(736, 320, ['Doğrudan karşılaştırılmadılar; popülasyonlar farklı.', 'Yüzdeleri sıralamak yanıltıcıdır; eGFR verisi olgunlaşmadı.'], 11.4, 16, fill='#6b4a00')
D.yeni('s10_apr', 'x10_25', 'Kompleman ve B Hücresi · Şekil', 'APRIL, BAFF ve Kompleman — Yeni İlaçlar Nereye Vurur?', F,
       '<b>Okuma:</b> APRIL ve BAFF, B hücresinin ve plazma hücresinin TACI ve BCMA reseptörleri üzerinden sağkalımını ve IgA yapımını destekler; sibeprenlimab yalnız APRIL’i, '
       'atasisept ve telitasisept ikisini birden bağlar. Felzartamab plazma hücresindeki CD38’i, iptakopan glomerülde alternatif yolun faktör B’sini hedefler.',
       'Şekil: solda B hücresi ve plazma hücresi; APRIL ve BAFF ligandları ve reseptörleri, plazma hücresindeki CD38 ve altta glomerüldeki kompleman yolu. '
       'Her ilacın hedefi işaretlidir. Sağda dört çalışmanın ara sonuçları; doğrudan karşılaştırma yapılmamıştır.')
