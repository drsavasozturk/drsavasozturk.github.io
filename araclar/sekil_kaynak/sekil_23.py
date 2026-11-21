#!/usr/bin/env python3
"""Ders 23 · Böbreğin Vasküler Hastalıkları — şekil tanımları (20 Kasım 2026)."""
from sekil_ortak import *
from sekil_gk import GK
import sekil_anat as AN

D = Ders('23')
L = D.L


def kart(F, x, y, w, h, bas, satirlar, c, fs=12.2, lh=16):
    F.r(x, y, w, h, TINT.get(c, '#fff'), c, 1.5, 10); F.t(x + 12, y + 22, bas, 13, 800, c)
    F.tl(x + 12, y + 42, satirlar, fs, lh, fill=INK)


def arter(F, cx, cy, R, lumen, katman=0, fibrinoid=False, trombus=False, ad=None):
    """Arter kesiti: adventisya, media (kas), intima; katman>0 ise soğan zarı (eş merkezli intimal tabakalar)."""
    F.el(cx, cy, R, R, '#f3e3d6', '#b98c6b', 1.6)                       # adventisya
    F.el(cx, cy, R * .82, R * .82, '#e7a8a0', '#a2564e', 1.4)            # media
    if fibrinoid:
        F.yol(f'M{cx - R * .8:.1f},{cy - R * .1:.1f} A{R * .8:.1f},{R * .8:.1f} 0 0 1 {cx + R * .55:.1f},{cy - R * .58:.1f} '
              f'L{cx + R * .32:.1f},{cy - R * .36:.1f} A{R * .48:.1f},{R * .48:.1f} 0 0 0 {cx - R * .48:.1f},{cy - R * .06:.1f} Z', '#a82447', 1.2, FIB, op=.9)
    ic = R * .62
    if katman:
        for i in range(katman):
            r = ic - i * (ic - lumen) / katman
            F.el(cx, cy, r, r, '#f8efe6' if i % 2 else '#efe0d2', '#c9a98d', 1)
    else:
        F.el(cx, cy, ic, ic, '#f8efe6', '#c9a98d', 1)
    F.el(cx, cy, lumen, lumen, '#fff' if not trombus else '#fff', '#b98c6b', 1.2)
    if trombus: F.el(cx, cy, lumen * .82, lumen * .7, FIB, '#a82447', 1.2, op=.92)
    if ad: F.t(cx, cy + 92, ad, 12.6, 800, INK, 'middle')


# ============================================================================================== 1 · TMA: akut ve kronik glomerül
F = Fig('tma', 400, 'Trombotik mikroanjiyopatide akut ve kronik glomerül lezyonları', w=1080)
serit(F, 6, 6, 528, 'Akut TMA', RED); zemin(F, 6, 42, 528, 352)
A = GK(F, 'lobul', 14, 50, 300, cerceve=LINE); A.kose(44)
A.endotel_sis(0, kalin=46); A.endotel_sis(1, kalin=40); A.trombus(2)
P = A.lumen_noktalar(0, 3, 15)
for i, p in enumerate(P):
    x, y = A.xy(p); r = 7 - i * .6                                                 # miğfer hücresi (şistosit)
    F.a(f'<g transform="rotate({40 * i - 20} {x:.1f} {y:.1f})"><path d="M{x - r:.1f},{y + 2:.1f} A{r:.1f},{r:.1f} 0 0 1 {x + r:.1f},{y + 2:.1f} L{x + r * .35:.1f},{y - r * .25:.1f} L{x - r * .15:.1f},{y + 2:.1f} Z" fill="#d9584f" stroke="#a8332c" stroke-width=".8"/></g>')
