#!/usr/bin/env python3
"""Ders 22 · Tübülointerstisyel hastalıklar — şekil tanımları (20 Kasım 2026)."""
import random
from sekil_ortak import *

D = Ders('22')
L = D.L
LENF, EOZ = '#4b3a78', '#e0607a'


def lenfosit(F, x, y, r=4.6): F.el(x, y, r, r, LENF, '#2d2050', .8)


def eozinofil(F, x, y, r=5.6):
    F.el(x, y, r, r, '#f6b3c0', EOZ, 1); F.el(x - 1.8, y, 1.9, 2.2, '#7a3a8f'); F.el(x + 1.8, y, 1.9, 2.2, '#7a3a8f')


# ============================================================================================== 1 · akut ve kronik TİN
F = Fig('tin', 372, 'Akut interstisyel nefrit ve kronik tübülointerstisyel nefritin histolojik farkı', w=1080)
TUB = [(96, 116), (210, 100), (160, 212), (290, 196), (82, 280), (236, 300), (330, 104)]
for p, (x0, bas, c) in enumerate(((6, 'Akut interstisyel nefrit', RED), (546, 'Kronik tübülointerstisyel nefrit', PUR))):
    serit(F, x0, 6, 528, bas, c); zemin(F, x0, 42, 528, 324)
    F.r(x0 + 10, 50, 368, 300, '#fbf1ef' if p == 0 else '#eef2f5', None, rx=8)
    rg = random.Random(7 + p)
    if p == 0:
        for (x, y) in TUB: tubul_kesit(F, x0 + x, y + 0, 34)
        n = 0
        while n < 120:
            x, y = rg.uniform(x0 + 16, x0 + 372), rg.uniform(56, 344)
            if all(math.hypot(x - (x0 + u), y - v) > 42 for u, v in TUB):
                (eozinofil if rg.random() < .14 else lenfosit)(F, x, y); n += 1
        for (u, v, a) in ((96, 116, -30), (96, 116, 60), (96, 116, 170), (210, 100, 200), (210, 100, 110)):
            lenfosit(F, x0 + u + 24 * math.cos(math.radians(a)), v + 24 * math.sin(math.radians(a)), 4.2)
        etk(F, (x0 + 96 + 24 * math.cos(math.radians(-30)), 116 + 24 * math.sin(math.radians(-30))), x0 + 392, 92, ['Tübülit:', 'lenfosit', 'epitelde'], fs=11.6)
        etk(F, (x0 + 46, 180), x0 + 392, 172, ['Mononükleer', 'infiltrasyon'], fs=11.6)
        ez = (x0 + 300, 252)
        eozinofil(F, *ez); etk(F, ez, x0 + 392, 240, ['Eozinofil'], fs=11.6)
        etk(F, (x0 + 196, 156), x0 + 392, 296, ['İnterstisyel', 'ödem: tübüller', 'aralanmış'], fs=11.6)
    else:
        for k in range(26):
            yy = 58 + k * 11.2
            F.yol(f'M{x0 + 14},{yy:.1f} C{x0 + 110},{yy - 6:.1f} {x0 + 240},{yy + 7:.1f} {x0 + 374},{yy:.1f}', '#6a9fb8', 1.6, op=.55)
        TA = [(100, 124), (200, 110), (150, 216), (280, 204), (90, 286), (236, 296), (330, 118)]
        for (x, y) in TA: tubul_kesit(F, x0 + x, y, 30, atrofik=True)
        for _ in range(10):
            x, y = rg.uniform(x0 + 20, x0 + 370), rg.uniform(60, 340)
            if all(math.hypot(x - (x0 + u), y - v) > 30 for u, v in TA): lenfosit(F, x, y)
        etk(F, (x0 + 100 + 21, 124), x0 + 392, 96, ['Tübüler atrofi:', 'kalın TBM,', 'dar lümen'], fs=11.6)
        etk(F, (x0 + 50, 172), x0 + 392, 196, ['İnterstisyel', 'fibroz'], fs=11.6)
        lenfosit(F, x0 + 330, 252); etk(F, (x0 + 330, 252), x0 + 392, 288, ['Az hücresel', 'infiltrasyon'], fs=11.6)
