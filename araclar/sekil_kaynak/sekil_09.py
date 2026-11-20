#!/usr/bin/env python3
"""Ders 09 · Membranöz Nefropati — şekil tanımları (sekil_kit ile çizilir)."""
from sekil_kit import *

L = []
OZGUN = ' <i>Özgün şematik çizim; ölçekli değildir.</i>'
D = '09'


def yeni(sid, hedef, kicker, baslik, F, alt, notu, ozgun=OZGUN):
    L.append(dict(id=sid, ders=D, mod='yeni', hedef=hedef, kicker=kicker, baslik=baslik, svg=F.svg(), alt=alt + ozgun, **{'not': notu}))


def ic(sid, hedef, F, alt=None, konum='son'):
    L.append(dict(id=sid, ders=D, mod='ic', hedef=hedef, svg=F.svg(), alt=alt, konum=konum))


def hap(F, x, y, txt, c=BRAND, fs=12.2, fill=None):
    w = gen(txt, fs) + 22
    F.r(x, y - 13, w, 26, fill or TINT.get(c, '#fff'), c, 1.3, 13); F.t(x + w / 2, y + 4.4, txt, fs, 700, INK, 'middle'); return w


# ============================================================================================== A · antijen haritası
F = Fig('ant', 398, 'Membranöz nefropatide hedef antijenlerin sıklığı, baskın IgG alt sınıfı ve klinik ipuçları', w=1080)
X0, PX = 190, 3.2            # sıklık ekseni: %0 = 190, %100 = 510
F.t(16, 24, 'Antijen', 12.6, 800, BRANDD); F.t(X0, 24, 'Sıklık (%)', 12.6, 800, BRANDD); F.t(576, 24, 'Baskın IgG', 12.6, 800, BRANDD, 'middle'); F.t(650, 24, 'Klinik karşılığı', 12.6, 800, BRANDD)
for v in (0, 20, 40, 60, 80, 100):
    F.ln(X0 + v * PX, 34, X0 + v * PX, 362, LINE, 1, '3 4'); F.t(X0 + v * PX, 46, str(v), 11, None, MUT, 'middle')
SAT = [('PLA2R', (70, 80), 'IgG4', 'Primer MN’nin baskın sistemi; sekonder MN’de nadir', BRAND),
       ('NELL1', (5, 10), 'IgG1', 'Üçte birine kadar malignite; segmental boyanma (%93,4)', BRAND),
       ('THSD7A', (1, 5), 'IgG4', 'Batıda ~%5, Japon hastalarda daha sık; malignite bildirilmiş', BRAND),
       ('Sema3B', 'nadir', 'IgG1', 'Erken çocukluk çağı MN’si; erişkinde nadir', BRAND),
       ('PCDH7 · HTRA1', 'nadir', 'değişken', 'Yeni primer alt tipler; PCDH7’de kompleman zayıf olabilir', BRAND),
       ('EXT1 / EXT2', None, '—', 'Otoimmün zemin: sınıf V lupus; genç kadında uyarıcı', PUR),
       ('NCAM1 · TGFBR3', None, '—', 'Lupus ilişkili MN; NCAM1 nöropsikiyatrik lupusla ilişkili', PUR),
       ('NEP', 'çok nadir', 'IgG1', 'Antenatal MN: feto-maternal alloimmünizasyon', GOLD)]
for i, (ad, sk, igg, kl, c) in enumerate(SAT):
    y = 76 + i * 38
    if i % 2 == 0: F.r(6, y - 19, 1068, 38, '#f6f9fb', None, rx=6)
    F.r(6, y - 15, 5, 30, c, None, rx=2.5); F.t(20, y + 4.5, ad, 13, 800, INK)
    if isinstance(sk, tuple):
        F.r(X0 + sk[0] * PX, y - 10, max(8, (sk[1] - sk[0]) * PX), 20, c, None, rx=4)
        F.t(X0 + sk[1] * PX + 10, y + 4.5, '%%%d–%d' % sk, 12.6, 800, c)
    elif sk:
        F.r(X0, y - 10, 9, 20, c, None, rx=4, op=.45); F.t(X0 + 18, y + 4.5, sk, 12, None, INK2, it=True)
    else:
        F.t(X0 + 4, y + 4.5, 'sıklık verilmemiş', 12, None, MUT, it=True)
    F.t(576, y + 4.5, igg, 12.6, 800 if igg.startswith('IgG') else None, INK if igg.startswith('IgG') else MUT, 'middle')
    F.t(650, y + 4.5, kl, 12.2, None, INK)
