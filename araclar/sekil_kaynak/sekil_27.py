#!/usr/bin/env python3
"""Ders 27 · Obstrüktif nefropati — şekil tanımları (20 Kasım 2026)."""
import random
from sekil_ortak import *
from sekil_glom import etk
import sekil_anat as A

D = Ders('27')
TAS, TAS_K = '#c9a36b', '#7a5a2a'
BOB = 'M-6,-50 C-36,-50 -38,50 -6,50 C16,50 22,28 12,12 C6,4 6,-4 12,-12 C22,-28 16,-50 -6,-50 Z'


def tas(F, x, y, r, tohum=1):
    rg = random.Random(tohum); n = 9; pts = []
    for i in range(n):
        a = 2 * math.pi * i / n; rr = r * rg.uniform(.72, 1.08)
        pts.append(f'{x + rr * math.cos(a):.1f},{y + rr * math.sin(a):.1f}')
    F.a(f'<polygon points="{" ".join(pts)}" fill="{TAS}" stroke="{TAS_K}" stroke-width="1.4" stroke-linejoin="round"/>')


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def madde(F, x, y, items, fs=12, lh=18, fill=INK):
    for it in items:
        it = it if isinstance(it, list) else [it]
        F.t(x, y, '• ' + it[0], fs, None, fill); y += lh
        for d in it[1:]: F.t(x + 11, y, d, fs, None, fill); y += lh
    return y


def uyol(p, q):
    """ureter() ile aynı eğri: p'den q'ya kübik Bezier kontrol noktaları."""
    return (p, (p[0], (p[1] + q[1]) / 2), (q[0], (p[1] + q[1]) / 2), q)


# ============================================================================================== 1 · üç hemodinamik faz
F = Fig('faz', 372, 'Tek taraflı tam üreter obstrüksiyonunda renal kan akımı ve intratübüler basıncın zamanla değişimi: üç faz', w=1080)
X0, X1 = 92, 700
def TX(t): return X0 + math.sqrt(t / 24) * (X1 - X0)
B = [(0, 2, '#fdeaea', 'Faz 1', RED), (2, 5, '#fff6e0', 'Faz 2', GOLD), (5, 24, '#f1ecf8', 'Faz 3', PUR)]
for a, b, c, ad, cc in B:
    F.r(TX(a), 40, TX(b) - TX(a), 262, c, None, rx=0); F.t((TX(a) + TX(b)) / 2, 58, ad, 12.6, 800, cc, 'middle')
def egri(P, ust, alt, vmax, c, ad, alt_et=False):
    def Y(v): return alt - v / vmax * (alt - ust)
    F.ln(X0, alt, X1, alt, INK2, 1.6); F.ln(X0, ust - 6, X0, alt, INK2, 1.6)
    yb = Y(P[0][1]); F.ln(X0, yb, X1, yb, MUT, 1.2, '5 4'); F.t(X1 - 4, yb + (14 if alt_et else -6), 'bazal', 11, None, MUT, 'end')
    F.yol('M' + ' L'.join(f'{TX(t):.1f},{Y(v):.1f}' for t, v in P), c, 3.2)
    F.t(X0 - 10, (ust + alt) / 2 - 6, ad[0], 12.4, 800, c, 'end'); F.t(X0 - 10, (ust + alt) / 2 + 10, ad[1], 11.4, None, c, 'end')
RBF = [(0, 100), (.4, 118), (1, 134), (1.5, 140), (2, 132), (3, 118), (4, 106), (5, 95), (8, 68), (12, 52), (18, 42), (24, 36)]
PR = [(0, 12), (.4, 32), (1, 44), (2, 50), (3, 50.5), (4, 49.5), (5, 46), (8, 35), (12, 26), (18, 19), (24, 16)]
egri(RBF, 78, 182, 160, BRAND, ('RBF', 'akım'))
egri(PR, 206, 300, 60, RED, ('Basınç', 'intratübüler'), True)
for t in (0, 1, 2, 5, 12, 24):
    F.ln(TX(t), 300, TX(t), 305, INK2, 1.4); F.t(TX(t), 322, str(t), 11.4, None, MUT, 'middle')
