#!/usr/bin/env python3
"""Ders 21 · Kalıtsal Tübülopatiler ve CAKUT — şekil tanımları (sekil_kit ile çizilir)."""
from sekil_kit import *

L = []
OZGUN = ' <i>Özgün şematik çizim; ölçekli değildir.</i>'
D = '21'


def yeni(sid, hedef, kicker, baslik, F, alt, notu):
    L.append(dict(id=sid, ders=D, mod='yeni', hedef=hedef, kicker=kicker, baslik=baslik, svg=F.svg(), alt=alt + OZGUN, **{'not': notu}))


def ic(sid, hedef, F, alt=None, konum='son'):
    L.append(dict(id=sid, ders=D, mod='ic', hedef=hedef, svg=F.svg(), alt=alt, konum=konum))


def kutu(F, x, y, w, txt, c=INK2, fill='#fff', fs=12.6, h=32, kalin=True, tc=None):
    F.r(x, y - h / 2, w, h, fill, c, 1.6, 8); F.t(x + w / 2, y + fs * .36, txt, fs, 800 if kalin else None, tc or INK, 'middle')


def rozet(F, x, y, txt, c=RED, w=48):
    F.r(x - w / 2, y - 11, w, 22, c, None, rx=11); F.t(x, y + 4.4, txt, 12, 800, '#fff', 'middle')


def altigen(F, x, y, r=9, fill='#f0e2a0', st=GOLD):
    p = ' '.join('%.1f,%.1f' % (x + r * math.cos(math.radians(60 * i)), y + r * math.sin(math.radians(60 * i))) for i in range(6))
    F.a(f'<polygon points="{p}" fill="{fill}" stroke="{st}" stroke-width="1.5"/>')


# ============================================================================================== 1 · Henle kalın çıkan kol
F = Fig('tal', 416, 'Henle kalın çıkan kol hücresinde Bartter sendromu tiplerinin ve FHHNC’nin hedefleri', w=1080)
epitel(F, 'Henle kalın çıkan kol hücresi', h=338,
    para=('Ca²⁺ · Mg²⁺ — paraselüler yol (klodin-16 / klodin-19)', ['FHHNC', [('CLDN16 · CLDN19', 'i')]], PUR),
    apikal=[
        dict(y=98, ad='NKCC2', iyon='Na⁺ · K⁺ · 2Cl⁻', renk=BRAND, isaret='x', alt='kıvrım diüretiği burayı kapatır',
             tag=['Bartter tip 1', [('SLC12A1', 'i'), ' · antenatal'], 'idrar Ca²⁺ yüksek']),
        dict(y=196, ad='ROMK', iyon='K⁺', yon='cik', tip='kanal', renk=GREEN, isaret='x', alt=['K⁺ lümene geri döner,', 'lümeni pozitif (+) tutar'],
             tag=['Bartter tip 2', [('KCNJ1', 'i'), ' · antenatal'], 'yenidoğanda geçici', 'hiperkalemi']),
    ],
    bazal=[
        dict(y=84, ad='Na⁺/K⁺-ATPaz', iyon='3Na⁺', ters='2K⁺', yon='cik', tip='pompa', renk=INK2),
        dict(y=170, ad='ClC-Kb', iyon='Cl⁻', yon='cik', tip='kanal', renk=GOLD, isaret='x',
             tag=['Bartter tip 3', [('CLCNKB', 'i'), ' · değişken yaş'], 'Gitelman’ı taklit edebilir']),
        dict(y=236, ad='Barttin', tip='tas', renk=GOLD, isaret='x', alt=['ClC-K kanallarının', 'β alt birimi'],
             tag=['Bartter tip 4a / 4b', [('BSND', 'i'), ' / ', ('CLCNKA+CLCNKB', 'i')], 'sensorinöral işitme kaybı']),
    ])
F.r(721, 142, 38, 120, 'none', GOLD, 1.4, 14, '4 3')
F.el(440, 296, 50, 19, '#fff', PUR, 2); F.t(440, 301, 'MAGE-D2', 13, 800, PUR, 'middle')
F.yol('M478,284 C640,262 640,98 434,98', PUR, 2.2, ok=True, dash='6 4')
F.t(584, 188, 'NKCC2 ve NCC’yi', 11.8, None, PUR, 'end'); F.t(584, 203, 'zara yerleştirir', 11.8, None, PUR, 'end')
F.etiket(14, 296, 196, ['Bartter tip 5', [('MAGED2', 'i'), ' · X’e bağlı'], 'ağır antenatal tablo;', 'kendiliğinden düzelir'], RED, 12.4)
F.ln(213, 296, 388, 296, RED, 1.4, '2 4')
yeni('s21_tal', 'x21_8', 'Tuz Kaybı · 1 · Şekil', 'Bartter Sendromu — Henle Kalın Çıkan Kolunda Beş Hedef', F,
     '<b>Okuma:</b> NKCC2 tuzu hücreye alır; ROMK potasyumu lümene geri vererek lümeni pozitif tutar; klorür ClC-Kb ile kana çıkar. '
     'Zincirin hangi halkası koparsa kopsun tuz kaybı başlar. Kalsiyum ve magnezyumu paraselüler yoldan iten güç lümenin pozitif gerilimidir; '
     'gerilim kaybolunca ikisi de geri emilemez. Tip 1, 2 ve (aktif dönemde) tip 5’teki hiperkalsiüri bundandır; tip 3 ve 4’te idrar kalsiyumu değişken ya da normaldir.',
     'Şekil: Henle kalın çıkan kol hücresi. Bartter sendromunun beş tipi tek bir taşıma zincirinin farklı halkalarıdır. '
     'Tip 1 NKCC2, tip 2 ROMK, tip 3 ClC-Kb, tip 4 barttin, tip 5 MAGE-D2. Altta paraselüler kalsiyum ve magnezyum yolu ile klodin 16 ve 19 görülüyor.')

# ============================================================================================== 2 · distal kıvrımlı tübül
F = Fig('dkt', 348, 'Distal kıvrımlı tübül hücresi: Gitelman ve EAST sendromlarının hedefleri', w=1080)
epitel(F, 'Distal kıvrımlı tübül hücresi', h=334,
    apikal=[
        dict(y=98, ad='NCC', iyon='Na⁺ · Cl⁻', renk=BRAND, isaret='x', alt='tiyazid burayı kapatır',
             tag=['Gitelman sendromu', [('SLC12A3', 'i'), ' · otozomal resesif'], 'hipokalsiüri,', 'hipomagnezemi']),
        dict(y=222, ad='TRPM6', iyon='Mg²⁺', tip='kanal', renk=GOLD, alt=['NCC kaybında azalır', '(fare modeli)'],
             tag=['Hipomagnezemi', 'idrarla Mg²⁺ kaybı:', 'Gitelman ve EAST’in', 'ortak bulgusu'], tagc=GOLD),
    ],
    bazal=[
        dict(y=84, ad='Na⁺/K⁺-ATPaz', iyon='3Na⁺', ters='2K⁺', yon='cik', tip='pompa', renk=INK2),
        dict(y=184, ad='Kir4.1', iyon='K⁺', yon='cik', tip='kanal', renk=GREEN, isaret='x', alt=['K⁺ geri dönüşü', 'pompayı besler'],
             tag=['EAST / SeSAME', [('KCNJ10', 'i'), ' · otozomal resesif'], 'epilepsi, ataksi,', 'işitme kaybı']),
        dict(y=286, ad='ClC-Kb', iyon='Cl⁻', yon='cik', tip='kanal', renk=GOLD, isaret='x',
             tag=['Bartter tip 3', [('CLCNKB', 'i')], 'Gitelman benzeri tablo']),
    ])