xx = 16
for (c, tx) in ((BRAND, 'podosit antijenleri (NELL1 ve THSD7A’da malignite aranır)'), (PUR, 'otoimmün zemin (lupus)'), (GOLD, 'alloimmün')):
    F.r(xx, 374, 12, 12, c, None, rx=3); F.t(xx + 18, 385, tx, 11.8, None, INK2); xx += 40 + gen(tx, 11.8)
yeni('s09_antijen', 'x09_7', 'Temel Bilgiler · 3 · Şekil', 'Antijen Haritası — Sıklık ve Klinik İpucu', F,
     '<b>Okuma:</b> Dört olgunun üçünde antijen PLA2R’dir. PLA2R negatif olguda sıradaki soru antijenin ne olduğudur: NELL1 ve THSD7A maligniteyi, '
     'EXT1/EXT2 ve NCAM1 lupusu, Sema3B çocukluk çağını düşündürür. Sıklıklar slayttaki tablodan alınmıştır.',
     'Şekil: membranöz nefropatide antijen haritası. PLA2R olguların yüzde yetmiş ile seksenini oluşturur. NELL1 yüzde beş ile on, THSD7A yüzde bir ile beş arasındadır. '
     'Diğer antijenler nadirdir ama klinik ipucu taşır: EXT1 ve EXT2 lupusu, NELL1 ve THSD7A maligniteyi düşündürür.', ozgun=' <i>Özgün çizim.</i>')

# ============================================================================================== B · primer mi sekonder mi: glomerül lobülü
from sekil_glom import Lobul, etk, mini_glomerul, yakinlastir, BOW as _BOW
from sekil_gk import GK
F = Fig('psk', 470, 'Primer ve sekonder membranöz nefropatide glomerül lobülü: birikim yerleşimi ve immünfloresan bulguları', w=1080, mh=420)
for (x, bas, c) in ((6, 'Primer MN', BRAND), (546, 'Sekonder MN — örnek: sınıf V lupus', PUR)):
    F.r(x, 6, 528, 30, TINT[c], None, rx=8); F.t(x + 264, 27, bas, 14, 800, c, 'middle')
    F.r(x, 42, 528, 310, _BOW, None, rx=10)
A = GK(F, 'lobul', 14, 50, 288, cerceve=LINE); A.kose(44)
A.silinme(0, 158, 36); A.silinme(1, 272, 80); A.silinme(2, 176, 303)
for k, n in ((0, 16), (1, 8), (2, 7)):
    Q = A.dagit(k, n); A.subepitelyal(k, Q); A.diken(k, A.aralar(Q))
    if k == 0: QA = Q
a1 = min(QA, key=lambda a: abs(((a - 335) + 180) % 360 - 180)); a2 = min(A.aralar(QA), key=lambda a: abs(((a - 5) + 180) % 360 - 180))
A.etiket(A.duvar(0, 300, 'ayak'), 318, 66, ['Podosit: ayaksı', 'çıkıntılar silinmiş'])
A.etiket(A.duvar(0, a1, 'subepi'), 318, 116, ['Subepitelyal', 'birikim (yalnız)'])
A.etiket(A.duvar(0, a2, 'subepi'), 318, 166, ['GBM dikenleri', '(birikimler arasında)'])
A.etiket(A.duvar(0, 22, 'gbm'), 318, 216, ['Glomerüler', 'bazal membran'])
A.etiket(A.duvar(0, 40, 'endotel'), 318, 262, ['Pencereli endotel'])
A.etiket('matriks', 318, 306, ['Mezangiyum:', 'sakin, birikim yok'])
B = GK(F, 'lobul', 554, 50, 288, cerceve=LINE); B.kose(44)
B.silinme(0, 158, 36); B.silinme(1, 272, 80); B.silinme(2, 176, 303)
for k, n in ((0, 12), (1, 6), (2, 5)):
    Q = B.dagit(k, n); B.subepitelyal(k, Q)
    if k == 0: QB = Q
