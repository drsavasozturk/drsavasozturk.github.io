#!/usr/bin/env python3
"""Ders 19 · ADPKD ve Kistik Böbrek Hastalıkları — şekil tanımları (20 Kasım 2026)."""
import random
from sekil_ortak import *
import sekil_anat as AN

D = Ders('19')
L = D.L
KIST, KIST_K = '#e3f2fa', '#4f86a8'


def hucre(F, x, y, w=26, h=30, a1=RED, a2=GREEN, ters=False):
    F.r(x, y, w, h, '#f6e7d8', '#b48a6a', 1.1, 4)
    F.el(x + w / 2, y + (h * .62 if not ters else h * .38), 6, 5, '#9a7bb5', None)
    yy = y + (5.5 if not ters else h - 5.5)
    F.el(x + w / 2 - 5, yy, 3.3, 3.3, a1, None); F.el(x + w / 2 + 5, yy, 3.3, 3.3, a2, None)


# ============================================================================================== 1 · iki vuruş ve doz eşiği
F = Fig('iki', 356, 'ADPKD’de iki vuruş modeli: germline mutasyon, ikinci somatik olay, klonal kist ve polisistin doz eşiği', w=1080)
serit(F, 6, 6, 700, 'İki vuruş: kist tek bir hücreden doğar', BRANDD); zemin(F, 6, 42, 700, 308)
for p, (x0, bas, alt) in enumerate(((14, '1 · Germline', ['Her hücrede bir mutant', 'bir sağlam allel']),
                                     (244, '2 · İkinci vuruş', ['Tek hücrede sağlam', 'allel kaybolur']),
                                     (474, '3 · Klonal kist', ['Hücre çoğalır, sıvı salgılar;', 'kist tübülden ayrılır']))):
    F.t(x0 + 112, 68, bas, 13.2, 800, BRANDD, 'middle')
    F.r(x0 + 4, 124, 216, 34, IDRAR, None, rx=0, op=.35); F.t(x0 + 112, 146, 'tübül lümeni', 11, 700, '#8a6a00', 'middle')
    for i in range(8):
        cx = x0 + 4 + i * 27
        mut = (p >= 1 and i == 4)
        hucre(F, cx, 92)
        if p == 2 and i in (3, 4, 5): continue
        hucre(F, cx, 158, a2=RED if mut else GREEN, ters=True)
    if p == 1: F.el(x0 + 4 + 4 * 27 + 13, 173, 19, 19, 'none', RED, 2.2)
    if p == 2:
        cx0, cy0, R = x0 + 116, 230, 46
        F.el(cx0, cy0, R, R, KIST, KIST_K, 1.6)
        for k in range(14):
            a = math.radians(k * 360 / 14); hx, hy = cx0 + (R - 8) * math.cos(a), cy0 + (R - 8) * math.sin(a)
            F.el(hx, hy, 8, 6, '#f6e7d8', '#b48a6a', 1)
            F.el(hx - 2.6, hy, 2.1, 2.1, RED, None); F.el(hx + 2.6, hy, 2.1, 2.1, RED, None)
        F.t(cx0, cy0 + 5, 'kist sıvısı', 11, 700, KIST_K, 'middle')
        F.ok(x0 + 116, 158, x0 + 116, 182, INK2, 2)
    F.tl(x0 + 10, 300, alt, 11.8, 16, fill=INK)
for k, (c, t) in enumerate(((RED, 'mutant allel'), (GREEN, 'sağlam allel'))):
    F.el(26 + k * 120, 340, 4, 4, c, None); F.t(36 + k * 120, 344, t, 11.4, 700, INK2)
F.t(696, 344, 'Kistler nefronların %1’inden azından köken alır; her kist klonaldir.', 11.4, 700, INK2, 'end')
serit(F, 716, 6, 358, 'Doz eşiği modeli', PUR); zemin(F, 716, 42, 358, 308)
F.ln(760, 90, 760, 270, INK2, 1.6); F.ln(760, 270, 1060, 270, INK2, 1.6)
F.t(768, 80, 'işlevsel polisistin düzeyi', 11.4, 700, MUT)
for i, (v, c, t1, t2) in enumerate(((100, GREEN, 'İki sağlam', 'allel'), (52, GOLD, 'Germline', 'heterozigot'), (8, RED, 'İkinci', 'vuruş'))):
    bx = 790 + i * 92; bh = 170 * v / 100
    F.r(bx, 270 - bh, 56, bh, c, None, rx=4); F.t(bx + 28, 288, t1, 11.6, 800, INK, 'middle'); F.t(bx + 28, 302, t2, 11.2, None, INK2, 'middle')
