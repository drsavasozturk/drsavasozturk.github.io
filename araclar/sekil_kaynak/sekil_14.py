#!/usr/bin/env python3
"""Ders 14 · Enfeksiyon ve Glomerüler Hastalık — şekiller."""
from sekil_ortak import *
D = Ders('14'); L = D.L

# ---------------------------------------------------------------- 1 · PSGN lobülü ve mekanizma
F = Fig('psg', 436, 'Poststreptokoksik glomerülonefritte eksüdatif glomerül lobülü ve patogenez basamakları', w=1080, mh=410)
serit(F, 6, 6, 620, 'Eksüdatif glomerülonefrit', RED); zemin(F, 6, 42, 620, 388)
mg = mini_glomerul(F, 70, 112, 34, vp=-90, up=128, fs=9.5); yakinlastir(F, mg, (340, 236), 135, kutu_a=-10)
A = Lobul(F, 340, 236, .92, endokap=True, endokap_n=5, hump=[-55, 5, 100, 160, 220, 285], mez=1)
etk(F, A.dep['hump'][1], 492, 80, ['Subepitelyal hörgüç', '(hump)'], True)
etk(F, A.p_lumen(1), 492, 300, ['Lümende nötrofil', 've monosit'], True)
etk(F, A.p_endo(2), 186, 300, ['Şişmiş endotel,', 'daralmış lümen'], False)
etk(F, A.yakin('mez', 340, 280), 492, 396, ['Mezangiyal birikim'], True)
serit(F, 640, 6, 434, 'Patogenez', BRANDD)
ADM = [('Nefritojenik suş', 'deri: M 49, 55, 57, 60 · boğaz: M 1, 2, 4, 12', RED),
       ('Glomerüle yerleşen antijen', 'NAPlr ve SPEB (öncüsü zSPEB); iyileşme serumlarının %92’sinde anti-NAPlr', GOLD),
       ('Alternatif yol', 'C3 düşük, C1q normal; bazı olgularda mezangiyal MBL (lektin yolu)', PUR),
       ('Klasik yol neden yok?', '“Evazinler” C1q’yu bağlar ve IgG’yi keser', BRAND)]
for i, (ad, tx, c) in enumerate(ADM):
    y = 48 + i * 92
    F.r(650, y, 414, 76, TINT.get(c, '#fff'), c, 1.4, 10)
    F.t(664, y + 24, ad, 12.6, 800, c)
    words = tx.split(' '); lines = ['']
    for w_ in words:
        if gen(lines[-1] + ' ' + w_, 11.6) > 386: lines.append(w_)
        else: lines[-1] = (lines[-1] + ' ' + w_).strip()
    F.tl(664, y + 44, lines, 11.6, 15.5, fill=INK)
    if i < 3: F.ok(857, y + 77, 857, y + 91, INK2, 2)
D.yeni('s14_psg', 'x14_6', 'Temel Bilgiler · 2 · Şekil', 'PSGN — Hörgüçler, Nötrofiller ve Alternatif Yol', F,
       '<b>Okuma:</b> Kapiller lümenler nötrofil ve monositle dolu, endotel şişmiş: eksüdatif glomerülonefrit. GBM’nin dış yüzünde iri subepitelyal hörgüçler tipiktir ama patognomonik değildir. '
       'Streptokok antijenleri glomerüle yerleşir; kompleman alternatif yoldan etkinleşir, bu yüzden C3 düşer, C1q normal kalır.',
       'Şekil: solda poststreptokoksik glomerülonefritte glomerül lobülü; lümenlerde nötrofil ve monosit, şişmiş endotel, subepitelyal hörgüçler ve mezangiyal birikim. '
       'Sağda patogenez basamakları: nefritojenik suş, glomerüle yerleşen streptokok antijeni, alternatif kompleman yolu ve klasik yolun neden etkin olmadığı.')

