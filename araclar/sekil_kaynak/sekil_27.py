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
YAZ = [('0 · Normal', 'sistem genişlememiş'), ('1 · Yalnız pelvis', 'kaliksler normal'), ('2 · Pelvis + bazı kaliksler', 'diğerleri normal'),
       ('3 · Tüm kaliksler', 'parankim normal'), ('4 · Parankim incelmesi', 'kaliksler de genişlemiş')]
GS = ((319, 545), (327, 546), (328, 546), (329, 546), (336, 545))   # resim boyutu (px); ChatGPT ile çizildi, yazısız
f = .282
for i in range(5):
    cx = 118 + i * 212
    F.a(f'<g data-etk="d{i}" data-c="{cx - 10},126">')
    A.resim(F, f'an_us{i}', cx - 10 - GS[i][0] / 2 * f, 50, GS[i][0] * f, oran=GS[i][1] / GS[i][0])
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
    P = A.resim(F, 'an_rpf_a' if rpf else 'an_rpf_b', ox + 6, 10, 528, oran=2 / 3)
    F.t(ox + 30, 34, 'ön', 11.4, 700, MUT); F.t(ox + 30, 350, 'arka', 11.4, 700, MUT)
    F.t(ox + 30, 196, 'Sağ', 11.4, 700, MUT); F.t(ox + 510, 196, 'Sol', 11.4, 700, MUT, 'end')
    if rpf: N = dict(ao=(540, 277), aoa=(548, 318), ivc=(432, 286), ur=((372, 311), (610, 311)), man=(586, 212), vert=(490, 395), pso=(322, 390))
    else: N = dict(ao=(534, 186), ivc=(400, 223), ur=((292, 296), (670, 296)), nod=(530, 262), vert=(490, 395), pso=(322, 390))
    Q = {k: (P(*v) if not isinstance(v[0], tuple) else tuple(P(*q) for q in v)) for k, v in N.items()}
    def yaz(q, t, c, dy=0): F.a(f'<text x="{q[0]:.1f}" y="{q[1] + dy:.1f}" font-size="10.5" font-weight="800" fill="#fff" text-anchor="middle" stroke="{c}" stroke-width="2.6" paint-order="stroke">{t}</text>')
    yaz(Q['ivc'], 'VKİ', '#2f4f86', 4); yaz(Q['pso'], 'psoas', '#7a3530', 4); yaz(Q['vert'], 'vertebra', '#8a7350', 4)
    return Q


Q = kesit(F, 0, True)
F.t(270, 34, 'Retroperitoneal fibroz', 14, 800, PUR, 'middle')
A.cagri(F, Q['aoa'], 352, 314, ['Aort vertebraya yapışık', 'öne itilmemiş'], fs=11.8)
A.cagri(F, Q['man'], 368, 92, ['Fibröz manto önü ve yanları', 'sarar, arkaya girmez'], fs=11.8)
A.cagri(F, Q['ur'][0], 156, 118, ['Üreterler mediale', 'çekilir, sabitlenir'], fs=11.8, sol=True)
Q = kesit(F, 540, False)
F.t(810, 34, 'Lenfoma · malign kitle', 14, 800, RED, 'middle')
A.cagri(F, (Q['ao'][0] + 10, Q['ao'][1] - 10), 878, 92, ['Aort öne itilmiş', '(“yüzen aort”)'], fs=11.8)
A.cagri(F, Q['nod'], 886, 314, ['Kitle aortun arkasına girer;', 'büyük lenf nodları'], fs=11.8)
A.cagri(F, Q['ur'][1], 948, 170, ['Üreterler', 'laterale itilir'], fs=11.8)
D.yeni('s27_rpf', 'x27_28', 'Retroperitoneal Fibroz · Şekil', 'RPF ve Lenfoma — Aort Nerede?', F,
       '<b>Okuma:</b> Retroperitoneal fibrozda periaortik doku aortu önden ve yanlardan sarar, arkaya girmez; aort vertebraya yapışık kalır ve üreterler mediale çekilir. '
       'Lenfomada kitle aortun arkasına da uzanır, aortu öne iter; büyük lenf nodları ve laterale itilmiş üreterler malignite lehinedir.',
       'Şekil: iki aksiyel kesit, ön yukarıda, hastanın sağı solda. Solda retroperitoneal fibroz: vertebra, iki psoas kası, aort ve vena kava önden ve yanlardan bir fibröz manto ile sarılmış; aort vertebraya yapışık, üreterler mantonun içinde mediale çekilmiş. '
       'Sağda lenfoma: aortun arkasına giren büyük lenf nodları aortu vertebradan uzaklaştırıp öne itmiş; üreterler laterale itilmiş.')

# ============================================================================================== 4 · nefrostomi ve retrograd stent
F = Fig('dren', 446, 'Obstrüksiyonda drenaj: perkütan nefrostomi ve retrograd double-J stent; hangi durumda hangisi', w=1080)


# Resimler: ChatGPT ile çizildi (yazısız). Konumlar resmin pikselinden (1536 × 1024 kaynak) ölçüldü.
DS = 340 / 942
def DA(px, py): return (12 + (px - 36) * DS, 42 + (py - 42) * DS)
def DB(px, py): return (552 + (px - 796) * DS, 42 + (py - 42) * DS)
def yol(T, ad, pts): F.a(f'<path data-etk="{ad}" d="{A.yol_d([T(*q) for q in pts])}" fill="none" stroke="none"/>')
for j, ox in enumerate((0, 540)):
    F.r(ox + 6, 6, 528, 380, '#fbf8f2', LINE, 1.2, 12)
