#!/usr/bin/env python3
"""Ders 07 · Minimal Değişiklik Hastalığı — şekiller."""
from sekil_ortak import *
from sekil_gk import *
D = Ders('07'); L = D.L

# ---------------------------------------------------------------- 1 · ışık mikroskopisi: normal glomerül + immünfloresan
F = Fig('mdh_lm', 372, 'Minimal değişiklik hastalığında ışık mikroskopisinde normal görünen glomerül ve immünfloresan bulguları', w=1080)
zemin(F, 6, 6, 650, 360)
G = GK(F, 'yumak', 196, 12, 292, kirp=(0, 0, 680, 800))
G.etiket('afferent', 186, 44, ['Afferent arteriyol'], sag=False)
G.etiket('efferent', 500, 44, ['Efferent arteriyol'])
G.etiket('damar_kutbu', 500, 96, ['Damar kutbu'])
G.etiket(G.kapsul(200, 'duvar'), 186, 150, ['Bowman kapsülü ve', 'pariyetal epitel'], sag=False)
G.etiket(G.kapsul(158, 'bosluk') if False else (G.kc[0] + (G.ki - 30) * math.cos(math.radians(158)), G.kc[1] + (G.ki - 30) * math.sin(math.radians(158))), 186, 236, ['Bowman boşluğu'], sag=False)
G.etiket((470, 340), 500, 168, ['Kapiller ilmekler:', 'açık, ince duvarlı'])
G.etiket((322, 425), 500, 236, ['Mezangiyum: normal', 'ya da hafif artmış'])
G.etiket('idrar_kutbu', 186, 318, ['İdrar kutbu'], sag=False)
G.etiket('tubul', 500, 330, ['Proksimal tübül'])
serit(F, 668, 6, 406, 'İmmünfloresan', BRAND)
if_patern(F, 768, 116, 62, 'negatif', baslik='Çoğu olgu: negatif')
if_patern(F, 974, 116, 62, 'mez', renk='#7ad7f0', baslik='Alt grup: mezangiyal', alt=['IgM ya da C1q'])
F.r(668, 252, 406, 114, '#fff', LINE, 1.4, 10)
F.tl(682, 274, ['• Işıkta glomerül normal ya da minimaldir', '• Glomerüllerin <%10’unda global (segmental değil)', '  skleroz olabilir: yaşlanma', '• Mezangiyal IgM ya da C1q birikimi olan alt grupların', '  sonucu daha kötü bildirilmiştir'], 12, 17.5, fill=INK)
D.yeni('s07_isik', 'x07_8', 'Temel Bilgiler · 4 · Şekil', 'Işıkta “Minimal” — Normal Görünen Glomerül', F,
       '<b>Okuma:</b> Üstte damar kutbunda afferent ve efferent arteriyol, altta proksimal tübüle açılan idrar kutbu. Kapiller ilmekler açık, mezangiyum en çok hafif artmıştır; '
       'segmental skleroz görülürse tanı yeniden düşünülür. İmmünfloresan çoğu olguda negatiftir.',
       'Şekil: ışık mikroskopisinde normal görünen bir glomerül. Üstte damar kutbunda afferent ve efferent arteriyol, altta proksimal tübüle açılan idrar kutbu. '
       'Kapiller ilmekler açık ve ince duvarlıdır. Sağda immünfloresan: çoğu olguda negatif, küçük bir alt grupta mezangiyal IgM ya da C1q.')

# ---------------------------------------------------------------- 2 · elektron mikroskopisi: normal ve MDH lobülü
F = Fig('mdh_em', 430, 'Normal glomerül lobülü ile minimal değişiklik hastalığında yaygın ayaksı çıkıntı silinmesi', w=1080, mh=410)
for (x, bas, c) in ((6, 'Normal', GREEN), (546, 'Minimal değişiklik hastalığı (EM)', BRAND)):
    serit(F, x, 6, 528, bas, c); zemin(F, x, 42, 528, 318)