# ---------------------------------------------------------------- 2 · üç İF paterni
F = Fig('psi', 300, 'Poststreptokoksik glomerülonefritte üç immünfloresan paterni', w=1080)
PT = [('1 · Yıldızlı gök', 'yildiz', ['akut/subakut evre', 'kapiller duvar ve mezangiyumda', 'dağınık güçlü C3']),
      ('2 · Çelenk (garland)', 'kaba', ['çok sayıda subepitelyal hörgüç', '+ ağır proteinüri', 'aktif hastalık']),
      ('3 · Mezangiyal', 'mez', ['subakut-kronik dönem', 'birikimler temizlenir,', 'baskın C3 kalır'])]
for i, (ad, t, sat) in enumerate(PT):
    x = 6 + i * 358; cx = x + 175
    serit(F, x, 6, 350, ad, (RED, GOLD, BRAND)[i])
    if_patern(F, cx, 116, 66, t)
    F.tl(cx, 222, sat, 12, 16, fill=INK, a='middle')
F.t(6, 292, 'EM: subepitelyal hörgüç tipiktir ama patognomonik değildir. C3 ilk haftada %90’dan fazlasında düşüktür.', 11.6, None, INK2)
D.yeni('s14_psi', 'x14_7', 'Temel Bilgiler · 3 · Şekil', 'Üç Floresan Paterni — Hastalığın Saati', F,
       '<b>Okuma:</b> Yıldızlı gök paterni erken evrede görülür; çelenk paterni çok sayıda hörgüç ve ağır proteinüriyle birlikte aktif hastalığı gösterir; mezangiyal paternde birikimler temizlenirken C3 kalır.',
       'Şekil: üç immünfloresan paterni. Yıldızlı gökte kapiller duvar ve mezangiyumda dağınık C3; çelenkte kapiller duvarlar boyunca kaba, birleşik birikimler; mezangiyal paternde boyanma mezangiyumla sınırlı.')

# ---------------------------------------------------------------- 3 · zaman çizgisi ve biyopsi bayrakları (slayt içi, x14_8)
F = Fig('psz', 248, 'Poststreptokoksik glomerülonefritte doğal zaman çizgisi ve biyopsi gerektiren dört kırmızı bayrak', mh=254)
F.t(14, 22, 'Beklenen seyir', 13.5, 800, BRANDD); F.t(1110, 22, 'zaman ekseni ölçeksizdir', 11, None, MUT, 'end')
X0, X1, Y = 40, 1110, 66
F.ln(X0, Y, X1, Y, INK2, 3)
SEG = [(X0, 230, '#c9d6e0', 'Gizli dönem', ['boğaz: 7–10 gün', 'deri: 2–4 hafta']), (230, 420, '#f3c2bd', 'Nefrit', ['hematüri, ödem,', 'hipertansiyon']),
       (420, 600, '#cfe8d6', 'Diürez', ['7–10 günde idrar artar,', 'bulgular geriler']), (600, 820, '#e7f3ea', 'C3 normale döner', ['C3 düşüklüğü', '< 2 ay sürer']),
       (820, X1, '#f4f8f5', 'Hafif bulgular', ['mikrohematüri, < 500 mg/gün', 'proteinüri 1 yıla kadar'])]
for (a, b, c, ad, alt) in SEG:
    F.r(a, Y - 14, b - a - 3, 28, c, None, rx=6); F.t((a + b) / 2, Y + 5, ad, 12, 800, INK, 'middle')
    F.tl((a + b) / 2, Y + 34, alt, 11.2, 14.5, fill=INK2, a='middle')