yeni('s21_dkt', 'x21_10', 'Tuz Kaybı · 3 · Şekil', 'Gitelman ve EAST — Distal Kıvrımlı Tübülde Aynı Zincir', F,
     '<b>Okuma:</b> NCC tuzu alır; bazolateraldeki Kir4.1 potasyumu geri döndürerek pompayı çalışır tutar. NCC (Gitelman) ya da Kir4.1 (EAST) '
     'bozulduğunda tablo aynıdır: tiyazid almış gibi hipokalemik alkaloz, hipomagnezemi ve hipokalsiüri. Ayırt eden böbrek değil, böbrek dışı '
     'bulgudur: Kir4.1 beyin ve iç kulakta da bulunur.',
     'Şekil: distal kıvrımlı tübül hücresi. Apikalde NCC ve magnezyum kanalı TRPM6, bazolateralde Kir 4.1 ve ClC-Kb. '
     'Gitelman sendromunda NCC, EAST sendromunda Kir 4.1 bozuktur; ikisi de aynı laboratuvar tablosunu verir.')

# ============================================================================================== 3 · esas hücre (Liddle, AME, PHA-1)
F = Fig('esas', 368, 'Toplayıcı kanal esas hücresi: Liddle sendromu, görünürde mineralokortikoid fazlalığı, PHA tip 1 ve Geller sendromu', w=1080)
epitel(F, 'Toplayıcı kanal esas hücresi', h=352,
    apikal=[
        dict(y=100, ad='ENaC', iyon='Na⁺', tip='kanal', renk=BRAND, isaret='a', alt='amilorid burayı kapatır',
             tag=['Liddle sendromu', [('SCNN1B · SCNN1G', 'i')], 'işlev kazanımı: kanal', 'zardan çekilemez']),
        dict(y=306, ad='ROMK', iyon='K⁺', yon='cik', tip='kanal', renk=GREEN, alt=['Na⁺ girdikçe K⁺', 'sekresyonu artar']),
    ],
    bazal=[dict(y=86, ad='Na⁺/K⁺-ATPaz', iyon='3Na⁺', ters='2K⁺', yon='cik', tip='pompa', renk=INK2)])
F.etiket(14, 200, 196, ['PHA tip 1 · resesif', 'ENaC α, β, γ işlev kaybı', 'ter ve akciğer de etkilenir'], RED, 12.4)
F.ln(212, 186, 316, 130, RED, 1.4, '2 4'); F.isaret(322, 127, 'x', 8)
# NEDD4-2
F.el(440, 178, 46, 16, '#fff', GOLD, 2); F.t(440, 182.5, 'NEDD4-2', 12.2, 800, GOLD, 'middle')
F.engel(404, 167, 356, 142, GOLD, 2.4, 6)
F.t(494, 174, 'ENaC’i işaretler,', 11.8, None, INK2); F.t(494, 189, 'zardan çeker', 11.8, None, INK2)
# MR ve aldosteron
F.r(596, 200, 58, 34, PUR, None, rx=8); F.t(625, 222, 'MR', 13.5, 800, '#fff', 'middle')
F.ok(836, 217, 658, 217, PUR, 2.6); F.t(766, 208, 'Aldosteron', 13, 800, PUR)
F.ok(594, 217, 506, 217, PUR, 2.4); F.t(500, 213, 'ENaC ve pompa', 11.8, None, INK2, 'end'); F.t(500, 228, 'sayısı ↑', 11.8, None, INK2, 'end')
F.engel(625, 262, 625, 238, RED, 2.4); F.t(625, 277, 'spironolakton', 12, 700, RED, 'middle')
# kortizol
F.r(604, 290, 92, 30, GREEN, None, rx=8); F.t(650, 310, '11β-HSD2', 12.5, 800, '#fff', 'middle'); F.isaret(696, 290, 'x')
F.ok(836, 305, 700, 305, GOLD, 2.6); F.t(766, 296, 'Kortizol', 13, 800, GOLD)
F.ok(602, 305, 546, 305, GREEN, 2.4); F.t(540, 309, 'Kortizon (etkisiz)', 12, 700, GREEN, 'end')
F.yol('M722,297 Q706,254 660,232', GOLD, 2, ok=True, dash='5 4')
F.etiket(870, 162, 196, ['PHA tip 1 · dominant', [('NR3C2', 'i'), ' · MR işlev kaybı']], RED, 12.4); F.ln(868, 170, 658, 208, RED, 1.4, '2 4')
F.etiket(870, 230, 196, ['Geller sendromu', 'MR’da işlev kazanımı;', 'gebelikte ağırlaşır'], RED, 12.4); F.ln(868, 234, 658, 227, RED, 1.4, '2 4')
F.etiket(870, 314, 196, ['AME', [('HSD11B2', 'i'), ' eksik (resesif):'], 'kortizol MR’ı uyarır;', 'meyan kökü: edinsel biçim'], RED, 12.4)
yeni('s21_esas', 'x21_12', 'Hipertansif · 1 · Şekil', 'Liddle, AME ve PHA Tip 1 — Esas Hücrede Aldosteron Ekseni', F,
     '<b>Okuma:</b> Aldosteron MR’a bağlanınca ENaC ve pompa artar; sodyum girer, potasyum çıkar. Eksen üç yerden <b>açık kalabilir</b>: kanal '
     '(Liddle), reseptör (Geller) ya da reseptörü kortizolden koruyan enzimin yokluğu (AME); üçünde de renin ve aldosteron baskılıdır. Eksen '
     '<b>kapandığında</b> tablo tersine döner: PHA tip 1’de tuz kaybı, hiperkalemi ve çok yüksek aldosteron vardır.',
     'Şekil: toplayıcı kanal esas hücresi. Aldosteron mineralokortikoid reseptörüne bağlanır, ENaC ve sodyum potasyum pompası artar. '
     'Liddle sendromunda kanal zardan çekilemez. Görünürde mineralokortikoid fazlalığında kortizolü kortizona çeviren enzim yoktur. '
     'Psödohipoaldosteronizm tip 1’de ise kanal ya da reseptör çalışmaz.')

# ============================================================================================== 4 · Gordon (PHA-2)
F = Fig('gor', 352, 'Distal kıvrımlı tübül hücresinde WNK–SPAK–NCC yolu ve Gordon sendromu', w=1080)
epitel(F, 'Distal kıvrımlı tübül hücresi', h=338,
    apikal=[
        dict(y=108, ad='NCC', iyon='Na⁺ · Cl⁻', renk=BRAND, isaret='a',
             tag=['Gordon sendromu (PHA-2)', 'NCC aşırı etkin: tuz', 'tutulumu, hipertansiyon']),
        dict(y=270, ad='ROMK', iyon='K⁺', yon='cik', tip='kanal', renk=MUT, isaret='x', alt=['WNK, ROMK’u', 'zardan çeker'],
             tag=['Hiperkalemi + asidoz', 'distale Na⁺ az ulaşır,', 'ROMK azalır: K⁺ ve H⁺', 'atılamaz; serum Na⁺ normal']),
    ],
    bazal=[dict(y=308, ad='Na⁺/K⁺-ATPaz', iyon='3Na⁺', ters='2K⁺', yon='cik', tip='pompa', renk=INK2)])
