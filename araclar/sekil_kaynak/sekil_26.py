#!/usr/bin/env python3
"""Ders 26 · Nefrolitiazis — şekil tanımları (20 Kasım 2026)."""
import random
from sekil_ortak import *
from sekil_glom import etk
import sekil_anat as A

D = Ders('26')
L = D.L
TAS, TAS_K = '#c9a36b', '#7a5a2a'


def tas(F, x, y, r, tohum=1, renk=TAS, kenar=TAS_K):
    rg = random.Random(tohum); n = 9
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n; rr = r * rg.uniform(.72, 1.08)
        pts.append(f'{x + rr * math.cos(a):.1f},{y + rr * math.sin(a):.1f}')
    F.a(f'<polygon points="{" ".join(pts)}" fill="{renk}" stroke="{kenar}" stroke-width="1.4" stroke-linejoin="round"/>')


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


# ============================================================================================== 1 · taşın yeri, ağrının yeri ve kolik mekanizması
F = Fig('yer', 452, 'Üriner sistemde taşın yerleri, üç fizyolojik darlık ve ağrının yayılımı; renal koliğin mekanizması', w=1080)
serit(F, 6, 6, 600, 'Taşın yeri ağrının yerini söyler', BRANDD); zemin(F, 6, 42, 600, 404)
# Resim: ChatGPT ile çizildi (yazısız, 1024 × 1536 px); konumlar resim pikselinden ölçüldü.
X0, Y0, SK = 34, 44, 266 / 1024
A.resim(F, 'an_yer', X0, Y0, 266, oran=1.5)
def P(px, py): return (X0 + px * SK, Y0 + py * SK)
UY = [P(x, y) for x, y in ((420, 452), (428, 470), (440, 500), (445, 530), (449, 560), (450, 590), (449, 620), (453, 650), (462, 680), (476, 710),
                           (495, 740), (519, 770), (540, 800), (557, 830), (567, 860), (571, 890), (570, 920), (565, 950), (558, 980), (549, 1010),
                           (544, 1040), (541, 1070), (541, 1100), (546, 1130), (552, 1160), (564, 1190), (583, 1220), (610, 1250), (640, 1272))]
F.t(40, 342, 'iliyak arter ve ven', 10.8, 700, '#8e2b26')
kal = A.tas(F, *P(312, 228), 6.5, 3)
p_upj, p_il, p_uvj = UY[0], P(568, 885), UY[-1]
AGRI = ((48, 170, 34, 'yan'), (96, 304, 40, 'alt karın · kasık'), (176, 420, 26, 'kasık · genital'))
TS = []
for n, ((x, y), tt, r_) in enumerate(((p_upj, 5, 6), (p_il, 7, 6), (p_uvj, 11, 5.5)), 1):
    ag = AGRI[n - 1]
    TS.append(A.tas(F, x, y, r_, tt, grup=f'data-etk="tas{n}" data-c="{x:.1f},{y:.1f}" data-agri="{ag[0]},{ag[1]},{ag[2]},{ag[3]}"'))
for n, (x, y) in enumerate((p_upj, p_il, p_uvj), 1): A.rozet(F, x - 20, y + (2 if n == 1 else (-10 if n == 2 else -12)), n)
A.cagri(F, kal, 330, 74, ['Kaliks taşı', 'tıkamazsa çoğu kez sessiz'], grup='data-etk="c0"')
A.cagri(F, TS[0], 330, 150, ['1 · Üreteropelvik bileşke · üst üreter', 'yan ağrısı'], grup='data-etk="c1"')
A.cagri(F, TS[1], 330, 246, ['2 · İliyak damar çaprazı · orta üreter', 'alt karın ve kasığa yayılan ağrı;', 'apandisiti taklit edebilir'], grup='data-etk="c2"')
A.cagri(F, TS[2], 330, 322, ['3 · Üreterovezikal bileşke', 'kasık, testis ya da labiaya yayılım;', 'sık idrar, sıkışma, dizüri'], grup='data-etk="c3"')
# hareket yolu (görünmez): pelvisten üreter boyunca mesane içine
YOL = [P(345, 360), P(400, 420)] + UY + [P(668, 1286), P(700, 1290)]
uz = [0]
for i in range(1, len(YOL)): uz.append(uz[-1] + math.hypot(YOL[i][0] - YOL[i - 1][0], YOL[i][1] - YOL[i - 1][1]))
def oran(q): return uz[min(range(len(YOL)), key=lambda i: (YOL[i][0] - q[0]) ** 2 + (YOL[i][1] - q[1]) ** 2)] / uz[-1]
F.a(f'<path data-etk="yol" data-dur="{oran(p_upj):.3f} {oran(p_il):.3f} {oran(p_uvj):.3f}" d="{A.yol_d(YOL)}" fill="none" stroke="none"/>')
F.tl(330, 410, ['Numaralar: üç fizyolojik darlık; taşlar en', 'sık burada takılır. En darı: 3.'], 11.4, 15, fill=INK2)
serit(F, 616, 6, 458, 'Kolik neden olur?', RED); zemin(F, 616, 42, 458, 404)
Z = [(845, 82, 'Üreter tıkanır'), (845, 150, 'Proksimal basınç ↑ · üreter spazmı'), (845, 218, 'Prostaglandin salınımı'),
     (845, 286, 'Afferent dilatasyon: idrar yapımı sürer'), (845, 354, 'Basınç ↑↑ → kapsül ve sistem gerilimi = ağrı')]
