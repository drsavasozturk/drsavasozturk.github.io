#!/usr/bin/env python3
"""Ders 08 · Fokal Segmental Glomerüloskleroz — şekiller."""
from sekil_ortak import *
from sekil_gk import *
D = Ders('08'); L = D.L

# ---------------------------------------------------------------- 1 · Columbia: beş varyant
F = Fig('col', 410, 'Columbia sınıflamasına göre FSGS’nin beş histolojik varyantı', w=1080)
VAR = [('Kollapsing', 'kol', ['Kapiller kollaps + üstteki', 'podositlerde hipertrofi', 've hiperplazi'], ('En kötü prognoz', RED)),
       ('Tip lezyonu', 'tip', ['Lezyon tübüler kutupta,', 'proksimal tübül çıkışının', 'bitişiğinde'], ('En iyi prognoz', GREEN)),
       ('Hücresel', 'huc', ['Endokapiller hiperselülarite', '(köpük hücreleri olabilir),', 'sklerozdan önce'], ('Erken lezyon', GOLD)),
       ('Perihilar', 'per', ['Vasküler kutupta skleroz', 've hiyalinoz (tutulan', 'glomerüllerin >%50’si)'], ('Adaptifte sık', BRAND)),
       ('NOS', 'nos', ['Öteki varyantların ölçütü', 'yok; segmental skleroz', 'başka bir yerde'], ('En sık varyant', INK2))]
for i, (ad, tur, sat, (rz, rc)) in enumerate(VAR):
    x = 6 + i * 216; cx = x + 104
    serit(F, x, 6, 208, ad, rc if rc != INK2 else BRANDD)
    zemin(F, x, 40, 208, 214)
    G = GK(F, 'yumak', cx - 90, 44, 180, kirp=(0, 20, 680, 800))
    if tur == 'kol': G.kollaps(pod=(330, 150))
    elif tur == 'tip':
        G.skleroz(62, 118, derin=.34); kp_ = G.kopuk(3, 40, 140)
        if kp_: etk(F, G.xy(kp_[0]), x + 200, 236, ['köpük hücreleri'], False, fs=10.5, kalin=False)
    elif tur == 'huc': G.cekirdekler(34, 150, 235); G.kopuk(4, 150, 235)
    elif tur == 'per': G.skleroz(236, 304, derin=.38); G.hiyalinoz()
    else: G.skleroz(160, 222, derin=.38)
    F.tl(cx, 278, sat, 12, 16, fill=INK, a='middle')
    rozet(F, cx, 344, rz, rc)
F.t(6, 386, 'Değerlendirme sırası:', 12.4, 800, BRANDD)
xx = 152
for j, ad in enumerate(['kollapsing (bir glomerül yeter)', 'tip', 'hücresel', 'perihilar', 'NOS']):
    w = hap(F, xx, 382, ad, BRAND, 12); xx += w + 6
    if j < 4: F.ok(xx - 2, 382, xx + 14, 382, INK2, 2); xx += 20
D.yeni('s08_col', 'x08_5', 'Temel Bilgiler · 2 · Şekil', 'Columbia Sınıflaması — Beş Varyant, Beş Glomerül', F,
       '<b>Okuma:</b> Her çizimde üstte vasküler kutup (afferent ve efferent arteriyol), altta proksimal tübüle açılan tübüler kutup var. Tip lezyonu tübüler kutupta, '
       'perihilar lezyon vasküler kutupta oturur; lezyonun yeri adı belirler. Sınıflama prognoz verir, primer ile sekonderi ayırmaz.',
       'Şekil: fokal segmental glomerülosklerozun beş varyantı. Kollapsingde kapiller yumak çöker ve üstündeki podositler çoğalır. Tip lezyonu proksimal tübülün çıkış yerindedir. '
       'Hücreselde kapiller lümenler köpük hücreleriyle dolar. Perihilar lezyon vasküler kutuptadır ve hiyalinoz eşlik eder. NOS ötekilerin ölçütünü karşılamaz. Değerlendirme bu sırayla yapılır.')

