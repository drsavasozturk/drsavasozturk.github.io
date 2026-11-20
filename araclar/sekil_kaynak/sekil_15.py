#!/usr/bin/env python3
"""Ders 15 · Diğer Glomerüler Hastalıklar — şekiller."""
from sekil_ortak import *
from sekil_gk import *
D = Ders('15'); L = D.L


def kart(F, x, y, w, h, bas, satirlar, c=BRAND, fs=11.6, lh=16.5):
    F.r(x, y, w, h, '#fff', c, 1.4, 10); F.t(x + 14, y + 24, bas, 12.8, 800, c)
    yy = y + 46
    for s_ in satirlar:
        ws = s_.split(' '); ls = ['']
        for w_ in ws:
            if gen(ls[-1] + ' ' + w_, fs) > w - 42: ls.append(w_)
            else: ls[-1] = (ls[-1] + ' ' + w_).strip()
        F.t(x + 14, yy, '•', fs, 800, c); F.tl(x + 26, yy, ls, fs, lh, fill=INK); yy += lh * len(ls) + 4


# ---------------------------------------------------------------- 1 · lipoprotein glomerülopatisi
F = Fig('lpg', 392, 'Lipoprotein glomerülopatisinde genişlemiş kapiller lümenleri dolduran katmanlı lipoprotein tıkaçları', w=1080, mh=392)
serit(F, 6, 6, 600, 'Glomerül lobülü', GOLD); zemin(F, 6, 42, 600, 344)
A = GK(F, 'lobul', 14, 46, 326, cerceve=LINE); A.kose(46)
A.lipo(0); A.lipo(1); A.lipo(2)
A.etiket(A.kp(0, 300, A.R(0, 300)[0] - 60), 352, 80, ['Soluk, katmanlı', '(lameller) lipoprotein', 'tıkaçları'])
A.etiket(A.kp(2, 260, A.R(2, 260)[0] - 70), 352, 214, ['Kapiller lümenleri', 'dolduran tıkaç;', 'eritrosit yok'])
A.etiket(A.kp(2, 300, A.R(2, 300)[0] - 110), 352, 330, ['Fibrin negatif:', 'trombüs değildir'])
kart(F, 626, 6, 448, 214, 'Tanı ve ayırım', ['Yağ boyaları (Oil Red O, Sudan) pozitif.', 'İmmünfloresan negatif ya da zayıf ApoE/ApoB.', 'Fibrin boyaları negatif: TMA’dan ayıran nokta.',
                                             'Serum ApoE yüksek; tip III hiperlipoproteinemi benzeri profil.', 'Ksantom ve erken ateroskleroz beklenmez — ailevi disbetalipoproteinemiden farkı.',
                                             'İlk tanımlanan varyant: ApoE-Sendai (Arg145Pro).'], GOLD)
D.yeni('s15_lpg', 'x15_17', 'Lipid ve Matriks · 1 · Şekil', 'Lipoprotein Glomerülopatisi — Lümeni Dolduran Katmanlı Tıkaç', F,
       '<b>Okuma:</b> Kapiller lümenler genişlemiş ve soluk, kat kat lipoprotein tıkaçlarıyla dolmuştur. Fibrin boyalarının negatif olması bunun trombüs olmadığını, dolayısıyla TMA’nın dışlandığını gösterir.',
       'Şekil: solda lipoprotein glomerülopatisinde glomerül lobülü; kapiller lümenler genişlemiş ve soluk, katmanlı lipoprotein tıkaçlarıyla dolu. Sağda tanı ipuçları.')

