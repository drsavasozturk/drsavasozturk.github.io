#!/usr/bin/env python3
"""Ders 20 · Alport sendromu ve kollajen IV hastalıkları — şekil tanımları (20 Kasım 2026)."""
from sekil_ortak import *
from sekil_gk import GK

D = Ders('20')
L = D.L
IFY = '#7cf06a'


def birey(F, x, y, erkek, durum, r=15):
    """durum: 0 sağlam · 1 heterozigot (yarım) · 2 hasta (dolu)."""
    if erkek: F.r(x - r, y - r, 2 * r, 2 * r, '#fff', INK, 1.8, 2)
    else: F.el(x, y, r, r, '#fff', INK, 1.8)
    if durum == 2:
        if erkek: F.r(x - r, y - r, 2 * r, 2 * r, RED, INK, 1.8, 2)
        else: F.el(x, y, r, r, RED, INK, 1.8)
    elif durum == 1:
        if erkek: F.r(x - r, y - r, r, 2 * r, RED, None, rx=0); F.r(x - r, y - r, 2 * r, 2 * r, 'none', INK, 1.8, 2)
        else: F.a(f'<path d="M{x},{y - r} A{r},{r} 0 0 0 {x},{y + r} Z" fill="{RED}"/>'); F.el(x, y, r, r, 'none', INK, 1.8)


def soy(x0, baslik, c, ebeveyn, cocuk, alt, akraba=False):
    serit(F, x0, 6, 350, baslik, c); zemin(F, x0, 42, 350, 290)
    m = x0 + 175
    (e1, d1), (e2, d2) = ebeveyn
    birey(F, m - 50, 92, e1, d1); birey(F, m + 50, 92, e2, d2); F.ln(m - 35, 92 - (2.5 if akraba else 0), m + 35, 92 - (2.5 if akraba else 0), INK, 1.8)
    if akraba: F.ln(m - 35, 94.5, m + 35, 94.5, INK, 1.8)
    F.ln(m, 92, m, 128, INK, 1.8); n = len(cocuk); xs = [m - 120 + i * 240 / (n - 1) for i in range(n)]
    F.ln(xs[0], 128, xs[-1], 128, INK, 1.8)
    for x, (e, d, t) in zip(xs, cocuk):
        F.ln(x, 128, x, 146, INK, 1.8); birey(F, x, 161, e, d)
        F.t(x, 196, t, 11, 700, INK2, 'middle')
    F.tl(x0 + 14, 228, alt, 11.8, 16, fill=INK)


# ============================================================================================== 1 · üç kalıtım biçimi
F = Fig('kal', 352, 'Alport sendromunda X’e bağlı, otozomal resesif ve otozomal dominant kalıtım soy ağaçları', w=1080)
soy(6, 'X’e bağlı · COL4A5 · ~%65', RED, [(False, 1), (True, 0)],
    [(True, 2, 'hasta'), (True, 0, 'sağlam'), (False, 1, 'heterozigot'), (False, 0, 'sağlam')],
    ['Heterozigot anneden: oğulların yarısı hasta,', 'kızların yarısı heterozigot.', 'Heterozigot kadın “taşıyıcı” değil, hastadır;', 'ağırlık X inaktivasyonuna bağlı.'])
soy(365, 'Otozomal resesif · COL4A3/COL4A4 · ~%15', PUR, [(True, 1), (False, 1)],
    [(True, 2, 'hasta'), (False, 1, 'heterozigot'), (True, 1, 'heterozigot'), (False, 0, 'sağlam')],
    ['Anne ve baba heterozigot (çoğu kez izole', 'hematüri); çocukların dörtte biri hasta.', 'Cinsiyet farkı yok; akraba evliliği sık —', 'Türkiye için önemli (çift çizgi).'], akraba=True)
soy(724, 'Otozomal dominant · COL4A3/COL4A4 · ~%20', GOLD, [(True, 1), (False, 0)],
    [(True, 1, 'etkilenmiş'), (False, 0, 'sağlam'), (False, 1, 'etkilenmiş'), (True, 0, 'sağlam')],
    ['Çocukların yarısı tek allel taşır.', 'Yelpaze geniş: izole hematüriden', 'ilerleyici böbrek yetmezliğine kadar;', 'böbrek dışı bulgu yok ya da hafif.'])
for k, (d, t) in enumerate(((2, 'hasta (iki allel / hemizigot)'), (1, 'tek allel (heterozigot)'), (0, 'sağlam'))):
    birey(F, 22 + k * 230, 344, False, d, 7); F.t(34 + k * 230, 348, t, 11, 700, INK2)