B.mezangiyal(7); B.mez_hucre(3); B.subendotelyal(0, [12]); B.subendotelyal(2, [258], gen=12)
t = B.tri(2, 290)
b1 = min(QB, key=lambda a: abs(((a - 320) + 180) % 360 - 180))
B.etiket(B.duvar(0, 285, 'ayak'), 858, 66, ['Podosit: ayaksı', 'çıkıntılar silinmiş'])
B.etiket(B.duvar(0, b1, 'subepi'), 858, 116, ['Subepitelyal', 'birikim'])
B.etiket(B.duvar(0, 12, 'subendo'), 858, 166, ['Seyrek', 'subendotelyal birikim'])
B.etiket(t, 858, 222, ['Tübüloretiküler', 'inklüzyon (endotel)'])
B.etiket(B.T['mez_nokta'][0] if False else max(B._mzk, key=lambda q: q[0]), 858, 296, ['Mezangiyal birikim', 've hiperselülarite'])
IFL = [(6, BRAND, ['IgG4 baskın ya da eş baskın', 'PLA2R pozitif, IgG ile birlikte', 'C1q negatif ya da zayıf', 'IgA ve IgM yok']),
       (546, PUR, ['IgG1, IgG2 ya da IgG3 baskın', 'IgA ve/veya IgM bulunabilir', 'C1q pozitif', 'PLA2R negatif · EXT1/EXT2, NCAM1, TGFBR3'])]
for (x, c, hl) in IFL:
    F.t(x + 6, 376, 'İmmünfloresan', 12.4, 800, c)
    xx, yy = x + 6, 400
    for h_ in hl:
        w_ = gen(h_, 12.2) + 22
        if xx + w_ > x + 526: xx, yy = x + 6, yy + 32
        hap(F, xx, yy, h_, c); xx += w_ + 8
yeni('s09_primsek', 'x09_12', 'Temel Bilgiler · 6 · Şekil', 'Primer mi Sekonder mi — Birikim Nerede, Hangi IgG?', F,
     '<b>Okuma:</b> Üç kapiller ilmek ve ortada mezangiyal hücre (glomerül lobülü). Primer MN’de birikim yalnız subepitelyaldir, IgG4 baskındır. Mezangiyal ya da '
     'subendotelyal birikim, C1q pozitifliği ve endotelde tübüloretiküler inklüzyon sekonder nedeni, özellikle lupusu düşündürür; saf sınıf V’te subendotelyal birikim seyrektir.',
     'Şekil: glomerül lobülü; üç kapiller ilmek, pencereli endotel, glomerüler bazal membran, podositler ve ortada mezangiyal hücre. Solda primer, sağda sekonder membranöz nefropati. '
     'Primerde birikimler yalnız subepitelyaldir ve IgG4 baskındır. Sekonderde birikim mezangiyuma ve seyrek olarak endotel altına da yayılır, C1q pozitiftir, endotelde tübüloretiküler inklüzyon görülebilir.')

# ============================================================================================== D · doğal seyir (slayt içi)
F = Fig('sey', 246, 'Membranöz nefropatide remisyon durumuna göre on yıllık böbrek sağkalımı ve nüks oranları', mh=262)
F.t(40, 22, 'On yıllık böbrek sağkalımı (%)', 13.5, 800, BRANDD)
for v in (0, 25, 50, 75, 100):
    yy = 206 - v * 1.5; F.ln(92, yy, 540, yy, LINE if v else INK2, 1 if v else 1.8, '3 4' if v else None); F.t(84, yy + 4, str(v), 11.5, None, MUT, 'end')
for k, (ad, v, c) in enumerate((('Tam remisyon', 100, GREEN), ('Kısmi remisyon', 90, GOLD), ('Remisyon yok', 45, RED))):
    bx = 140 + k * 140; F.r(bx, 206 - v * 1.5, 84, v * 1.5, c, None, rx=4)
    F.t(bx + 42, 206 - v * 1.5 - 7, '%%%d' % v, 14, 800, c, 'middle'); F.t(bx + 42, 226, ad, 12.6, 700, INK, 'middle')
F.ln(580, 10, 580, 240, LINE, 1.5)
F.t(610, 22, 'Remisyondan sonra nüks (%)', 13.5, 800, BRANDD)
NX, NP = 770, 4.5
for v in (0, 20, 40, 60):
    F.ln(NX + v * NP, 40, NX + v * NP, 150, LINE, 1, '3 4'); F.t(NX + v * NP, 166, str(v), 11.5, None, MUT, 'middle')
F.t(760, 78, 'Tam remisyon sonrası', 12.6, 700, INK, 'end'); F.r(NX + 25 * NP, 64, 15 * NP, 22, GREEN, None, rx=4); F.t(NX + 40 * NP + 10, 80, '%25–40', 13, 800, GREEN)
F.t(760, 124, 'Kısmi remisyon sonrası', 12.6, 700, INK, 'end'); F.r(NX, 110, 50 * NP, 22, GOLD, None, rx=4, op=.55); F.ln(NX + 50 * NP, 106, NX + 50 * NP, 136, GOLD, 3)
F.t(NX + 50 * NP + 10, 126, '%50’ye kadar', 13, 800, GOLD)
F.tl(610, 196, ['Tam remisyondan nüks edenlerin çoğu nefrotik olmayan düzeyde kalır;', 'nüks ilk remisyondan 20 yıl sonra bile bildirilmiştir.'], 12.2, 16.5, fill=INK2)
ic('s09_seyir', 'x09_21', F)