# ---------------------------------------------------------------- 2 · fibronektin glomerülopatisi
F = Fig('fng', 380, 'Fibronektin depozitli glomerülopatide mezangiyal ve subendotelyal masif PAS pozitif birikimler', w=1080, mh=380)
serit(F, 6, 6, 600, 'Glomerül lobülü', '#b0466a'); zemin(F, 6, 42, 600, 332)
A = GK(F, 'lobul', 14, 46, 316, cerceve=LINE); A.kose(46)
A.matriks_artisi(.85); A.mezangiyal(10, 30, renk='#d97aa6', kenar='#9a3560')
for k, Q in ((0, [195, 230, 300, 340, 15]), (1, [300, 340, 20, 60]), (2, [200, 240, 280])): A.subendotelyal(k, Q, gen=16, yuk=16, renk='#7b2d6b', kenar='#4a1640')
A.etiket((452, 720) if False else max(A._mzk, key=lambda q: q[0] - q[1] * .2), 344, 80, ['Mezangiyumda masif', 'PAS pozitif birikim'])
A.etiket(A.duvar(0, 340, 'subendo'), 344, 180, ['Subendotelyal', 'birikimler'])
A.etiket((450, 800), 344, 290, ['Lobüler, MPGN', 'benzeri görünüm'])
kart(F, 626, 6, 448, 190, 'Fibronektin depozitli glomerülopati', ['Kalıtım otozomal dominant, değişken penetrans.', 'Birikimler PAS pozitif, Kongo kırmızısı negatif; fibronektin immünhistokimyası pozitif.',
                                                                     'FN1 geninde üç heterozigot missense mutasyon (W1925R, L1974R, Y973C): grubun %40’ı.', 'Klinik: proteinüri, mikroskopik hematüri, hipertansiyon; 2.–4. dekatta yavaş ilerleyen böbrek yetmezliği.'], '#b0466a')
D.yeni('s15_fng', 'x15_19', 'Lipid ve Matriks · 3 · Şekil', 'Fibronektin Glomerülopatisi — Matriksin Kendisi Birikir', F,
       '<b>Okuma:</b> Birikim bir immün kompleks değil, matriks proteinidir: mezangiyum ve subendotelyal alan PAS pozitif, Kongo kırmızısı negatif homojen materyalle dolar ve glomerül MPGN’yi andırır. '
       'Tanıyı fibronektin immünhistokimyası koydurur.',
       'Şekil: solda fibronektin depozitli glomerülopatide glomerül lobülü; mezangiyumda ve endotel altında masif pembe birikimler. Sağda kalıtım, boyanma özellikleri ve genetik.')

# ---------------------------------------------------------------- 3 · obeziteye bağlı glomerülopati
F = Fig('org', 340, 'Obeziteye bağlı glomerülopatide glomerülomegali ve sabit podosit sayısı', w=1080)
zemin(F, 6, 6, 660, 328)
G1 = GK(F, 'yumak', 150 - 72, 96, 144, kirp=(0, 20, 680, 800)); G1.podosit_isaret(8)
G2 = GK(F, 'yumak', 470 - 118, 14, 236, kirp=(0, 20, 680, 800)); G2.podosit_isaret(8)
F.t(150, 286, 'Normal glomerül', 12.6, 800, INK, 'middle'); F.t(150, 304, '8 podosit', 11.6, None, INK2, 'middle')
F.t(470, 310, 'Glomerülomegali', 12.6, 800, RED, 'middle'); F.t(470, 326, 'yine 8 podosit → yoğunluk düşük', 11.6, None, INK2, 'middle')
F.ok(262, 170, 338, 170, INK2, 2.6); F.t(300, 158, 'hiperfiltrasyon', 11.4, None, INK2, 'middle')
F.el(32, 26, 7, 5.7, '#e9e3ff', '#3b2a73', 1.6); F.el(32, 26, 3.2, 2.6, '#3b2a73'); F.t(46, 30, 'işaretli: podosit', 11.2, None, INK2)
ADM = [('1', 'Obezite → metabolik yük ve renal vazodilatasyon → hiperfiltrasyon ve glomerülomegali'),
       ('2', 'Glomerül yüzeyi büyür, podosit sayısı artmaz; her podositin örteceği alan genişler'),
       ('3', 'Podosit gerilir, ayaksı çıkıntılar silinir, ayrılır → segmental skleroz')]
for i, (n, tx) in enumerate(ADM):
    y = 14 + i * 74
    F.r(682, y, 392, 66, TINT[BRAND], None, rx=10); F.el(704, y + 33, 14, 14, BRAND); F.t(704, y + 38, n, 13, 800, '#fff', 'middle')
    ws = tx.split(' '); ls = ['']
    for w_ in ws:
        if gen(ls[-1] + ' ' + w_, 11.8) > 330: ls.append(w_)
        else: ls[-1] = (ls[-1] + ' ' + w_).strip()
    F.tl(726, y + 28 - 8 * (len(ls) - 1), ls, 11.8, 16, fill=INK)
