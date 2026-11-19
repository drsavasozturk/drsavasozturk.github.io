#!/usr/bin/env python3
"""Ders 13 · Hızlı İlerleyen Glomerülonefrit — şekiller."""
from sekil_ortak import *
D = Ders('13'); L = D.L

# ---------------------------------------------------------------- 1 · kresentin evrimi (slayt içi, x13_5)
F = Fig('kre', 298, 'Kapiller duvar yırtığından fibröz kresente: kresentin dört evresi', mh=306)
EV = [('1 · Kapiller duvarda yırtık', dict(nekroz=(195, 250)), ['Fibrinoid nekroz; fibrinojen', 'Bowman boşluğuna geçer'], None),
      ('2 · Hücresel kresent', dict(hilal=(150, 300, 'hucresel')), ['Paryetal epitel çoğalır,', 'makrofaj ve T hücresi göçer'], ('Geri dönüşlü', GREEN)),
      ('3 · Fibroselüler kresent', dict(hilal=(140, 320, 'fibroselular'), kapsul_yirtik=(230, 26)), ['Bowman kapsülünde yırtık,', 'fibroblast göçü'], ('Kısmen geri dönüşlü', GOLD)),
      ('4 · Fibröz kresent', dict(hilal=(110, 350, 'fibroz'), skleroz=(150, 300), yapisiklik=False, hiyalin=False), ['Kollajen ve skar;', 'glomerül kaybı'], ('Geri dönüşsüz', RED))]
for i, (ad, op, sat, rz) in enumerate(EV):
    x = 8 + i * 284; cx = x + 134
    zemin(F, x, 4, 268, 196)
    G = Glomerul(F, cx, 108, 62, vp=-90, up=90, tubul_boy=.38, arteriyol_boy=.26, **op)
    if i == 0: etk(F, G.nekroz_p, x + 44, 34, ['fibrin'], False, fs=10.5, kalin=False)
    F.t(cx, 222, ad, 12.6, 800, BRANDD, 'middle'); F.tl(cx, 240, sat, 11.2, 14.5, fill=INK, a='middle')
    if rz: rozet(F, cx, 278, rz[0], rz[1], 11)
    if i < 3: F.ok(x + 270, 104, x + 282, 104, INK2, 2)
D.ic('s13_kre', 'x13_5', F)

# ---------------------------------------------------------------- 2 · üç immünopatolojik sınıf
F = Fig('ifr', 352, 'Kresentik glomerülonefritte üç immünopatolojik sınıfın immünfloresan paterni', w=1080)
SN = [('Tip 1 · Lineer', 'lineer', 'IgG, GBM boyunca düz çizgi', 'Anti-GBM hastalığı', 'erişkin HİGN’nin ~%10–15’i', 'kompleman normal'),
      ('Tip 2 · Granüler', 'kaba', 'IgG, IgA, C3 benekli/granüler', 'IgAN · lupus · enfeksiyon · kriyo · MPGN', '~%25–40', 'kompleman sıklıkla düşük'),
      ('Tip 3 · Pauci-immün', 'negatif', 'boyanma yok ya da çok az', 'ANCA ilişkili vaskülit (GPA, MPA, EGPA)', 'en sık, ~%50–60', 'kompleman normal')]
for i, (ad, t, pat, hs, sk, km) in enumerate(SN):
    x = 6 + i * 358; cx = x + 175
    serit(F, x, 6, 350, ad, (RED, PUR, BRAND)[i])
    if_patern(F, cx, 122, 70, t)
    F.t(cx, 222, pat, 12.2, 800, INK, 'middle')
    F.t(cx, 248, hs, 12, 700, (RED, PUR, BRAND)[i], 'middle')
    F.t(cx, 270, sk, 11.6, None, INK2, 'middle'); F.t(cx, 290, km, 11.6, None, INK2, 'middle')