F.t(314, 132, 'tiyazid kapatır', 11.8, 700, RED, 'end'); F.engel(318, 128, 328, 119, RED, 2.2, 5)
F.r(590, 62, 130, 32, '#fff', PUR, 1.8, 8); F.t(655, 83, 'KLHL3 – CUL3', 12.8, 800, PUR, 'middle')
F.t(655, 110, 'ubikitin ligaz', 11.5, None, INK2, 'middle')
F.engel(655, 116, 655, 147, PUR, 2.4); F.t(645, 136, 'yıkıma gönderir', 11.5, None, PUR, 'end')
F.r(600, 152, 110, 32, TINT[GOLD], GOLD, 1.8, 8); F.t(655, 173, 'WNK1 · WNK4', 12.8, 800, GOLD, 'middle')
F.ok(598, 168, 540, 168, GOLD, 2.4)
F.r(432, 152, 106, 32, TINT[BRAND], BRAND, 1.8, 8); F.t(485, 173, 'SPAK · OSR1', 12.8, 800, BRAND, 'middle')
F.ok(432, 158, 388, 132, BRAND, 2.4)
F.el(374, 126, 10, 10, GOLD, '#fff', 1.6); F.t(374, 130.4, 'P', 11.5, 800, '#fff', 'middle')
F.t(440, 202, 'NCC’yi fosforiller (etkinleştirir)', 11.5, None, BRAND)
F.el(524, 238, 50, 15, '#fff', INK2, 1.8); F.t(524, 242.4, 'Kalsinörin', 12, 800, INK2, 'middle')
F.t(586, 258, 'NCC ve KLHL3’ü', 11.5, None, INK2); F.t(586, 272, 'defosforile eder', 11.5, None, INK2)
F.yol('M478,232 Q402,200 379,139', INK2, 1.8, dash='5 4'); F.ln(385.6, 136.5, 372.4, 141.5, INK2, 2.6)
F.yol('M572,230 Q727,226 727,150 Q727,112 718,98', INK2, 1.8, ok=True, dash='5 4')
F.etiket(870, 80, 196, ['KLHL3 · CUL3 mutasyonu', 'WNK yıkılamaz, birikir', 'CUL3: daha ağır seyir'], RED, 12.4); F.ln(868, 80, 724, 80, RED, 1.4, '2 4')
F.etiket(870, 168, 196, ['WNK1 · WNK4 mutasyonu', 'kinaz artar ya da', 'yıkımdan kaçar'], RED, 12.4); F.ln(868, 168, 714, 168, RED, 1.4, '2 4')
F.etiket(870, 242, 196, ['Takrolimus', 'kalsinörini baskılar: KLHL3', 've NCC fosforile kalır, WNK4', 'birikir; edinsel Gordon tablosu'], GOLD, 12.4); F.engel(868, 238, 578, 238, GOLD, 2.2, 7)
yeni('s21_gordon', 'x21_13', 'Aldosteron ekseni · 2 · Şekil', 'Gordon Sendromu — WNK Birikir, NCC Kapanamaz', F,
     '<b>Okuma:</b> KLHL3–CUL3, WNK kinazlarını yıkıma gönderen ubikitin ligazdır. KLHL3, CUL3, WNK1 ya da WNK4 mutasyonlarında WNK birikir; '
     'SPAK/OSR1 üzerinden NCC fosforile ve sürekli etkin kalır. Tablo tiyazidin ayna görüntüsüdür; düşük doz tiyazidin tabloyu düzeltmesi bundandır. '
     'Takrolimus kalsinörini baskılar; KLHL3 ve NCC fosforile kalır, aynı son noktaya ulaşılır.',
     'Şekil: Gordon sendromu. KLHL3 ve CUL3 birlikte WNK kinazlarını yıkıma gönderir. Bu sistem bozulunca WNK birikir, SPAK ve OSR1 üzerinden '
     'NCC’yi sürekli etkin tutar. Sonuç tuz tutulumu, hipertansiyon ve hiperkalemidir. Takrolimus kalsinörini baskılayarak benzer bir tablo yapar.')

# ============================================================================================== 5 · proksimal tübül hücresi (Fanconi)
F = Fig('fan', 412, 'Proksimal tübül hücresi: Fanconi sendromunda birlikte bozulan taşıma yolları', w=1080)
epitel(F, 'Proksimal tübül hücresi', h=398, firca=True,
    apikal=[
        dict(y=78, ad='SGLT2', iyon='Na⁺ · glukoz', renk=BRAND, tag=['Glukozüri', 'kan şekeri normalken']),
        dict(y=150, ad='NaPi-IIa / IIc', iyon='Na⁺ · fosfat', renk=GOLD, tag=['Fosfatüri, hipofosfatemi', 'raşitizm / osteomalazi']),
        dict(y=222, ad='Aminoasit taşıyıcıları', iyon='Na⁺ · aminoasit', renk=PUR, tag=['Yaygın aminoasidüri']),
        dict(y=294, ad='NHE3', iyon='Na⁺', ters='H⁺', renk=GREEN, tag=['Bikarbonatüri', 'proksimal (tip 2) RTA']),
        dict(y=366, ad='Megalin · kübilin', iyon='DMA proteinler', tip='res', renk=ACC, alt='reseptör aracılı endositoz',
             tag=['DMA proteinüri', 'dipstick eser ya da negatif']),
    ],
    bazal=[
        dict(y=92, ad='Na⁺/K⁺-ATPaz', iyon='3Na⁺', ters='2K⁺', yon='cik', tip='pompa', renk=INK2,
             tag=['Sık ortak yol', '(tek yol değil): ATP azalınca', 'Na⁺ gradyanı düşer'], tagc=BRAND),
        dict(y=196, ad='NBCe1', iyon='Na⁺ · 3HCO₃⁻', yon='cik', renk=GREEN),
        dict(y=278, ad='GLUT2', iyon='glukoz', yon='cik', renk=BRAND, tag=['Fanconi-Bickel sendromu', [('SLC2A2', 'i'), ' (GLUT2)']]),
    ])
F.el(584, 152, 46, 23, '#fde9c8', GOLD, 2); F.yol('M552,152 q8,-13 16,0 t16,0 t16,0 t16,0', GOLD, 1.8)
F.t(584, 192, 'Mitokondri', 12, 800, GOLD, 'middle')
F.ok(626, 140, 706, 118, GOLD, 2.4); F.t(680, 146, 'ATP', 12.5, 800, GOLD, 'middle')
F.etiket(516, 348, 218, ['Neden hepsi birlikte bozulur?', 'Na⁺’a bağlı taşıyıcılar gradyanla', 'çalışır; gradyanı pompa ATP ile', 'kurar. Endositoz da ATP ister.'], BRAND, 12.2)
yeni('s21_fanconi', 'x21_15', 'Proksimal · 1 · Şekil', 'Fanconi Sendromu — Tek Hücre, Birlikte Duran Taşıyıcılar', F,
     '<b>Okuma:</b> Fanconi sendromu tek bir taşıyıcının değil, hücrenin enerji ve endositoz düzeninin hastalığıdır. Sistinozis, tenofovir, ifosfamid, '
     'hafif zincirler, ağır metaller ve mitokondriyal sitopatiler aynı son yolu bozar; idrarda glukoz, fosfat, aminoasit, bikarbonat, ürat ve düşük '
     'molekül ağırlıklı (DMA) proteinler birlikte görülür.',
     'Şekil: proksimal tübül hücresi. Solda fırçamsı kenardaki taşıyıcılar, sağda bazolateral çıkış yolları. Megalin dışındaki apikal taşıyıcılar sodyum '
     'gradyanıyla çalışır; gradyanı bazolateral sodyum potasyum ATPaz kurar. Megalin ile endositoz da enerji ister. Hücrenin enerjisi azaldığında hepsi birlikte durur; Fanconi sendromunun sık görülen mantığı budur.')

# ============================================================================================== 6 · endositoz ve lizozom (Dent, sistinozis)
F = Fig('end', 432, 'Proksimal tübül hücresinde endositoz ve lizozom yolu: Dent hastalığı ve sistinozis', w=1080)
F.r(6, 8, 214, 300, LUMEN, None, rx=8); F.r(220, 8, 854, 300, HUCRE, None, rx=0)
yy = 14
while yy < 304:
    F.ln(209, yy, 220, yy, BRANDD, 2.2); yy += 7