F.t((X0 + X1) / 2, 348, 'Obstrüksiyondan sonra geçen süre (saat; eksen sıkıştırılmış)', 12, 700, INK2, 'middle')
M = [(730, 40, 'Faz 1 · 0–2 saat', RED, ['RBF ↑ · basınç ↑', 'PGE₂, PGI₂, NO: afferent dilatasyon', 'Ağrı bu dönemdeki basınç artışından']),
     (730, 140, 'Faz 2 · 2–5 saat', GOLD, ['RBF ↓ · basınç yüksek kalır', 'Efferent (postglomerüler)', 'vazokonstriksiyon']),
     (730, 240, 'Faz 3 · > 5 saat', PUR, ['RBF ↓↓ · basınç bazale doğru düşer', 'Preglomerüler: TxA₂, Ang II, ET-1', 'Basıncın düşmesi iyileşme değil'])]
for x, y, bas, c, sat in M:
    F.r(x, y, 344, 92, TINT[c], c, 1.5, 10); F.t(x + 14, y + 22, bas, 13.2, 800, c); F.tl(x + 14, y + 43, sat, 11.8, 16, fill=INK)
F.t(730, 354, 'Eğriler şematik; deneysel modele dayanır.', 11, None, MUT)
D.yeni('s27_faz', 'x27_11', 'Patofizyoloji · Şekil', 'Üç Faz — Akım ve Basınç Zaman İçinde', F,
       '<b>Okuma:</b> İlk iki saatte prostaglandin ve NO aracılı afferent dilatasyonla akım ve basınç birlikte artar. '
       'İki ile beş saat arasında akım düşerken efferent vazokonstriksiyon basıncı yüksek tutar. Beş saatten sonra preglomerüler vazokonstriksiyon akımı daha da azaltır; basıncın normale dönmesi obstrüksiyonun çözüldüğü anlamına gelmez.',
       'Şekil: yatay eksende obstrüksiyondan sonra geçen saatler; üstte renal kan akımı, altta intratübüler basınç, kesikli çizgiler bazal değer. '
       'Birinci fazda, ilk iki saatte, ikisi birlikte yükselir. İkinci fazda, iki ile beş saat arasında, efferent vazokonstriksiyonla akım düşmeye başlar, basınç yüksek kalır. '
       'Üçüncü fazda, beş saatten sonra, tromboksan, anjiyotensin iki ve endotelin aracılı preglomerüler vazokonstriksiyonla akım bazalın altına iner, basınç ise bazale doğru düşer.')

# ============================================================================================== 2 · hidronefroz dereceleri ve ultrasonun iki tuzağı
F = Fig('us', 432, 'Hidronefrozun ultrasonda derecelendirilmesi ve ultrasonun yalancı negatif ve yalancı pozitif tuzakları', w=1080)
serit(F, 6, 6, 1068, 'Hidronefroz dereceleri (SFU 0–4)', BRANDD); zemin(F, 6, 42, 1068, 216)
DER = ((0, 0, 0, 0), (2, 0, 0, 0), (3, (0, 0, 0, 0, 2, 2, 2, 2), 3, 0), (3, 3, 3, 0), (4, 4, 4, 1))
YAZ = [('0 · Normal', 'sistem genişlememiş'), ('1 · Yalnız pelvis', 'kaliksler normal'), ('2 · Pelvis + bazı kaliksler', 'diğerleri normal'),
       ('3 · Tüm kaliksler', 'parankim normal'), ('4 · Parankim incelmesi', 'kaliksler de genişlemiş')]
for i in range(5):
    cx, cy, k = 118 + i * 212, 126, 1.34
    pel, kal, maj, ince = DER[i]
    F.a(f'<g data-etk="d{i}" data-c="{cx - 10},{cy}">')
    A.bobrek(F, cx, cy, k, pel=pel, kal=kal, maj=maj, ince=ince, damar=False)
    F.t(cx - 10, 214, YAZ[i][0], 12.6, 800, INK, 'middle'); F.t(cx - 10, 231, YAZ[i][1], 11.6, None, INK2, 'middle')
    F.a('</g>')
for j, (x, bas, c, sat) in enumerate(((6, 'Yalancı NEGATİF · hidronefroz yok, obstrüksiyon var', RED,
                                       ['İlk saatler: sistem henüz genişlemedi', 'Hipovolemi, düşük idrar yapımı', 'RPF ya da malign sarma: üreter genişleyemez',
                                        'Staghorn taş sistemi doldurur', 'Forniks rüptürü: dekomprese sistem']),
                                      (546, 'Yalancı POZİTİF · hidronefroz var, obstrüksiyon yok', GOLD,
                                       ['Ekstrarenal pelvis · parapelvik kist', 'Gebelik (sağda belirgin) · vezikoüreteral reflü', 'Yüksek idrar akımı · dolu mesane',
                                        'Önceden açılmış obstrüksiyonun kalıcı genişlemesi']))):
    F.r(x, 268, 528, 158, TINT[c], c, 1.6, 10); F.t(x + 16, 294, bas, 13.2, 800, c); F.tl(x + 16, 320, ['• ' + t for t in sat], 12.2, 22, fill=INK)