F.r(6, 306, 1068, 40, TINT[GOLD], GOLD, 1.3, 10)
F.t(540, 331, 'Seroloji: anti-GBM (ELISA) · ANA, anti-dsDNA, C3/C4, kriyoglobulin, HBV/HCV, kan kültürü · ANCA (PR3, MPO ELISA + IIF)', 12, 700, '#6b4a00', 'middle')
D.yeni('s13_ifr', 'x13_6', 'Temel Bilgiler · 2 · Şekil', 'Üç Sınıf, Üç Floresan — Lineer, Granüler, Boş', F,
       '<b>Okuma:</b> Anti-GBM hastalığında IgG bazal membranı düz bir çizgi gibi boyar; immün kompleks hastalıklarında boyanma benekli ve kabadır; ANCA ilişkili vaskülitte glomerülde '
       'immün birikim yok denecek kadar azdır. Kresentin nedenini immünfloresan belirler.',
       'Şekil: üç immünfloresan paterni. Birinci tipte bazal membran boyunca lineer IgG; anti-GBM hastalığı. İkinci tipte granüler boyanma; immün kompleks glomerülonefritleri. '
       'Üçüncü tipte boyanma yok; ANCA ilişkili vaskülit, en sık neden.')

# ---------------------------------------------------------------- 3 · anti-GBM: kreatinin ve antijen
F = Fig('agb', 326, 'Anti-GBM hastalığında başvuru kreatinine göre bir yıllık sağkalım ve Goodpasture antijeninin yeri', w=1080)
F.t(6, 22, 'Bir yıllık sağkalım · başvuru durumuna göre (71 hasta)', 13.5, 800, BRANDD)
cubuk(F, 60, 66, 560, 170, [(['Kreatinin < 5,7 mg/dL', 'n = 19'], [100, 95], ['%100', '%95']), (['Kreatinin ≥ 5,7, diyaliz yok', 'n = 13'], [83, 82], ['%83', '%82']),
                              (['Başvuruda diyaliz', 'n = 39'], [65, 8], ['%65', '%8'])], [('Hasta sağkalımı', BRAND), ('Renal sağkalım', RED)], ymax=112, adim=25, fs=12, bw=58)
F.t(6, 312, 'Biyopside %100 kresent + diyaliz: hastaların tamamı diyalize bağımlı kaldı.', 12, 800, RED)
F.ln(660, 10, 660, 318, LINE, 1.5)
F.t(684, 22, 'Antijen: tip IV kollajen α3 zincirinin NC1 bölgesi', 13, 800, BRANDD)
F.r(684, 40, 390, 150, '#e4f0f4', GBM_K, 1.4, 10); F.t(696, 60, 'Glomerüler bazal membran', 11.6, 800, GBM_K)
for j in range(3):
    y = 96 + j * 30
    for (a, b) in ((704, 846), (900, 1050)):
        for (dy, c) in ((-4, '#d9534f'), (0, '#3b7dbf'), (4, '#6a9a5e')):
            F.yol('M' + ' L'.join('%.1f,%.1f' % (a + t * 6, y + dy + 2 * math.sin(t * .8 + dy)) for t in range(int((b - a) / 6) + 1)), c, 1.6)
    F.el(861, y, 12, 11, GOLD, '#8a5a00', 1.4); F.el(885, y, 12, 11, GOLD, '#8a5a00', 1.4)
F.t(873, 178, 'NC1 heksameri', 11, 800, '#8a5a00', 'middle'); F.t(775, 178, 'protomer (α3α4α5)', 10.6, None, INK2, 'middle'); F.t(975, 178, 'protomer', 10.6, None, INK2, 'middle')
F.ln(861, 64, 861, 76, RED, 3); F.ln(861, 76, 853, 84, RED, 3); F.ln(861, 76, 869, 84, RED, 3)
F.t(874, 66, 'anti-GBM IgG', 11, 800, RED)
F.tl(684, 212, ['α3 (COL4A3, 2q36–37) · α4 · α5 zincirleri üçlü sarmal oluşturur;', 'iki protomer C uçlarında NC1 heksameriyle birleşir.',
                 'Epitop heksamer içinde gizlidir; tetikleyiciler açığa çıkarır.', 'Antikor bazal membranı düz bir çizgi gibi boyar (lineer IgG);', 'alveol bazal membranında da aynı antijen vardır.'], 11.6, 17, fill=INK)
F.t(684, 312, 'Tedavi kararı saatlerle ölçülür: test sonucu beklenmez.', 12, 800, RED)
D.yeni('s13_agb', 'x13_18', 'Anti-GBM · 1 · Şekil', 'Anti-GBM — Kreatinin Kaderi Belirler, Antijen α3(IV) NC1', F,
       '<b>Okuma:</b> Başvuru kreatinini 5,7 mg/dL’nin altındaysa bir yıllık renal sağkalım %95’tir; başvuruda diyaliz gerekiyorsa %8’e düşer. Antikor tip IV kollajenin α3 zincirinin NC1 bölgesine bağlanır.',
       'Şekil: solda başvuru durumuna göre bir yıllık hasta ve renal sağkalım: kreatinin beş virgül yedinin altında yüzde yüz ve doksan beş, üstünde ama diyalizsiz seksen üç ve seksen iki, '
       'başvuruda diyalizde altmış beş ve sekiz. Sağda bazal membrandaki tip dört kollajen ağı ve alfa üç zincirinin NC1 bölgesine bağlanan antikor.', oz=OZGUN)