# ============================================================================================== E · antikor–proteinüri gecikmesi (slayt içi)
F = Fig('gec', 150, 'Anti-PLA2R titresinin proteinüriden önce düşmesini gösteren şematik zaman eğrisi', mh=156)
GX, GW, GY, GH = 96, 600, 18, 104
F.ln(GX, GY, GX, GY + GH, INK2, 1.8); F.ln(GX, GY + GH, GX + GW, GY + GH, INK2, 1.8)
F.t(GX - 8, GY + 6, '%100', 11, None, MUT, 'end'); F.t(GX - 8, GY + GH / 2 + 4, '%50', 11, None, MUT, 'end'); F.t(GX - 8, GY + GH + 4, '0', 11, None, MUT, 'end')
F.ln(GX, GY + GH / 2, GX + GW, GY + GH / 2, LINE, 1.2, '4 4')
F.t(GX, GY + GH + 22, 'Rituksimab', 11.8, 800, INK); F.t(GX + GW, GY + GH + 22, 'zaman →', 11.8, None, MUT, 'end')
def egri(t50, n, taban=0):
    pts = []
    for i in range(0, 121):
        t = 24 * i / 120; v = taban + (100 - taban) * math.exp(-math.log(2) * (t / t50) ** n)
        pts.append('%.1f,%.1f' % (GX + GW * t / 24, GY + GH * (1 - v / 100)))
    return 'M' + ' L'.join(pts)
F.yol(egri(3, 1.25), PUR, 3.2); F.yol(egri(12.08, 2.6, 12), GOLD, 3.2)
F.t(GX + 8, GY - 6, 'başlangıç değerinin yüzdesi', 10.8, None, MUT)
xa, xp = GX + GW * 3 / 24, GX + GW * 13 / 24
F.el(xa, GY + GH / 2, 5, 5, PUR, '#fff', 1.5); F.el(xp, GY + GH / 2, 5, 5, GOLD, '#fff', 1.5)
F.ok(xa + 9, GY + GH / 2 + 13, xp - 9, GY + GH / 2 + 13, INK, 2, cift=True); F.t(xp - 14, GY + GH / 2 + 31, 'ortalama 10 ay', 12.6, 800, INK, 'end')
F.t(xa + 22, GY + 34, 'anti-PLA2R', 12.4, 800, PUR); F.t(xp + 60, GY + 40, 'proteinüri', 12.4, 800, GOLD)
F.t(730, 34, 'Antikor önce düşer', 14, 800, BRANDD)
F.tl(730, 56, ['Anti-PLA2R titresindeki %50 azalma, proteinürideki eşdeğer', 'azalmadan ortalama 10 ay önce gerçekleşir (Ruggenenti serisi;', 'anti-PLA2R pozitif 81 hasta). Antikor düşerken proteinürinin', 'hâlâ yüksek olması başarısızlık değildir.'], 12.2, 16.5, fill=INK)
F.t(730, 134, 'Şematik eğriler; hasta verisi değildir.', 11.4, None, MUT, it=True)
ic('s09_gecikme', 'x09_26', F)

# ============================================================================================== F · VTE
F = Fig('vte', 386, 'Membranöz nefropatide serum albümin düzeyine göre venöz tromboemboli riski ve profilaksi kararı', w=1080)
xx = 6
for tx in ('İki kohort, 898 hasta', 'VTE: 65 hasta (%7,2)', 'VTE’ye ortanca süre 3,8 ay', 'çoğu ilk iki yılda'):
    xx += hap(F, xx, 20, tx, BRAND) + 8
F.t(6, 62, 'Albümin düştükçe VTE riski: model türetimi, ölçüm değil', 13.5, 800, BRANDD)
F.t(6, 79, 'albümin 4,0 g/dL = 1; her 1,0 g/dL azalmada × 2,13 (Lionaki) katsayısıyla hesaplanmıştır', 11.4, None, MUT)
BX, BY, BH, BW = 70, 96, 190, 440
ax = lambda a_: BX + (4.0 - a_) * BW / 2.0
ay = lambda r_: BY + BH - r_ * 36
for v in (0, 1, 2, 3, 4, 5):
    F.ln(BX - 10, ay(v), BX + BW + 10, ay(v), LINE if v else INK2, 1 if v else 1.8, '3 4' if v else None); F.t(BX - 16, ay(v) + 4, '×%d' % v, 11.5, None, MUT, 'end')
