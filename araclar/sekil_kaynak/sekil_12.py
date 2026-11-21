#!/usr/bin/env python3
"""Ders 12 · Lupus Nefriti — şekiller."""
from sekil_ortak import *
from sekil_gk import *
D = Ders('12'); L = D.L

# ---------------------------------------------------------------- 1 · ISN/RPS sınıfları
F = Fig('isn', 452, 'ISN/RPS lupus nefriti sınıfları I–VI', w=1080)
SN = [('I · Minimal mezangiyal', 'L', 'I', ['Işıkta normal glomerül; İF/EM’de', 'yalnız mezangiyal birikim'], None),
      ('II · Mezangiyal proliferatif', 'L', 'II', ['Mezangiyal hiperselülarite', '(≥ 4 çekirdek) + mezangiyal birikim'], None),
      ('III · Fokal', 'G', 'III', ['Segmental ya da global, aktif ya da', 'inaktif GN; < %50 glomerül'], 3),
      ('IV · Diffüz', 'G', 'IV', ['Aynı lezyonlar, ≥ %50 glomerül;', 'subendotelyal birikim (“tel halka”)'], 7),
      ('V · Membranöz', 'L', 'V', ['GBM kalınlaşması + subepitelyal', 've mezangiyal birikim; PLA2R negatif'], None),
      ('VI · İleri sklerozan', 'G', 'VI', ['≥ %90 glomerül global sklerotik;', 'rezidüel aktivite yok'], 9)]
for i, (ad, tur, op, sat, ik) in enumerate(SN):
    r_, c_ = divmod(i, 3); x = 6 + c_ * 358; y = 6 + r_ * 224; cx = x + (130 if ik is not None else 175)
    renk = (GREEN, GREEN, GOLD, RED, BRAND, INK2)[i]
    serit(F, x, y, 350, ad, renk if renk != INK2 else BRANDD, h=26, fs=13.5)
    zemin(F, x, y + 30, 350, 144)
    if tur == 'L':
        G = GK(F, 'lobul', cx - 76, y + 34, 152, kirp=(190, 430, 790, 980), cerceve=LINE)
        if op == 'I': G.mezangiyal(5, 22)
        elif op == 'II': G.mez_hucre(6, 26); G.mezangiyal(4, 20)
        elif op == 'IV':
            for k, n in ((0, 7), (1, 3), (2, 3)): G.subendotelyal(k, G.dagit(k, n), gen=14, yuk=16)
            G.lumende(0, 'monosit', 2, 36); G.lumende(0, 'notrofil', 1, 32); G.mez_hucre(2); G.mezangiyal(3, 20)
        elif op == 'V':
            G.silinme(0, 158, 36); G.silinme(2, 176, 303)
            for k, n in ((0, 14), (1, 6), (2, 6)): Q = G.dagit(k, n); G.subepitelyal(k, Q, gen=9, yuk=20); G.diken(k, G.aralar(Q))
            G.mezangiyal(3, 20)
    else:
        G = GK(F, 'yumak', cx - 61, y + 33, 122, kirp=(0, 20, 680, 800))
        if op == 'III': G.lokosit(12, 140, 250, r=17); G.lobuler(13, .85, '#6e2a5c', (150, 205)); G.fibrinoid(180, .66, 50)
        elif op == 'IV': G.lokosit(30, r=17); G.lobuler(13, .85, '#6e2a5c', (150, 115, 80, 45, 10, 335, 205)); G.fibrinoid(60, .62, 46)
        else: G.global_skleroz()
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
A = GK(F, 'lobul', 14, 48, 350, cerceve=LINE); A.kose(50)
A.silinme(0, 300, 30)
Q = A.dagit(0, 10, 'dis', 250, 35); A.subepitelyal(0, Q); A.subepitelyal(2, A.dagit(2, 4))
A.subendotelyal(0, [195, 345], gen=12); A.subendotelyal(1, [10], gen=12); A.subendotelyal(2, [250], gen=12)
MZ = A.mezangiyal(6, 17); A.mez_hucre(2)
t = A.tri(2, 288)
A.etiket(A.duvar(0, Q[len(Q) // 2], 'subepi'), 380, 212, ['Subepitelyal'])
A.etiket(A.duvar(0, 345, 'subendo'), 380, 252, ['Subendotelyal'])
A.etiket(max(MZ, key=lambda q: q[0]), 380, 300, ['Mezangiyal'])
A.etiket(t, 380, 352, ['Tübüloretiküler', 'inklüzyon (endotel)'])
q = A.xy(A.duvar(0, 345, 'subendo'))
F.el(530, 118, 44, 44, '#f2f2f2', '#3a4a5a', 1.6)
for j in range(7): F.yol(f'M{496 + j * 3:.0f},{94 + j * 6:.0f} q{34 - j * 2},{-14 + j * 2} {68 - j * 6},0', '#3a4a5a', 1.4)
F.ln(q[0], q[1], 490, 136, '#3a4a5a', 1.1, '3 3'); F.t(530, 178, '“Parmak izi”', 11.8, 800, '#3a4a5a', 'middle'); F.t(530, 193, 'organize alt yapı', 11.2, None, INK2, 'middle')
serit(F, 620, 6, 454, 'İmmünfloresan: “full-house”', PUR)
for j, ad in enumerate(['IgG', 'IgA', 'IgM', 'C3', 'C1q']):
    cx = 676 + (j % 3) * 150; cy = 100 + (j // 3) * 150
    if_patern(F, cx, cy, 44, 'mez_kap', baslik=ad, fs=11.5, resim='if_fh')
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