LL = []
for x0 in (6, 546):
    A_ = GK(F, 'lobul', x0 + 10, 50, 300, cerceve=LINE); A_.kose(); LL.append(A_)
A, B = LL
A.etiket(A.duvar(0, 320, 'ayak'), 324, 168, ['Ayaksı çıkıntılar ve', 'aralarında yarık', 'diyaframı'])
A.etiket(A.duvar(0, 8, 'gbm'), 324, 230, ['GBM: normal'])
A.etiket(A.duvar(0, 30, 'endotel'), 324, 272, ['Pencereli endotel'])
A.etiket('mez_hucre2', 324, 318, ['Mezangiyal hücre'])
A.etiket('pod_govde', 324, 76, ['Podosit gövdesi'])
B.silinme(0, 158, 36); B.silinme(1, 272, 80); B.silinme(2, 176, 303); B.mikrovillus(); B.vakuol(4)
B.etiket(B.duvar(0, 345, 'subepi'), 864, 186, ['Yaygın ayaksı', 'çıkıntı silinmesi', '(füzyon)'])
B.etiket(max(B.T['dis_kontur'], key=lambda q: q[0] - 3 * abs(q[1] - 330) if q[1] < 600 else -9e9), 864, 122, ['Mikrovillus', 'dönüşümü'])
B.etiket((628, 148), 864, 66, ['Podosit:', 'vakuolizasyon'])
B.etiket(B.duvar(0, 15, 'gbm'), 864, 262, ['GBM normal;', 'birikim yok'])
F.r(6, 370, 1068, 54, TINT[BRAND], BRAND, 1.4, 10)
F.t(540, 393, 'MDH tanısı iki mikroskopinin birlikte okunmasıyla konur', 13.5, 800, BRANDD, 'middle')
F.t(540, 413, 'Işık mikroskopisi normal + EM’de yaygın ayaksı çıkıntı silinmesi + elektron-yoğun birikim yok', 12.4, None, INK, 'middle')
D.yeni('s07_em', 'x07_9', 'Temel Bilgiler · 4 · Şekil', 'Elektron Mikroskopisi — Ayaksı Çıkıntılar Silinir, Başka Bir Şey Olmaz', F,
       '<b>Okuma:</b> Solda normal lobül: ayrı ayrı ayaksı çıkıntılar ve aralarında yarık diyaframları. Sağda MDH: ayaksı çıkıntılar GBM üzerinde kesintisiz bir tabakaya dönüşmüş, '
       'podositte mikrovillus ve vakuoller var; GBM normal ve birikim yok. Ayaksı çıkıntı silinmesi tek başına özgül değildir; ışık mikroskopisi normal olduğunda MDH’yi gösterir.',
       'Şekil: solda normal glomerül lobülü, sağda minimal değişiklik hastalığı. Normalde ayaksı çıkıntılar ayrı ayrı durur. Minimal değişiklik hastalığında yaygın olarak silinir, '
       'podositte mikrovillus ve vakuoller görülür. Bazal membran normaldir, birikim yoktur.')

# ---------------------------------------------------------------- 3 · remisyon zamanı ve nüks kalıbı
F = Fig('mdh_rem', 300, 'Minimal değişiklik hastalığında çocuk ve erişkinde remisyona girme zamanı ve çocukta nüks kalıbı', w=1080)
F.t(6, 22, 'Remisyona süre — slayttaki üç veri noktası', 13.5, 800, BRANDD)
X0, X1, Y = 40, 690, 150; ws = (X1 - X0) / 18
F.ln(X0, Y, X1, Y, INK2, 2.4)
F.r(X0 + 13 * ws, Y - 8, 4 * ws, 16, TINT[RED], None, rx=4, op=.9)
for wk in range(0, 19, 2):
    x = X0 + wk * ws; F.ln(x, Y - 5, x, Y + 5, INK2, 1.6); F.t(x, Y + 22, f'{wk}', 11.5, None, MUT, 'middle')