# ---------------------------------------------------------------- 2 · primer mi adaptif mi: EM ve glomerül boyutu
F = Fig('pad', 448, 'Primer ve adaptif FSGS’de ayaksı çıkıntı silinmesinin yaygınlığı ve glomerül boyutu', w=1080, mh=410)
for (x, bas, c) in ((6, 'Primer FSGS', RED), (546, 'Adaptif FSGS (sekonder FSGS’nin bir türü)', BRAND)):
    serit(F, x, 6, 528, bas, c); zemin(F, x, 42, 528, 322)
A = GK(F, 'lobul', 16, 66, 286, cerceve=LINE); ka = A.kose(40)
A.silinme(0, 158, 36); A.silinme(1, 272, 80); A.silinme(2, 176, 303)
A.etiket(A.duvar(0, 330, 'subepi'), 330, 110, ['Yaygın silinme', '(>%80, difüz)'])
A.etiket(A.duvar(0, 12, 'gbm'), 330, 222, ['GBM normal'])
F.t(20, 59, 'Glomerül boyutu normal', 11.5, 800, INK2)
B = GK(F, 'lobul', 556, 66, 286, cerceve=LINE); kb = B.kose(62)
B.silinme(0, 300, 30)
B.etiket(B.duvar(0, 345, 'subepi'), 870, 92, ['Segmental silinme', '(genellikle <%50)'])
B.etiket(B.duvar(2, 260, 'ayak'), 870, 236, ['Korunmuş ama', 'gerilmiş ayaksı', 'çıkıntılar'])
F.t(560, 59, 'Glomerülomegali (büyük glomerül)', 11.5, 800, BRAND)
haplar(F, 14, 392, 510, ['Ani başlangıç', 'Albümin düşük', 'Ödem belirgin', 'İmmünsüpresyon endike'], RED, 12)
haplar(F, 554, 392, 510, ['Sinsi başlangıç', 'Albümin normal', 'Ödem yok ya da hafif', 'RAAS blokajı, nedene yönelik'], BRAND, 12)
D.yeni('s08_pad', 'x08_8', 'Temel Bilgiler · 4 · Şekil', 'Primer mi Adaptif mi — EM ve Glomerül Boyutu Söyler', F,
       '<b>Okuma:</b> Primer FSGS’de dolaşan bir etken bütün podositleri etkiler; silinme yaygındır. Adaptif FSGS’de glomerül büyümüştür, podositler gerilmiştir ve silinme yalnız '
       'bazı bölgelerdedir. Ayrımı histolojik varyant değil, klinik tablo ve EM yapar.',
       'Şekil: solda primer, sağda adaptif fokal segmental glomerüloskleroz. Primerde ayaksı çıkıntılar yaygın olarak silinmiştir ve glomerül normal boyuttadır. '
       'Adaptifte glomerül büyümüştür, ayaksı çıkıntılar gerilmiştir ve silinme segmentaldir. Altta klinik farklar.')

# ---------------------------------------------------------------- 3 · örnekleme
F = Fig('ork', 336, 'FSGS’de örnekleme hatası: yüzeyel korteks örneği ve glomerül sayısına göre lezyonu kaçırma olasılığı', w=1080)
F.t(6, 22, 'Korteks kesiti: lezyon önce derin korteksi tutar', 13.5, 800, BRANDD)
F.r(20, 40, 560, 230, '#fbf3ec', '#d9b9a0', 1.4, 0); F.r(20, 270, 560, 28, '#f1e3d6', None, rx=0)
for xx in range(28, 580, 14): F.ln(xx, 272, xx + 6, 296, '#e0c9b4', 2)
F.ln(14, 40, 586, 40, '#9a7b62', 3)
F.t(590, 46, 'kapsül', 11.5, 700, '#7a5b42'); F.t(590, 286, 'medulla', 11.5, 700, '#7a5b42')
F.t(30, 62, 'yüzeyel korteks', 11.5, 800, '#7a5b42'); F.t(30, 260, 'jukstamedüller (derin) korteks', 11.5, 800, '#7a5b42')
rng = random.Random(4)
gl = []
for yy in range(78, 256, 30):
    for xx in range(46, 570, 34):
        gl.append((xx + rng.uniform(-8, 8), yy + rng.uniform(-6, 6)))