pts = ['%.1f,%.1f' % (ax(4.0 - i * .02), ay(2.13 ** (i * .02))) for i in range(101)]
F.yol('M%.1f,%.1f L' % (ax(4.0), ay(0)) + ' L'.join(pts) + ' L%.1f,%.1f Z' % (ax(2.0), ay(0)), None, 0, RED, op=.12)
F.yol('M' + ' L'.join(pts), RED, 3.2)
for a_ in (4.0, 3.5, 3.0, 2.8, 2.5, 2.0):
    rr = 2.13 ** (4.0 - a_)
    F.el(ax(a_), ay(rr), 5, 5, RED, '#fff', 1.6); F.t(ax(a_) + (8 if a_ == 4.0 else -4), ay(rr) - 10, ('×%.1f' % rr).replace('.', ','), 12.6, 800, RED, 'start' if a_ == 4.0 else 'end')
    F.ln(ax(a_), ay(0), ax(a_), ay(0) + 5, INK2, 1.4); F.t(ax(a_), ay(0) + 20, ('%.1f' % a_).replace('.', ','), 12.4, 700, INK, 'middle')
F.t(BX + BW / 2, ay(0) + 38, 'serum albümin (g/dL)', 11.8, None, MUT, 'middle')
F.ln(ax(2.8), BY - 4, ax(2.8), ay(0), INK2, 1.6, '5 4')
F.t(ax(2.8) - 8, BY + 8, 'riskin en yüksek olduğu eşik: < 2,8 g/dL', 11.8, 800, INK, 'end'); F.t(ax(2.8) - 8, BY + 23, '(ayrı analiz)', 11.2, None, MUT, 'end')
# karar
F.t(580, 62, 'Profilaktik antikoagülasyon: karar', 13.5, 800, BRANDD)
F.etiket(580, 112, 494, ['1 · Albümin < 2,8 g/dL', 'Riskin en yüksek olduğu eşik; tek bağımsız öngörücü tanıdaki hipoalbüminemidir.'], RED, 12.6)
F.ok(827, 140, 827, 158, INK2, 2.4)
F.etiket(580, 190, 494, ['2 · Albümin < 2,0–2,5 g/dL ve kanama riski düşük-orta (ATRIA)', 'Karar analizine göre varfarinin yararı riskini aşıyor görünür.'], GOLD, 12.6)
F.ok(827, 218, 827, 236, INK2, 2.4)
F.etiket(580, 268, 494, ['3 · Profilaksiyi ciddi biçimde tartışın', 'Karar hasta ile paylaşılır; DMAH alternatif rejim olarak desteklenmiştir.'], GREEN, 12.6)
F.r(580, 306, 494, 72, '#fff', LINE, 1.4, 10)
F.tl(594, 327, ['• Randomize kontrollü çalışma yok; uzlaşı yok.', '• Doğrudan oral antikoagülanlar için güvenlik verisi çok az.', '• Arteriyel ve kardiyovasküler olay riski de anlamlıdır.'], 12, 17, fill=INK2)
yeni('s09_vte', 'x09_30', 'Tromboz · Şekil', 'Venöz Tromboemboli — Albümin Düştükçe Risk Katlanır', F,
     '<b>Okuma:</b> Eğri ölçülmüş olay oranı değildir; Lionaki çalışmasındaki tek katsayıdan (her 1,0 g/dL azalmada 2,13 kat) türetilmiştir '
     've yalnız eğilimi göstermek içindir. 2,8 g/dL eşiği aynı çalışmanın ayrı bir analizinden gelir. Karar basamakları slayttaki eşiklerle aynıdır.',
     'Şekil: solda serum albümin düştükçe venöz tromboemboli riskinin nasıl katlandığı, sağda profilaktik antikoagülasyon kararının basamakları. '
     'Albümin iki virgül sekizin altında risk en yüksektir. Albümin iki ile iki buçuğun altında ve kanama riski düşükse profilaksi ciddi biçimde tartışılır.',
     ozgun=' <i>Özgün çizim.</i>')