D.yeni('s27_us', 'x27_19', 'Tuzaklar · Şekil', 'Hidronefroz Dereceleri ve Ultrasonun İki Tuzağı', F,
       '<b>Okuma:</b> Derece 1’de yalnız pelvis, 2’de pelvis ile bazı kaliksler, 3’te tüm kaliksler genişler; 4’te buna parankim incelmesi eklenir. '
       'Hidronefroz obstrüksiyonla eş anlamlı değildir: erken dönemde, hipovolemide ve retroperitoneal sarmada obstrüksiyon genişleme yapmayabilir; reflü, gebelik ve yüksek akım genişleme yapar ama obstrüksiyon değildir.',
       'Şekil: üstte beş böbrek, sıfırdan dörde hidronefroz dereceleri: normal; yalnız pelvis genişlemiş; pelvis ve bazı kaliksler; tüm kaliksler, parankim normal; kaliksler genişlemiş ve parankim incelmiş. '
       'Altta iki kutu: solda hidronefroz olmadan obstrüksiyon nedenleri, sağda obstrüksiyon olmadan hidronefroz nedenleri.')

# ============================================================================================== 3 · RPF: aortu sarar, öne itmez
F = Fig('rpf', 372, 'Aksiyel kesitte retroperitoneal fibroz ile lenfomanın aort ve üreterlerle ilişkisi', w=1080)


def kesit(F, ox, rpf):
    F.r(ox + 6, 6, 528, 360, '#fbf8f2', LINE, 1.2, 12)
    F.t(ox + 30, 34, 'ön', 11.4, 700, MUT); F.t(ox + 30, 350, 'arka', 11.4, 700, MUT)
    F.t(ox + 30, 196, 'Sağ', 11.4, 700, MUT); F.t(ox + 510, 196, 'Sol', 11.4, 700, MUT, 'end')
    cx = ox + 270
    F.a(f'<path d="{A.yuvarla([(cx - 170, 250), (cx - 150, 160), (cx - 80, 118), (cx, 108), (cx + 80, 118), (cx + 150, 160), (cx + 170, 250), (cx + 120, 300), (cx, 292), (cx - 120, 300)])}" fill="#fbf0d2" opacity=".85"/>')   # retroperitoneal yağ
    for sx in (-1, 1):   # psoas
        A.kas(F, [(cx + sx * x, y) for x, y in ((48, 240), (64, 230), (86, 234), (98, 252), (92, 274), (74, 284), (56, 276), (46, 258))])
        A.kas(F, [(cx + sx * x, y) for x, y in ((12, 322), (30, 312), (52, 318), (58, 336), (44, 350), (20, 350), (11, 338))])   # paraspinal
    if rpf:
        A.fibroz(F, [(cx - 82, 240), (cx - 98, 204), (cx - 78, 164), (cx - 34, 144), (cx + 14, 140), (cx + 58, 150), (cx + 92, 176), (cx + 100, 214),
                     (cx + 86, 242), (cx + 56, 238), (cx + 30, 232), (cx, 230), (cx - 30, 232), (cx - 58, 240)])
        ao, ivc, ur = (cx + 22, 210), (cx - 32, 218), ((cx - 54, 226), (cx + 58, 226))
    else:
        ao, ivc, ur = (cx + 18, 150), (cx - 44, 167), ((cx - 112, 226), (cx + 116, 226))
    A.vertebra(F, cx, 264, .9)
    if not rpf:
        for i, (u, v, rx, ry) in enumerate(((-4, 212, 24, 18), (32, 214, 22, 17), (-40, 200, 19, 15), (64, 198, 18, 15), (10, 184, 18, 14),
                                             (-24, 178, 15, 13), (50, 174, 16, 13), (-76, 216, 14, 12), (92, 214, 14, 12), (20, 174, 17, 12))):
            A.lenf(F, cx + u, v, rx, ry, (i * 37) % 60 - 30, i + 2)
    A.arter_kesit(F, *ao, 17, kalsifik=False); A.ven_kesit(F, *ivc, 18, 11)
    for u in ur: A.ureter_kesit(F, *u, 5.5)
    F.t(ivc[0], ivc[1] + (-16 if rpf else -15), 'VKİ', 10.5, 800, '#2f4f86', 'middle')
    F.a(f'<text x="{cx - 73}" y="{266}" font-size="10.5" font-weight="800" fill="#fff" text-anchor="middle" stroke="#7a3530" stroke-width="2.4" paint-order="stroke">psoas</text>'); F.t(cx, 252, 'vertebra', 10.5, 700, '#8a7350', 'middle')
    return cx, ao, ivc, ur