def mini_g(x, y, lez):
    F.el(x, y, 10, 10, BOW, GBM_K, 1.1); F.el(x, y, 7.2, 7.2, '#f4b7b4', '#c95c58', .8)
    if lez: F.yol(f'M{x:.1f},{y:.1f} L{x + 7.6:.1f},{y - 2:.1f} A7.6,7.6 0 0 1 {x - 1:.1f},{y + 7.6:.1f} Z', '#4f5f68', .9, '#8c9ba4')
for (x, y) in gl:
    lez = (y > 200 and rng.random() < .45) or (180 < y <= 200 and rng.random() < .3)
    mini_g(x, y, lez)
F.r(150, 34, 70, 140, 'none', BRAND, 2.4, 10, dash='7 4'); F.etiket(228, 112, 150, ['Yüzeyel örnek', 'lezyon yok →', '“MDH” raporu'], BRAND, 12, fill='#ffffff')
F.r(400, 34, 70, 250, 'none', GREEN, 2.4, 10, dash='7 4'); F.etiket(476, 112, 108, ['Derin korteksi', 'de içeren', 'örnek'], GREEN, 12, fill='#ffffff')
mini_g(30, 320, False); F.t(46, 324, 'normal glomerül', 11.5, None, INK2); mini_g(170, 320, True); F.t(186, 324, 'segmental skleroz', 11.5, None, INK2)
F.ln(640, 10, 640, 330, LINE, 1.5)
F.t(664, 22, 'Örnek hesap: lezyonu hiç görmeme olasılığı', 13.5, 800, BRANDD)
GX, GY, GW, GH = 708, 52, 350, 214
for v in (0, 25, 50, 75, 100):
    yy = GY + GH - v * GH / 100; F.ln(GX, yy, GX + GW, yy, LINE if v else INK2, 1 if v else 1.8, '3 4' if v else None); F.t(GX - 8, yy + 4, f'%{v}', 11.2, None, MUT, 'end')
ns = [5, 10, 15, 20, 25, 30]
for n in ns:
    x = GX + (n - 5) * GW / 25; F.t(x, GY + GH + 18, str(n), 11.5, None, MUT, 'middle')
F.t(GX + GW, GY + GH + 36, 'biyopsideki glomerül sayısı', 11.5, None, MUT, 'end')
for (p_, c, ad) in ((.1, RED, 'glomerüllerin %10’u tutulmuşsa'), (.2, GOLD, '%20’si tutulmuşsa')):
    pts = [(GX + (n - 5) * GW / 25, GY + GH - (1 - p_) ** n * GH) for n in range(5, 31)]
    F.yol('M' + ' L'.join('%.1f,%.1f' % q for q in pts), c, 3)
    for n in ns:
        v = (1 - p_) ** n * 100; q = (GX + (n - 5) * GW / 25, GY + GH - v * GH / 100); F.el(q[0], q[1], 4, 4, c, '#fff', 1.2)
        if n == 10: F.t(q[0] + 7, q[1] - 7, ('%' + f'{v:.0f}'), 11.6, 800, c)
    ly = GY + 14 + (0 if p_ == .1 else 22); F.ln(GX + 150, ly - 4, GX + 178, ly - 4, c, 3); F.t(GX + 184, ly, ad, 11.8, 800, c)
F.t(664, 316, '(1 − p)ⁿ; bağımsız örnekleme varsayımı — çalışma verisi değildir.', 11.2, None, MUT)
D.yeni('s08_ork', 'x08_9', 'Temel Bilgiler · 5 · Şekil', 'FSGS Neden Kaçırılır — Derin Korteks ve Glomerül Sayısı', F,
       '<b>Okuma:</b> Lezyon fokaldir ve erken dönemde derin korteksi tutar; yüzeyel bir örnekte hiç görülmeyebilir. Sağdaki eğriler basit bir olasılık hesabıdır: glomerüllerin '
       '%10’u tutulmuşsa 10 glomerüllük bir örnekte lezyonu hiç görmeme olasılığı yaklaşık %35’tir.',
       'Şekil: solda böbrek korteksi. Segmental skleroz önce derin, jukstamedüller korteksteki glomerülleri tutar; yüzeyel bir biyopsi örneği lezyonu kaçırabilir. '
       'Sağda örnek hesap: biyopside kaç glomerül varsa lezyonu hiç görmeme olasılığı ne kadardır.', oz=OZGUN_G)