F.t(X0, Y + 40, 'tedaviye başladıktan sonra hafta', 11.5, None, MUT)
def isaret_(x, yy, renk, baslik, alt, ust=True, xn=None):
    xn = x if xn is None else xn
    F.ln(xn, Y, x + (0 if xn == x else 200), yy + (12 if ust else -12), renk, 1.6, '4 3'); F.el(xn, Y, 6.5, 6.5, renk, '#fff', 1.6)
    F.etiket(x - 6, yy, 230, [baslik] + alt, renk, 12.4)
isaret_(X0 + 8 / 7 * ws, 70, GREEN, 'Çocuk: %50 remisyonda', ['tedavinin 8. gününde'])
isaret_(X0 + 10 * ws, 70, BRAND, 'Erişkin: ortanca süre', ['2 aydan uzun (bazı', 'serilerde 10 hafta)'])
isaret_(X0 + 15 * ws - 200, 236, RED, 'Erişkin: 3–4. ayda', ['%25 hâlâ remisyonsuz'], ust=False, xn=X0 + 15 * ws)
F.ln(730, 10, 730, 292, LINE, 1.5)
F.t(756, 22, 'Çocukta nüks kalıbı', 13.5, 800, BRANDD)
segs = [(25, '#9fd1b0', 'Hiç nüks etmez'), (25, '#f3d58a', 'Seyrek nükseder'), (50, '#e8908a', 'Çok sayıda nüks')]
yy = 50
for (v, c, ad) in segs:
    hh = v * 2.1; F.r(770, yy, 70, hh, c, '#fff', 1.4, 4); F.t(805, yy + hh / 2 + 5, f'%{v}', 13.5, 800, INK, 'middle')
    F.t(856, yy + hh / 2 + 5, ad, 12.6, 700, INK); yy += hh
F.tl(856, yy - 50 * 2.1 / 2 + 24, ['sık nükseden (6 ayda ≥ 2 ya da', '12 ayda ≥ 4 nüks) ya da steroide bağımlı'], 11.6, 15, fill=INK2)
F.t(756, 284, 'Çocuk ve erişkinde %75’e kadar en az bir nüks', 11.6, None, INK2)
D.yeni('s07_rem', 'x07_17', 'Doğal Seyir · Şekil', 'Çocuk ve Erişkin — Remisyon Saati Farklı İşler', F,
       '<b>Okuma:</b> Çocukta yanıt günlerle, erişkinde haftalarla ölçülür; erişkinde 16 haftadan önce steroid direnci denmemesinin gerekçesi budur. '
       'Sağdaki sütun çocuklarda nüks dağılımıdır. Zaman ekseninde yalnız slayttaki üç veri işaretlenmiştir; bir eğri çizilmemiştir.',
       'Şekil: solda remisyona süre. Çocukların yarısı tedavinin sekizinci gününde remisyondadır. Erişkinde ortanca süre iki aydan uzundur ve üç ile dördüncü ayda dörtte biri hâlâ remisyona girmemiştir. '
       'Sağda çocukta nüks kalıbı: yüzde yirmi beşi hiç nüks etmez, yüzde yirmi beşi seyrek, yüzde ellisi çok sayıda nüks yaşar.', oz=OZGUN_G)

# ---------------------------------------------------------------- 4 · Waldman serisi (slayt içi)
F = Fig('wald', 148, 'Waldman serisinde 95 erişkin minimal değişiklik hastasının sonuçları', w=1140, mh=150)
F.t(14, 20, 'Waldman serisi · 95 erişkin', 13, 800, BRANDD)
SAT = [('En az bir nüks', 73, '%73', BRAND), ('Sık nükseden', 28, '%28', BRAND), ('Steroide dirençli', 26, '> %25 (dörtte birden fazla)', GOLD),
       ('Akut böbrek yetmezliği', 25.3, '24/95 (%25)', RED), ('SDBY (çoğu steroide yanıtsız)', 4.2, '4/95 (%4)', RED)]
