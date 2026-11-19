#!/usr/bin/env python3
"""Ders 12 · Lupus Nefriti — şekiller."""
from sekil_ortak import *
D = Ders('12'); L = D.L

# ---------------------------------------------------------------- 1 · ISN/RPS sınıfları
F = Fig('isn', 452, 'ISN/RPS lupus nefriti sınıfları I–VI', w=1080)
SN = [('I · Minimal mezangiyal', 'L', dict(mez=2, mez_boy=4), ['Işıkta normal glomerül; İF/EM’de', 'yalnız mezangiyal birikim'], None),
      ('II · Mezangiyal proliferatif', 'L', dict(acik=1.2, mez_hiper=6, mez=3), ['Mezangiyal hiperselülarite', '(≥ 4 çekirdek) + mezangiyal birikim'], None),
      ('III · Fokal', 'G', dict(endokap_seg=(140, 260), nekroz=(200, 240)), ['Segmental ya da global, aktif ya da', 'inaktif GN; < %50 glomerül'], 3),
      ('IV · Diffüz', 'L', dict(endokap=True, subendo=[(0, -90, 150, 8), (1, 30, 150, 8), (2, 150, 150, 8)], mez=2), ['Aynı lezyonlar, ≥ %50 glomerül;', 'subendotelyal birikim (“tel halka”)'], 7),
      ('V · Membranöz', 'L', dict(subepi=dict(evre=2, aralik=16), mez=2, efase=True), ['GBM kalınlaşması + subepitelyal', 've mezangiyal birikim; PLA2R negatif'], None),
      ('VI · İleri sklerozan', 'G', dict(**{'global': True}), ['≥ %90 glomerül global sklerotik;', 'rezidüel aktivite yok'], 9)]
for i, (ad, tur, op, sat, ik) in enumerate(SN):
    r_, c_ = divmod(i, 3); x = 6 + c_ * 358; y = 6 + r_ * 224; cx = x + (130 if ik is not None else 175)
    renk = (GREEN, GREEN, GOLD, RED, BRAND, INK2)[i]
    serit(F, x, y, 350, ad, renk if renk != INK2 else BRANDD, h=26, fs=13.5)
    zemin(F, x, y + 30, 350, 144)
    if tur == 'L': Lobul(F, cx, y + 102, .52, **op)
    else: Glomerul(F, cx, y + 102, 50, vp=180, up=0, tubul_boy=.5, arteriyol_boy=.3, **op)
    F.tl(x + 6, y + 194, sat, 13, 17, fill=INK)
    if ik is not None:
        for j in range(10):
            r2, c2 = divmod(j, 5); q = (x + 250 + c2 * 19, y + 84 + r2 * 22)
            F.el(q[0], q[1], 7.5, 7.5, BOW, GBM_K, 1.1); F.el(q[0], q[1], 5.3, 5.3, (RED if i != 5 else SKL_K) if j < ik else '#f4b7b4', None)
        F.t(x + 288, y + 148, f'{ik}/10 glomerül', 12.4, 800, INK2, 'middle')
D.yeni('s12_isn', 'x12_8', 'Temel Bilgiler · 3 · Şekil', 'ISN/RPS — Altı Sınıf, Altı Çizim', F,
       '<b>Okuma:</b> Sınıf I ve II’de birikim mezangiyumla sınırlıdır. III ile IV’ü ayıran lezyonun türü değil, tutulan glomerül oranıdır (sağdaki küçük daireler). '
       'IV’te subendotelyal “tel halka” birikimleri ve endokapiller hiperselülarite tipiktir. V membranözdür; VI’da glomerüllerin en az %90’ı global sklerotiktir.',
       'Şekil: lupus nefritinin altı sınıfı. Birinci ve ikinci sınıfta birikim mezangiyumda, ikincide mezangiyal hücreler de artmış. Üçüncü sınıfta glomerüllerin yarısından azında segmental lezyon, '
       'dördüncüde yarısından fazlasında; subendotelyal tel halka birikimleri ve lümende iltihap hücreleri. Beşinci sınıf membranöz, altıncı sınıfta glomerüller global sklerotik.')