D.yeni('s22_tin', 'x22_5', 'Temel Bilgiler · 2 · Şekil', 'Akut ve Kronik — Ödem ve Hücre ya da Fibroz ve Atrofi', F,
       '<b>Okuma:</b> Akut interstisyel nefritte tübüller ödemle aralanır, interstisyumu mononükleer hücreler ve yer yer eozinofiller doldurur; '
       'lenfositler tübül epitelinin içine girer (tübülit). Kronik tabloda hücre azdır; tübüller atrofiktir ve aralarını fibroz doldurur.',
       'Şekil: solda akut interstisyel nefrit: aralanmış tübüller arasında yoğun lenfosit ve eozinofil infiltrasyonu, tübül epitelinde lenfosit. '
       'Sağda kronik tübülointerstisyel nefrit: kalın bazal membranlı, dar lümenli atrofik tübüller ve aralarında fibroz, az sayıda hücre.')

# ============================================================================================== 2 · aristolokik asit
F = Fig('aa', 352, 'Aristolokik asitten aristolaktam DNA aduktlarına, TP53 imza mutasyonuna ve ürotelyal karsinoma giden yol', w=1080)


def kutu(x, y, w, t1, t2, c, h=58):
    F.r(x, y, w, h, TINT.get(c, '#fff'), c, 1.6, 10); F.t(x + w / 2, y + 23, t1, 12.6, 800, c, 'middle')
    if t2: F.t(x + w / 2, y + 42, t2, 11.4, None, INK, 'middle')


kutu(10, 30, 210, 'Aristolochia clematitis', 'tohumu buğday ununa karışır', GREEN)
F.ok(222, 59, 250, 59, INK2, 2.2)
kutu(252, 30, 180, 'Aristolokik asit', 'ekmekle yıllarca alınır', GOLD)
F.ok(434, 59, 462, 59, INK2, 2.2)
kutu(464, 30, 220, 'Böbrek ve ürotel', 'toksin hücrelere alınır', BRAND)
F.ok(574, 90, 420, 130, RED, 2.2); F.ok(574, 90, 790, 130, PUR, 2.2)
kutu(250, 132, 340, 'dA- ve dG-aristolaktam DNA aduktları', 'böbrek korteksinde var, diğer KBH’de yok', RED)
F.ok(420, 192, 420, 214, RED, 2.2)
kutu(250, 216, 340, 'Üroteldeki tümörde TP53 imzası', '%89’u A:T’de; bunların %78’i A:T → T:A', RED)
F.ok(420, 276, 420, 290, RED, 2.2)
kutu(250, 292, 340, 'Üst üriner sistem ürotelyal karsinomu', None, RED, 46)
kutu(640, 132, 300, 'Proksimal tübül hasarı', 'sinsi, ilerleyici', PUR)
F.ok(790, 192, 790, 214, PUR, 2.2)
kutu(640, 216, 300, 'İnterstisyel fibroz', 'kronik böbrek yetmezliği', PUR)
F.r(10, 132, 220, 206, '#fff', INK2, 1.2, 10)
F.t(22, 156, 'Epidemiyolojik imza', 12.6, 800, INK2)
F.tl(22, 180, ['Belirli köylerde odaklanır', 'Ailesel ama kalıtsal değil:', 'aynı evde yaşayanlar hastalanır,', 'göç edenler hastalanmaz', '', 'Balkan endemik nefropatisi', '(Grollman 2007)'], 11.8, 16, fill=INK)
F.r(960, 132, 112, 160, '#fdeaea', RED, 1.2, 10)
F.tl(970, 156, ['Bitkisel', 'ürünlerde de', 'aynı toksin:', 'aristolokik', 'asit', 'nefropatisi'], 11.6, 16, fill=RED, fw=700)
D.yeni('s22_aa', 'x22_12', 'Toksik · Şekil', 'Aristolokik Asit — Ekmekten DNA’ya', F,
       '<b>Okuma:</b> Aristolochia tohumu buğdayla karışır; aristolokik asit proksimal tübülde hem sinsi tübüler hasara ve fibroza, hem de DNA’ya bağlanarak aristolaktam aduktlarına yol açar. '
       'Ürotelyal tümörlerde TP53’teki A:T → T:A transversiyonu toksinin moleküler imzasıdır.',
       'Şekil: buğday ununa karışan Aristolochia tohumundan aristolokik asit alınır; böbrek ve ürotel hücrelerine girer. Bir kolda aristolaktam DNA aduktları, ürotelyal tümörde TP53 geninde A:T’den T:A’ya transversiyon '
       've üst üriner sistem ürotelyal karsinomu; öbür kolda tübüler hasar ve interstisyel fibrozla kronik böbrek yetmezliği. Solda epidemiyolojik imza: köye odaklanma, ailesel ama kalıtsal olmayan patern.')