for i, (ad, v, yaz, c) in enumerate(SAT):
    y = 34 + i * 22.5
    F.t(286, y + 13, ad, 12.2, 700, INK, 'end'); F.r(296, y + 2, 600, 15, '#f2f5f8', None, rx=4); F.r(296, y + 2, v * 6, 15, c, None, rx=4)
    F.t(296 + v * 6 + 8, y + 14, yaz, 12.2, 800, c)
D.ic('s07_wald', 'x07_18', F)

# ---------------------------------------------------------------- 5 · ISKDC nüks rejimi (slayt içi)
F = Fig('iskdc', 214, 'ISKDC önerisine göre çocukta nüks tedavisinde prednizon dozu ve süresi', w=1140, mh=220)
F.t(14, 20, 'ISKDC nüks rejimi · prednizon (mg/m²)', 13, 800, BRANDD)
X0, Y0, H = 110, 40, 130; gw = 58          # hafta genişliği
F.ln(X0, Y0 + H, X0 + 9.2 * gw, Y0 + H, INK2, 1.8); F.ln(X0, Y0, X0, Y0 + H, INK2, 1.8)
for v in (0, 20, 40, 60):
    yy = Y0 + H - v * H / 66; F.t(X0 - 8, yy + 4, str(v), 11.5, None, MUT, 'end'); F.ln(X0, yy, X0 + 9.2 * gw, yy, LINE, 1, '3 4')
for wk in range(0, 10):
    F.t(X0 + wk * gw, Y0 + H + 18, str(wk), 11.5, None, MUT, 'middle')
F.t(X0 + 9.2 * gw, Y0 + H + 36, 'hafta', 11.5, None, MUT, 'end')
y60 = Y0 + H - 60 * H / 66; y40 = Y0 + H - 40 * H / 66
F.r(X0, y60, 2.2 * gw, Y0 + H - y60, BRAND, None, rx=3)
F.r(X0 + 2.2 * gw, y60, 1.8 * gw, Y0 + H - y60, BRAND, None, rx=3, op=.28, dash='5 4')
F.t(X0 + 8, y60 - 8, '60 mg/m²/gün, her gün', 12.2, 800, BRAND)
F.t(X0 + 3.1 * gw, y60 + 18, 'yanıta kadar', 11.4, None, INK2, 'middle'); F.t(X0 + 3.1 * gw, y60 + 32, '(en fazla 4 hafta)', 11.4, None, INK2, 'middle')
F.ln(X0 + 4 * gw, Y0 - 4, X0 + 4 * gw, Y0 + H, RED, 1.6, '5 4'); F.t(X0 + 4 * gw + 4, Y0 + 4, 'remisyon (en geç 4. hafta)', 11.4, 800, RED)
for wk in range(4):
    for d in range(3):
        x = X0 + (4 + wk) * gw + d * gw / 7 + 4; F.r(x, y40, gw / 7 - 2, Y0 + H - y40, GOLD, None, rx=2)
F.t(X0 + 4.15 * gw, y40 - 8, '40 mg/m², haftada 3 ardışık gün · 4 hafta', 12.2, 800, GOLD)
F.r(760, 40, 366, 130, '#fff', LINE, 1.4, 10)
F.t(774, 62, 'İlk atak için (Cochrane 2020, 2024)', 12.6, 800, GREEN)
F.tl(774, 82, ['Prednizonu 2–3 aydan uzun sürdürmek', 'nüksü azaltmaz; ek steroid maruziyeti', 'yarar getirmez.', 'Nüks tedavisinde uzlaşılmış tek bir rejim', 'yoktur; ISKDC önerisi bir örnektir.'], 11.8, 16.5, fill=INK)
F.t(X0, Y0 + H + 36, 'Yanıt süresi hastaya göre değişir; kesik bölge en uzun süreyi gösterir.', 11.2, None, MUT)
D.ic('s07_iskdc', 'x07_22', F)