cx, ao, ivc, ur = kesit(F, 0, True)
F.t(270, 34, 'Retroperitoneal fibroz', 14, 800, PUR, 'middle')
A.cagri(F, (ao[0] + 12, ao[1] + 16), 344, 300, ['Aort vertebraya yapışık', 'öne itilmemiş'], fs=11.8)
A.cagri(F, (cx + 46, 158), 368, 92, ['Fibröz manto önü ve yanları', 'sarar, arkaya girmez'], fs=11.8)
A.cagri(F, (ur[0][0] - 3, ur[0][1] + 5), 60, 306, ['Üreterler mediale', 'çekilir, sabitlenir'], fs=11.8)
cx, ao, ivc, ur = kesit(F, 540, False)
F.t(810, 34, 'Lenfoma · malign kitle', 14, 800, RED, 'middle')
A.cagri(F, (ao[0] + 12, ao[1] - 12), 878, 92, ['Aort öne itilmiş', '(“yüzen aort”)'], fs=11.8)
A.cagri(F, (cx + 30, 222), 874, 302, ['Kitle aortun arkasına girer;', 'büyük lenf nodları'], fs=11.8)
A.cagri(F, (ur[1][0] + 4, ur[1][1] - 5), 948, 170, ['Üreterler', 'laterale itilir'], fs=11.8)
D.yeni('s27_rpf', 'x27_28', 'Retroperitoneal Fibroz · Şekil', 'RPF ve Lenfoma — Aort Nerede?', F,
       '<b>Okuma:</b> Retroperitoneal fibrozda periaortik doku aortu önden ve yanlardan sarar, arkaya girmez; aort vertebraya yapışık kalır ve üreterler mediale çekilir. '
       'Lenfomada kitle aortun arkasına da uzanır, aortu öne iter; büyük lenf nodları ve laterale itilmiş üreterler malignite lehinedir.',
       'Şekil: iki aksiyel kesit, ön yukarıda, hastanın sağı solda. Solda retroperitoneal fibroz: vertebra, iki psoas kası, aort ve vena kava önden ve yanlardan bir fibröz manto ile sarılmış; aort vertebraya yapışık, üreterler mantonun içinde mediale çekilmiş. '
       'Sağda lenfoma: aortun arkasına giren büyük lenf nodları aortu vertebradan uzaklaştırıp öne itmiş; üreterler laterale itilmiş.')

# ============================================================================================== 4 · nefrostomi ve retrograd stent
F = Fig('dren', 446, 'Obstrüksiyonda drenaj: perkütan nefrostomi ve retrograd double-J stent; hangi durumda hangisi', w=1080)


def sistem(F, ox):
    cx, cy, k = ox + 110, 146, 1.62
    BX, BY = ox + 252, 334
    E = A.giris(BX, BY, 42, 30, -1)
    ux, uy = A.cikis(cx, cy, k, pel=2)
    YOL = A.egri(((ux, uy), (ux + 8, uy + 74), (E[0] - 34, E[1] - 96), E), 40)
    st = YOL[19]
    A.ureter(F, YOL[19:], 5.4)
    G = A.bobrek(F, cx, cy, k, pel=2, kal=2, maj=2, ureter=YOL[:20], uw=10.4, damar=False)
    M = A.mesane(F, BX, BY, 42, 30, taraflar=(-1,), uretra=14)
    A.tas(F, st[0] - 3, st[1] + 2, 7.5, 5)
    F.a(f'<path data-etk="durgun" d="{A.yol_d([G["pel"]] + YOL[:18])}" fill="none" stroke="none"/>')
    for i in (1, 3, 5, 6):
        F.a(f'<path data-etk="kaliks" d="{A.yol_d([G["kal"][i], G["maj"][0 if i > 4 else (1 if i > 2 else 2)], G["pel"]])}" fill="none" stroke="none"/>')
    return G, M, YOL, st