F.ln(764, 214, 1060, 214, RED, 2, '7 5'); F.t(1058, 208, 'kritik eşik', 11.6, 800, RED, 'end')
F.tl(732, 326, ['Eşiğin altında kistogenez başlar;', 'hipomorfik alel ve çevre etkenleri de düşürür.'], 11.2, 14, fill=INK2)
D.yeni('s19_iki', 'x19_5', 'Klasik Çerçeve · 2 · Şekil', 'İki Vuruş ve Doz Eşiği — Kist Tek Bir Hücreden Doğar', F,
       '<b>Okuma:</b> Germline mutasyon her hücrede vardır; kist, sağlam allelin de kaybolduğu tek bir hücreden başlar ve klonal olarak büyür. '
       'Güncel “doz eşiği” yorumunda belirleyici olan, işlevsel polisistin düzeyinin kritik eşiğin altına inmesidir.',
       'Şekil: solda üç adım. Her tübül hücresinde bir mutant ve bir sağlam allel vardır; tek bir hücrede ikinci, somatik olayla sağlam allel kaybolur; '
       'bu hücre çoğalıp sıvı salgılayarak klonal bir kist oluşturur ve kist tübülden ayrılır. Sağda doz eşiği modeli: işlevsel polisistin düzeyi kritik eşiğin altına indiğinde kist oluşumu başlar.')

# ============================================================================================== 2 · kistik böbrek hastalıkları haritası
F = Fig('har', 446, 'Kistik böbrek hastalıklarında böbrek büyüklüğü ve kistlerin dağılımı', w=1080)


def kistler(cx, cy, k, n, rmin, rmax, bolge='her', tohum=1, renk=KIST):
    rg = random.Random(tohum); P = []
    for _ in range(4000):
        if len(P) >= n: break
        if bolge == 'km':                     # kortikomedüller bileşke
            a = math.radians(rg.uniform(100, 260)); r = rg.uniform(.52, .64)
            x, y = -10 + 24 * r * math.cos(a), 46 * r * math.sin(a)
        else:
            x, y = rg.uniform(-34, 8), rg.uniform(-44, 44)
            if ((x + 12) / 24) ** 2 + (y / 46) ** 2 > 1: continue
        rr = rg.uniform(rmin, rmax)
        if all(math.hypot(x - u, y - v) > rr + q + 1.2 for u, v, q in P): P.append((x, y, rr))
    for x, y, rr in P: F.el(cx + x * k, cy + y * k, rr * k, rr * k, renk, KIST_K, 1)
    return P


H = [('ADPKD', 'büyük', ['İki taraflı, çok sayıda, her', 'boyutta kist; karaciğer kisti']),
     ('ARPKD', 'büyük', ['Toplayıcı kanallarda radyal', 'mikrokistler; hepatik fibroz']),
     ('Nefronofitizis', 'küçük ya da normal', ['Kortikomedüller bileşkede', 'küçük kistler']),
     ('ADTKD', 'küçük ya da normal', ['Kist az ya da yok;', 'sessiz sediment']),
     ('Tüberoz skleroz', 'normal ya da büyük', ['Kist + anjiyomiyolipom', '(sarı, yağlı)']),
     ('von Hippel-Lindau', 'normal', ['Kist + berrak hücreli', 'böbrek kanseri']),
     ('Medüller sünger böbrek', 'normal', ['Papillada duktal ektazi,', 'taş ve kalsifikasyon']),
     ('Edinsel kistik hastalık', 'küçük', ['Uzun süreli diyaliz;', 'böbrek hücreli karsinom riski']),
     ('Basit kist', 'normal', ['Tek ya da az; yaşla artar,', 'Bosniak ile değerlendirilir'])]