F.r(682, 244, 392, 90, '#fff', RED, 1.4, 10)
F.t(696, 266, 'Podosit yoğunluğu prognozu belirliyor', 12.4, 800, RED)
F.tl(696, 286, ['46 hasta, ortanca 4,1 yıl: 18’i (%39) bileşik', 'sonlanıma ulaştı; düşük podosit yoğunluğu', 'olan grupta sonuç belirgin daha kötü.'], 11.6, 16, fill=INK)
D.yeni('s15_org', 'x15_22', 'Gözden Kaçanlar · 2 · Şekil', 'Glomerül Büyüyor, Podosit Sayısı Aynı Kalıyor', F,
       '<b>Okuma:</b> İki glomerülde de sekiz podosit çizilmiştir; büyük glomerülde her podositin örtmesi gereken yüzey genişlemiştir. Podosit yoğunluğunun düşmesi, '
       'obeziteye bağlı glomerülopatide hem segmental sklerozun hem de kötü sonucun belirleyicisidir.',
       'Şekil: solda normal glomerül, ortada hiperfiltrasyonla büyümüş glomerül; ikisinde de sekiz podosit var. Sağda üç basamaklı mekanizma ve podosit yoğunluğunun prognostik değeri.')

# ---------------------------------------------------------------- 4 · idiyopatik nodüler glomerüloskleroz
F = Fig('nod', 360, 'İdiyopatik nodüler glomerülosklerozda Kimmelstiel-Wilson benzeri nodüller ve olguların ortak özellikleri', w=1080)
zemin(F, 6, 6, 640, 348)
G = GK(F, 'yumak', 40, 44, 250, kirp=(0, 20, 680, 800)); G.mez_agac(op=.45, cek=0); NP = G.noduller(6, 50); hp = G.hiyalinoz()
G.etiket(NP[1], 300, 30, ['Nodüller: mezangiyumda', 'hücreden fakir, lameller', 'matriks birikimi'], fs=11.6)
G.etiket(hp, 132, 24, ['Arteriyolde hiyalinoz'], fs=11.6)
B = GK(F, 'lobul', 390, 98, 206, cerceve=LINE); B.gbm_kalin(0, 158, 36, 4, 10); B.gbm_kalin(2, 176, 303, 4, 10); B.gbm_kalin(1, 272, 80, 4, 10)
B.nodul((452, 720), 120)
B.etiket((452, 720), 400, 336, ['Kimmelstiel-Wilson benzeri nodül'], fs=11.6)
F.t(666, 22, 'Tanımlayıcı seri · 5073 biyopside 23 olgu (%0,45)', 13, 800, BRANDD)
for i, (ad, v) in enumerate((('Hipertansiyon', 95.7), ('Sigara (ort. 52,9 paket-yılı)', 91.3), ('Hiperkolesterolemi', 90.0), ('Başvuruda böbrek yetmezliği', 82.6), ('Proteinüri > 3 g/gün', 69.6))):
    y = 40 + i * 28
    F.t(860, y + 14, ad, 11.6, 700, INK, 'end'); F.r(870, y + 3, 150, 15, '#f2f5f8', None, rx=4); F.r(870, y + 3, v * 1.5, 15, (RED, RED, RED, GOLD, GOLD)[i], None, rx=4)
    F.t(1074, y + 15, ('%' + f'{v:.1f}').replace('.', ','), 11.6, 800, INK, 'end')
F.t(666, 196, 'Nodül gördüğünüzde ayırıcı tanı sırası', 12.6, 800, BRANDD)
haplar(F, 666, 222, 408, ['1 Diyabetik nefropati', '2 Amiloidoz', '3 MIDD', '4 Fibriler, immünotaktoid, kriyo', '5 MPGN, kronik TMA', '6 İdiyopatik'], BRAND, 11.4)
D.yeni('s15_nod', 'x15_23', 'Gözden Kaçanlar · 3 · Şekil', 'Diyabetsiz Kimmelstiel-Wilson — Nodül Var, Şeker Yok', F,
       '<b>Okuma:</b> Mezangiyumda hücreden fakir, katmanlı nodüller diyabetik nefropatiyle aynı görünümü verir; ama hastalarda diyabet yoktur. Uzun süreli hipertansiyon, yoğun sigara ve '
       'hiperkolesterolemi neredeyse her olguda vardır. Tanı ancak diyabet, amiloid ve monoklonal birikim dışlandıktan sonra konur.',
       'Şekil: solda nodüler glomerüloskleroz; mezangiyumda katmanlı nodüller ve arteriyolde hiyalinoz, yanında büyütülmüş bir nodül. Sağda yirmi üç olguda ortak özellikler ve nodül görüldüğünde ayırıcı tanı sırası.', oz=OZGUN)