W = []
for i, (x, y, t) in enumerate(Z):
    w = gen(t, 12.4, True) + 26; W.append(w); F.r(x - w / 2, y - 18, w, 36, '#fff' if i < 4 else '#fdeaea', RED, 1.5, 18); F.t(x, y + 4.5, t, 12.4, 800, INK, 'middle')
    if i < 4: F.ok(x, y + 19, x, y + 48, RED, 2.2)
xs4, xs1 = 845 + W[4] / 2, 845 + W[1] / 2
F.yol(f'M{xs4 + 2:.0f},354 C1066,340 1066,160 {xs1 + 6:.0f},152', RED, 2.2, ok=True, dash='6 4'); F.t(1036, 246, 'kısır', 11, 700, RED, 'end'); F.t(1036, 260, 'döngü', 11, 700, RED, 'end')
F.engel(690, 190, 845 - W[2] / 2 - 4, 218, '#1f8a4c', 3); F.t(632, 186, 'NSAİİ', 13, 800, GREEN)
F.tl(632, 412, ['NSAİİ prostaglandini keser: hem ağrıyı', 'hem lümen içi basıncı azaltır.'], 11.6, 15, fill=GREEN, fw=700)
D.yeni('s26_yer', 'x26_6', 'Temel Bilgiler · 3 · Şekil', 'Taşın Yeri, Ağrının Yeri ve Koliğin Mekanizması', F,
       '<b>Okuma:</b> Taşlar üreterin üç darlığında takılır: üreteropelvik bileşke, iliyak damar çaprazı ve en dar yer olan üreterovezikal bileşke. Ağrının yeri taşın yerini söyler. '
       'Ağrıyı taşın kendisi değil tıkanmanın yarattığı basınç yapar; prostaglandin bu döngüyü besler, NSAİİ onu keser.',
       'Şekil: solda böbrek, üreter ve mesane. Üst kalikste sessiz bir taş; üreterin üç fizyolojik darlığında, yani üreteropelvik bileşkede, iliyak damarların çaprazladığı yerde ve üreterovezikal bileşkede birer taş. '
       'Üst üreter taşı yan ağrısı; orta üreter taşı alt karın ve kasığa yayılan, apandisiti taklit edebilen ağrı; üreterovezikal bileşke taşı kasık, testis ya da labiaya yayılan ağrı ile sık idrar, sıkışma ve dizüri yapar. '
       'Sağda kolik döngüsü: tıkanma, basınç artışı ve spazm, prostaglandin salınımı, afferent dilatasyonla idrar yapımının sürmesi ve basıncın daha da artması; NSAİİ prostaglandin basamağını keser.')

# ============================================================================================== 2 · idrar kristalleri
F = Fig('kri', 434, 'İdrar mikroskopisinde taş tiplerinin kristalleri: kalsiyum oksalat, ürik asit, strüvit, sistin, kalsiyum fosfat', w=1080)


def alan(x0, y0, bas, alt, c):
    F.r(x0, y0, 350, 200, '#fbf8f2', LINE, 1.2, 10)
    F.el(x0 + 82, y0 + 100, 74, 74, '#eef3f6', '#9aa9b5', 1.4)
    bas = bas if isinstance(bas, list) else [bas]
    F.tl(x0 + 166, y0 + 36, bas, 13.2, 17, fw=800, fill=c)
    F.tl(x0 + 166, y0 + 44 + 17 * len(bas), alt, 11.6, 17, fill=INK)
    return x0 + 82, y0 + 100