F.ln(220, 8, 220, 308, BRANDD, 4.5, cap='butt')
F.t(18, 30, 'LÜMEN · idrar', 12.5, 800, GOLD, ls='.06em')
F.t(647, 32, 'Proksimal tübül hücresi — endositoz ve lizozom yolu', 15, 800, BRANDD, 'middle')
for (px, py) in ((96, 128), (130, 112), (150, 140), (116, 152), (170, 120), (76, 146)): F.el(px, py, 5, 5, ACC)
F.t(18, 186, 'Süzülen DMA proteinler', 12, 700, ACC)
_ = __import__('sekil_kit')._sekil(F, 220, 122, 'res', ACC)
F.t(196, 90, 'Megalin · kübilin', 12.5, 800, INK, 'end')
F.ok(236, 122, 290, 122, ACC, 2.4)
F.el(322, 122, 26, 26, '#fff', ACC, 2.5, dash='5 3')
for (px, py) in ((314, 116), (330, 126), (318, 132)): F.el(px, py, 4, 4, ACC)
F.t(322, 168, 'Kaplı kesecik', 11.8, 700, INK2, 'middle')
F.etiket(238, 224, 168, ['OCRL', 'Dent-2 · Lowe sendromu', 'kesecik trafiği bozulur'], RED, 12.2); F.ln(322, 174, 322, 190, RED, 1.4, '2 4')
F.ok(350, 122, 424, 122, ACC, 2.4)
F.el(490, 127, 62, 62, '#fff7e0', GOLD, 2.5)
F.t(490, 106, 'Erken endozom', 12.5, 800, GOLD, 'middle'); F.t(490, 130, 'pH düşer', 12.2, 700, INK, 'middle'); F.t(490, 147, 'ligand ayrılır', 11.5, None, INK2, 'middle')
F.el(446, 172, 13, 13, INK2, '#fff', 1.6); F.t(446, 176, 'H⁺', 10.5, 800, '#fff', 'middle'); F.t(446, 204, 'V-ATPaz', 11.8, 800, INK, 'middle')
F.el(538, 172, 15, 11, BRAND, '#fff', 1.6); F.isaret(553, 160, 'x', 8.5)
F.t(562, 190, 'ClC-5', 12.5, 800, BRAND); F.t(562, 205, '2Cl⁻ girer · H⁺ çıkar', 11.5, None, INK2)
F.etiket(456, 268, 222, ['Dent-1 · CLCN5', 'endozomda asitlenme ve klorür', 'birikimi bozulur; megalin', 'zara geri dönemez'], RED, 12.2); F.ln(550, 212, 550, 228, RED, 1.4, '2 4')
F.yol('M452,66 C400,42 300,46 232,86', ACC, 2.2, ok=True, dash='6 4'); F.t(330, 40, 'megalin zara geri döner', 11.5, None, ACC, 'middle')
F.ok(554, 122, 666, 122, INK2, 2.4); F.t(610, 112, 'geç endozom', 11.2, None, MUT, 'middle')
F.el(742, 134, 72, 72, '#f3ecfa', PUR, 2.5)
F.t(742, 92, 'Lizozom', 13, 800, PUR, 'middle'); F.t(742, 111, 'proteinleri', 11.5, None, INK2, 'middle'); F.t(742, 126, 'aminoasitlere yıkar', 11.5, None, INK2, 'middle')
for (px, py) in ((716, 156), (742, 168), (768, 154)): altigen(F, px, py, 9)
F.t(742, 194, 'sistin', 11.8, 800, GOLD, 'middle')
F.r(803, 118, 22, 32, PUR, '#fff', 2, 11); F.isaret(827, 112, 'x', 8.5)
F.ok(828, 134, 904, 134, PUR, 2.4); F.t(868, 124, 'sistin + H⁺', 12, 700, PUR, 'middle')
F.t(838, 162, 'Sistinozin', 12.5, 800, INK)
F.etiket(866, 232, 200, ['Nefropatik sistinozis', [('CTNS', 'i'), ' · otozomal resesif'], 'sistin çıkamaz, birikir,', 'kristalleşir'], RED, 12.2); F.ln(852, 168, 886, 192, RED, 1.4, '2 4')
F.r(6, 320, 524, 104, '#fff', RED, 1.4, 10)
F.t(20, 342, 'Dent hastalığında ne olur?', 13, 800, RED)
F.tl(20, 362, ['ClC-5 çalışmayınca megalin ve kübilin zara geri dönemez; fırçamsı', 'kenarda reseptör azalır. Süzülen DMA proteinler geri alınamaz ve idrara',
               'çıkar. Hiperkalsiürinin mekanizması ise tam aydınlatılmamıştır.'], 12.2, 17, fill=INK)
F.r(542, 320, 532, 104, '#fff', PUR, 1.4, 10)
F.t(556, 342, 'Sisteamin nasıl çalışır?', 13, 800, PUR)
F.tl(556, 362, ['Lizozoma girer ve sistini ikiye böler: sistein + sistein-sisteamin (karma', 'disülfit). Karma disülfit lizin taşıyıcısından (PQLC2 / SLC66A1), sistein',
                'kendi taşıyıcısından çıkar; bozuk sistinozin böylece atlanmış olur.'], 12.2, 17, fill=INK)
yeni('s21_endo', 'x21_16', 'Proksimal · 2 · Şekil', 'Dent Hastalığı ve Sistinozis — Aynı Yolun İki Durağı', F,
     '<b>Okuma:</b> Süzülen küçük proteinler megalin-kübilin ile yakalanır, endozomda asit ortamda reseptörden ayrılır, lizozomda aminoasitlere yıkılır. '
     'Dent hastalığı yolun başını (endozom), sistinozis sonunu (lizozomdan çıkış) tutar; ikisi de düşük molekül ağırlıklı proteinüri ve Fanconi tablosu verir.',
     'Şekil: proksimal tübül hücresinde endositoz yolu. Dent hastalığında endozomdaki ClC-5 çalışmaz, megalin zara geri dönemez. '
     'Sistinoziste lizozom zarındaki sistinozin yoktur, sistin lizozomda birikir. Sisteamin sistini parçalayarak başka taşıyıcılardan çıkmasını sağlar.')

# ============================================================================================== 7 · sistinüri + XLH
F = Fig('sxl', 398, 'Sistinüride apikal aminoasit taşıyıcısı ve X’e bağlı hipofosfatemide FGF23 ekseni', w=1080)
F.r(6, 6, 514, 30, TINT[BRAND], None, rx=8); F.t(18, 27, 'Sistinüri — taşıyıcı kusuru', 14, 800, BRANDD)
F.r(6, 42, 250, 250, LUMEN, None, rx=8); F.r(256, 42, 264, 250, HUCRE, None, rx=0)
yy = 48
while yy < 288:
    F.ln(245, yy, 256, yy, BRANDD, 2.2); yy += 7