# ---------------------------------------------------------------- 5 · yarık diyaframı
F = Fig('yar', 380, 'Yarık diyaframının yakın görünümü: nefrin ve podosin', w=1080)
zemin(F, 6, 6, 600, 368)
GY = 238
F.r(20, GY, 572, 34, '#e4f0f4', GBM_K, 1.4, 6); F.r(20, GY + 9, 572, 12, GBM_D, None, rx=0); F.t(582, GY + 31, 'Glomerüler bazal membran', 10.4, 800, GBM_K, 'end')
F.t(146, 30, 'Ayaksı çıkıntı · aktin iskeleti', 12, 800, POD_K, 'middle'); F.t(458, 30, 'Komşu podositin ayaksı çıkıntısı', 12, 800, POD_K, 'middle')
for (x0, x1) in ((30, 262), (342, 574)):
    F.yol(f'M{x0},{GY} L{x0},86 Q{x0},44 {(x0 + x1) / 2},44 Q{x1},44 {x1},86 L{x1},{GY} Z', POD_K, 2, POD)
    for j in range(6):
        xx = x0 + 28 + j * 35; F.ln(xx, 70, xx, GY - 14, '#b46a5a', 1.1)
    for j in range(6): F.ln(x0 + 16, 88 + j * 22, x1 - 16, 92 + j * 22, '#b46a5a', .7)
for j in range(4):
    y = 210 + j * 6
    F.ln(262, y, 308, y + 2, RED, 2.2); F.ln(342, y + 3, 296, y + 1, RED, 2.2)
    for t in range(4): F.el(270 + t * 10, y + .6 + t * .5, 1.8, 1.8, '#fff', RED, .8); F.el(334 - t * 10, y + 2.6 - t * .5, 1.8, 1.8, '#fff', RED, .8)
for (x, sg) in ((262, -1), (342, 1)):
    F.yol(f'M{x},{206} q{sg * 9},12 0,26', PUR, 3.4)
F.r(236, 204, 16, 26, '#6a9a5e', None, rx=3); F.r(352, 204, 16, 26, '#6a9a5e', None, rx=3)
etk(F, (258, 222), 30, 300, ['Podosin (NPHS2)', 'zara tutunma noktasında,', 'nefrinle birlikte'], True, c=PUR, fs=11.4)
etk(F, (302, 222), 226, 300, ['Nefrin (NPHS1)', 'iki yandan gelip fermuar', 'gibi kenetlenir'], True, c=RED, fs=11.4)
etk(F, (360, 216), 426, 300, ['CD2AP', 'nefrini aktin', 'iskeletine bağlar'], True, c='#3f6f3a', fs=11.4)
kart(F, 626, 6, 448, 368, 'İki kurucu gen', ['NPHS1 · nefrin: Fin tipi konjenital nefrotik sendrom; intrauterin başlar, doğumda masif proteinüri; immünsüpresyona yanıtsız.',
                                              'Nefrin, immünglobulin ailesinden 1241 aminoasitlik transmembran adezyon molekülüdür.',
                                              'Nakilde: nefrini hiç görmemiş konakçıda de novo anti-nefrin antikoru gelişip nefrotik sendrom tekrarlayabilir.',
                                              'NPHS2 · podosin: otozomal resesif steroide dirençli nefrotik sendrom (1q25–31).'], RED)
D.yeni('s15_yar', 'x15_27', 'Genetik Podositopatiler · 2 · Şekil', 'Yarık Diyaframı — Nefrin Fermuarı, Podosin Kilidi', F,
       '<b>Okuma:</b> Komşu podositlerin ayaksı çıkıntıları arasındaki yarık diyaframını iki yandan gelen nefrin molekülleri kurar; podosin bu kompleksin zara bağlandığı yerde bulunur, '
       'CD2AP kompleksi aktin iskeletine bağlar. NPHS1 ya da NPHS2 bozulduğunda bariyer doğuştan ya da erken çocuklukta çöker.',
       'Şekil: solda iki komşu ayaksı çıkıntı ve aralarındaki yarık diyaframı; nefrin molekülleri fermuar gibi kenetlenir, podosin zarla birleştiği yerde, CD2AP aktin iskeletine bağlar. Sağda iki genin kliniği.')