def kare_zarf(x, y, s, a=0):
    F.a(f'<g transform="rotate({a} {x} {y})"><rect x="{x - s}" y="{y - s}" width="{2 * s}" height="{2 * s}" fill="#ffffff" fill-opacity=".7" stroke="#5d7385" stroke-width="1.3"/>'
        f'<path d="M{x - s},{y - s} L{x + s},{y + s} M{x + s},{y - s} L{x - s},{y + s}" stroke="#5d7385" stroke-width="1"/></g>')


def poly(x, y, pts, fill, st='#5d7385', a=0):
    F.a(f'<polygon transform="rotate({a} {x} {y})" points="{" ".join(f"{x + u:.1f},{y + v:.1f}" for u, v in pts)}" fill="{fill}" stroke="{st}" stroke-width="1.3" stroke-linejoin="round"/>')


x, y = alan(6, 6, ['Kalsiyum oksalat', 'dihidrat'], ['“Zarf” (oktahedron)', 'CaOx (mono + di) %60–70', 'pH değişken · opak'], BRANDD)
for (u, v, s, a) in ((-30, -26, 15, 0), (18, -34, 11, 10), (-6, 16, 19, -8), (36, 26, 10, 20), (-44, 30, 9, 5)): kare_zarf(x + u, y + v, s, a)
x, y = alan(366, 6, ['Kalsiyum oksalat', 'monohidrat'], ['“Bisküvi”, kum saati', 'Daha sert; ESWL’ye dirençli', 'pH değişken · opak'], BRANDD)
for (u, v, a) in ((-28, -24, 20), (20, -30, -30), (-8, 14, 70), (34, 24, 0), (-42, 34, -10)):
    F.a(f'<g transform="rotate({a} {x + u} {y + v})"><ellipse cx="{x + u - 7}" cy="{y + v}" rx="9" ry="7" fill="#fff" fill-opacity=".8" stroke="#5d7385" stroke-width="1.3"/>'
        f'<ellipse cx="{x + u + 7}" cy="{y + v}" rx="9" ry="7" fill="#fff" fill-opacity=".8" stroke="#5d7385" stroke-width="1.3"/></g>')
x, y = alan(726, 6, 'Ürik asit', ['Elmas, eşkenar dörtgen,', 'rozet · %5–10', 'Oral tedaviyle eritilebilir', 'pH < 5,5 · RADYOLÜSEN'], GOLD)
for (u, v, s, a) in ((-30, -24, 18, 10), (16, -30, 13, -20), (-4, 18, 22, 35), (36, 22, 12, 0), (-44, 34, 10, -30)):
    poly(x + u, y + v, [(0, -s), (s * .62, 0), (0, s), (-s * .62, 0)], '#f2c96b', '#a8781a', a)
x, y = alan(6, 214, ['Strüvit', '(Mg-amonyum-fosfat)'], ['“Tabut kapağı” prizması', '%5–15 · staghorn', 'pH > 7,2 · opak'], RED)
for (u, v, s, a) in ((-24, -22, 1, 15), (22, 8, 1.25, -20), (-30, 34, .8, 40)):
    poly(x + u, y + v, [(-26 * s, -8 * s), (-16 * s, -14 * s), (16 * s, -14 * s), (26 * s, -8 * s), (26 * s, 8 * s), (-26 * s, 8 * s)], '#fff', '#5d7385', a)
    F.a(f'<line transform="rotate({a} {x + u} {y + v})" x1="{x + u - 16 * s:.1f}" y1="{y + v - 14 * s:.1f}" x2="{x + u - 26 * s:.1f}" y2="{y + v - 8 * s:.1f}" stroke="#5d7385" stroke-width="1"/>')
x, y = alan(366, 214, 'Sistin', ['Altıgen saydam levha', '%1–2 (çocukta daha sık)', 'Asit idrarda çöker (pH < 7)', 'Hafif opak (kükürt)'], PUR)
for (u, v, s, a) in ((-24, -22, 18, 0), (18, -10, 14, 15), (-14, 26, 15, 30), (36, 32, 10, 5)):
    poly(x + u, y + v, [(s * math.cos(math.radians(60 * i)), s * math.sin(math.radians(60 * i))) for i in range(6)], '#fff', '#5d7385', a)