F.ln(256, 42, 256, 292, BRANDD, 4.5, cap='butt')
F.t(18, 62, 'LÜMEN', 11.5, 800, GOLD, ls='.06em'); F.t(388, 64, 'Proksimal tübül hücresi', 13, 800, BRANDD, 'middle')
F.ok(96, 142, 342, 142, BRAND, 2.6)
F.el(238, 124, 13, 17, PUR, '#fff', 1.8); F.r(243, 120, 26, 44, BRAND, '#fff', 2, 13); F.isaret(274, 112, 'x')
F.t(214, 100, 'rBAT', 13, 800, INK, 'end'); F.t(214, 115, [('SLC3A1', 'i'), ' · tip A'], 11.8, None, INK2, 'end')
F.t(294, 106, 'b⁰,⁺AT', 13, 800, INK); F.t(294, 121, [('SLC7A9', 'i'), ' · tip B'], 11.8, None, INK2)
F.t(18, 166, 'sistin · ornitin · lizin · arjinin', 12.2, 700, BRAND)
F.t(288, 166, 'karşılığında nötral aminoasit', 11.5, None, MUT); F.t(288, 180, 'lümene çıkar', 11.5, None, MUT)
for (px, py) in ((52, 214), (86, 230), (118, 208), (150, 234), (184, 212)): altigen(F, px, py, 10)
F.t(18, 266, 'Yalnız sistin çöker (asit idrarda', 12, 700, GOLD); F.t(18, 281, 'çözünmez): altıgen kristal, taş', 12, 700, GOLD)
F.t(288, 232, 'Dördü de idrarla atılır;', 12, None, INK); F.t(288, 248, 'taş yapan yalnız sistindir.', 12, None, INK)
F.t(6, 318, 'Tedavi hedefi', 12.4, 800, GREEN)
cx_ = 104
for tx_ in ('idrar pH > 7,5', 'dansite ≤ 1,005', 'sistin bağlayıcı tiyol'):
    w_ = gen(tx_, 12.2) + 22; F.r(cx_, 302, w_, 26, TINT[GREEN], GREEN, 1.3, 13); F.t(cx_ + w_ / 2, 319.5, tx_, 12.2, 700, INK, 'middle'); cx_ += w_ + 8
F.tl(6, 350, ['Fransız kohortu (442 hasta): 16 yaş üstü hastaların %26,7’sinde eGFR < 60;', 'KBH ile ilişkili etkenler yaş, hipertansiyon ve ciddi parankim hasarı.'], 12, 16, fill=INK2)
# XLH
F.r(540, 6, 534, 30, TINT[PUR], None, rx=8); F.t(552, 27, 'X’e bağlı hipofosfatemi — FGF23 fazlalığı', 14, 800, PUR)
F.r(540, 52, 142, 100, '#f6efe2', GOLD, 1.8, 12)
F.t(611, 74, 'Kemik · osteosit', 12.5, 800, GOLD, 'middle'); F.t(611, 99, [('PHEX', 'i'), ' işlev kaybı'], 12.5, None, INK, 'middle'); F.isaret(678, 56, 'x')
F.t(611, 132, 'FGF23 yapımı ↑', 13, 800, RED, 'middle')
F.ok(684, 102, 784, 102, RED, 3); F.t(734, 92, 'FGF23 ↑', 13, 800, RED, 'middle')
F.engel(734, 168, 734, 110, GREEN, 2.4); F.t(734, 184, 'burosumab', 12.4, 800, GREEN, 'middle'); F.t(734, 199, 'FGF23’ü bağlar', 11.5, None, INK2, 'middle')
F.r(790, 52, 284, 240, HUCRE, BRANDD, 2, 10); F.t(942, 74, 'Proksimal tübül hücresi', 13, 800, BRANDD, 'middle')
F.r(784, 84, 12, 38, PUR, '#fff', 1.6, 6); F.t(804, 98, 'FGFR1 · Klotho', 12.5, 800, INK)
F.ok(820, 108, 820, 132, INK2, 2.2)
F.etiket(800, 162, 264, ['NaPi-IIa / IIc zardan çekilir', 'fosfat geri emilimi ↓ → fosfatüri'], RED, 12.2)
F.ok(820, 188, 820, 208, INK2, 2.2)
F.etiket(800, 246, 264, ['1α-hidroksilaz ↓ · 24-hidroksilaz ↑', '1,25(OH)₂D düşük ya da', 'uygunsuz normal'], RED, 11.8)
F.r(540, 302, 534, 90, '#fff', PUR, 1.4, 10); F.t(554, 323, 'Sonuç', 12.6, 800, PUR)
F.tl(554, 342, ['Hipofosfatemi + düşük ya da uygunsuz normal 1,25(OH)₂D: çocukta raşitizm,', 'erişkinde osteomalazi. Klasik tedavi (fosfat + aktif D vitamini) eksiği yerine',
                'koyar; burosumab ise aracıyı, yani fazla FGF23’ü hedefler.'], 12, 16, fill=INK)
yeni('s21_sxl', 'x21_17', 'Proksimal · 3 · Şekil', 'Sistinüri ve XLH — Biri Taşıyıcı, Diğeri Hormon Hastalığı', F,
     '<b>Okuma:</b> İkisi de proksimal tübülde geri emilim kaybıyla görünür, ama mekanizma farklıdır. Sistinüride kusur taşıyıcının kendisindedir '
     '(rBAT / b⁰,⁺AT). XLH’de taşıyıcı sağlamdır; kemikten gelen fazla FGF23 fosfat taşıyıcısını zardan çeker ve aktif D vitamini yapımını baskılar.',
     'Şekil: solda sistinüri, sağda X’e bağlı hipofosfatemi. Sistinüride apikal aminoasit taşıyıcısı bozuktur; dört aminoasit atılır, yalnız sistin taş yapar. '
     'X’e bağlı hipofosfatemide FGF23 artar, fosfat taşıyıcıları zardan çekilir, aktif D vitamini düşer. Burosumab FGF23’ü bağlar.')