A.etiket(A.duvar(0, 330, 'endotel'), 326, 84, ['Şişmiş endotel,', 'daralmış lümen'])
A.etiket(P[0], 326, 168, ['Parçalanmış eritrosit', '(şistosit)'])
A.etiket(A.lumen_noktalar(2, 1, 24)[0], 326, 262, ['Fibrin trombüsü', 'lümeni tıkar'])
F.tl(20, 384, ['Mezangiyoliz ve arteriyolde fibrinoid nekroz da görülebilir.'], 11.6, 15, fill=INK2)
serit(F, 546, 6, 528, 'Kronik TMA', PUR); zemin(F, 546, 42, 528, 352)
B = GK(F, 'lobul', 554, 50, 300, cerceve=LINE); B.kose(44)
B.cift_kontur(0, 166, 30); B.cift_kontur(2, 182, 296)
B.etiket(B.kp(0, 268, B.R(0, 268)[0] - 25), 866, 92, ['Yeni bazal membran:', 'GBM çift kontur'])
B.etiket(B.kp(2, 240, B.R(2, 240)[0] - 12), 866, 206, ['Araya giren mezangiyum', 've içe itilmiş endotel'])
F.tl(560, 384, ['Arterlerde soğan zarı, iskemik glomerül retraksiyonu, kortikal atrofi.'], 11.6, 15, fill=INK2)
D.yeni('s23_tma', 'x23_5', 'Temel Bilgiler · 2 · Şekil', 'TMA — Bir Lezyon, İki Evre', F,
       '<b>Okuma:</b> Akut evrede endotel şişer ve lümen daralır, kapillerde fibrin trombüsü ve parçalanmış eritrositler görülür. '
       'Hasar sürerse endotelin altında yeni bazal membran yapılır; GBM çift kontur verir. Görünüm nedeni söylemez: aynı lezyon onlarca nedenden doğar.',
       'Şekil: solda akut trombotik mikroanjiyopatide glomerül lobülü. Endotel şişmiş, lümenler daralmış, bir kapilleri fibrin trombüsü dolduruyor, '
       'lümende parçalanmış eritrositler var. Sağda kronik evre: endotelin altında yeni bazal membran oluşmuş, glomerül bazal membranı çift kontur veriyor.')

# ============================================================================================== 2 · Goldblatt: 2K-1C ve 1K-1C
F = Fig('gold', 380, 'Renovasküler hipertansiyonda iki böbrek tek darlık ve tek böbrek tek darlık modelleri', w=1080)
# Resimler: ChatGPT ile çizildi (yazısız, 820 × 557 px); konumlar resim pikselinden.
GS = 368 / 820


def model(x0, baslik, c, iki):
    serit(F, x0, 6, 528, baslik, c); zemin(F, x0, 42, 528, 332)
    ix, iy = x0 + 80, 46
    def P(px, py): return (ix + px * GS, iy + py * GS)
    AN.resim(F, 'an_gold_a' if iki else 'an_gold_b', ix, iy, 368, oran=557 / 820)
    if iki: ao, kl, bk, sk = 465, (328, 290), (170, 300), (720, 310)
    else: ao, kl, bk, sk = 485, (350, 300), (190, 300), (720, 310)
    k = P(*bk); F.t(k[0], 272, 'Darlıklı böbrek', 12.4, 800, INK, 'middle'); rozet(F, k[0], 291, 'renin ↑' if iki else 'renin ↑ (erken)', RED)
    AN.ad(F, *P(ao - 42, 70), 'aorta', 11.4, INK2, 'end', 700)
    s_ = P(*sk)
    if iki:
        F.t(s_[0], 272, 'Sağlam böbrek', 12.4, 800, INK, 'middle')
        F.t(s_[0], 290, 'basınç natriürezi → tuz atılır', 11.4, 700, GREEN, 'middle')
    else:
        F.yol(f'M{s_[0]},{s_[1] - 50} C{s_[0] - 30},{s_[1] - 50} {s_[0] - 34},{s_[1] + 50} {s_[0]},{s_[1] + 50} C{s_[0] + 30},{s_[1] + 50} {s_[0] + 34},{s_[1] - 50} {s_[0]},{s_[1] - 50} Z', INK2, 1.6, 'none', dash='5 4')
        F.t(s_[0], 272, 'Karşı böbrek yok', 12.4, 800, INK2, 'middle')
        F.t(s_[0], 290, '(ya da iki taraflı darlık)', 11.4, None, INK2, 'middle')
    q = P(*kl); a0 = P(ao, 40); a1 = P(ao, 540)
    F.a(f'<g data-etk="g" data-tip="{"2k" if iki else "1k"}" data-klips="{q[0]:.1f},{q[1]:.1f}" data-bob="{k[0] + 18:.1f},{k[1]:.1f}" '
        f'data-ao="{a0[0]:.1f},{a0[1]:.1f},{a1[1]:.1f}" data-kut="{x0 + 18},{54}" data-faz="{P(ao, 0)[0] + 22:.1f},{62}"></g>')