x, y = alan(726, 214, ['Kalsiyum fosfat', '(brushit)'], ['İnce iğne kümeleri', 'CaP %10–15 (çoğu apatit;', 'brushit nadir, çok sert)', 'pH > 6,5 · opak'], GREEN)
for (u, v) in ((-24, -20), (22, 14), (-28, 34)):
    for a in range(0, 180, 30):
        ra = math.radians(a); F.ln(x + u - 18 * math.cos(ra), y + v - 18 * math.sin(ra), x + u + 18 * math.cos(ra), y + v + 18 * math.sin(ra), '#5d7385', 1.4)
F.t(540, 428, 'Kristal tek başına taş tipini kanıtlamaz; taş analizi gerekir.', 11.2, None, INK2, 'middle')
D.yeni('s26_kri', 'x26_5', 'Temel Bilgiler · 2 · Şekil', 'Taş Tipleri — İdrarda Görülen Kristaller', F,
       '<b>Okuma:</b> Kalsiyum oksalat dihidrat zarf, monohidrat bisküvi ya da kum saati; ürik asit elmas ya da rozet; strüvit tabut kapağı; sistin altıgen; brushit iğne kümeleri verir. '
       'İdrar pH’ı ve grafide görünürlük ipucudur: ürik asit taşı asidik idrarda oluşur ve direkt grafide görünmez.',
       'Şekil: altı mikroskop alanı. Kalsiyum oksalat dihidrat zarf biçimli, monohidrat bisküvi ya da kum saati biçimli; ürik asit sarı elmas biçimli; strüvit tabut kapağı prizması; '
       'sistin altıgen saydam levha; brushit ince iğne kümeleri. Her alanda taşın sıklığı, idrar pH’ı ve direkt grafide görünürlüğü yazıyor.')

# ============================================================================================== 3 · süpersatürasyon ve Randall plağı
F = Fig('ran', 388, 'Süpersatürasyon bölgeleri ve renal papillada Randall plağı üzerinde kalsiyum oksalat taşı', w=1080)
serit(F, 6, 6, 420, 'Süpersatürasyon (SS)', BRANDD); zemin(F, 6, 42, 420, 340)
for i, (y0, h, c, sat) in enumerate(((60, 96, '#f6c6bf', ['Metastabil sınırın üstü', 'kendiliğinden çekirdeklenme']),
                                     (156, 110, '#f8e5a6', ['SS 1 – metastabil sınır', 'var olan kristal büyür;', 'heterojen çekirdeklenme olabilir']),
                                     (266, 96, '#cdeedd', ['SS < 1', 'kristal çözünür']))):
    F.r(40, y0, 70, h, c, None, rx=0)
    yy = y0 + h / 2 - 8 * (len(sat) - 1) - 2
    F.t(126, yy, sat[0], 13, 800, INK); F.tl(126, yy + 18, sat[1:], 12, 16, fill=INK)
F.r(40, 60, 70, 302, 'none', INK2, 1.6, 4)
F.ok(24, 356, 24, 72, INK2, 2.2); F.t(24, 62, 'SS', 12, 800, INK2, 'middle')
for yb, t in ((156, 'metastabil sınır'), (266, 'SS = 1')):
    F.ln(34, yb, 116, yb, INK, 2); F.ln(116, yb, 414, yb, INK2, 1, '4 4'); F.t(414, yb - 5, t, 11, 700, INK2, 'end')