# ============================================================================================== G · Ponticelli takvimi (slayt içi)
F = Fig('pon', 92, 'Ponticelli siklik rejiminin altı aylık takvimi', mh=96)
F.t(14, 40, 'Ponticelli', 13.5, 800, BRANDD); F.t(14, 58, 'siklik rejimi', 12.4, None, INK2); F.t(14, 75, '6 ay', 12.4, 800, INK2)
for a_ in range(6):
    x = 118 + a_ * 170; st = a_ % 2 == 0; c = BRAND if st else GOLD
    F.r(x, 4, 164, 84, TINT[c], c, 1.5, 10); F.t(x + 12, 24, '%d. ay' % (a_ + 1), 13, 800, c)
    F.tl(x + 12, 43, (['Metilprednizolon 1 g IV,', '3 gün; sonra prednizon', '0,5 mg/kg/gün, 27 gün'] if st else ['Oral sitotoksik ajan:', 'siklofosfamid', '(ya da klorambusil)']), 11.6, 15, fill=INK)
    if a_ < 5: F.ok(x + 164, 46, x + 170, 46, INK2, 2)
ic('s09_ponticelli', 'x09_34', F)

# ============================================================================================== H · B hücresi soyağacı ve hedefler
F = Fig('bhc', 404, 'B hücresi olgunlaşma basamakları, CD20 ve CD38 ekspresyonu ve membranöz nefropatide kullanılan antikorların hedefleri', w=1080)
HC = [(76, 'Pro-B', '#dbe7f1'), (222, 'Pre-B', '#cfe3f3'), (372, 'Geçiş B', '#bcdaf0'), (522, 'Naif B', '#a9d0ec'), (672, 'Bellek B', '#8fc1e6'), (828, 'Plazmablast', '#d9c7ee'), (990, 'Plazma hücresi', '#c4a9e6')]
F.r(6, 6, 290, 26, '#f2f5f8', None, rx=8); F.t(151, 24, 'Kemik iliği', 12, 800, INK2, 'middle')
F.r(302, 6, 596, 26, '#f2f5f8', None, rx=8); F.t(600, 24, 'Kan ve lenfoid doku', 12, 800, INK2, 'middle')
F.r(904, 6, 170, 26, '#f2f5f8', None, rx=8); F.t(989, 24, 'Kemik iliği nişi', 12, 800, INK2, 'middle')
for k, (x, ad, c) in enumerate(HC):
    if k: F.ok(HC[k - 1][0] + 40, 84, x - 40, 84, INK2, 2.2)
    F.el(x, 84, 34, 34, c, BRANDD if k < 5 else PUR, 2); F.el(x - 6, 80, 15, 15, '#fff', None, op=.55)
    F.t(x, 138, ad, 12.8, 800, INK, 'middle')
# antikor üretimi
for x in (828, 990):
    for dx in (-12, 0, 12):
        F.yol('M%d,152 l0,10 m0,-10 l-4,-6 m4,6 l4,-6' % (x + dx), PUR, 1.8)
F.t(909, 178, 'otoantikor (anti-PLA2R) üretir', 12, 700, PUR, 'middle')
# CD20
F.t(6, 218, 'CD20', 13, 800, BRAND); F.r(188, 203, 518, 20, BRAND, None, rx=10); F.r(706, 203, 100, 20, BRAND, None, rx=10, op=.25)
F.t(447, 217.5, 'pre-B’den bellek B’ye kadar var; plazma hücresinde yok', 11.8, 700, '#fff', 'middle')
F.t(6, 264, 'CD38', 13, 800, PUR); F.r(52, 249, 354, 20, PUR, None, rx=10, op=.4); F.r(794, 249, 264, 20, PUR, None, rx=10)
F.t(926, 263.5, 'en yoğun: plazmablast, plazma hücresi', 11.8, 700, '#fff', 'middle'); F.t(420, 263.5, 'öncül ve geçiş B · ayrıca NK hücreleri', 11.6, None, INK2)
# ilaçlar
F.etiket(188, 304, 518, ['Anti-CD20: rituksimab (tip I, kimerik) · obinutuzumab (tip II, glikomühendislikli)',
                           'Antikor üreten hücreyi değil, öncülünü tüketir; antikor bu yüzden gecikerek düşer.'], BRAND, 12.2)
F.ln(262, 224, 262, 280, BRAND, 1.6, '3 4')
F.etiket(730, 304, 344, ['Anti-CD38: felzartamab', 'M-PLACE: immünolojik yanıt %76,9;', 'kısmi proteinüri remisyonu %34,6'], PUR, 12.2)
F.ln(926, 270, 926, 274, PUR, 1.6, '3 4')
F.r(6, 346, 1068, 52, '#fff', GOLD, 1.4, 10)
F.tl(20, 366, [[('İki uyarı. ', 'b'), 'Rituksimaba karşı antikor MN serilerinde %23–47 sıklıkta gelişir ve yanıtsızlığın gözden kaçan nedenidir. Bergamo serisinde (n = 10)'],
               'felzartamab NK ve geçiş B hücrelerini azalttı, ama bellek B, plazmablast ve plazma hücreleri etkilenmedi; proteinüri düzelmedi.'], 12, 17, fill=INK)