model(6, 'İki böbrek, tek darlık (2K-1C)', BRAND, True)
F.r(18, 308, 504, 56, '#fff', BRAND, 1.4, 10)
F.t(32, 330, 'Renin bağımlı · volüm normal', 13, 800, BRAND)
F.t(32, 350, 'RAAS blokajı kan basıncını iyi düşürür; toplam kreatinin çoğu kez korunur.', 11.8, None, INK)
model(546, 'Tek böbrek, tek darlık (1K-1C)', RED, False)
F.r(558, 308, 504, 56, '#fff', RED, 1.4, 10)
F.t(572, 330, 'Önce renin ↑, sonra tuz ve su tutulur → volüm bağımlı', 13, 800, RED)
F.t(572, 350, 'RAAS blokajı tehlikeli: tüm nefronların filtrasyonu efferent tonusa bağlı.', 11.8, None, INK)
D.yeni('s23_gold', 'x23_6', 'Temel Bilgiler · 3 · Şekil', 'Goldblatt Modelleri — Karşı Böbrek Her Şeyi Değiştirir', F,
       '<b>Okuma:</b> Solda darlıklı böbrek renin salgılar, sağlam böbrek artan basınçla tuzu atar; tablo renin bağımlıdır. '
       'Sağda bütün böbrek kütlesi darlığın arkasındadır; tuz ve su tutulur, tablo volüm bağımlı hâle gelir ve RAAS blokajı filtrasyonu çökertebilir.',
       'Şekil: solda iki böbrek tek darlık modeli. Darlıklı böbrek renin salgılar, karşı sağlam böbrek basınç natriürezi ile tuzu atar; tablo renin bağımlıdır. '
       'Sağda tek böbrek ya da iki taraflı darlık: önce renin yükselir, sonra tuz ve su tutulur ve tablo volüm bağımlı olur; burada RAAS blokajı tehlikelidir.')

# ============================================================================================== 3 · malign hipertansiyon: arter kesitleri ve kısır döngü
F = Fig('mht', 360, 'Malign hipertansiyonda arter ve arteriyol lezyonları ile kısır döngü', w=1080)
serit(F, 6, 6, 640, 'Damar duvarı', BRANDD); zemin(F, 6, 42, 640, 312)
MS = 620 / 2052                                  # resim: ChatGPT ile çizildi (yazısız, 2052 × 684 px)
AN.resim(F, 'an_mht', 16, 46, 620, oran=684 / 2052)
for cx, ad in ((450, 'Normal interlobüler arter'), (1119, 'Soğan zarı (onion-skin)'), (1778, 'Arteriyol: fibrinoid nekroz')):
    F.t(16 + cx * MS, 268 - 14, ad, 12.6, 800, INK, 'middle')
F.tl(30, 280, ['Eş merkezli intimal tabakalar lümeni iğne ucuna indirir.', 'Arteriyol duvarı fibrinle dolar, lümende trombüs oluşur.',
               'Sonuç: iskemi ve mikroanjiyopatik hemoliz — ikincil TMA.'], 12, 17, fill=INK)
serit(F, 656, 6, 418, 'Kısır döngü', RED); zemin(F, 656, 42, 418, 312)
K = [(865, 84, 'Çok yüksek kan basıncı'), (972, 170, 'Damar hasarı ve iskemi'), (865, 256, 'Renin–anjiyotensin ↑'), (758, 170, 'Basınç natriürezi → volüm ↓')]
for x, y, t in K:
    w = gen(t, 12.4, True) + 22; F.r(x - w / 2, y - 16, w, 32, '#fff', RED, 1.5, 16); F.t(x, y + 4.5, t, 12.4, 800, INK, 'middle')
F.yol('M925,100 Q972,118 972,150', RED, 2.4, ok=True); F.yol('M972,190 Q972,226 922,238', RED, 2.4, ok=True)
F.yol('M758,190 Q758,232 806,238', RED, 2.4, ok=True); F.yol('M806,94 Q758,112 758,150', RED, 2.4, ok=True)
F.ok(865, 238, 865, 104, RED, 2.4); F.t(872, 132, 'basınç ↑', 11.4, 700, RED)
F.tl(672, 306, ['Hasta çoğu kez hipovolemiktir;', 'agresif diüretik zararlıdır.'], 12, 16, fill=RED, fw=700)
D.yeni('s23_mht', 'x23_7', 'Temel Bilgiler · 4 · Şekil', 'Malign Hipertansiyon — Soğan Zarı, Fibrinoid Nekroz ve Kısır Döngü', F,
       '<b>Okuma:</b> İnterlobüler arterlerde eş merkezli intimal çoğalma (soğan zarı), arteriyollerde fibrinoid nekroz ve trombüs lümeni kapatır. '
       'İskemi renin–anjiyotensini uyarır, basınç daha da yükselir; basınç natriürezi volümü azaltır ve RAAS’ı ayrıca uyarır.',
       'Şekil: solda normal interlobüler arter, soğan zarı görünümünde lümeni daralmış arter ve fibrinoid nekrozlu, trombüslü arteriyol. '
       'Sağda kısır döngü: yüksek basınç damar hasarı ve iskemiye, iskemi renin ve anjiyotensin artışına, bu da basıncın daha da artmasına yol açar; '
       'basınç natriürezi volümü azaltarak döngüyü besler.')