# ---------------------------------------------------------------- 4 · imlifidaz
F = Fig('iml', 268, 'İmlifidazın IgG’yi menteşe bölgesinden kesmesi ve GOOD-IDES-01 sonuçları', w=1080)
def igg(x, y, s=1.0, c=RED):
    F.ln(x, y, x, y + 34 * s, c, 7 * s); F.ln(x, y, x - 22 * s, y - 26 * s, c, 7 * s); F.ln(x, y, x + 22 * s, y - 26 * s, c, 7 * s)
    F.ln(x - 6 * s, y + 2, x - 26 * s, y - 22 * s, '#f6c3bf', 2.4 * s); F.ln(x + 6 * s, y + 2, x + 26 * s, y - 22 * s, '#f6c3bf', 2.4 * s)
F.t(6, 22, 'İmlifidaz (IdeS): IgG’yi menteşeden keser', 13.5, 800, BRANDD)
igg(90, 110, 1.3); F.t(90, 190, 'IgG', 12.4, 800, INK, 'middle')
F.ok(150, 110, 230, 110, INK2, 2.6); F.t(190, 98, 'İmlifidaz', 12, 800, GREEN, 'middle')
F.ln(70, 117, 110, 117, GREEN, 2.4, '4 3'); F.t(66, 121, 'kesim', 10.6, 700, GREEN, 'end')
F.ln(290, 104, 268, 78, RED, 9); F.ln(290, 104, 312, 78, RED, 9); F.ln(290, 104, 290, 116, RED, 9)
F.t(290, 140, 'F(ab’)₂', 12.4, 800, INK, 'middle')
F.ln(360, 112, 360, 150, RED, 9); F.t(360, 172, 'Fc', 12.4, 800, INK, 'middle')
F.r(20, 206, 420, 54, TINT[GREEN], GREEN, 1.3, 10)
F.t(32, 228, 'İnfüzyondan 6 saat sonra tüm hastalarda', 12, 800, GREEN); F.t(32, 246, 'anti-GBM antikoru referans aralığın altında', 12, None, INK)
F.ln(470, 10, 470, 260, LINE, 1.5)
F.t(494, 22, 'GOOD-IDES-01 · faz 2a · 15 hasta (eGFR < 15; 10’u diyalizde)', 13, 800, BRANDD)
cubuk(F, 540, 68, 300, 140, [(['6. ayda diyalizden', 'bağımsız'], [67, 18], ['%67 (10/15)', '%18 (9/50)'])], [('İmlifidaz + standart', GREEN), ('Tarihsel kontrol', MUT)], ymax=80, adim=20, fs=12, bw=70)
F.r(870, 40, 204, 170, TINT[GOLD], GOLD, 1.3, 10)
F.t(882, 62, 'Dürüst okuma', 12, 800, '#6b4a00'); F.tl(882, 82, ['Tek kollu, 15 hasta;', 'karşılaştırma tarihsel', 'kontrolle. Tarihsel kontrol', 'olumsuz görünme eğilimi', 'taşır; randomize', 'doğrulama yok.'], 11.4, 16, fill='#6b4a00')
D.yeni('s13_iml', 'x13_20', 'Anti-GBM · 3 · Şekil', 'İmlifidaz — Altı Saatte Kesilen Antikor', F,
       '<b>Okuma:</b> Streptokok kökenli bir endopeptidaz olan imlifidaz, IgG’yi menteşe bölgesinden F(ab’)₂ ve Fc parçalarına ayırır; dolaşan anti-GBM antikoru saatler içinde etkisizleşir. '
       'Diyalizden bağımsızlık oranı yüksek görünse de kanıt tek kollu bir faz 2a çalışmasına dayanır.',
       'Şekil: solda imlifidazın IgG’yi menteşe bölgesinden kesmesi; F(ab’) iki ve Fc parçaları. Sağda altıncı ayda diyalizden bağımsızlık: imlifidazla yüzde altmış yedi, tarihsel kontrolde yüzde on sekiz.', oz=OZGUN_G)