yeni('s09_bhucre', 'x09_39', 'Yeni Ajanlar · Şekil', 'B Hücresinden Plazma Hücresine — İlaç Nereye Vurur?', F,
     '<b>Okuma:</b> CD20 plazma hücresinde bulunmaz; anti-CD20 tedavi antikor fabrikasını değil, fabrikayı besleyen B hücrelerini tüketir. CD38 ise en yoğun '
     'plazma hücresindedir; anti-CD38’in mantığı budur, ancak eldeki klinik veri bu beklentiyi henüz karşılamamıştır.',
     'Şekil: B hücresinin olgunlaşma basamakları ve iki hedef molekül. CD20 pre-B hücresinden bellek B hücresine kadar bulunur, plazma hücresinde yoktur. '
     'CD38 en yoğun plazmablast ve plazma hücresindedir. Rituksimab ve obinutuzumab CD20’yi, felzartamab CD38’i hedefler.')

# ============================================================================================== I · MAJESTY
F = Fig('maj', 372, 'MAJESTY çalışmasında obinutuzumab ve takrolimus kollarının 104. hafta sonuçları', w=1080)
F.t(6, 22, 'MAJESTY · 104. hafta sonuçları (%)', 13.5, 800, BRANDD)
F.r(60, 52, 384, 24, TINT[GREEN], None, rx=8); F.t(252, 69, 'yüksek olması iyi', 11.8, 800, GREEN, 'middle')
F.r(452, 52, 252, 24, TINT[RED], None, rx=8); F.t(578, 69, 'düşük olması iyi', 11.8, 800, RED, 'middle')
cubuk(F, 60, 112, 644, 180, [(['Tam remisyon', '(birincil sonlanım)'], [37, 6], ['%37', '%6']), (['Tam ya da kısmi', 'remisyon'], [51, 13], ['%51', '%13']),
                              (['İmmünolojik remisyon', 'alt grup: titre ≥ 175'], [69, 13], ['%69', '%13']), (['Nüks'], [12, 58], ['%12', '%58']), (['Kaçış tedavisi'], [28, 61], ['%28', '%61'])],
      [('Obinutuzumab', BRAND), ('Takrolimus', GOLD)], ymax=80, adim=20, fs=12.6, bw=40, lejx=720, lejant=False)
F.ln(448, 84, 448, 292, LINE, 1.5)
F.r(730, 52, 14, 14, BRAND, None, rx=3); F.t(750, 64, 'Obinutuzumab (n = 71)', 12.6, 800, INK); F.r(730, 76, 14, 14, GOLD, None, rx=3); F.t(750, 88, 'Takrolimus (n = 70)', 12.6, 800, INK)
F.etiket(730, 158, 344, ['Tasarım', 'Faz 3; 142 hasta randomize (analiz: 71 ve 70)', 'Obinutuzumab 1 g IV: 1. gün, 2., 24., 26. hafta', 'Takrolimus 12 ay, ardından 8 haftada azaltma'], BRAND, 12.2)
F.etiket(730, 240, 344, ['Birincil sonlanım: tam remisyon', '26/71 ile 4/70; düzeltilmiş fark 31 puan', '(%95 GA 18–44; p < 0,001)'], GREEN, 12.2)
F.tl(730, 292, ['Tam remisyon süresi (ortanca): 105 ile 55 hafta', 'Grade ≥ 3 advers olay: %22 ile %19', 'Ciddi advers olay: %17 ile %14'], 12.2, 17, fill=INK2)
F.tl(6, 344, ['Tam ya da kısmi remisyonda fark anlamlıdır. Hiyerarşik sınama eGFR sonlanımında durduğu için tam remisyon süresi resmî olarak sınanmamıştır;',
              'nüks, kaçış tedavisi ve immünolojik remisyon (başlangıç titresi ≥ 175 RU/mL olan alt grup) tanımlayıcıdır.'], 11.6, 16, fill=INK2)
yeni('s09_majesty', 'x09_44', 'Güncelleme · Ağustos 2026 · Şekil', 'MAJESTY — Beş Sonlanım Tek Bakışta', F,
     '<b>Okuma:</b> Obinutuzumab kolunda remisyon ve immünolojik remisyon daha sık, nüks ve kaçış tedavisi gereksinimi daha seyrektir. '
     'Takrolimus kolundaki yüksek nüks oranı, kalsinörin inhibitörü kesildikten sonra bilinen sorunun yansımasıdır. Sayılar slayttaki tablodan alınmıştır.',
     'Şekil: MAJESTY çalışmasının yüz dördüncü hafta sonuçları. Tam remisyon obinutuzumab kolunda yüzde otuz yedi, takrolimus kolunda yüzde altıdır. '
     'Nüks yüzde on iki ile yüzde elli sekiz, kaçış tedavisi gereksinimi yüzde yirmi sekiz ile yüzde altmış birdir.', ozgun=' <i>Özgün çizim.</i>')