# ---------------------------------------------------------------- 2 · İF ve EM imzası
F = Fig('imz', 420, 'Lupus nefritinde birikimlerin her yerde bulunması, tübüloretiküler inklüzyon, parmak izi yapısı ve full-house immünfloresan', w=1080, mh=410)
serit(F, 6, 6, 600, 'Elektron mikroskopisi: birikim her yerde', PUR); zemin(F, 6, 42, 600, 372)
mg = mini_glomerul(F, 70, 112, 34, vp=-90, up=128, fs=9.5); yakinlastir(F, mg, (320, 232), 130, kutu_a=-10)
A = Lobul(F, 320, 232, .92, subepi=dict(evre=1, aralik=26), subendo=[(0, -110, 60, 5), (1, 40, 60, 5), (2, 160, 50, 5)], mez=3, mez_hiper=3, tri=True, tri_i=1, efase=[(-40, 60)])
etk(F, A.yakin('subepi', 200, 140), 170, 240, ['Subepitelyal'], False)
etk(F, A.yakin('subendo', 300, 110), 170, 300, ['Subendotelyal'], False)
etk(F, A.yakin('mez', 320, 300), 170, 384, ['Mezangiyal'], False)
etk(F, A.tri_p, 470, 360, ['Tübüloretiküler', 'inklüzyon (endotel)'], True)
q = A.yakin('subendo', 420, 260)
F.el(540, 150, 44, 44, '#f2f2f2', '#3a4a5a', 1.6)
for j in range(7): F.yol(f'M{506 + j * 3:.0f},{126 + j * 6:.0f} q{34 - j * 2},{-14 + j * 2} {68 - j * 6},0', '#3a4a5a', 1.4)
F.ln(q[0], q[1], 504, 168, '#3a4a5a', 1.1, '3 3'); F.t(540, 210, '“Parmak izi”', 11.8, 800, '#3a4a5a', 'middle'); F.t(540, 225, 'organize alt yapı', 11.2, None, INK2, 'middle')
serit(F, 620, 6, 454, 'İmmünfloresan: “full-house”', PUR)
for j, ad in enumerate(['IgG', 'IgA', 'IgM', 'C3', 'C1q']):
    cx = 676 + (j % 3) * 150; cy = 100 + (j // 3) * 150
    if_patern(F, cx, cy, 44, 'mez_kap', baslik=ad, fs=11.5)
F.r(920, 214, 154, 132, '#fff', LINE, 1.4, 10)
F.tl(932, 236, ['IgG çoğu kez baskın;', 'güçlü C1q klasik yolu', 'gösterir. Hastaların', '~%50’sinde tübüler bazal', 'membranda da birikim.', 'Fibrin: aktif lezyon.'], 11.2, 15.5, fill=INK)
D.yeni('s12_imz', 'x12_9', 'Temel Bilgiler · 4 · Şekil', 'Lupusun İmzası — Her Yerde Birikim, Her Antikor', F,
       '<b>Okuma:</b> Lupus nefritinde birikimler mezangiyal, subendotelyal ve subepitelyal alanların hepsinde bulunabilir. Endotelde tübüloretiküler inklüzyon yüksek interferon ortamını yansıtır; '
       'bazı birikimlerde parmak izi benzeri organize alt yapı görülür. İmmünfloresanda IgG, IgA, IgM, C3 ve C1q’nun birlikte bulunması “full-house” paternidir.',
       'Şekil: solda lupus nefritinde glomerül lobülü; birikimler mezangiyal, subendotelyal ve subepitelyal alanların hepsinde, endotelde tübüloretiküler inklüzyon ve büyütülmüş parmak izi yapısı. '
       'Sağda immünfloresanda beş boyanın beşi de pozitif: full-house paterni.')

# ---------------------------------------------------------------- 3 · NIH aktivite ve kroniklik
F = Fig('nih', 266, 'Modifiye NIH aktivite ve kroniklik indekslerinin bileşenleri ve en yüksek puanları', w=1080)
F.t(6, 22, 'Aktivite indeksi · en fazla 24', 13.5, 800, RED); F.t(236, 22, 'her lezyon 0–3 · kresent ve fibrinoid nekroz × 2', 11.4, None, INK2)
ux = 42.5; X0 = 20
AKT = [('Hücresel/fibroselüler kresent × 2', 6, RED), ('Fibrinoid nekroz × 2', 6, '#d9534f'), ('Nötrofil / karyoreksis', 3, GOLD), ('Endokapiller hiperselülarite', 3, '#e1a94a'),
       ('Hiyalin birikim (tel halka)', 3, PUR), ('İnterstisyel inflamasyon', 3, '#9a7cc0')]
xx = X0
for (ad, v, c) in AKT:
    F.r(xx, 54, v * ux - 2, 30, c, None, rx=4); F.t(xx + v * ux / 2, 74, str(v), 13, 800, '#fff', 'middle')
    F.tl(xx + 3, 100, [ad] if gen(ad, 11) < v * ux - 6 else ad.split(' ', 1), 11, 14, fill=INK); xx += v * ux
F.ln(X0 + 2 * ux, 46, X0 + 2 * ux, 90, INK, 2.2, '4 3'); F.t(X0 + 2 * ux + 4, 50, 'tedavi sonrası > 2: kötü prognoz', 11, 800, INK)
F.t(6, 152, 'Kroniklik indeksi · en fazla 12', 13.5, 800, BRANDD)
KR = [('Total glomerüloskleroz', 3, '#6f8796'), ('Fibröz kresent', 3, '#8aa2b0'), ('Tübüler atrofi', 3, '#a3b7c2'), ('İnterstisyel fibroz', 3, '#bccbd3')]
xx = X0
for (ad, v, c) in KR:
    F.r(xx, 166, v * ux - 2, 30, c, None, rx=4); F.t(xx + v * ux / 2, 186, str(v), 13, 800, '#fff', 'middle')
    F.tl(xx + 3, 212, ad.split(' ', 1), 11, 14, fill=INK); xx += v * ux
F.ln(X0 + 6 * ux, 158, X0 + 6 * ux, 202, INK, 2.2, '4 3'); F.t(X0 + 6 * ux + 4, 162, '> 6: kötü prognoz', 11, 800, INK)
F.r(560, 150, 514, 110, '#fff', LINE, 1.4, 10)
F.t(574, 172, 'Puanlama', 12.4, 800, BRANDD)
for j, (p_, t_) in enumerate((('0', 'yok'), ('1', 'hafif (< %25)'), ('2', 'orta (%25–50)'), ('3', 'ağır (> %50)'))):
    x = 574 + j * 124; F.r(x, 186, 26, 24, BRAND, None, rx=5); F.t(x + 13, 203, p_, 13, 800, '#fff', 'middle'); F.t(x + 32, 203, t_, 11.4, None, INK)
F.t(574, 236, 'Tedaviye “tam” klinik yanıt alınsa da histolojik aktivite sürebilir:', 11.4, None, INK2); F.t(574, 252, 'tekrar biyopsinin gerekçesi budur.', 11.4, None, INK2)
D.yeni('s12_nih', 'x12_10', 'Temel Bilgiler · 5 · Şekil', 'NIH İndeksi — Puanlar Nereden Gelir?', F,
       '<b>Okuma:</b> Kutuların genişliği her lezyonun alabileceği en yüksek puanla orantılıdır. Kresent ve fibrinoid nekroz iki kat sayıldığı için aktivite indeksinin yarısını oluşturur. '
       'Kesikli çizgiler slayttaki iki eşiği gösterir.',
       'Şekil: üstte aktivite indeksi: kresent ve fibrinoid nekroz altışar puan, nötrofil, endokapiller hiperselülarite, tel halka ve interstisyel inflamasyon üçer puan; toplam yirmi dört. '
       'Altta kroniklik indeksi: dört lezyon, üçer puan, toplam on iki. Tedavi sonrası aktivite ikinin, kroniklik altının üstündeyse prognoz kötüdür.', oz=OZGUN_G)

# ---------------------------------------------------------------- 4 · üç çalışma
F = Fig('lnt', 300, 'BLISS-LN, AURORA-1 ve REGENCY çalışmalarında böbrek yanıt oranları', w=1080)
F.t(6, 22, 'Standart tedavinin üstüne eklenen ilaç ile plasebo · böbrek yanıtı (%)', 13.5, 800, BRANDD)
cubuk(F, 60, 66, 700, 160, [(['BLISS-LN · belimumab', 'birincil etkin yanıt · 104. hafta'], [43, 32], ['%43', '%32']), (['BLISS-LN · belimumab', 'tam yanıt · 104. hafta'], [30, 20], ['%30', '%20']),
                              (['AURORA-1 · voklosporin', 'tam yanıt · 52. hafta'], [41, 23], ['%41', '%23']), (['REGENCY · obinutuzumab', 'tam yanıt · 76. hafta'], [46.4, 33.1], ['%46,4', '%33,1'])],
      [('İlaç + standart', PUR), ('Plasebo + standart', MUT)], ymax=60, adim=10, fs=12, bw=54)
F.r(790, 40, 284, 252, '#fff', LINE, 1.4, 10)
F.t(804, 62, 'Okurken', 12.6, 800, BRANDD)
for j, ls in enumerate((['Yanıt tanımları, süreler ve standart', 'tedaviler farklıdır; çubukları', 'yan yana sıralamak yanıltıcıdır.'], ['BLISS-LN: böbrekle ilişkili olay', 'ya da ölüm HR 0,51.'],
                         ['AURORA-1: odds oranı 2,65; eGFR’ye', 'hemodinamik etkiye dikkat.'], ['REGENCY: 24. haftada prednizon', '5 mg/gün zemininde.'])):
    yy = 86 + [0, 56, 96, 136][j]; F.t(806, yy, '•', 11.4, 800, INK); F.tl(818, yy, ls, 11.4, 16, fill=INK)
D.yeni('s12_lnt', 'x12_23', 'Obinutuzumab · Şekil', 'Üç Faz 3, Üç Mekanizma — Böbrek Yanıtı', F,
       '<b>Okuma:</b> Üç çalışmada da standart tedavinin üstüne eklenen ilaç böbrek yanıtını artırdı. Belimumab BAFF’ı, voklosporin kalsinörini, obinutuzumab CD20’yi hedefler. '
       'Tanımlar ve süreler farklı olduğu için çalışmalar birbiriyle karşılaştırılmamalıdır.',
       'Şekil: üç faz 3 çalışmasında böbrek yanıtı. BLISS-LN’de birincil etkin yanıt yüzde kırk üç ile otuz iki, tam yanıt otuz ile yirmi; AURORA-1’de tam yanıt kırk bir ile yirmi üç; '
       'REGENCY’de tam yanıt kırk altı virgül dört ile otuz üç virgül bir.', oz=OZGUN_G)