F.el(X0, Y, 6, 6, RED, '#fff', 1.6); F.t(X0 - 6, Y - 22, 'enfeksiyon', 11, 700, RED); F.el(230, Y, 6, 6, RED, '#fff', 1.6); F.t(230, Y - 22, 'nefrit başlar', 11, 700, RED, 'middle')
F.t(14, 148, 'Biyopsi gerektiren dört kırmızı bayrak', 13.5, 800, RED)
BY = [('Oligüri', '> 1 hafta'), ('Böbrek fonksiyon kaybı', '> 2 hafta'), ('Hipokomplementemi', '> 1 ay · C3G’ye dönüşüm?'), ('Atipik tablo', 'öncesinde enfeksiyon yok, nefrotik düzey ya da erişkin')]
for i, (ad, tx) in enumerate(BY):
    x = 14 + i * 280
    F.r(x, 162, 268, 76, TINT[RED], RED, 1.4, 10); F.t(x + 14, 188, f'{i + 1} · {ad}', 12.6, 800, RED)
    ws = tx.split(' '); ls = ['']
    for w_ in ws:
        if gen(ls[-1] + ' ' + w_, 11.6) > 240: ls.append(w_)
        else: ls[-1] = (ls[-1] + ' ' + w_).strip()
    F.tl(x + 14, 208, ls, 11.6, 15, fill=INK)
D.ic('s14_psz', 'x14_8', F)

# ---------------------------------------------------------------- 4 · üç virüs, üç lezyon
F = Fig('vir', 440, 'Hepatit B, hepatit C ve HIV’in imza glomerüler lezyonları', w=1080, mh=410)
VR = [('HBV · membranöz nefropati', BRAND, 'L', dict(subepi=dict(evre=2, aralik=18), mez=2, mez_hiper=3, efase=True, subendo=[(2, 160, 26, 3)]),
       ['HBeAg küçük, katyonik → subepitelyal', 'HBsAg, HBcAg büyük → subendotelyal,', 'mezangiyal · IgG4 baskın değil']),
      ('HCV · kriyoglobulinemik MPGN', PUR, 'L', dict(cift=True, kriyo=(0, 2), subendo=[(1, 30, 70, 5)], mez=2, mez_hiper=3),
       ['Lümende kriyoglobulin “yalancı trombüs”ü;', 'çift kontur · C4 belirgin düşük,', 'romatoid faktör yüksek']),
      ('HIV · kollapsing glomerülopati', RED, 'G', dict(cokme=True),
       ['Yumak çöker, podositler çoğalır; tübüler', 'mikrokistler, endotelde tübüloretiküler', 'inklüzyon · APOL1 · hipertansiyon yok'])]
for i, (ad, c, tur, op, sat) in enumerate(VR):
    x = 6 + i * 358; cx = x + 175
    serit(F, x, 6, 350, ad, c); zemin(F, x, 42, 350, 290)
    if tur == 'L':
        mg = mini_glomerul(F, x + 52, 92, 26, vp=-90, up=128, etiket=False); yakinlastir(F, mg, (cx + 20, 200), 100, kutu_a=-10)
        A = Lobul(F, cx + 20, 200, .74, **op)
        if i == 1: etk(F, A.p_lumen(0), x + 340, 60, ['kriyoglobulin'], False, fs=11, kalin=False)
    else:
        Glomerul(F, cx, 186, 84, vp=180, up=0, tubul_boy=.55, arteriyol_boy=.32, **op)
        etk(F, P((cx, 186), 84 * .66, 90), x + 336, 312, ['hiperplastik podositler'], False, fs=11, kalin=False)
    F.tl(x + 10, 358, sat, 11.8, 16.5, fill=INK)
D.yeni('s14_vir', 'x14_11', 'Temel Bilgiler · 6 · Şekil', 'Üç Virüs, Üç İmza — MN, MPGN, Kollapsing', F,
       '<b>Okuma:</b> HBV’de antijenin büyüklüğü ve yükü birikimin yerini belirler: küçük, katyonik HBeAg bazal membranı geçip subepitelyal birikir. HCV’de tip II kriyoglobulinler MPGN paterni '
       've kapiller lümende yalancı trombüs yapar. HIV’de doğrudan viral etki ve APOL1 genotipi kollapsing glomerülopatiye yol açar.',
       'Şekil: solda hepatit B ilişkili membranöz nefropati; subepitelyal ve mezangiyal birikimler. Ortada hepatit C ilişkili kriyoglobulinemik membranoproliferatif glomerülonefrit; '
       'çift kontur ve lümende kriyoglobulin trombüsleri. Sağda HIV ilişkili kollapsing glomerülopati; çökmüş yumak ve çoğalmış podositler.')