HB = [(288, 373), (253, 360), (153, 229), (155, 233), (207, 303), (188, 286), (209, 310), (149, 224), (203, 306)]; HS = .34
for i, (ad, boy, sat) in enumerate(H):
    x0 = 6 + (i % 3) * 358; y0 = 6 + (i // 3) * 146
    F.r(x0, y0, 350, 138, '#fbf8f2', LINE, 1.2, 10)
    w, h = HB[i]; cx, cy = x0 + 68, y0 + 69                  # resim: ChatGPT ile çizildi (yazısız); ortak ölçek, boyut farkı gerçek
    AN.resim(F, f'an_har{i}', cx - w * HS / 2, cy - h * HS / 2, w * HS, oran=h / w, grup=(f'data-etk="adpkd"' if i == 0 else None))
    if i == 0:   # hareket: aynı hastanın böbreği 20, 40, 60 yaşta (ChatGPT ile çizildi); başlangıçta gizli
        for j, ((yw, yh), yy) in enumerate((((245, 398), 100), ((390, 548), 115), ((652, 825), 125))):
            ys = yy / yh                                 # 20 yaş normale yakın, 60 yaş statik ADPKD boyunda
            AN.resim(F, f'an_yas{j}', cx - yw * ys / 2, cy - yy / 2, yw * ys, oran=yh / yw, grup=f'data-etk="yas{j}" style="opacity:0"')
    F.t(x0 + 136, y0 + 34, ad, 13.4, 800, INK)
    F.t(x0 + 136, y0 + 54, 'Böbrek: ' + boy, 11.8, 700, BRANDD)
    F.tl(x0 + 136, y0 + 78, sat, 11.8, 16, fill=INK)
D.yeni('s19_har', 'x19_9', 'Klasik Çerçeve · 5 · Şekil', 'Kistik Böbrek Hastalıkları — Büyüklük ve Kistin Yeri', F,
       '<b>Okuma:</b> İlk soru böbreğin büyüklüğüdür: büyükse ADPKD ya da ARPKD; küçükse nefronofitizis, ADTKD ya da edinsel kistik hastalık. '
       'İkinci soru kistin yeridir: her yerde (ADPKD), toplayıcı kanallarda (ARPKD), kortikomedüller bileşkede (nefronofitizis), papillada (medüller sünger böbrek).',
       'Şekil: dokuz kistik böbrek hastalığında böbrek büyüklüğü ve kistlerin dağılımı. ADPKD büyük böbrek ve her boyutta çok sayıda kist; ARPKD büyük böbrek ve toplayıcı kanallarda radyal mikrokistler; '
       'nefronofitizis ve ADTKD küçük ya da normal böbrek; tüberoz sklerozda anjiyomiyolipom, von Hippel-Lindau’da kanser, medüller sünger böbrekte papillada ektazi ve taş, edinsel kistik hastalıkta küçük ama kistik böbrek, basit kistte tek kist.')

# ============================================================================================== 3 · Mayo görüntüleme sınıflaması
F = Fig('mayo', 380, 'Mayo görüntüleme sınıflamasında boya göre düzeltilmiş böbrek hacmi, yaş ve 1A–1E alt sınıfları', w=1080)
X0, X1, Y0, Y1 = 90, 760, 330, 30
def X(a): return X0 + (a - 15) / (80 - 15) * (X1 - X0)
def Y(v): return Y0 - (math.log10(v) - 2) / (math.log10(4000) - 2) * (Y0 - Y1)
F.r(X0, Y1, X1 - X0, Y0 - Y1, '#fbf8f2', None, rx=0)
for v in (100, 200, 500, 1000, 2000, 4000):
    F.ln(X0, Y(v), X1, Y(v), LINE, 1); F.t(X0 - 8, Y(v) + 4, f'{v:,}'.replace(',', '.'), 11.4, None, MUT, 'end')
for a in range(20, 81, 10):
    F.ln(X(a), Y0, X(a), Y0 + 5, INK2, 1.4); F.t(X(a), Y0 + 20, str(a), 11.4, None, MUT, 'middle')
F.ln(X0, Y0, X1, Y0, INK2, 1.8); F.ln(X0, Y1, X0, Y0, INK2, 1.8)
F.t((X0 + X1) / 2, Y0 + 40, 'Yaş (yıl)', 12.4, 700, INK2, 'middle')
F.a(f'<text x="24" y="{(Y0 + Y1) / 2:g}" font-size="12.4" font-weight="700" fill="{INK2}" text-anchor="middle" transform="rotate(-90 24 {(Y0 + Y1) / 2:g})">htTBH (mL/m, logaritmik)</text>')
SIN = [(1.5, '#7fb88f'), (3.0, '#c9b04e'), (4.5, '#e09452'), (6.0, '#c0392b')]
onceki = None
for r, c in SIN:
    pts = []
    for a in range(15, 81):
        v = 150 * (1 + r / 100) ** a
        if v > 4000: break
        pts.append((X(a), Y(v)))
    F.yol('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts), c, 2.4)
    ex, ey = pts[-1]; F.t(min(ex + 6, X1 - 4), ey + (14 if ex > X1 - 30 else 4), ('%' + f'{r:g}').replace('.', ','), 11.4, 800, c, 'end' if ex > X1 - 30 else 'start')
ET = [('1A', 72, 0, 1.5), ('1B', 70, 1.5, 3.0), ('1C', 62, 3.0, 4.5), ('1D', 52, 4.5, 6.0), ('1E', 36, 6.0, 9.0)]
for ad, a, r0, r1 in ET:
    v = 150 * math.sqrt((1 + r0 / 100) ** a * (1 + r1 / 100) ** a)
    F.t(X(a), Y(v) + 5, ad, 14, 800, INK, 'middle')
F.t(X0 + 8, Y1 + 18, 'Sınır eğrileri: yıllık tahmini büyüme', 11.4, 700, INK2)
F.t(X1 - 8, Y(112), 'Varsayım: 0 yaşta htTBH 150 mL/m', 11, None, INK2, 'end')
F.r(784, 30, 290, 150, '#fff', RED, 1.4, 10)
F.t(798, 54, 'Mayo kohortu · 10 yılda SDBY', 13, 800, RED)
F.t(798, 82, 'Sınıf 1A: %2,4', 13, 700, INK); F.t(798, 104, 'Sınıf 1B–1D: ara değerler', 12.4, None, INK); F.t(798, 126, 'Sınıf 1E: %66,9', 13, 700, RED)
F.t(798, 156, 'CRISP: %2,2 → %22,3', 12, None, INK2)
F.r(784, 196, 290, 134, '#fff', GOLD, 1.4, 10)
F.t(798, 220, 'Kullanılmaz', 13, 800, GOLD)
F.tl(798, 244, ['1 · Atipik örüntü (sınıf 2A, 2B):', 'asimetrik, tek taraflı, segmental', 'ya da iki taraflı atrofik', '2 · PKD1/PKD2 dışı genler'], 11.8, 16, fill=INK)
D.yeni('s19_mayo', 'x19_15', 'Prognoz · 1 · Şekil', 'Mayo Sınıflaması — Hacim, Yaş ve Beş Alt Sınıf', F,
       '<b>Okuma:</b> Boya göre düzeltilmiş toplam böbrek hacmi (htTBH) ve yaş birlikte hastayı 1A–1E alt sınıflarından birine yerleştirir; '
       'sınırlar yıllık tahmini böbrek büyümesine karşılık gelir. Alt sınıf yükseldikçe 10 yıllık SDBY riski artar. Eğriler nomogramın mantığını gösterir; hesap için nomogram kullanılır.',
       'Şekil: yatay eksende yaş, dikey eksende logaritmik htTBH. Dört sınır eğrisi yıllık yüzde bir buçuk, üç, dört buçuk ve altı böbrek büyümesine karşılık gelir ve beş alt sınıfı ayırır. '
       'Sağda Mayo kohortunda on yılda son dönem böbrek yetmezliği: sınıf 1A’da yüzde 2,4, sınıf 1E’de yüzde 66,9. Atipik örüntüde ve PKD1 ya da PKD2 dışı genlerde sınıflama kullanılmaz.')

# ============================================================================================== 4 · tolvaptan: kist epitelinde cAMP
F = Fig('tol', 384, 'Kist epitel hücresinde vazopressin, cAMP, klorür salgısı ve hücre çoğalması; tolvaptanın etki yeri ve TEMPO 3:4 sonucu', w=1080)
epitel(F, 'Kist epitel hücresi', h=368, mx=230, bx=600, rx=740, lumen_ad='KİST LÜMENİ', kan_ad='KAN',
       apikal=[dict(y=110, ad='CFTR', iyon='Cl⁻', yon='cik', tip='kanal', renk=GOLD)],
       bazal=[dict(y=96, ad='V2 reseptörü', iyon='AVP', tip='res', renk=PUR),
              dict(y=196, ad='NKCC1', iyon='Na⁺ · K⁺ · 2Cl⁻', tip='tas', renk=BRAND),
              dict(y=300, ad='Na⁺/K⁺-ATPaz', iyon='3Na⁺', ters='2K⁺', yon='cik', tip='pompa', renk=INK2)])
F.engel(616, 46, 610, 76, RED, 2.6); F.t(626, 48, 'tolvaptan', 12.6, 800, RED)
F.ok(520, 112, 520, 140, PUR, 2.2)
F.r(470, 142, 100, 28, '#fff', PUR, 1.6, 8); F.t(520, 161, 'cAMP ↑', 12.4, 800, PUR, 'middle')
F.ok(468, 156, 448, 156, PUR, 2.2); F.r(392, 142, 54, 28, '#fff', PUR, 1.6, 8); F.t(419, 161, 'PKA', 12.4, 800, PUR, 'middle')
F.ok(394, 146, 262, 118, PUR, 2.2)
F.ok(412, 172, 404, 220, PUR, 2.2)
F.tl(14, 150, ['PKA kanalı açar; Cl⁻ kiste geçer,', 'su izler, kist büyür'], 11.6, 15, fill=INK2)
F.r(296, 222, 206, 46, '#fdeaea', RED, 1.4, 8); F.t(399, 241, 'B-Raf → MEK → ERK', 12, 800, RED, 'middle'); F.t(399, 259, 'hücre çoğalması', 11.6, None, INK, 'middle')
F.ok(440, 290, 500, 172, INK2, 1.8, '4 3'); F.r(250, 292, 220, 46, '#f2f5f8', INK2, 1.2, 8); F.t(360, 311, 'Polisistin eksikliği:', 11.6, 800, INK2, 'middle'); F.t(360, 328, 'hücre içi Ca²⁺ ↓ → cAMP ↑', 11.6, None, INK, 'middle')
serit(F, 756, 8, 318, 'TEMPO 3:4 · 3 yıl', BRANDD); zemin(F, 756, 44, 318, 332)
F.t(774, 72, 'Yıllık toplam böbrek hacmi artışı', 12.4, 800, INK)
for i, (ad, v, c) in enumerate((('Tolvaptan', 2.8, BRAND), ('Plasebo', 5.5, MUT))):
    by = 96 + i * 62; bw = 230 * v / 6
    F.r(774, by, bw, 34, c, None, rx=5); F.t(774 + bw + 8, by + 23, ('%' + str(v)).replace('.', ','), 14, 800, c)
    F.t(774, by + 52, ad, 11.8, 700, INK2)
F.tl(774, 252, ['Hacim artışı yaklaşık yarıya indi', '(p < 0,001).', 'REPRISE (ileri hastalık): 12 ayda', 'eGFR değişimi −2,34’e karşı −3,61', 'mL/dk/1,73 m²'], 12, 17, fill=INK)
D.yeni('s19_tol', 'x19_27', 'Tedavi · 1 · Şekil', 'Tolvaptan — Kistin Motoru cAMP’yi Kısmak', F,
       '<b>Okuma:</b> AVP V2 reseptörü üzerinden cAMP’yi artırır; cAMP–PKA apikal CFTR’den klorür salgısını (su izler, kist büyür) ve B-Raf–MEK–ERK üzerinden hücre çoğalmasını sürer. '
       'Polisistin eksikliğinde hücre içi kalsiyum düşer, cAMP yükselir. Tolvaptan V2 reseptörünü bloke eder; TEMPO 3:4’te yıllık hacim artışı yaklaşık yarıya indi.',
       'Şekil: kist epitel hücresi. Kan tarafında vazopressin V2 reseptörüne bağlanır, siklik AMP yükselir, protein kinaz A apikal CFTR kanalından klorürü kist lümenine verir ve su onu izler; '
       'aynı sinyal B-Raf, MEK ve ERK üzerinden hücre çoğalmasını artırır. Tolvaptan V2 reseptörünü bloke eder. Sağda TEMPO 3:4: yıllık böbrek hacmi artışı tolvaptanla yüzde 2,8, plaseboyla yüzde 5,5.')