# ============================================================================================== 8 · glioksilat yolu (primer hiperoksalüri)
F = Fig('oks', 430, 'Karaciğer hücresinde glioksilat metabolizması: primer hiperoksalüri tipleri ve siRNA hedefleri', w=1080)
F.r(6, 8, 790, 414, '#fbf7f0', '#b08a5a', 2, 16); F.t(520, 34, 'KARACİĞER HÜCRESİ · sitozol', 12.5, 800, '#8a6a3a', ls='.06em')
F.r(22, 42, 470, 150, '#eaf7ef', GREEN, 1.8, 14); F.t(36, 62, 'Peroksizom', 12.5, 800, GREEN)
kutu(F, 36, 124, 90, 'Glikolat'); kutu(F, 232, 124, 100, 'Glioksilat'); kutu(F, 420, 124, 60, 'Glisin')
F.ok(128, 124, 228, 124, INK2, 2.6); F.t(178, 112, 'GO', 13, 800, INK, 'middle'); F.t(178, 148, 'HAO1', 11.5, None, INK2, 'middle', it=True)
F.ok(334, 124, 416, 124, INK2, 2.6); F.t(375, 112, 'AGT', 13, 800, INK, 'middle'); F.t(375, 148, 'AGXT', 11.5, None, INK2, 'middle', it=True)
F.isaret(375, 124, 'x', 8.5); rozet(F, 428, 76, 'PH1')
F.t(508, 208, 'Piridoksin (B6) AGT’nin kofaktörüdür;', 11.5, 700, GREEN); F.t(508, 223, 'yanıt yalnız PH1’de beklenir.', 11.5, 700, GREEN)
F.etiket(110, 78, 150, ['Lumasiran (siRNA)'], PUR, 12); F.engel(206, 92, 206, 117, PUR, 2.4, 7)
kutu(F, 60, 262, 90, 'Glikolat'); kutu(F, 232, 262, 100, 'Glioksilat'); kutu(F, 470, 262, 112, 'OKSALAT', RED, TINT[RED], 13.5, tc=RED)
F.ok(282, 142, 282, 243, RED, 2.2, '6 4'); F.t(292, 216, 'AGT yoksa sitozole taşar', 11.2, None, RED)
F.ok(334, 262, 466, 262, RED, 3); F.t(400, 252, 'LDHA', 13, 800, INK, 'middle')
F.etiket(420, 312, 152, ['Nedosiran (siRNA)'], PUR, 12); F.engel(432, 296, 432, 270, PUR, 2.4, 7)
F.ok(230, 262, 154, 262, INK2, 2.6); F.t(192, 250, 'GRHPR', 12.5, 800, INK, 'middle'); F.isaret(192, 262, 'x', 8.5); rozet(F, 192, 288, 'PH2')
F.ok(96, 244, 96, 144, INK2, 2.2); F.t(104, 216, 'peroksizoma döner', 11.2, None, MUT)
F.r(22, 326, 470, 84, '#fde9c8', GOLD, 1.8, 14); F.t(36, 346, 'Mitokondri', 12.5, 800, GOLD)
kutu(F, 36, 378, 114, 'Hidroksiprolin'); kutu(F, 204, 378, 58, 'HOG'); kutu(F, 334, 378, 146, 'Glioksilat + pirüvat')
F.ok(152, 378, 200, 378, INK2, 2.6); F.ok(264, 378, 330, 378, INK2, 2.6); F.isaret(297, 378, 'x', 8.5)
F.t(292, 354, 'HOGA1', 12.5, 800, INK, 'end'); rozet(F, 322, 349, 'PH3', w=44)
F.ok(430, 360, 322, 282, INK2, 2.2, '6 4')
F.etiket(508, 112, 276, ['İki siRNA, iki basamak', 'Lumasiran GO’yu susturur: glioksilat', 'azalır; biriken glikolat idrarla atılır.', 'Nedosiran LDHA’yı susturur; etkisi PH1’de', 'gösterildi, PH2’de gösterilemedi.'], PUR, 12)
F.t(508, 372, 'PH3: HOG birikir; oksalat artışının', 11.5, None, INK2); F.t(508, 387, 'yolu tam aydınlatılmamıştır.', 11.5, None, INK2)
F.ok(584, 262, 892, 262, RED, 3); F.t(690, 252, 'kana geçer', 12, 700, RED, 'middle')
F.r(812, 8, 262, 34, TINT[RED], None, rx=8); F.t(943, 30, 'Oksalat başlıca böbrekten atılır', 13, 800, RED, 'middle')
bobrek(F, 936, 262, 1.05)
for (px, py) in ((924, 240), (918, 282), (932, 262)): F.el(px, py, 3.4, 3.4, '#fff', GOLD, 1.2)
F.tl(826, 342, ['• Kalsiyum oksalat taşı, nefrokalsinoz', '• GFR düşünce plazma oksalatı yükselir', '• Sistemik oksaloz: kemik, retina,', '  miyokard, damar, deri'], 12.2, 17, fill=INK)
F.tl(826, 76, ['PH1 tanısı konmadan yapılan', 'izole böbrek nakli greft', 'kaybıyla sonuçlanır.'], 12, 16, fill=INK2)
yeni('s21_oksalat', 'x21_18', 'Proksimal Tübül · 4 · Şekil', 'Primer Hiperoksalüri — Glioksilat Yolunda Üç Enzim, İki İlaç', F,
     '<b>Okuma:</b> Glioksilatın iki zararsız çıkışı vardır: peroksizomda AGT ile glisine, sitozolde GRHPR ile glikolata döner. Bu yollardan biri '
     'kapanınca glioksilat LDH ile oksalata çevrilir. İlaçlar bozuk enzimi onarmaz; yolu daha önce (GO) ya da en sonda (LDHA) keser.',
     'Şekil: karaciğer hücresinde glioksilat metabolizması. Tip 1’de peroksizomdaki AGT, tip 2’de sitozoldeki GRHPR, tip 3’te mitokondrideki HOGA1 eksiktir. '
     'Sonuçta oksalat artar ve başlıca böbrekten atıldığı için böbrekte birikir. Lumasiran glikolat oksidazı, nedosiran laktat dehidrogenaz A’yı susturur.')

# ============================================================================================== 9 · RTA: üç hücre
F = Fig('rta', 400, 'Renal tübüler asidozun üç tipi: distal, proksimal ve hiperkalemik tipte bozulan hücre düzeni', w=1080)
PAN = [(6, 'Tip 1 · distal', RED), (366, 'Tip 2 · proksimal', GOLD), (726, 'Tip 4 · hiperkalemik', PUR)]
for (x, bas, c) in PAN:
    F.r(x, 6, 348, 30, TINT[c], None, rx=8); F.t(x + 174, 27, bas, 13.5, 800, c, 'middle')
g = mini(F, 6, 348, 42, 222, 'α-interkale hücre', cw=170,
         apikal=[(100, 'H⁺-ATPaz', 'H⁺', 'cik', 'pompa', BRAND, 'x'), (188, 'H⁺/K⁺-ATPaz', 'H⁺', 'cik', 'pompa', INK2, None)],
         bazal=[(144, 'AE1', 'HCO₃⁻', 'cik', 'tas', GREEN, 'x')])
F.t((g['mx'] + g['bx']) / 2, 238, 'CA II', 12, 800, INK, 'middle'); F.t((g['mx'] + g['bx']) / 2, 253, 'CO₂ + H₂O → H⁺ + HCO₃⁻', 11, None, INK2, 'middle')
g = mini(F, 366, 348, 42, 222, 'Proksimal tübül hücresi', cw=170,
         apikal=[(104, 'NHE3', 'H⁺', 'cik', 'tas', GREEN, None)], bazal=[(150, 'NBCe1', 'HCO₃⁻', 'cik', 'tas', GREEN, 'x')])
F.tl(372, 168, ['H⁺ + HCO₃⁻', '→ CO₂ + H₂O', '(CA IV)'], 11.2, 14.5, fill=INK2)
F.t((g['mx'] + g['bx']) / 2, 238, 'CA II', 12, 800, INK, 'middle'); F.t((g['mx'] + g['bx']) / 2, 253, 'CO₂ + H₂O → H⁺ + HCO₃⁻', 11, None, INK2, 'middle')
g = mini(F, 726, 348, 42, 222, 'Esas hücre', cw=170,
         apikal=[(100, 'ENaC ↓', 'Na⁺', 'gir', 'kanal', BRAND, None), (180, 'ROMK ↓', 'K⁺', 'cik', 'kanal', GREEN, None)], bazal=[])
F.t((g['mx'] + g['bx']) / 2, 236, 'H⁺’i komşu α-interkale', 11, None, INK2, 'middle'); F.t((g['mx'] + g['bx']) / 2, 250, 'hücre atar; o da azalır', 11, None, INK2, 'middle')
F.r(g['bx'] - 62, 132, 40, 28, PUR, None, rx=7); F.t(g['bx'] - 42, 151, 'MR', 12.5, 800, '#fff', 'middle')
F.ok(g['bx'] + 70, 146, g['bx'] - 18, 146, PUR, 2.4); F.t(g['bx'] + 10, 136, 'Aldosteron', 12, 800, PUR)
F.t(g['bx'] + 10, 168, 'eksik ya da', 11.2, None, RED); F.t(g['bx'] + 10, 182, 'dirençli', 11.2, None, RED); F.isaret(g['bx'] - 20, 128, 'x', 8.5)
SON = [
    (6, RED, 'H⁺ atılamaz: idrar pH > 5,5 kalır', ['Serum K⁺ düşük · HCO₃⁻ < 10 mmol/L olabilir', 'Nefrokalsinoz ve kalsiyum fosfat taşı sık',
                                                   [('ATP6V1B1, ATP6V0A4', 'i'), ' (işitme kaybı) · ', ('SLC4A1', 'i'), ' · ', ('CA2', 'i')], 'Edinsel: Sjögren, SLE, amfoterisin B, lityum']),
    (366, GOLD, 'HCO₃⁻ geri emilemez: eşik düşer', ['Distal sağlam: idrar pH < 5,5’e inebilir', 'Serum K⁺ düşük · HCO₃⁻ 12–20 mmol/L’de durur',
                                                    [('SLC4A4', 'i'), ' (göz bulguları) · çoğu kez Fanconi'], 'Edinsel: miyelom, tenofovir, ifosfamid']),
    (726, PUR, 'Na⁺ girişi azalır: K⁺ ve H⁺ atılamaz', ['Serum K⁺ YÜKSEK — ayırt edici bulgu', 'Hiperkalemi amonyum yapımını da baskılar',
                                                        'İdrar pH genellikle < 5,5 · HCO₃⁻ > 17 mmol/L', 'Diyabet, KBH, kalsinörin inhibitörü, RAS blokeri']),
]
for (x, c, bas, sat) in SON:
    F.r(x, 274, 348, 120, '#fff', c, 1.5, 10); F.t(x + 12, 295, bas, 12.6, 800, c)
    F.tl(x + 12, 315, sat, 11.6, 17.5, fill=INK)