# ============================================================================================== 3 · ADTKD: dört gen
F = Fig('adt', 372, 'Otozomal dominant tübülointerstisyel böbrek hastalığında dört ana gen ve ayırt edici bulguları', w=1080)
serit(F, 6, 6, 300, 'Nefronda yer', BRANDD); zemin(F, 6, 42, 300, 324)
F.el(70, 104, 30, 30, '#f1d7d3', '#a2564e', 1.6); F.el(70, 104, 20, 20, '#e7a8a0', None)
F.yol('M100,104 C140,96 150,130 124,140 C100,150 118,176 150,170 L170,168 L170,330 C170,348 194,348 194,330 L194,190 C200,170 230,168 240,186 '
      'C252,206 232,224 250,236 L270,236 L270,354', '#8aa9bd', 10, 'none')
F.yol('M100,104 C140,96 150,130 124,140 C100,150 118,176 150,170 L170,168 L170,330 C170,348 194,348 194,330 L194,190 C200,170 230,168 240,186 '
      'C252,206 232,224 250,236 L270,236 L270,354', '#eaf3f8', 6, 'none')
F.ln(14, 92, 46, 98, '#c0392b', 5); F.r(26, 86, 16, 12, '#f2d27a', '#b98a1e', 1.2, 3)
F.yol('M100,104 C140,96 150,130 124,140 C100,150 118,176 150,170 L170,168 L170,330 C170,348 194,348 194,330 L194,190 C200,170 230,168 240,186 '
      'C252,206 232,224 250,236 L270,236 L270,354', PUR, 15, 'none', op=.16)
for (x, y, c) in ((34, 92, GOLD), (194, 260, RED), (270, 300, BRAND)): F.el(x, y, 7, 7, c, '#fff', 1.6)
F.t(16, 122, 'REN', 12, 800, GOLD); F.t(16, 137, 'JG hücresi', 10.8, None, INK2)
F.t(206, 264, 'UMOD', 12, 800, RED); F.t(258, 296, 'MUC1', 12, 800, BRAND, 'end')
F.t(210, 120, 'HNF1B:', 12, 800, PUR); F.t(210, 135, 'tüm nefron', 11, None, PUR)
K = [('ADTKD-UMOD', RED, ['Erken başlangıçlı gut, hiperürisemi', 'Uromodulin yanlış katlanır, ER’de birikir', 'Ürik asidin fraksiyonel atılımı düşük', 'SDBY 30–70 yaş; allopurinol seyri değiştirmez']),
     ('ADTKD-MUC1', BRAND, ['Ayırt edici böbrek dışı bulgu yok', 'VNTR bölgesinde sitozin insersiyonu', 'Standart dizileme saptamaz — özel yöntem', 'SDBY 30–60 yaş; gut daha seyrek']),
     ('ADTKD-REN', GOLD, ['Çocuklukta anemi, hiperkalemi,', 'hafif hipotansiyon, hiperürisemi', 'Renin ↓ → aldosteron ↓ → tuz kaybı', 'RAS blokajı ve NSAİİ’den kaçınılır']),
     ('ADTKD-HNF1B', PUR, ['Böbrek kisti + MODY5 + hipomagnezemi', 'Hipokalemi, karaciğer enzimi ↑,', 'genital anomali, pankreas hipoplazisi', 'Sıklıkla 17q12 delesyonu (de novo olabilir)'])]
for i, (ad, c, sat) in enumerate(K):
    x = 318 + (i % 2) * 380; y = 6 + (i // 2) * 182
    F.r(x, y, 370, 172, TINT.get(c, '#fff'), c, 1.6, 10); F.t(x + 14, y + 26, ad, 14, 800, c)
    F.tl(x + 14, y + 56, sat, 12, 22, fill=INK)
D.yeni('s22_adt', 'x22_16', 'Sınıflama · Şekil', 'ADTKD — Dört Gen, Dört İpucu', F,
       '<b>Okuma:</b> Sessiz sediment ve az proteinüriyle ilerleyen ailesel böbrek yetmezliğinde gen, ipucuyla tahmin edilir: erken gut (UMOD), '
       'ipucu yok ve özel test gerekir (MUC1), çocuklukta anemi ve hiperkalemi (REN), kist + diyabet + hipomagnezemi (HNF1B).',
       'Şekil: solda nefron üzerinde genlerin başlıca yeri: renin jukstaglomerüler hücrede, uromodulin kalın çıkan kolda, HNF1B birçok segmentte. '
       'Sağda dört kart: UMOD erken gut ve hiperürisemi; MUC1 böbrek dışı bulgu yok, özel genetik yöntem gerekir; REN çocuklukta anemi, hiperkalemi, hipotansiyon; '
       'HNF1B böbrek kisti, MODY5 diyabeti ve hipomagnezemi.')
