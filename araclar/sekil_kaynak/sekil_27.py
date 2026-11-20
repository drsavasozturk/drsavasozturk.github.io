#!/usr/bin/env python3
"""Ders 27 · Obstrüktif nefropati — şekil tanımları (20 Kasım 2026)."""
import random
from sekil_ortak import *
from sekil_glom import etk

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
F = Fig('us', 416, 'Hidronefrozun ultrasonda derecelendirilmesi ve ultrasonun yalancı negatif ve yalancı pozitif tuzakları', w=1080)
serit(F, 6, 6, 1068, 'Hidronefroz dereceleri (SFU 0–4)', BRANDD); zemin(F, 6, 42, 1068, 200)
G = [((4, 6), (2.5, 2), 2.5), ((9, 13), (2.5, 2), 2.5), ((12, 16), None, None), ((15, 20), (8, 7), 8), ((17, 23), (11, 10), 11)]
YAZ = [('0 · Normal', 'sistem genişlememiş'), ('1 · Yalnız pelvis', 'kaliksler normal'), ('2 · Pelvis + bazı kaliksler', 'diğerleri normal'),
       ('3 · Tüm kaliksler', 'parankim normal'), ('4 · Parankim incelmesi', 'kaliksler de genişlemiş')]
for i in range(5):
    cx, cy, k = 118 + i * 212, 128, 1.36
    (pw, ph), cal, kr = G[i]
    g = f'<g transform="translate({cx},{cy}) scale({k})"><path d="{BOB}" fill="#c9736b" stroke="#8e4a44" stroke-width="2"/>'
    uc = ((-8, -26), (-14, 0), (-8, 26)) if i < 4 else ((-15, -27), (-21, 0), (-15, 27))
    for j, (tx, ty) in enumerate(uc):
        if i == 2: r_, w_ = ((6, 5), (6, 5), (3, 2.4))[j]
        else: r_, w_ = kr, cal[1]
        g += f'<line x1="6" y1="0" x2="{tx}" y2="{ty}" stroke="{IDRAR}" stroke-width="{w_}" stroke-linecap="round"/><circle cx="{tx}" cy="{ty}" r="{r_}" fill="{IDRAR}"/>'
    g += f'<ellipse cx="8" cy="0" rx="{pw}" ry="{ph}" fill="{IDRAR}"/></g>'
    F.a(g)
    F.t(cx - 10, 212, YAZ[i][0], 12.6, 800, INK, 'middle'); F.t(cx - 10, 229, YAZ[i][1], 11.6, None, INK2, 'middle')
for j, (x, bas, c, sat) in enumerate(((6, 'Yalancı NEGATİF · hidronefroz yok, obstrüksiyon var', RED,
                                       ['İlk saatler: sistem henüz genişlemedi', 'Hipovolemi, düşük idrar yapımı', 'RPF ya da malign sarma: üreter genişleyemez',
                                        'Staghorn taş sistemi doldurur', 'Forniks rüptürü: dekomprese sistem']),
                                      (546, 'Yalancı POZİTİF · hidronefroz var, obstrüksiyon yok', GOLD,
                                       ['Ekstrarenal pelvis · parapelvik kist', 'Gebelik (sağda belirgin) · vezikoüreteral reflü', 'Yüksek idrar akımı · dolu mesane',
                                        'Önceden açılmış obstrüksiyonun kalıcı genişlemesi']))):
    F.r(x, 252, 528, 158, TINT[c], c, 1.6, 10); F.t(x + 16, 278, bas, 13.2, 800, c); F.tl(x + 16, 304, ['• ' + t for t in sat], 12.2, 22, fill=INK)
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
    for sx in (-1, 1): F.el(cx + sx * 92, 262, 34, 24, '#d9a59a', '#a2564e', 1.4)
    if rpf:
        F.yol(f'M{cx - 82},{232} C{cx - 96},{166} {cx - 40},{130} {cx},{136} C{cx + 46},{130} {cx + 98},{166} {cx + 84},{232} Z', '#9c9282', 1.4, '#d7cfc2')
        ao, ivc, ur = (cx + 22, 212), (cx - 34, 210), ((cx - 66, 222), (cx + 70, 222))
    else:
        for (u, v, r) in ((-6, 222, 22), (28, 222, 20), (-44, 206, 18), (58, 206, 18), (8, 196, 16), (-30, 182, 15), (50, 180, 16)):
            F.el(cx + u, v, r, r * .86, '#c6d4e3', '#6f87a3', 1.4)
        ao, ivc, ur = (cx + 18, 150), (cx - 46, 160), ((cx - 112, 224), (cx + 114, 224))
    F.r(cx - 46, 238, 92, 72, '#efe6d2', '#a8956b', 1.8, 22)
    F.yol(f'M{cx - 34},306 L{cx - 14},334 Q{cx},346 {cx + 14},334 L{cx + 34},306', '#a8956b', 7); F.yol(f'M{cx - 34},306 L{cx - 14},334 Q{cx},346 {cx + 14},334 L{cx + 34},306', '#efe6d2', 4)
    F.el(*ao, 20, 20, '#d9534f', '#8e2b26', 1.8); F.el(*ivc, 19, 12, '#6e8fc6', '#3f5f94', 1.6)
    for u in ur: F.el(*u, 6, 6, IDRAR, '#a07a00', 1.4)
    return cx, ao, ivc, ur