for j, ox in enumerate((0, 540)):
    F.r(ox + 6, 6, 528, 380, '#fbf8f2', LINE, 1.2, 12)
# ---- sol: perkütan nefrostomi (alt kalikse papilla ekseninden giriş, pelviste kıvrık uç)
G, M, YOL, st = sistem(F, 0)
PC = G['pel']; lk = G['kal'][1]
dx, dy = lk[0] - PC[0], lk[1] - PC[1]; Ln = math.hypot(dx, dy); dx, dy = dx / Ln, dy / Ln
S = (lk[0] + dx * 64, lk[1] + dy * 64)                 # cilt geçişi, kaliks ekseni üzerinde
nx, ny = -dy, dx
F.yol(f'M{S[0] - nx * 26:.0f},{S[1] - ny * 26:.0f} Q{S[0] + dx * 6:.0f},{S[1] + dy * 6:.0f} {S[0] + nx * 30:.0f},{S[1] + ny * 30:.0f}', '#b49a7c', 2.2, dash='5 4')
F.t(S[0] + nx * 30 - 2, S[1] + ny * 30 - 4, 'cilt', 11, 700, '#8e7e6b', 'end')
PG = A.pigtail(PC[0] + 1, PC[1] - 1, 8.5, 150, .82, 1)
NEF = A.egri(((32, 318), (31, 290), (S[0] + dx * 20, S[1] + dy * 20), S), 14) + A.egri((S, (S[0] - dx * 20, S[1] - dy * 20), (lk[0] + dx * 18, lk[1] + dy * 18), lk), 10)[1:] + \
      A.egri((lk, (lk[0] - dx * 10, lk[1] - dy * 10), (PG[0][0] - 6, PG[0][1] + 8), PG[0]), 8)[1:] + PG[1:]
A.kateter(F, NEF, 3.2, delik=0)
for q in PG[6::9]: F.el(q[0], q[1], 1, 1, '#0d2f52')   # yan delikler
F.r(10, 318, 46, 58, '#fff6cc', '#a07a00', 1.6, 8); F.r(13, 346, 40, 27, '#f4d36b', None, rx=5); F.t(33, 340, 'torba', 10.8, 700, '#7a5a00', 'middle')
F.a(f'<path data-etk="akis" d="{A.yol_d(PG[::-1] + NEF[::-1][len(PG):] + [(33, 352)])}" fill="none" stroke="none"/>')
F.t(30, 34, 'Perkütan nefrostomi', 14, 800, BRANDD)
F.tl(300, 64, ['Tercih edilen durumlar', ], 12.6, 17, fill=BRANDD, fw=800)
madde(F, 300, 88, [['Ürosepsis, instabilite:', 'lokal anestezi yeterli'], ['Malign bası, mesane', 'invazyonu'], ['Ayrık fonksiyon ve', 'kurtarılabilirlik ölçümü']])
F.tl(300, 216, ['Dikkat: perirenal kanama;', 'koagülopatide stent.'], 12, 17, fill=RED, fw=700)
# ---- sağ: retrograd double-J stent
G, M, YOL, st = sistem(F, 540)
PC = G['pel']; TN = M['tunel'][-1]; BX, BY = 540 + 252, 334
P1 = A.pigtail(PC[0], PC[1] - 2, 8.5, 90, .85, -1)[::-1]
ic = [(x + 4.2 * math.exp(-((i - 18) / 3.2) ** 2), y) for i, (x, y) in enumerate(YOL[1:], 1)]     # yalnız taşın yanından geçerken kayar
O = TN[-1]; PS = (O[0] + 8, O[1] - 14); CC = (PS[0] + 6.4, PS[1] + 6.4)
alt = TN[1:] + [(O[0] + 4, O[1] - 6), PS]
P2 = A.pigtail(CC[0], CC[1], 9, 225, .85, 1)
DJ = P1 + [(PC[0] + 2, PC[1] + 8)] + ic + alt + P2[1:]
A.kateter(F, DJ, 2.6)
F.a(f'<path data-etk="akis" d="{A.yol_d(P1[-1:] + [(PC[0] + 2, PC[1] + 8)] + ic + alt + [(CC[0] + 8, CC[1] - 4)])}" fill="none" stroke="none"/>')
F.t(570, 34, 'Retrograd double-J stent', 14, 800, PUR)
F.tl(840, 64, ['Tercih edilen durumlar'], 12.6, 17, fill=PUR, fw=800)
madde(F, 840, 88, [['Koagülopati ya da', 'antikoagülan'], ['Aynı seansta taş tedavisi', '(enfeksiyon yoksa)'], ['Uzun süreli konfor:', 'dış torba yok']])
F.tl(840, 212, ['Dikkat: stent sendromu;', 'malign basıda başarısızlık', 'sık; gebelikte 4–6 haftada', 'değişim.'], 12, 17, fill=RED, fw=700)
F.r(6, 394, 1068, 46, '#fff', INK2, 1.2, 10)
F.tl(22, 413, ['Enfekte obstrüktif taşta randomize karşılaştırma (Pearle 1998): ateş ve lökosit düzelmesi', ' iki yöntemde benzer; seçimi hastanın durumu, lojistik ve ekip deneyimi belirler.'], 12, 18, fill=INK)
D.yeni('s27_dren', 'x27_32', 'Kanıt + Karar · Şekil', 'Nefrostomi mi, Stent mi? — Çizimle', F,
       '<b>Okuma:</b> Nefrostomi kateteri ciltten alt kaliks yoluyla pelvise girer ve dışarıda torbaya açılır; double-J stent sistoskopiyle yerleştirilir, bir ucu pelviste, diğeri mesanede kıvrılır. '
       'Ürosepsis, instabilite, malign bası ve ayrık fonksiyon sorusu nefrostomiyi; koagülopati, aynı seansta taş tedavisi ve uzun dönem konfor stenti öne çıkarır.',
       'Şekil: iki üriner sistem çizimi; ikisinde de üreterin ortasında tıkayan bir taş ve genişlemiş pelvis var. Solda perkütan nefrostomi: kateter ciltten alt kaliks yoluyla pelvise girmiş, ucu kıvrık, dışarıda torbaya bağlı. '
       'Sağda double-J stent: bir kıvrık ucu pelviste, üreter boyunca taşın yanından geçip diğer kıvrık ucu mesanede. Her çizimin yanında tercih edildiği durumlar ve dikkat edilecekler; altta Pearle çalışmasının sonucu.')