D.yeni('s20_kal', 'x20_5', 'Temel Bilgiler · 2 · Şekil', 'Üç Kalıtım Biçimi — Soy Ağacında Alport', F,
       '<b>Okuma:</b> X’e bağlı biçimde heterozigot anneden doğan oğulların yarısı hasta, kızların yarısı heterozigottur; heterozigot kadın hastadır. '
       'Otozomal resesif biçimde heterozigot anne ve babanın çocuklarının dörtte biri ağır hastalık geliştirir. Otozomal dominant biçimde çocukların yarısı etkilenir; seyir değişkendir.',
       'Şekil: üç soy ağacı. Solda X’e bağlı kalıtım: heterozigot anne ve sağlam baba; oğulların yarısı hasta, kızların yarısı heterozigot. '
       'Ortada otozomal resesif kalıtım: iki heterozigot ebeveyn, çocukların dörtte biri hasta. Sağda otozomal dominant kalıtım: bir etkilenmiş ebeveyn, çocukların yarısı tek allel taşır.')

# ============================================================================================== 2 · GBM ve kollajen IV α5 boyanması
F = Fig('gbm', 410, 'Alport sendromunda glomerül bazal membranının elektron mikroskopi görünümü ve kollajen IV alfa 5 immünfloresan paternleri', w=1080)
serit(F, 6, 6, 520, 'Elektron mikroskopisi · yerleşmiş hastalık', BRANDD); zemin(F, 6, 42, 520, 362)
A = GK(F, 'lobul', 14, 50, 300, cerceve=LINE); A.kose(44)
A.lamel(0, 166, 290); A.gbm_kalin(2, 186, 228, 4, 14); A.lamel(2, 236, 290)
A.silinme(0, 300, 30)
A.etiket(A.duvar(0, 230, 'gbm'), 324, 88, ['Lamina densa bölünmesi:', 'sepet örgüsü (basket-weave)'])
A.etiket(A.duvar(0, 345, 'ayak'), 324, 196, ['Ayaksı çıkıntı silinmesi', '(proteinüri ilerledikçe)'])
A.etiket(A.duvar(2, 205, 'gbm'), 324, 286, ['Düzensiz kalınlaşma', 've incelme'])
F.tl(20, 376, ['Erken dönemde tek bulgu yaygın GBM incelmesi olabilir.', 'Işık mikroskopisi erken dönemde normaldir.'], 11.6, 15, fill=INK2)
serit(F, 536, 6, 538, 'Kollajen IV α5 boyanması (immünfloresan)', GREEN); zemin(F, 536, 42, 538, 362)


def ifpanel(cx, cy, gbm, bowman, dtbm, bas, alt):
    R = 46
    F.r(cx - 64, cy - 64, 128, 128, '#08110b', None, rx=10)
    F.el(cx - 6, cy, R, R, 'none', IFY if bowman == 1 else '#1a2b1e', 3.2 if bowman == 1 else 1.2)
    if bowman == .5:
        F.a(f'<path d="M{cx - 6 - R},{cy} A{R},{R} 0 0 1 {cx - 6},{cy - R}" fill="none" stroke="{IFY}" stroke-width="3.2"/>')
    loops = [(-21, -13, 13), (2, -22, 12), (18, -4, 12), (9, 18, 12), (-15, 15, 13), (-3, -1, 10)]
    for k, (x, y, r) in enumerate(loops):
        on = gbm == 1 or (gbm == .5 and k in (0, 2, 4))
        F.el(cx - 6 + x, cy + y, r, r, 'none', IFY if on else '#1a2b1e', 2.2 if on else 1)
    tx, ty = cx + 46, cy + 44
    if dtbm == .5: F.a(f'<path d="M{tx - 10},{ty} A10,10 0 0 1 {tx},{ty - 10}" fill="none" stroke="{IFY}" stroke-width="2.4"/>'); F.el(tx, ty, 10, 10, 'none', '#1a2b1e', 1)
    else: F.el(tx, ty, 10, 10, 'none', IFY if dtbm else '#1a2b1e', 2.4 if dtbm else 1)
    F.t(cx, cy - 72, bas, 12.4, 800, INK, 'middle'); F.t(cx, cy + 82, alt, 11.4, None, INK2, 'middle')