# ---------------------------------------------------------------- 4 · adaptif FSGS: hiperfiltrasyondan skleroza
F = Fig('adf', 312, 'Adaptif FSGS’de hiperfiltrasyon, glomerüler hipertrofi, podosit ayrılması ve segmental skleroz basamakları', w=1080)
ADM = [('1 · Normal', 'Normal glomerül, normal yük'), ('2 · Hipertrofi', 'Nefron başına yük ↑: glomerül büyür,', 'podosit sayısı artmaz; çıkıntılar gerilir'),
       ('3 · Podosit ayrılır', 'Örtme kapasitesi tükenir; GBM', 'çıplak kalır'), ('4 · Segmental skleroz', 'Pariyetal hücreyle yapışıklık (sineşi)', 've skar')]
for i, t in enumerate(ADM):
    x = 6 + i * 270; zemin(F, x, 6, 258, 226)
    F.t(x + 129, 254, t[0], 13, 800, BRANDD, 'middle'); F.tl(x + 129, 272, list(t[1:]), 11.6, 15.5, fill=INK2, a='middle')
GK(F, 'lobul', 135 - 75, 42, 150)
GK(F, 'lobul', 405 - 106, 10, 212)
Z = GK(F, 'lobul', 675 - 106, 10, 212); Z.ayrilma(0, 300, 20)
Z.etiket(Z.duvar(0, 340, 'gbm'), 742, 30, ['çıplak GBM'], sag=True, fs=11)
for i in range(3): F.ok(6 + i * 270 + 250, 118, 6 + i * 270 + 282, 118, INK2, 2.6)
G = GK(F, 'yumak', 945 - 92, 10, 184, kirp=(0, 30, 680, 790)); G.skleroz(325, 35, derin=.4)
D.yeni('s08_adf', 'x08_15', 'Patogenez · Şekil', 'Adaptif FSGS — Büyüyen Glomerül, Çoğalamayan Podosit', F,
       '<b>Okuma:</b> Glomerül büyüdükçe aynı sayıdaki podosit daha geniş bir yüzeyi örtmek zorunda kalır; eşik aşılınca hücre ayrılır, çıplak GBM paryetal hücreye yapışır ve '
       'segmental skleroz gelişir. Yetmezlik immünolojik değil mekaniktir; RAAS blokajı glomerüler basıncı düşürerek bu zinciri yavaşlatır.',
       'Şekil: adaptif fokal segmental glomerülosklerozun dört basamağı. Normal glomerül, hiperfiltrasyonla büyümüş glomerül ve gerilmiş podositler, podositin ayrıldığı çıplak bazal membran, '
       've sonunda yapışıklıkla birlikte segmental skleroz.')

# ---------------------------------------------------------------- 5 · genetik: filtrasyon bariyerinde genler
F = Fig('gen', 452, 'Genetik FSGS ve steroide dirençli nefrotik sendromda genlerin filtrasyon bariyerindeki yerleri', w=1080)
X0, Y0, SC = 16, 66, 1.62
F.a(f'<g transform="translate({X0} {Y0}) scale({SC})">')
B = bariyer(F, 0, 0, 392, 196)
# aktin iskeleti ve TRPC6
for xc in B['fp']:
    F.ln(xc - 3, B['yg'] + 4, xc - 3, B['yg'] + 16, '#8e2a2a', .9); F.ln(xc + 3, B['yg'] + 4, xc + 3, B['yg'] + 16, '#8e2a2a', .9); F.ln(xc - 4, B['yg'] + 10, xc + 4, B['yg'] + 10, '#8e2a2a', .7)