yeni('s21_rta', 'x21_21', 'Asidifikasyon · 1 · Şekil', 'Renal Tübüler Asidoz — Üç Tip, Üç Ayrı Hücre', F,
     '<b>Okuma:</b> Tip 1’de distal hücre H⁺ pompalayamaz; idrar hiçbir zaman asitleşmez. Tip 2’de proksimal hücre bikarbonatı geri alamaz, ama distal '
     'sağlam olduğu için idrar asitleşebilir. Tip 4’te sorun aldosteron eksenidir; potasyum yüksektir ve tek başına bu bulgu tipi ayırır.',
     'Şekil: renal tübüler asidozun üç tipi yan yana. Solda distal tip: alfa interkale hücrede proton pompası ya da AE1 bozuktur. '
     'Ortada proksimal tip: bikarbonat geri emilimi bozuktur. Sağda hiperkalemik tip: aldosteron eksik ya da etkisizdir, potasyum ve proton atılamaz.')

# ============================================================================================== 10 · AVP direnci
F = Fig('avp', 356, 'Toplayıcı kanal esas hücresinde vazopressin–V2 reseptörü–akuaporin 2 yolu ve AVP direnci', w=1080)
epitel(F, 'Toplayıcı kanal esas hücresi', h=342,
    apikal=[
        dict(y=110, ad='AQP2', iyon='H₂O', tip='kanal', renk=BRAND, isaret='x',
             tag=['Konjenital · yaklaşık %10', [('AQP2', 'i'), ' · otozomal resesif'], 'ya da dominant']),
        dict(y=292, ad='ENaC', iyon='Li⁺', tip='kanal', renk=GOLD, alt=['lityum buradan girer;', 'amilorid engeller'],
             tag=['Lityum', 'edinsel biçimin', 'en sık nedeni'], tagc=GOLD),
    ],
    bazal=[
        dict(y=96, ad='V2 reseptörü', iyon='AVP', tip='res', renk=PUR, isaret='x',
             tag=['Konjenital · yaklaşık %90', [('AVPR2', 'i'), ' · X’e bağlı'], 'V2 reseptörü işlev kaybı']),
        dict(y=292, ad='AQP3 · AQP4', iyon='H₂O', yon='cik', tip='kanal', renk=BRAND),
    ])
F.ok(672, 102, 672, 142, PUR, 2.2)
F.r(600, 146, 122, 28, '#fff', PUR, 1.6, 8); F.t(661, 165, 'Gs · adenilat siklaz', 11.6, 800, PUR, 'middle')
F.ok(598, 160, 582, 160, PUR, 2.2); F.r(520, 146, 60, 28, '#fff', PUR, 1.6, 8); F.t(550, 165, 'cAMP', 12, 800, PUR, 'middle')
F.ok(518, 160, 502, 160, PUR, 2.2); F.r(440, 146, 60, 28, '#fff', PUR, 1.6, 8); F.t(470, 165, 'PKA', 12, 800, PUR, 'middle')
F.ok(452, 176, 428, 204, PUR, 2.2)
F.el(412, 226, 22, 22, '#fff', BRAND, 2.2); F.r(402, 219, 6, 14, BRAND, None, rx=3); F.r(416, 219, 6, 14, BRAND, None, rx=3)
F.t(444, 223, 'AQP2 kesecikleri', 12.2, 800, INK); F.t(444, 238, 'fosforillenir, zara taşınır', 11.5, None, INK2)
F.ok(396, 210, 354, 136, BRAND, 2.2, '6 4')
F.engel(428, 276, 418, 252, GOLD, 2.2, 7); F.t(440, 270, 'AQP2’yi azaltır', 11.5, 700, GOLD)
F.etiket(870, 196, 196, ['NSIAD — ters tablo', [('AVPR2', 'i'), ' işlev kazanımı:'], 'AVP olmadan da açık;', 'hiponatremi'], GREEN, 12.4); F.ln(868, 176, 772, 112, GREEN, 1.4, '2 4')
yeni('s21_avp', 'x21_22', 'Su Bozuklukları · 1 · Şekil', 'AVP Direnci — V2 Reseptöründen Su Kanalına', F,
     '<b>Okuma:</b> AVP bazolateraldeki V2 reseptörüne bağlanır; cAMP ve PKA üzerinden AQP2 kesecikleri apikal zara yerleşir ve su geçer. '
     'Reseptör ya da kanal bozuksa AVP de DDAVP de etkisiz kalır. Lityum hücreye ENaC’ten girer; lityuma bağlı tabloda amiloridin yararı bundandır.',
     'Şekil: toplayıcı kanal esas hücresi. Vazopressin V2 reseptörüne bağlanır, siklik AMP ve protein kinaz A üzerinden akuaporin 2 kesecikleri apikal zara taşınır. '
     'Konjenital AVP direncinin yüzde doksanında reseptör, yüzde onunda akuaporin 2 bozuktur. Lityum hücreye ENaC’ten girer.')

# ============================================================================================== 11 · antenatal hidronefroz: doğum sonrası zaman çizgisi (slayt içi)
F = Fig('ant', 228, 'Antenatal hidronefrozda doğum sonrası değerlendirmenin zaman çizgisi', mh=240)
F.r(40, 4, 1060, 32, TINT[RED], RED, 1.4, 8)
F.t(56, 25, [('Beklemeyin, hemen değerlendirin: ', 'b'), 'iki taraflı ağır genişleme · tek böbrek · anormal ya da kalın duvarlı mesane · oligohidramniyos'], 12.6)
F.ln(60, 80, 1090, 80, INK2, 3)
for (x, et, a) in ((60, 'Doğum', 'start'), (330, '48. saat', 'middle'), (600, '1. hafta', 'middle'), (870, '6–8. hafta', 'middle')):
    F.el(x, 80, 6.5, 6.5, '#fff', INK2, 3); F.t(x, 64, et, 12.8, 800, INK, a)
SEG = [(60, 262, RED, 'İlk USG için erken', ['göreli dehidratasyon genişlemeyi', 'olduğundan hafif gösterir']),
       (338, 254, GREEN, 'İlk USG: uygun pencere', ['48 saat – 1 hafta']),
       (608, 254, BRAND, 'İzlem USG’si', ['zamanı risk sınıfına göre belirlenir;', 'düşük riskte yeterlidir, gereksiz', 'girişim ve antibiyotikten kaçının']),
       (878, 212, PUR, 'Diüretikli sintigrafi (MAG3)', ['obstrüksiyon, diferansiyel işlev;', 'genellikle 6–8 haftadan önce', 'yapılmaz'])]