# ============================================================================================== 4 · TMA ayırıcı tanı: üç anahtar test
F = Fig('tmaa', 362, 'Trombotik mikroanjiyopatide üç anahtar testle ayırıcı tanı akışı', w=1080)
F.r(330, 8, 420, 50, '#fff', INK2, 1.6, 12)
F.t(540, 30, 'TMA: şistosit + trombositopeni + organ hasarı', 13.2, 800, INK, 'middle'); F.t(540, 48, 'DIC dışlandı (PT/aPTT, fibrinojen)', 11.6, None, INK2, 'middle')


def adim(x, y, w, t1, t2, c):
    F.r(x, y, w, 46, TINT.get(c, '#fff'), c, 1.6, 10); F.t(x + w / 2, y + 20, t1, 12.6, 800, c, 'middle'); F.t(x + w / 2, y + 37, t2, 11.4, None, INK2, 'middle')


adim(60, 92, 230, '1 · ADAMTS13 aktivitesi', '(ve inhibitör)', PUR); F.ok(420, 58, 230, 90, INK2, 2.2)
kart(F, 22, 186, 306, 132, 'TTP · ADAMTS13 < %10', ['Nörolojik bulgu baskın, böbrek görece hafif;', 'trombositopeni derin (sıklıkla < 30.000)', '→ acil plazma değişimi + kortikosteroid', '+ kaplasizumab ± rituksimab'], PUR, 11.6, 16)
F.ok(175, 138, 175, 184, PUR, 2.2)
adim(400, 92, 280, '2 · Gaitada Shiga toksini / STEC', 'ADAMTS13 normal ise', GOLD); F.ok(292, 115, 398, 115, INK2, 2.2)
kart(F, 386, 186, 306, 132, 'STEC-HÜS · Shiga toksini +', ['Kanlı ishal öyküsü, çoğunlukla çocuk', '→ destek tedavi: sıvı, elektrolit,', 'gerekirse diyaliz; antibiyotik ve', 'antimotiliteden kaçınılır'], GOLD, 11.6, 16)
F.ok(540, 138, 540, 184, GOLD, 2.2)
adim(790, 92, 268, '3 · Kompleman değerlendirmesi', 'ikisi de negatifse; ikincil neden?', RED); F.ok(682, 115, 788, 115, INK2, 2.2)
kart(F, 750, 186, 324, 132, 'aHÜS ya da ikincil TMA', ['aHÜS: böbrek baskın → gecikmeden', 'ekülizumab ya da ravulizumab', '(meningokok aşısı/profilaksisi zorunlu)', 'İkincil: nedeni tedavi et, ilacı kes'], RED, 11.6, 16)
F.ok(924, 138, 924, 184, RED, 2.2)
F.t(540, 334, 'Testler tedaviyi geciktirmez: TTP olasılığı varsa plazma değişimi sonuç beklenmeden başlar.', 12, 800, RED, 'middle')
F.t(540, 354, 'Gebelikte ayrıca: preeklampsi/HELLP, gebelikle ilişkili aHÜS, TTP (Ders 42).', 11.6, None, INK2, 'middle')
D.yeni('s23_tmaa', 'x23_10', 'Ayırıcı Tanı · Şekil', 'TMA Ayırıcı Tanısı — Üç Test, Üç Yol', F,
       '<b>Okuma:</b> Önce ADAMTS13: %10’un altındaysa TTP. Normalse gaitada Shiga toksini aranır: pozitifse STEC-HÜS. '
       'İkisi de negatifse kompleman değerlendirilir ve ikincil nedenler (ilaç, malignite, nakil, enfeksiyon, otoimmün hastalık, malign hipertansiyon, B12 eksikliği) taranır.',
       'Şekil: trombotik mikroanjiyopatide üç anahtar test. ADAMTS13 aktivitesi yüzde onun altındaysa TTP; normalse gaitada Shiga toksini pozitifse STEC ilişkili HÜS; '
       'ikisi de negatifse kompleman değerlendirmesi ile kompleman aracılı HÜS ya da ikincil TMA ayrılır. Her grubun tedavisi kutuda yazıyor.')