# ============================================================================================== 5 · tek taraflı ve çift taraflı
F = Fig('tek', 352, 'Tek taraflı ve çift taraflı obstrüksiyonun böbrek fonksiyonuna etkisi', w=1080)
for j, (ox, bas, c) in enumerate(((0, 'Tek taraflı · karşı böbrek sağlam', BRAND), (540, 'Çift taraflı · ya da tek böbrek', RED))):
    F.r(ox + 6, 6, 528, 340, '#fbf8f2', LINE, 1.2, 12); F.t(ox + 30, 34, bas, 14, 800, c)
# sol panel: tek taraflı (hareketli: n = tıkanma öncesi, d = tıkanma sonrası; durağan görünüm d)
bx, by = 156, 262
Ms = dict(cx=bx, cy=by, rx=30, ry=22)
E1, E2 = A.giris(bx, by, 30, 22, -1), A.giris(bx, by, 30, 22, 1)
def uy(p, q, n=24): return A.egri((p, (p[0], (p[1] + q[1]) / 2 + 6), (q[0], (p[1] + q[1]) / 2 - 6), q), n)
c1, c2 = (80, 126), (240, 124)
o1 = A.cikis(*c1, 1.32, pel=0); U1 = uy(o1, E1)
A.bobrek(F, *c1, 1.32, pel=0, ureter=U1, uw=4.2, damar=False)
o2n, o2d = A.cikis(*c2, 1.16, True, pel=0), A.cikis(*c2, 1.16, True, pel=3)
U2n, U2d = uy(o2n, E2), uy(o2d, E2)
st = U2d[13]
F.a('<g data-etk="d">'); A.ureter(F, U2d[13:], 4)
A.bobrek(F, *c2, 1.16, ayna=True, pel=3, kal=3, maj=3, ureter=U2d[:14], uw=6.4, damar=False); F.a('</g>')
A.bobrek(F, *c2, 1.16, ayna=True, pel=0, ureter=U2n, uw=4, damar=False, grup='data-etk="n" style="opacity:0"')
A.mesane(F, bx, by, 30, 22, taraflar=(-1, 1), duvar=5, uretra=12)
A.tas(F, st[0], st[1] + 1, 6, 3, grup='data-etk="tas"')
F.a(f'<path data-etk="akis-s" d="{A.yol_d(U1)}" fill="none" stroke="none"/><path data-etk="akis-o" d="{A.yol_d(U2n)}" fill="none" stroke="none"/>'
    f'<path data-etk="durgun" d="{A.yol_d(U2d[:12])}" fill="none" stroke="none"/>')