cx, ao, ivc, ur = kesit(F, 0, True)
F.t(270, 34, 'Retroperitoneal fibroz', 14, 800, PUR, 'middle')
etk(F, (ao[0] + 14, ao[1] + 18), 336, 296, ['Aort vertebraya yapışık', 'öne itilmemiş'], fs=11.8)
etk(F, (cx + 40, 150), 360, 92, ['Fibröz manto önü ve yanları', 'sarar, arkaya girmez'], fs=11.8)
etk(F, ur[0], 52, 300, ['Üreterler mediale', 'çekilir, sabitlenir'], fs=11.8)
cx, ao, ivc, ur = kesit(F, 540, False)
F.t(810, 34, 'Lenfoma · malign kitle', 14, 800, RED, 'middle')
etk(F, (ao[0] + 14, ao[1] - 14), 870, 92, ['Aort öne itilmiş', '(“yüzen aort”)'], fs=11.8)
etk(F, (cx + 28, 222), 866, 300, ['Kitle aortun arkasına girer;', 'büyük lenf nodları'], fs=11.8)
etk(F, ur[1], 940, 170, ['Üreterler', 'laterale itilir'], fs=11.8)
D.yeni('s27_rpf', 'x27_28', 'Retroperitoneal Fibroz · Şekil', 'RPF ve Lenfoma — Aort Nerede?', F,
       '<b>Okuma:</b> Retroperitoneal fibrozda periaortik doku aortu önden ve yanlardan sarar, arkaya girmez; aort vertebraya yapışık kalır ve üreterler mediale çekilir. '
       'Lenfomada kitle aortun arkasına da uzanır, aortu öne iter; büyük lenf nodları ve laterale itilmiş üreterler malignite lehinedir.',
       'Şekil: iki aksiyel kesit, ön yukarıda, hastanın sağı solda. Solda retroperitoneal fibroz: vertebra, iki psoas kası, aort ve vena kava önden ve yanlardan bir fibröz manto ile sarılmış; aort vertebraya yapışık, üreterler mantonun içinde mediale çekilmiş. '
       'Sağda lenfoma: aortun arkasına giren büyük lenf nodları aortu vertebradan uzaklaştırıp öne itmiş; üreterler laterale itilmiş.')

# ============================================================================================== 4 · nefrostomi ve retrograd stent
F = Fig('dren', 446, 'Obstrüksiyonda drenaj: perkütan nefrostomi ve retrograd double-J stent; hangi durumda hangisi', w=1080)


def sistem(F, ox):
    cx, cy, k = ox + 112, 126, 1.7
    ux, uy = bobrek(F, cx, cy, k, pelvis=2)
    bx, by = ox + 250, 318
    ureter(F, ux, uy, bx, by - 24, gen=6)
    mesane(F, bx, by + 6, 40, 28, uretra=14)
    P = uyol((ux, uy), (bx, by - 24))
    up = [bez(*P, t / 40) for t in range(0, 20)]; d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in up)
    F.yol(d, '#a07a00', 11.6); F.yol(d, IDRAR, 9)
    st = bez(*P, .5); tas(F, st[0], st[1], 7.5, 5)
    return cx, cy, k, P, (bx, by + 6), st


for j, ox in enumerate((0, 540)):
    F.r(ox + 6, 6, 528, 380, '#fbf8f2', LINE, 1.2, 12)