F.t(124, 378, 'SS = iyon aktivite çarpımı / Ksp', 11.4, 700, INK2)
serit(F, 436, 6, 638, 'Dört adım ve Randall plağı', PUR); zemin(F, 436, 42, 638, 340)
# Resim: ChatGPT ile çizildi (yazısız, 1024 × 1536 px)
RX0, RY0, RSK = 456, 44, 224 / 1024
A.resim(F, 'an_ran', RX0, RY0, 224, h=336, oran=None)
def R_(px, py): return (RX0 + px * RSK, RY0 + 336 / 2 - 768 * RSK + py * RSK)
A.cagri(F, R_(515, 1035), 704, 252, ['Randall plağı: papilla ucunda epitel', 'altında kalsiyum fosfat (apatit)'])
A.cagri(F, R_(600, 1085), 704, 330, ['Ürotel aralanır, plak açığa çıkar;', 'kalsiyum oksalat üzerine tutunur'])
A.cagri(F, R_(530, 600), 704, 160, ['Henle kulpu ince kollarının', 'bazal membranında başlar, interstisyuma yayılır'])
A.ad(F, *R_(300, 140), 'piramit (medulla)', 11); A.ad(F, *R_(512, 870), 'papilla', 11); A.ad(F, *R_(250, 1260), 'kaliks', 11, '#8a5a00')
F.tl(700, 74, ['1 Süpersatürasyon → 2 heterojen çekirdeklenme', '→ 3 büyüme ve kümelenme → 4 tutunma.', 'Taş için kristal tutulmalı: çoğu kez plağa.'], 12, 17, fill=INK, fw=700)
D.yeni('s26_ran', 'x26_11', 'Patogenez · Şekil', 'Süpersatürasyondan Taşa — Randall Plağı', F,
       '<b>Okuma:</b> SS 1’in altında kristal çözünür; 1 ile metastabil sınır arasında var olan kristal büyür ve heterojen çekirdeklenme olabilir; sınırın üstünde kendiliğinden çekirdeklenme olur. '
       'Taş için kristalin böbrekte tutulması gerekir: kalsiyum oksalat taşlarının çoğu papilla ucundaki epitel altı kalsiyum fosfat plağına (Randall plağı) tutunarak büyür.',
       'Şekil: solda süpersatürasyon ölçeği: birin altında çözünme, bir ile metastabil sınır arasında var olan kristalin büyümesi ve heterojen çekirdeklenme, sınırın üstünde kendiliğinden çekirdeklenme. '
       'Sağda koni biçimli renal papilla ve ucunu saran kaliks: Henle kulpu ince kollarının bazal membranında başlayıp interstisyuma yayılan epitel altı kalsiyum fosfat birikimi, yani Randall plağı, papilla ucunda ürotelin aralandığı yerde açığa çıkmış; üzerine kalsiyum oksalat taşı tutunmuş.')

# ============================================================================================== 4 · ürik asit ve idrar pH’ı
F = Fig('uri', 372, 'İdrar pH’ına göre protone (çözünmeyen) ürik asit oranı; pKa 5,5, korunma ve eritme hedefleri', w=1080)
X0, X1, Y0, Y1 = 90, 760, 320, 40
def X(p): return X0 + (p - 4.5) / 3 * (X1 - X0)
def Y(f): return Y0 - f * (Y0 - Y1)
F.a(f'<defs><linearGradient id="g26cap" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fbe7c6" stop-opacity="0"/><stop offset=".45" stop-color="#fbe7c6" stop-opacity=".9"/><stop offset="1" stop-color="#f6cf8f"/></linearGradient></defs>')
F.r(X(6.8), Y1, X1 - X(6.8), Y0 - Y1, 'url(#g26cap)', None, rx=0)
F.r(X(6.2), Y1, X(6.8) - X(6.2), Y0 - Y1, '#d8f1e3', None, rx=0); F.t((X(6.2) + X(6.8)) / 2, Y1 + 16, 'korunma', 11.6, 800, GREEN, 'middle')
F.r(X(7.0), Y1, X(7.2) - X(7.0), Y0 - Y1, 'none', PUR, 1.6, 0, '5 4'); F.t((X(7.0) + X(7.2)) / 2, Y1 + 16, 'eritme', 11.6, 800, PUR, 'middle')
F.t((X(7.2) + X1) / 2, Y0 - 34, 'CaP', 11.6, 800, GOLD, 'middle'); F.t((X(7.2) + X1) / 2, Y0 - 20, 'riski ↑', 11.6, 800, GOLD, 'middle')
for v in (0, .25, .5, .75, 1):
    F.ln(X0, Y(v), X1, Y(v), LINE, 1); F.t(X0 - 8, Y(v) + 4, f'%{int(v * 100)}', 11.4, None, MUT, 'end')
for p in (4.5, 5, 5.5, 6, 6.5, 7, 7.5):
    F.ln(X(p), Y0, X(p), Y0 + 5, INK2, 1.4); F.t(X(p), Y0 + 20, f'{p:g}'.replace('.', ','), 11.4, None, MUT, 'middle')