A.cagri(F, (62, 178), 44, 306, ['Sağlam böbrek', 'hiperfiltrasyonla telafi'])
A.cagri(F, (240 - 8 * 1.16, 124), 306, 100, ['Obstrükte böbrek', 'sessizce fonksiyon kaybeder'], grup='data-etk="et"')
F.tl(300, 196, ['• Kreatinin normal kalır', '• Tanı yalnız görüntülemeyle', '• Drenaj sonrası poliüri beklenmez', '• Karar: renografide ayrık fonksiyon'], 12, 19, fill=INK)
# sağ panel: çift taraflı (BPH)
bx, by = 690, 254
c1, c2 = (614, 120), (766, 120)
for grp, pel, kal, w, (rx, ry, dv, pr, tr) in (('d', 3, 3, 8, (44, 34, 9, 2, True)), ('n', 0, 0, 4, (30, 22, 5, 1, False))):
    F.a(f'<g data-etk="{grp}"' + (' style="opacity:0"' if grp == 'n' else '') + '>')
    E1, E2 = A.giris(bx, by, rx, ry, -1), A.giris(bx, by, rx, ry, 1)
    UA = uy(A.cikis(*c1, 1.16, pel=pel), E1); UB = uy(A.cikis(*c2, 1.16, True, pel=pel), E2)
    A.bobrek(F, *c1, 1.16, pel=pel, kal=kal, maj=kal, ureter=UA, uw=w, damar=False)
    A.bobrek(F, *c2, 1.16, ayna=True, pel=pel, kal=kal, maj=kal, ureter=UB, uw=w, damar=False)
    M = A.mesane(F, bx, by, rx, ry, taraflar=(-1, 1), duvar=dv, uretra=14, prostat=pr, trabekul=tr)
    if grp == 'n': F.a(f'<path data-etk="akis-r" d="{A.yol_d(UA)}" fill="none" stroke="none"/><path data-etk="akis-r" d="{A.yol_d(UB)}" fill="none" stroke="none"/>'
                       f'<path data-etk="akis-u" d="M{bx},{by + ry - 4} L{bx},{by + ry + 26}" fill="none" stroke="none"/>')
    F.a('</g>')
F.t(bx - 30, 334, 'BPH: mesane çıkım obstrüksiyonu', 11.4, 700, '#7d4f73')
A.cagri(F, (bx + 40, by + 2), 852, 300, ['Mesane dolu, duvar kalın;', 'iki sistem genişlemiş'], grup='data-etk="et"')
madde(F, 846, 160, ['ABH, oligüri ya da anüri', 'Hiperkalemi, asidoz, ödem', 'Acil drenaj, sonra neden', ['Drenaj sonrası poliüri', '(POD) beklenir']], lh=19)
D.yeni('s27_tek', 'x27_13', 'Ayrım · Şekil', 'Tek Taraflı ve Çift Taraflı — Neden Farklı?', F,
       '<b>Okuma:</b> Karşı böbrek sağlamsa hiperfiltrasyonla telafi eder, kreatinin normal kalır ve obstrükte böbrek sessizce fonksiyon kaybeder; tanı görüntülemeyle konur. '
       'Mesane çıkım obstrüksiyonu gibi çift taraflı tıkanmada ya da tek böbrekte akut böbrek hasarı gelişir; acil drenaj gerekir ve sonrasında poliüri beklenir.',
       'Şekil: solda tek taraflı obstrüksiyon: bir üreterde taş ve o tarafta genişlemiş pelvis; karşı böbrek daha büyük çizilmiş ve hiperfiltrasyonla telafi ediyor; kreatinin normal. '
       'Sağda benign prostat büyümesine bağlı mesane çıkım obstrüksiyonu: mesane dolu ve duvarı kalın, iki üreter ve iki böbrek toplayıcı sistemi genişlemiş; akut böbrek hasarı ve acil drenaj.')