tr = B['fp'][9]; F.r(tr + 4.2, B['yg'] + 7, 3.4, 7, '#1f6f3f', None, rx=1)
for (dx, dy) in ((-26, -2), (24, 3), (-10, 5)):
    elips(F, B['pod'][0] + dx, B['pod'][1] + dy, 5.5, 2.6, 10, '#f4c27a', '#b9822e', .7)
    F.ln(B['pod'][0] + dx - 3.5, B['pod'][1] + dy, B['pod'][0] + dx + 3.5, B['pod'][1] + dy, '#b9822e', .5)
F.a('</g>')
T = lambda x, y: (X0 + x * SC, Y0 + y * SC)
yk = B['yarik'][6]; fp6 = B['fp'][6]
etk(F, T(yk[0], yk[1]), 250, 40, [('NPHS1 · nefrin (yarık diyaframı)')], True, c=RED, fs=12.4)
etk(F, T(fp6 + 6.5, B['yg'] + 2.2), 470, 64, ['NPHS2 · podosin'], True, c=RED, fs=12.4)
etk(F, T(30, B['ye'] + 10), 40, 40, ['COL4A3/4/5 · GBM'], True, c=BRAND, fs=12.4)
etk(F, T(tr + 6, B['yg'] + 10), 400, 404, ['TRPC6 · katyon kanalı'], True, c=GREEN, fs=12.4)
etk(F, T(B['fp'][3], B['yg'] + 10), 40, 404, ['ACTN4 · INF2 · aktin iskeleti'], True, c='#8e2a2a', fs=12.4)
etk(F, T(B['pod'][0] + 8, B['pod'][1] + 4), 400, 430, ['WT1 · çekirdek (transkripsiyon faktörü)'], True, c=PUR, fs=12.4)
etk(F, T(B['pod'][0] - 26, B['pod'][1] - 2), 40, 430, ['Mitokondri · COQ2, COQ6, mtDNA'], True, c=GOLD, fs=12.4)
F.t(X0, Y0 - 6 + 0 * SC + 34, '', 11)
F.t(X0 + 392 * SC - 8, Y0 + 20, 'kapiller lümen', 11.5, 700, MUT, 'end'); F.t(X0 + 392 * SC - 8, Y0 + 190 * SC, 'Bowman boşluğu', 11.5, 700, MUT, 'end')
GEN = [('NPHS1 (nefrin)', 'Konjenital NS (Fin tipi); ilk aylarda ağır proteinüri', RED),
       ('NPHS2 (podosin)', 'Çocukluk SRNS’nin en sık genetik nedeni; otozomal resesif', RED),
       ('WT1', 'Denys-Drash (Wilms), Frasier (gonadoblastom); genital anomali', PUR),
       ('INF2', 'Otozomal dominant; Charcot-Marie-Tooth eşlik edebilir', '#8e2a2a'),
       ('TRPC6 · ACTN4', 'Otozomal dominant, erişkin başlangıçlı ailesel FSGS', GREEN),
       ('COL4A3/4/5', 'FSGS paterni gösterebilir; Alport spektrumu', BRAND),
       ('mtDNA · COQ2 · COQ6', 'Sağırlık, diyabet, miyopati; bazı formlarda CoQ10', GOLD)]
F.t(686, 22, 'Gen ve klinik ipucu', 13.5, 800, BRANDD)
for i, (g_, kl, c) in enumerate(GEN):
    y = 44 + i * 50
    F.r(686, y, 388, 44, TINT.get(c, '#f6eded'), None, rx=8); F.r(686, y, 5, 44, c, None, rx=2)
    F.t(700, y + 18, g_, 12.6, 800, c); F.t(700, y + 36, kl, 11.6, None, INK)