# ---- sol: perkütan nefrostomi (resim 1108 × 1400 px; ikinci çizim, kateter papilla ekseninden girer)
DS2 = 344 / 1400
def DA(px, py): return (12 + px * DS2, 42 + py * DS2)
A.resim(F, 'an_dren_a', 12, 42, 1108 * DS2, oran=1400 / 1108)
for q in (((470, 200), (505, 300)), ((350, 290), (440, 335)), ((330, 420), (440, 405)), ((350, 480), (440, 465))): yol(DA, 'kaliks', q)
yol(DA, 'akis', ((498, 412), (520, 385), (548, 400), (545, 440), (480, 500), (430, 545), (380, 572), (300, 595), (200, 622), (150, 635), (100, 680), (70, 740),
                 (85, 820), (115, 900), (135, 960), (138, 1010), (138, 1080), (140, 1260)))
A.ad(F, *DA(95, 170), 'cilt', 10.8, '#8e7e6b'); A.ad(F, *DA(140, 1300), 'torba', 10.8, '#7a5a00')
F.t(30, 34, 'Perkütan nefrostomi', 14, 800, BRANDD)
F.tl(300, 64, ['Tercih edilen durumlar', ], 12.6, 17, fill=BRANDD, fw=800)
madde(F, 300, 88, [['Ürosepsis, instabilite:', 'lokal anestezi yeterli'], ['Malign bası, mesane', 'invazyonu'], ['Ayrık fonksiyon ve', 'kurtarılabilirlik ölçümü']])
F.tl(300, 216, ['Dikkat: perirenal kanama;', 'koagülopatide stent.'], 12, 17, fill=RED, fw=700)
# ---- sağ: retrograd double-J stent
A.resim(F, 'an_dren_b', 552, 42, 706 * DS, oran=942 / 706)
for q in (((1108, 180), (1120, 262)), ((1030, 240), (1085, 292)), ((1020, 330), (1080, 330)), ((1058, 420), (1105, 382))): yol(DB, 'kaliks', q)
yol(DB, 'akis', ((1112, 320), (1132, 330), (1150, 400), (1170, 480), (1182, 540), (1192, 600), (1204, 660), (1218, 720), (1240, 790), (1262, 840), (1300, 870)))
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
# Resimler: ChatGPT ile çizildi (yazısız; 460 × 500 px). n = tıkanma öncesi (gizli; hareketle belirir), d = tıkanma sonrası (durağan görünüm).
TK = .54
def T_(ox): return lambda px, py: (ox + px * TK, 46 + py * TK)
def yol(T, ad, pts): F.a(f'<path data-etk="{ad}" d="{A.yol_d([T(*q) for q in pts])}" fill="none" stroke="none"/>')
L_, R_ = T_(40), T_(580)
for T, ox, ka in ((L_, 40, 'A'), (R_, 580, 'B')):
    A.resim(F, f'an_tek_d{ka}', ox, 46, 460 * TK, oran=500 / 460, grup='data-etk="d"')
    A.resim(F, f'an_tek_n{ka}', ox, 46, 460 * TK, oran=500 / 460, grup='data-etk="n" style="opacity:0"')
yol(L_, 'akis-s', ((140, 150), (150, 250), (145, 300), (160, 360)))
yol(L_, 'akis-o', ((300, 150), (285, 250), (280, 300), (275, 360)))
yol(L_, 'durgun', ((300, 150), (290, 220), (285, 268)))
yol(R_, 'akis-r', ((150, 150), (160, 250), (160, 300), (165, 360))); yol(R_, 'akis-r', ((292, 150), (282, 250), (282, 300), (276, 360)))
yol(R_, 'akis-u', ((220, 440), (220, 488)))
A.cagri(F, L_(55, 235), 28, 298, ['Sağlam böbrek', 'hiperfiltrasyonla', 'telafi'], fs=11.6, grup='data-etk="et"')
A.cagri(F, L_(330, 100), 306, 100, ['Obstrükte böbrek', 'sessizce fonksiyon kaybeder'], grup='data-etk="et"')
F.tl(300, 178, ['• Kreatinin normal kalır', '• Tanı yalnız görüntülemeyle', '• Drenaj sonrası poliüri beklenmez', '• Karar: renografide ayrık fonksiyon'], 12, 19, fill=INK)
F.t(600, 336, 'BPH: mesane çıkım obstrüksiyonu', 11.4, 700, '#7d4f73')
A.cagri(F, R_(300, 380), 852, 296, ['Mesane dolu, duvar kalın;', 'iki sistem genişlemiş'], grup='data-etk="et"')
madde(F, 846, 160, ['ABH, oligüri ya da anüri', 'Hiperkalemi, asidoz, ödem', 'Acil drenaj, sonra neden', ['Drenaj sonrası poliüri', '(POD) beklenir']], lh=19)
D.yeni('s27_tek', 'x27_13', 'Ayrım · Şekil', 'Tek Taraflı ve Çift Taraflı — Neden Farklı?', F,
       '<b>Okuma:</b> Karşı böbrek sağlamsa hiperfiltrasyonla telafi eder, kreatinin normal kalır ve obstrükte böbrek sessizce fonksiyon kaybeder; tanı görüntülemeyle konur. '
       'Mesane çıkım obstrüksiyonu gibi çift taraflı tıkanmada ya da tek böbrekte akut böbrek hasarı gelişir; acil drenaj gerekir ve sonrasında poliüri beklenir.',
       'Şekil: solda tek taraflı obstrüksiyon: bir üreterde taş ve o tarafta genişlemiş pelvis; karşı böbrek hiperfiltrasyonla telafi ediyor; kreatinin normal. '
       'Sağda benign prostat büyümesine bağlı mesane çıkım obstrüksiyonu: mesane dolu ve duvarı kalın, iki üreter ve iki böbrek toplayıcı sistemi genişlemiş; akut böbrek hasarı ve acil drenaj.')