F.ln(X0, Y0, X1, Y0, INK2, 1.8); F.ln(X0, Y1, X0, Y0, INK2, 1.8)
F.t((X0 + X1) / 2, Y0 + 42, 'İdrar pH’ı', 12.4, 700, INK2, 'middle')
F.a(f'<text x="26" y="{(Y0 + Y1) / 2:g}" font-size="12.4" font-weight="700" fill="{INK2}" text-anchor="middle" transform="rotate(-90 26 {(Y0 + Y1) / 2:g})">protone ürik asit oranı</text>')
pts = [(X(4.5 + i * .025), Y(1 / (1 + 10 ** (4.5 + i * .025 - 5.5)))) for i in range(121)]
F.yol('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts), GOLD, 3)
F.ln(X(5.5), Y(.5), X(5.5), Y0, GOLD, 1.6, '4 3'); F.el(X(5.5), Y(.5), 6, 6, GOLD, '#fff', 1.6); F.t(X(5.5) + 10, Y(.5) - 8, 'pKa 5,5: yarı yarıya', 12, 800, GOLD)
F.el(X(6.5), Y(1 / 11), 6, 6, GREEN, '#fff', 1.6); F.t(X(6.5) + 8, Y(1 / 11) - 12, '%9', 12, 800, GREEN)
F.r(784, 40, 290, 116, '#fff', GOLD, 1.4, 10)
F.t(798, 64, 'Asıl sorun çoğu kez pH', 13, 800, GOLD)
F.tl(798, 88, ['pH < 5,5: çözünmeyen protone ürik', 'asit baskın; hacim ve ürik asit', 'atılımı da katkıda bulunur.', 'pH 6,5’te çözünürlük > 10 kat.'], 12, 17, fill=INK)
F.r(784, 168, 290, 152, '#fff', GREEN, 1.4, 10)
F.t(798, 192, 'Tedavi: alkalinizasyon', 13, 800, GREEN)
F.tl(798, 216, ['Korunma: idrar pH 6,2–6,8', '(hasta evde kâğıtla ölçer).', 'Eritme: pH 7,0–7,2 (EAU).', 'Uzun süre 7,0 üstü: kalsiyum', 'fosfat çökebilir.'], 12, 18, fill=INK)
D.yeni('s26_uri', 'x26_36', 'Ürik Asit Taşı · Şekil', 'Ürik Asit — pKa 5,5 Çizgisi', F,
       '<b>Okuma:</b> Ürik asidin pKa’sı 5,5’tir: bu pH’ta yarısı çözünmeyen protone biçimdedir, pH düştükçe bu oran hızla artar. '
       'Korunmada idrar pH’ı 6,2–6,8’de tutulur; taşı eritmek için EAU 7,0–7,2’yi önerir. pH yükseldikçe kalsiyum fosfat çökmesi riski artar; uzun süre 7,0’ın üstünde tutulmaz.',
       'Şekil: yatay eksende idrar pH’ı, dikey eksende protone yani çözünmeyen ürik asit oranı. pH 5,5’te oran yüzde elli, pH 6,5’te yaklaşık yüzde dokuz. '
       'Yeşil bant 6,2 ile 6,8 arası korunma hedefi, kesikli çerçeve 7,0 ile 7,2 arası eritme hedefi; 6,8’den sonra koyulaşan turuncu bant kalsiyum fosfat riskinin arttığını gösteriyor.')

# ============================================================================================== 5 · strüvit: üreaz kimyası ve staghorn
F = Fig('str', 352, 'Üreaz üreten bakteride üreden amonyak, alkali idrar ve strüvit çökmesi; staghorn taş', w=1080)
serit(F, 6, 6, 690, 'Üreaz: üreden taşa', RED); zemin(F, 6, 42, 690, 304)
AZ = [(30, 70, 'Üre', 'idrarda bol'), (200, 70, '2 NH₃ + CO₂', 'hidroliz ürünleri'), (408, 70, 'NH₄⁺ ↑ · pH > 7,2', 'amonyak alkalileştirir'),
     (30, 180, 'Mg²⁺ + NH₄⁺ + PO₄³⁻', 'alkali ortamda'), (310, 180, 'Strüvit (MgNH₄PO₄·6H₂O)', '+ karbonat apatit çöker')]
R = []
for i, (x, y, t1, t2) in enumerate(AZ):
    w = max(gen(t1, 13.2, True), gen(t2, 11.6)) + 30; R.append((x, y, w))
    F.r(x, y, w, 58, '#fdeaea' if i == 4 else '#fff', RED, 1.6, 10); F.t(x + w / 2, y + 25, t1, 13.2, 800, INK, 'middle'); F.t(x + w / 2, y + 44, t2, 11.6, None, INK2, 'middle')
def sag(i): return R[i][0] + R[i][2]
F.ok(sag(0) + 3, 99, R[1][0] - 4, 99, RED, 2.2); F.t((sag(0) + R[1][0]) / 2, 90, 'üreaz', 11.6, 800, RED, 'middle'); F.t((sag(0) + R[1][0]) / 2, 116, '+ H₂O', 11, None, INK2, 'middle')
F.ok(sag(1) + 3, 99, R[2][0] - 4, 99, RED, 2.2)
F.yol(f'M{R[2][0] + R[2][2] / 2:.0f},{130} C{R[2][0] + R[2][2] / 2:.0f},160 {R[3][0] + R[3][2] / 2:.0f},146 {R[3][0] + R[3][2] / 2:.0f},176', RED, 2.2, ok=True)
F.ok(sag(3) + 3, 209, R[4][0] - 4, 209, RED, 2.2)
F.r(22, 252, 662, 88, '#f2f5f8', INK2, 1.2, 10)
F.tl(36, 274, ['Üreaz üretenler: Proteus mirabilis (klasik), Klebsiella, Providencia, Morganella, Serratia,', 'Ureaplasma urealyticum, Corynebacterium urealyticum, S. saprophyticus, bazı Pseudomonas suşları'], 11.6, 18, fill=INK, fw=700)
F.t(36, 326, 'E. coli pratikte üreaz üretmez: en sık idrar yolu enfeksiyonu etkeni olsa da strüvit yapmaz.', 11.6, None, RED)
serit(F, 706, 6, 368, 'Staghorn (geyik boynuzu) taş', RED); zemin(F, 706, 42, 368, 304)
SX0, SY0, SSK = 708, 46, 250 / 760          # resim: ChatGPT ile çizildi, yazısız (760 × 760 px)
A.resim(F, 'an_str', SX0, SY0, 250, oran=1)
A.cagri(F, (SX0 + 395 * SSK, SY0 + 330 * SSK), 948, 92, ['Pelvisi ve kaliksleri', 'doldurur'], fs=12)
F.tl(724, 312, ['Tam çıkarılmalı (çoğunlukla PCNL);', 'kalan parça enfeksiyonu sürdürür.'], 11.8, 16, fill=RED, fw=700)
D.yeni('s26_str', 'x26_37', 'Strüvit · Şekil', 'Strüvit — Bakterinin Yaptığı Taş', F,
       '<b>Okuma:</b> Üreaz üreyi amonyak ve karbondioksite parçalar; amonyak idrarı 7,2’nin üstüne alkalileştirir ve amonyum sağlar; magnezyum amonyum fosfat ile karbonat apatit çöker. '
       'Taş hızla büyüyüp pelvis ve kaliksleri doldurur; enfeksiyonun kaynağı olduğu için tamamen çıkarılmalıdır.',
       'Şekil: solda kimyasal zincir: üre, üreazla iki amonyak ve karbondioksite ayrılır; amonyum artar ve idrar pH’ı 7,2’nin üstüne çıkar; magnezyum, amonyum ve fosfat strüvit olarak, '
       'karbonat apatitle birlikte çöker. Altta üreaz üreten bakteriler ve E. coli’nin üreaz üretmediği notu. Sağda pelvisi ve üç kaliksi dolduran geyik boynuzu biçimli taş.')

# ============================================================================================== 6 · hangi girişim, hangi taşa
F = Fig('gir', 410, 'Taşın yerine ve boyutuna göre girişim seçimi: ESWL, URS ve RIRS, PCNL', w=1080)
serit(F, 6, 6, 1068, 'Yer ve boyut belirler', BRANDD); zemin(F, 6, 42, 1068, 362)
GX0, GY0, GSK = 26, 52, 296 / 1062          # resim: ChatGPT ile çizildi, yazısız (s26_yer resminin üst kısmı)
A.resim(F, 'an_gir', GX0, GY0, 1024 * GSK, oran=1062 / 1024)
def GP(px, py): return (GX0 + px * GSK, GY0 + py * GSK)
def isa(p, r, tt, c):
    A.tas(F, p[0], p[1], r, tt); F.el(p[0], p[1], r + 5, r + 5, 'none', '#fff', 4.4, op=.85); F.el(p[0], p[1], r + 5, r + 5, 'none', c, 2.4)
isa(GP(312, 228), 4.5, 2, BRAND); isa(GP(222, 345), 4.5, 7, BRAND)
pel = GP(350, 372); isa(pel, 9, 4, RED); lk = GP(262, 498); isa(lk, 6, 6, RED)
ut = GP(449, 590); isa(ut, 4.2, 9, BRAND)
ua = GP(544, 1036); isa(ua, 4.2, 12, PUR)
A.cagri(F, (pel[0] + 14, pel[1] - 4), 206, 124, ['pelvis', '> 2 cm'], fs=11.8)
A.cagri(F, (lk[0] + 11, lk[1] + 4), 206, 178, ['alt kaliks', '> 1 cm'], fs=11.8)
A.cagri(F, (ut[0] + 9, ut[1]), 236, 232, ['proksimal', 'üreter'], fs=11.8)
A.cagri(F, (ua[0] + 9, ua[1]), 236, 318, ['distal', 'üreter'], fs=11.8)
K = [(300, 54, 'ESWL', BRAND, ['Böbrek taşı < 2 cm: üst ve orta kaliks, pelvis', 'Proksimal üreter taşı < 10 mm', 'Kontrendikasyon: gebelik, kesilemeyen antitrombotik,', 'kanama eğilimi, tedavisiz ÜSE, distal tıkanma,', 'aort anevrizması',
                                  'Dirençli: sistin, brushit, CaOx monohidrat (> 1000 HU)']),
     (300, 210, 'URS / fleksibl URS (RIRS) ± lazer', PUR, ['Üreter taşında birinci seçenek (distal, > 10 mm)', 'Proksimal < 10 mm: ESWL ile eşdeğer', 'ESWL’ye dirençli taş · gebelik (deneyimli merkez)',
                                                      'Antitrombotik kesilemiyorsa tercih edilen', 'RIRS ile 2 cm’e kadar böbrek taşı']),
     (690, 54, 'PCNL', RED, ['Taş > 2 cm · staghorn · strüvit (tam çıkarım)', 'Alt kaliks > 1 cm: PCNL ya da RIRS', 'ESWL ya da URS başarısız',
                             'Anomali: at nalı böbrek, kaliks divertikülü', 'Taşsızlık en yüksek; kanama ve sepsis riski', 'Antitrombotik genellikle kesilir ya da köprülenir']),
     (690, 210, 'Açık / laparoskopik', INK2, ['Modern pratikte < %1', 'Karmaşık anatomi, eş zamanlı düzeltici', 'cerrahi, endoskopik yöntemin', 'tekrarlayan başarısızlığı'])]
for x, y, bas, c, sat in K:
    F.r(x, y, 376, 148, TINT.get(c, '#fff'), c, 1.6, 10); F.t(x + 14, y + 24, bas, 14, 800, c); F.tl(x + 14, y + 46, sat, 11.6, 16, fill=INK)
F.tl(22, 382, ['Komplikasyonsuz küçük üreter taşı (≲ 10 mm): önce izlem; distal taşta alfa blokerle medikal atılım.',
               'Tıkalı ve enfekte böbrek: önce acil stent ya da nefrostomi; kesin taş tedavisi enfeksiyon geçince.'], 11.6, 16, fill=INK2, fw=700)
D.yeni('s26_gir', 'x26_43', 'Girişim · Şekil', 'Hangi Girişim, Hangi Taşa — Harita', F,
       '<b>Okuma:</b> Halkaların rengi kutularla eşleşir. 2 cm’in altındaki böbrek taşında ESWL ya da RIRS; 2 cm’in üstünde, staghorn ve strüvit taşında PCNL; distal ve büyük üreter taşında URS birinci seçenektir. '
       'ESWL’nin kontrendikasyonları ve dirençli taş tipleri seçimi değiştirir; antitrombotik kesilemiyorsa URS tercih edilir. Küçük üreter taşında önce izlem, enfekte tıkalı böbrekte önce drenaj gelir.',
       'Şekil: solda böbrekte üst ve orta kalikste mavi halkalı küçük taşlar, pelviste ve alt kalikste kırmızı halkalı büyük taşlar; üreterde mavi halkalı proksimal ve mor halkalı distal taş. '
       'Sağda dört kutu aynı renklerle: ESWL iki santimetrenin altındaki böbrek ve on milimetrenin altındaki proksimal üreter taşında; URS ya da RIRS üreter taşında birinci seçenek ve antitrombotik kesilemiyorsa tercih edilir; '
       'PCNL iki santimetrenin üstündeki, staghorn ve strüvit taşlarında; açık cerrahi yüzde birin altında. Altta küçük üreter taşında izlem ve enfekte tıkalı böbrekte acil drenaj notu.')