# ============================================================================================== J · Ehrenreich-Churg evreleri (slayt içi, x09_10)
from sekil_glom import bariyer, if_patern, elips, DEP as _DEP, GBM as _GBM, GBM_K as _GBMK, BOW as _BW
F = Fig('evr', 252, 'Membranöz nefropatide Ehrenreich-Churg elektron mikroskopi evreleri I–IV', mh=258)
EVR = [('Evre I', 'Subepitelyal birikimler; GBM', 'normal · ışıkta normal'), ('Evre II', 'Birikimler arasında GBM', '“dikenleri” · gümüşte spike'),
       ('Evre III', 'Birikimler yeni GBM ile', 'sarılır, GBM’nin içine alınır'), ('Evre IV', 'Kalın GBM; birikimler', 'lusenleşir (“krater”)')]
for i, (ad, l1, l2) in enumerate(EVR):
    x = 8 + i * 284; w = 268
    gk = (1, 1, 1.75, 2.0)[i]
    B = bariyer(F, x, 4, w, 166, efase=(0, 1), gbm_k=gk)
    xs = [.1, .26, .42, .58, .74, .9]
    if i <= 1:
        for f_ in xs: elips(F, x + f_ * w, B['yg'] + 4.5, 9, 6, 0, _DEP, '#fff', .8)
    if i == 1:
        for j in range(len(xs) - 1):
            xm = x + (xs[j] + xs[j + 1]) / 2 * w; F.r(xm - 2.4, B['yg'] - 1, 4.8, 12, _GBM, _GBMK, .9, 1.5)
    if i == 2:
        for f_ in xs: elips(F, x + f_ * w, B['yg'] - 8, 9, 6, 0, '#4d5864', '#2b3440', .8)
        for f_ in xs: F.r(x + f_ * w - 11, B['yg'] - 2, 22, 5, _GBM, None, rx=2)
    if i == 3:
        for f_ in xs: elips(F, x + f_ * w, B['yg'] - 12, 9, 6.5, 0, '#f8fbfc', '#7d8e99', 1)
    F.t(x + w / 2, 192, ad, 13.5, 800, BRANDD, 'middle'); F.t(x + w / 2, 210, l1, 11.6, None, INK, 'middle'); F.t(x + w / 2, 225, l2, 11.6, None, INK, 'middle')
    if i < 3: F.ok(x + w + 2, 84, x + w + 14, 84, INK2, 2)
F.t(8, 246, 'Her şeritte üstte kapiller lümen ve pencereli endotel, ortada GBM, altta silinmiş ayaksı çıkıntılar ve podosit. Evre süreyi gösterir, sonucu öngörmez.', 11.2, None, MUT)
ic('s09_evre', 'x09_10', F)

# ============================================================================================== K · immünfloresan imzası (slayt içi, x09_11)
F = Fig('mif', 166, 'Membranöz nefropatide immünfloresan imzası: ince granüler IgG, PLA2R ve C3; C1q yok', mh=146)
IFS = [('IgG', 'ince', ['tüm kapiller duvarlarda', 'ince granüler']), ('PLA2R', 'ince', ['IgG ile aynı yerde']), ('C3', 'ince', ['aktif hastalıkta pozitif']), ('C1q', 'negatif', ['yok ya da zayıf', '(C4d pozitif olabilir)'])]
for i, (ad, t, alt) in enumerate(IFS):
    cx = 80 + i * 175
    if_patern(F, cx, 56, 46, t, renk='#79f08b' if t != 'negatif' else '#79f08b', baslik=ad, alt=alt, fs=11.5)
F.r(748, 8, 384, 150, '#fff', LINE, 1.4, 10)
F.t(762, 30, 'İnce granüler kapiller duvar paterni', 12.6, 800, BRANDD)
F.tl(762, 50, ['Birikimler subepitelyal olduğu için boyanma', 'ilmeklerin dış yüzünü boncuk dizisi gibi izler.', 'Kappa ve lambda eşittir; monoklonal IgG’ye', 'bağlı MN çok seyrektir. C1q yokluğunda C4d', 'pozitifliği primer MN için tipiktir.'], 11.6, 16.5, fill=INK)
ic('s09_mif', 'x09_11', F)