cx, cy, k, P, bl, st = sistem(F, 0)
pv = (cx + 8 * k, cy); lc = (cx - 8 * k, cy + 26 * k)
F.yol(f'M{pv[0]:.0f},{pv[1]:.0f} L{lc[0]:.0f},{lc[1]:.0f} L{cx - 64},{cy + 72} C{cx - 92},{cy + 100} {cx - 92},{cy + 150} {cx - 80},{cy + 190}', '#2b6cb0', 3)
F.el(pv[0] + 2, pv[1] - 4, 8, 8, 'none', '#2b6cb0', 3)
F.ln(cx - 70, cy + 46, cx - 50, cy + 84, '#8e7e6b', 2, '4 3'); F.t(cx - 100, cy + 46, 'cilt', 11, 700, '#8e7e6b')
F.r(cx - 104, cy + 190, 46, 58, '#fff6cc', '#a07a00', 1.6, 8); F.t(cx - 81, cy + 224, 'torba', 10.8, 700, '#7a5a00', 'middle')
F.t(30, 34, 'Perkütan nefrostomi', 14, 800, BRANDD)
F.tl(300, 64, ['Tercih edilen durumlar', ], 12.6, 17, fill=BRANDD, fw=800)
madde(F, 300, 88, [['Ürosepsis, instabilite:', 'lokal anestezi yeterli'], ['Malign bası, mesane', 'invazyonu'], ['Ayrık fonksiyon ve', 'kurtarılabilirlik ölçümü']])
F.tl(300, 216, ['Dikkat: perirenal kanama;', 'koagülopatide stent.'], 12, 17, fill=RED, fw=700)
cx, cy, k, P, bl, st = sistem(F, 540)
pv = (cx + 8 * k, cy)
pts = [bez(*P, t / 20) for t in range(21)]
F.yol(f'M{pv[0]:.0f},{pv[1]:.0f} ' + ' '.join(f'L{x + 2.5:.1f},{y:.1f}' for x, y in pts) + f' L{bl[0] - 2:.0f},{bl[1] - 4:.0f}', '#2b6cb0', 2.6)
F.el(pv[0] - 2, pv[1] - 6, 8, 8, 'none', '#2b6cb0', 2.6); F.el(bl[0] - 12, bl[1] - 4, 9, 9, 'none', '#2b6cb0', 2.6)
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
# sol panel
bx = 150
u1 = bobrek(F, 70, 110, 1.45, pelvis=0)
u2 = bobrek(F, 236, 110, 1.25, pelvis=3, ayna=True)
ureter(F, *u1, bx - 10, 228, gen=4); ureter(F, *u2, bx + 10, 228, gen=5)
st = bez(*uyol(u2, (bx + 10, 228)), .55); tas(F, st[0], st[1], 6.5, 3)
mesane(F, bx, 250, 30, 22, uretra=12)
etk(F, (52, 172), 24, 304, ['Sağlam böbrek', 'hiperfiltrasyonla telafi'], fs=12)
etk(F, (236 - 8 * 1.25, 110), 300, 100, ['Obstrükte böbrek', 'sessizce fonksiyon kaybeder'], fs=12)
F.tl(300, 196, ['• Kreatinin normal kalır', '• Tanı yalnız görüntülemeyle', '• Drenaj sonrası poliüri beklenmez', '• Karar: renografide ayrık fonksiyon'], 12, 19, fill=INK)
# sağ panel
bx = 690
u1 = bobrek(F, 610, 104, 1.25, pelvis=3); u2 = bobrek(F, 770, 104, 1.25, pelvis=3, ayna=True)
ureter(F, *u1, bx - 12, 222, gen=7); ureter(F, *u2, bx + 12, 222, gen=7)
mesane(F, bx, 254, 44, 34, duvar=6, uretra=14)
F.el(bx, 298, 22, 12, '#c9a0c0', '#7d4f73', 1.6); F.t(bx - 30, 330, 'BPH: mesane çıkım obstrüksiyonu', 11.4, 700, '#7d4f73')
etk(F, (bx + 40, 250), 846, 92, ['Mesane dolu, duvar kalın;', 'iki sistem genişlemiş'], fs=12)
madde(F, 846, 160, ['AKİ, oligüri ya da anüri', 'Hiperkalemi, asidoz, ödem', 'Acil drenaj, sonra neden', ['Drenaj sonrası poliüri', '(POD) beklenir']], lh=19)
D.yeni('s27_tek', 'x27_13', 'Ayrım · Şekil', 'Tek Taraflı ve Çift Taraflı — Neden Farklı?', F,
       '<b>Okuma:</b> Karşı böbrek sağlamsa hiperfiltrasyonla telafi eder, kreatinin normal kalır ve obstrükte böbrek sessizce fonksiyon kaybeder; tanı görüntülemeyle konur. '
       'Mesane çıkım obstrüksiyonu gibi çift taraflı tıkanmada ya da tek böbrekte akut böbrek hasarı gelişir; acil drenaj gerekir ve sonrasında poliüri beklenir.',
       'Şekil: solda tek taraflı obstrüksiyon: bir üreterde taş ve o tarafta genişlemiş pelvis; karşı böbrek daha büyük çizilmiş ve hiperfiltrasyonla telafi ediyor; kreatinin normal. '
       'Sağda benign prostat büyümesine bağlı mesane çıkım obstrüksiyonu: mesane dolu ve duvarı kalın, iki üreter ve iki böbrek toplayıcı sistemi genişlemiş; akut böbrek hasarı ve acil drenaj.')