for (x, w, c, bas, sat) in SEG:
    F.r(x, 94, w, 80, TINT[c], c, 1.4, 8); F.t(x + 10, 114, bas, 12.8, 800, c); F.tl(x + 10, 132, sat, 11.8, 15.5, fill=INK)
F.t(60, 210, 'VCUG endikasyonu', 12.8, 800, BRANDD)
cx_ = 196
for tx_ in ('yüksek dereceli genişleme', 'üreter genişlemesi', 'dupleks sistem', 'mesane anomalisi', 'PUV şüphesi', 'ateşli İYE'):
    w_ = gen(tx_, 12.2) + 22; F.r(cx_, 192, w_, 26, '#fff', BRAND, 1.3, 13); F.t(cx_ + w_ / 2, 209.5, tx_, 12.2, 700, INK, 'middle'); cx_ += w_ + 8
ic('s21_ant', 'x21_29', F)

# ============================================================================================== 12 · VUR dereceleri + RIVUR / PRIVENT (slayt içi)
F = Fig('vur', 318, 'Vezikoüreteral reflü dereceleri ve RIVUR ile PRIVENT çalışmalarının sonuçları', mh=330)
F.t(20, 22, 'VUR dereceleri (işeme sistoüretrografisi)', 13.5, 800, BRANDD)
DER = [('I', 0, '#ddd6c4', 3.5, 0, ['yalnız üreter']), ('II', 0, IDRAR, 3.5, 0, ['pelvis ve kaliksler;', 'genişleme yok']), ('III', 1, IDRAR, 6, 0, ['hafif–orta', 'genişleme']),
       ('IV', 2, IDRAR, 9, 1, ['orta genişleme,', 'üreter kıvrımlı']), ('V', 3, IDRAR, 13, 2, ['ağır genişleme,', 'papilla izi silinmiş'])]
for k, (rm, pel, col, gw, kv, ac) in enumerate(DER):
    cx = 62 + k * 118
    ex, ey = bobrek(F, cx, 92, .66, pel, idrar=col)
    ureter(F, ex, ey + 4, cx + 30, 222, gw, kv)
    F.el(cx + 34, 240, 26, 18, '#b98a80', '#8e4a44', 1.4); F.el(cx + 34, 240, 23, 15, IDRAR)
    F.t(cx + 18, 282, rm, 15, 800, BRANDD, 'middle'); F.tl(cx + 18, 298, ac, 11.4, 13.5, fill=INK2, a='middle')
F.ln(646, 10, 646, 312, LINE, 1.5)
F.t(676, 22, 'Profilaksi: iki randomize çalışma', 13.5, 800, BRANDD)
cubuk(F, 716, 70, 396, 160, [(['RIVUR', 'yineleyen İYE'], [12.9, 23.6], ['%12,9', '%23,6']), (['RIVUR', 'TMP-SMX direnci'], [63, 19], ['%63', '%19']),
                               (['PRIVENT', 'İYE'], [13, 19], ['%13', '%19'])],
      [('Antibiyotik profilaksisi', BRAND), ('Plasebo', MUT)], ymax=80, adim=20, fs=12.6, bw=40)
F.t(676, 296, 'Böbrek skarı: iki kol arasında anlamlı fark yok (RIVUR).', 12.4, 800, RED)
F.t(676, 312, 'RIVUR 607, PRIVENT 576 çocuk · direnç: ilk yinelemesi E. coli olan 87 çocukta', 11.2, None, MUT)
ic('s21_vur', 'x21_31', F)

# ============================================================================================== 13 · UPJ darlığı, PUV, prune-belly (slayt içi)
F = Fig('obs', 344, 'Üreteropelvik bileşke darlığı, posterior üretral valv ve prune-belly sendromunda idrar yolu görünümü', mh=366)
OBS = [(10, 'Üreteropelvik bileşke darlığı', BRAND), (390, 'Posterior üretral valv (önceki slayt)', RED), (770, 'Prune-belly sendromu', PUR)]
for (x0, bas, c) in OBS:
    F.r(x0, 4, 360, 28, TINT[c], None, rx=8); F.t(x0 + 180, 23.5, bas, 13.5, 800, c, 'middle')
# UPJ
x0 = 10
e1 = bobrek(F, x0 + 116, 100, .8, 3); e2 = bobrek(F, x0 + 244, 100, .8, 0, ayna=True)
ureter(F, e1[0] + 2, e1[1] + 6, x0 + 168, 204, 3); ureter(F, e2[0], e2[1] + 2, x0 + 192, 204, 3)
mesane(F, x0 + 180, 228, 30, 22, 3, uretra=12)
F.ln(e1[0] - 5, e1[1] + 3, e1[0] + 9, e1[1] + 3, RED, 3.2); F.ln(e1[0] + 12, e1[1] + 3, e1[0] + 44, e1[1] - 10, RED, 1.4, '2 4'); F.t(e1[0] + 20, e1[1] - 30, 'darlık', 12, 800, RED)
F.t(x0 + 42, 46, 'geniş pelvis,', 11.5, None, INK2); F.t(x0 + 42, 60, 'ince üreter', 11.5, None, INK2)
F.tl(x0 + 6, 306, ['Antenatal hidronefrozun en sık yapısal nedeni.', 'Çoğu izlemle düzelir; işlev düşerse piyeloplasti.'], 12, 16, fill=INK)
# PUV
x0 = 390
e1 = bobrek(F, x0 + 112, 100, .8, 2); e2 = bobrek(F, x0 + 248, 100, .8, 2, ayna=True)
ureter(F, e1[0] + 2, e1[1] + 4, x0 + 164, 200, 8, 1); ureter(F, e2[0] - 2, e2[1] + 4, x0 + 196, 200, 8, 1)
mesane(F, x0 + 180, 220, 26, 20, 9, uretra=8, valv=True, arka=True)
F.t(x0 + 226, 218, 'kalın duvarlı mesane', 11.5, None, INK2); F.t(x0 + 200, 264, 'geniş posterior üretra, valv', 11.5, 700, RED)
F.tl(x0 + 6, 306, ['Yalnız erkek çocukta. Önce mesaneyi boşaltın, sonra', 'valv ablasyonu; mesane ömür boyu izlenir.'], 12, 16, fill=INK)
# prune-belly
x0 = 770
e1 = bobrek(F, x0 + 108, 100, .8, 2); e2 = bobrek(F, x0 + 252, 100, .8, 2, ayna=True)
ureter(F, e1[0] + 2, e1[1] + 4, x0 + 156, 200, 12, 2); ureter(F, e2[0] - 2, e2[1] + 4, x0 + 204, 200, 12, 2)
mesane(F, x0 + 180, 222, 44, 26, 2, uretra=10)
F.el(x0 + 74, 196, 9, 6.5, '#d9b38c', '#8a6a3a', 1.3); F.el(x0 + 288, 196, 9, 6.5, '#d9b38c', '#8a6a3a', 1.3)
F.t(x0 + 20, 220, 'inmemiş testis', 11.5, None, INK2); F.ln(x0 + 60, 208, x0 + 70, 202, INK2, 1.2)
F.yol('M%d,58 q-10,13 0,26 t0,26 t0,26 t0,26 t0,26 t0,26 t0,26 t0,26' % (x0 + 336), PUR, 2)
F.t(x0 + 180, 291, '', 11)
F.tl(x0 + 6, 306, ['Karın kası yetersizliği + iki taraflı kriptorşidizm', '+ geniş, atonik idrar yolları. Erkeklerde görülür.'], 12, 16, fill=INK)
F.t(x0 + 324, 52, 'gevşek karın duvarı', 11.2, None, PUR, 'end')
ic('s21_obs', 'x21_33', F)