# ============================================================================================== 5 · FMD, aterosklerotik darlık ve kolesterol embolisi
F = Fig('fmd', 356, 'Aterosklerotik renal arter darlığı, fibromusküler displazi ve kolesterol ateroembolizmi', w=1080)
serit(F, 6, 6, 660, 'Renal arter görüntüsü', BRANDD); zemin(F, 6, 42, 660, 308)
# Resimler: ChatGPT ile çizildi (yazısız; 840 × 360 ve 860 × 360 px, üst-alt kenar soluklaştırıldı)
for x0, bas, fmd, ad, pw in ((16, 'Aterosklerotik darlık', False, 'an_fmd_a', 840), (340, 'Fibromusküler displazi', True, 'an_fmd_b', 860)):
    F.t(x0 + 155, 70, bas, 13.2, 800, INK, 'middle')
    s_ = 310 / pw
    AN.resim(F, ad, x0, 84, 310, oran=360 / pw)
    if not fmd:
        q = (x0 + 220 * s_, 84 + 232 * s_)
        F.ln(q[0], q[1], q[0], 226, INK2, 1.2); F.el(q[0], q[1], 2.6, 2.6, '#fff', INK2, 1.1)
        F.t(q[0] + 4, 242, 'ostiyal / proksimal plak', 11.8, 700, INK, 'middle')
        F.tl(x0 + 10, 270, ['Yaşlı, aterosklerotik risk; girişim', 'çoğu hastada ilaç tedavisine üstün değil'], 11.4, 15, fill=INK2)
    else:
        q = (x0 + 650 * s_, 84 + 236 * s_)
        F.ln(q[0], q[1], q[0], 226, INK2, 1.2); F.el(q[0], q[1], 2.6, 2.6, '#fff', INK2, 1.1)
        F.t(q[0] - 30, 242, '“boncuk dizisi”: orta–distal segment', 11.8, 700, INK, 'middle')
        F.tl(x0 + 10, 266, ['Genç–orta yaş kadınlarda daha sık; girişim', 'gereken olgularda ilk seçenek stentsiz balon', 'anjiyoplastidir. Stent yalnızca gerekli', 'komplikasyonlarda kullanılır.'], 11.4, 15, fill=INK2)
serit(F, 676, 6, 398, 'Kolesterol ateroembolizmi', RED); zemin(F, 676, 42, 398, 308)
F.el(875, 150, 120, 92, '#f3e3d6', '#b98c6b', 1.6); F.el(875, 150, 100, 76, '#e7a8a0', '#a2564e', 1.4); F.el(875, 150, 78, 58, '#f8efe6', '#c9a98d', 1.2)
for (x, y, a) in ((840, 130, -18), (880, 160, 12), (905, 130, -30), (850, 170, 25), (900, 178, -8)):
    F.a(f'<ellipse cx="{x}" cy="{y}" rx="19" ry="4.2" transform="rotate({a} {x} {y})" fill="#fff" stroke="#9aa9b5" stroke-width="1.2"/>')
F.a('<ellipse cx="905" cy="130" rx="27" ry="13" transform="rotate(-30 905 130)" fill="#c9a7d6" stroke="#7d5a92" stroke-width="1.2" opacity=".85"/>')
F.a('<ellipse cx="905" cy="130" rx="19" ry="4.2" transform="rotate(-30 905 130)" fill="#fff" stroke="#9aa9b5" stroke-width="1.2"/>')
for (u, v) in ((886, 132), (896, 141), (915, 124), (922, 115), (900, 118)): F.el(u, v, 2.6, 2.6, '#5c3e74')
etk(F, (880, 160), 692, 270, ['İğ biçimli boş yarıklar (kolesterol kristali)'], True, fs=11.8)
etk(F, (922, 116), 978, 72, ['Çok çekirdekli', 'dev hücre'], True, fs=11.8)
F.tl(692, 296, ['Tetikleyici: anjiyografi, endovasküler girişim,', 'kardiyak cerrahi, antikoagülan/trombolitik.', 'Kreatinin girişimden 1–4 hafta sonra, basamaklı yükselir.'], 11.4, 15, fill=INK2)
D.yeni('s23_fmd', 'x23_14', 'İki Tanı · Şekil', 'Darlığın Yeri ve Kolesterol Kristali', F,
       '<b>Okuma:</b> Aterosklerotik darlık aort çıkışında, proksimaldedir; fibromusküler displazi orta–distal segmentte “boncuk dizisi” verir. '
       'Kolesterol embolisinde arkuat ve interlobüler arterlerde iğ biçimli boş yarıklar görülür: kristaller doku işlemi sırasında çözünür.',
       'Şekil: solda aorttan çıkan renal arter. Aterosklerotik darlık ostiyumda, proksimalde plakla; fibromusküler displazi orta ve distal segmentte boncuk dizisi görünümüyle. '
       'Sağda kolesterol ateroembolizminde küçük arter kesiti: lümende iğ biçimli boş yarıklar ve bir yarığı saran çok çekirdekli dev hücre.')