ifpanel(672, 134, 1, 1, 1, 'Normal', 'GBM, Bowman ve TBM boyanır')
ifpanel(938, 134, 0, 0, 0, 'X’e bağlı · erkek', 'α5 hiçbir yerde yok')
ifpanel(672, 314, .5, .5, .5, 'X’e bağlı · kadın', 'mozaik (kesintili)')
ifpanel(938, 314, 0, 1, 1, 'Otozomal resesif', 'GBM’de yok; Bowman, TBM’de var')
D.yeni('s20_gbm', 'x20_7', 'Temel Bilgiler · 4 · Şekil', 'Alport — Sepet Örgüsü ve α5 Paternleri', F,
       '<b>Okuma:</b> Yerleşmiş hastalıkta GBM düzensiz kalınlaşır ve incelir, lamina densa bölünerek sepet örgüsü görünümü alır. '
       'α5 boyanması kalıtım biçimini gösterir: X’e bağlı erkekte hiç yoktur, kadında mozaiktir; otozomal resesifte GBM’de yoktur ama α5α5α6 ağı sayesinde Bowman kapsülü ve distal tübül bazal membranında görülür. '
       'Normal boyanma tanıyı dışlamaz.',
       'Şekil: solda elektron mikroskopisinde Alport glomerül lobülü: lamina densa bölünmüş, sepet örgüsü görünümü, düzensiz kalınlaşma ve incelme, ayaksı çıkıntı silinmesi. '
       'Sağda kollajen dört alfa beş immünfloresan paternleri: normalde glomerül bazal membranı, Bowman kapsülü ve distal tübül bazal membranı boyanır; '
       'X’e bağlı erkekte hiç boyanma yok; X’e bağlı kadında mozaik; otozomal resesif hastalıkta glomerül bazal membranında yok, Bowman kapsülü ve tübül bazal membranında var.')

# ============================================================================================== 3 · X’e bağlı Alport: kadın ve erkek
F = Fig('kad', 352, 'X’e bağlı Alport sendromunda kadın ve erkeklerde bulguların sıklığı', w=1080)
serit(F, 6, 6, 700, 'X’e bağlı Alport · kadın ve erkek', BRANDD); zemin(F, 6, 42, 700, 304)
S = [('Hematüri', 95, 100, None), ('Proteinüri', 75, None, 'neredeyse tümü'), ('İşitme kaybı', 28, None, 'çok daha sık'),
     ('Oküler defekt', 15, None, 'daha sık'), ('40 yaşından önce SDBY', 12, 90, None), ('40 yaşından önce sağırlık', 10, 80, None)]
X0 = 196; W = 440
for i, (ad, k, e, et) in enumerate(S):
    y = 62 + i * 44
    F.t(X0 - 12, y + 19, ad, 12.2, 700, INK, 'end')
    F.r(X0, y + 2, W * k / 100, 15, RED, None, rx=3); F.t(X0 + W * k / 100 + 6, y + 14, '%' + str(k), 12, 800, RED)
    if e is not None:
        F.r(X0, y + 20, W * e / 100, 15, BRANDD, None, rx=3); F.t(X0 + W * e / 100 + 6, y + 32, '%' + str(e), 12, 800, BRANDD)
    else:
        F.t(X0, y + 32, 'erkek: ' + et, 11.6, 700, BRANDD)
F.r(X0, 328, 12, 10, RED, None, rx=2); F.t(X0 + 18, 337, 'kadın', 11.4, 700, INK2); F.r(X0 + 80, 328, 12, 10, BRANDD, None, rx=2); F.t(X0 + 98, 337, 'erkek', 11.4, 700, INK2)
serit(F, 716, 6, 358, 'Kadında risk ertelenir', RED); zemin(F, 716, 42, 358, 304)
F.tl(732, 72, ['SDBY riski 60 yaşından sonra artar:', '“risk yok” değil, “risk ertelenmiş”.'], 12.4, 18, fill=INK)
F.tl(732, 128, ['Genotip–fenotip ilişkisi yok;', 'aile içinde bile seyir değişken.'], 12.4, 18, fill=INK)
F.t(732, 186, 'İzlemde aranacak uyarı işaretleri', 12.6, 800, RED)
F.tl(732, 210, ['1 · Proteinürinin ortaya çıkması ve artması', '2 · İşitme kaybının gelişmesi'], 12.2, 18, fill=INK)
F.tl(732, 262, ['Hematüri %5 kadında saptanmaz:', 'yokluğu tanıyı dışlamaz.'], 12, 17, fill=INK2)
D.yeni('s20_kad', 'x20_10', 'Genotip-Fenotip · Şekil', 'X’e Bağlı Alport — Kadında Daha Hafif, Ama Hasta', F,
       '<b>Okuma:</b> Kadınlarda bulgular erkeklere göre daha seyrek ve geçtir; 40 yaşından önce SDBY kadınların %12’sinde, erkeklerin %90’ında gelişir. '
       'Risk ortadan kalkmaz, ertelenir: proteinüri ve işitme kaybı ortaya çıkan kadın daha yakından izlenmelidir.',
       'Şekil: X’e bağlı Alport sendromunda kadın ve erkeklerde bulguların sıklığı. Hematüri kadınların yüzde 95’inde, erkeklerin tümünde; '
       '40 yaşından önce son dönem böbrek yetmezliği kadınlarda yüzde 12, erkeklerde yüzde 90; 40 yaşından önce sağırlık yüzde 10’a karşı 80. '
       'Sağda kadında riskin ertelendiği ve izlemde proteinüri ile işitme kaybının uyarı işareti olduğu vurgulanıyor.')