D.yeni('s08_gen', 'x08_18', 'Tanı · Şekil', 'Genler Bariyerin Neresinde? — Podositin Moleküler Haritası', F,
       '<b>Okuma:</b> Yarık diyaframı (nefrin, podosin), ayaksı çıkıntının aktin iskeleti (α-aktinin-4, INF2) ve kanalları (TRPC6), çekirdek (WT1), mitokondri (koenzim Q10 yolu) '
       've GBM (tip IV kollajen) — her katmanın bir genetik nefrotik sendromu vardır. Genetik formlar immünsüpresyona genellikle yanıtsızdır ve nakil sonrası nüks riski düşüktür.',
       'Şekil: filtrasyon bariyerinin yakın görünümü ve genlerin yerleri. Yarık diyaframında nefrin ve podosin, ayaksı çıkıntıda aktin iskeleti ve TRPC6 kanalı, podosit çekirdeğinde WT1, '
       'mitokondride koenzim Q10 yolu, bazal membranda tip IV kollajen. Sağda her genin klinik ipucu.')

# ---------------------------------------------------------------- 6 · DUPLEX
F = Fig('dup', 262, 'DUPLEX çalışmasında sparsentan ve irbesartanın proteinüri ve eGFR eğimi sonuçları', w=1080)
F.t(6, 22, 'Kısmi remisyon · 36. hafta (ara analiz)', 13.5, 800, BRANDD)
cubuk(F, 60, 60, 360, 150, [(['Kısmi remisyon'], [42.0, 26.0], ['%42,0', '%26,0'])], [('Sparsentan (n = 184)', BRAND), ('İrbesartan (n = 187)', MUT)], ymax=50, adim=10, fs=12.6, bw=70)
F.t(240, 246, 'p = 0,009 · yanıt 108. haftaya kadar sürdü', 12, 700, GREEN, 'middle')
F.ln(470, 10, 470, 254, LINE, 1.5)
F.t(500, 22, 'Birincil sonlanım: eGFR eğimi farkı (108. hafta)', 13.5, 800, BRANDD)
FX, FW = 640, 400; lo, hi = -3, 4
fx = lambda v: FX + (v - lo) / (hi - lo) * FW
for v in range(lo, hi + 1):
    F.ln(fx(v), 60, fx(v), 190, LINE if v else INK2, 1 if v else 1.8, '3 4' if v else None); F.t(fx(v), 208, str(v).replace('-', '−'), 11.5, None, MUT, 'middle')
F.t(fx(lo), 226, '← irbesartan lehine', 11.5, None, MUT); F.t(fx(hi), 226, 'sparsentan lehine →', 11.5, None, MUT, 'end')
F.t(fx(.5), 244, 'mL/dk/1,73 m²/yıl', 11.2, None, MUT, 'middle')
for j, (ad, v, a, b) in enumerate((('Toplam eğim', .3, -1.7, 2.4), ('Kronik eğim', .9, -1.3, 3.0))):
    y = 92 + j * 56
    F.t(fx(lo) - 12, y + 4, ad, 12.6, 700, INK, 'end')
    F.ln(fx(a), y, fx(b), y, BRAND, 2.6); F.ln(fx(a), y - 6, fx(a), y + 6, BRAND, 2); F.ln(fx(b), y - 6, fx(b), y + 6, BRAND, 2)
    F.r(fx(v) - 6, y - 6, 12, 12, BRAND, None, rx=2)
    F.t(fx(b) + 10, y + 4, f'{v:+.1f} ({a:.1f} ile {b:.1f})'.replace('.', ',').replace('-', '−'), 11.8, 800, BRAND)
F.t(500, 254, 'Güven aralıkları sıfırı kesiyor: anlamlı fark yok.', 12, 800, RED)
D.yeni('s08_dup', 'x08_23', 'Tedavi · Şekil', 'DUPLEX — Proteinüri Ayrıştı, eGFR Eğimi Ayrışmadı', F,
       '<b>Okuma:</b> Sparsentan proteinüride kalıcı üstünlük sağladı; iki yıllık eGFR eğiminde ise güven aralıkları sıfırı kesiyor. Aktif kontrolün (irbesartan) kendisi etkili bir ilaçtır.',
       'Şekil: solda otuz altıncı haftada kısmi remisyon: sparsentan yüzde kırk iki, irbesartan yüzde yirmi altı. Sağda yüz sekizinci haftada eGFR eğimi farkı: '
       'toplam eğimde sıfır virgül üç, kronik eğimde sıfır virgül dokuz; iki güven aralığı da sıfırı içeriyor.', oz=OZGUN_G)
