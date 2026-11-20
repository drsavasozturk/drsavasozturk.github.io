#!/usr/bin/env python3
"""Ders 17 · Sistemik hastalıklar ve böbrek — şekil tanımları (20 Kasım 2026)."""
import random
from sekil_ortak import *
from sekil_glom import etk

D = Ders('17')

# ============================================================================================== 1 · Fabry: X'e bağlı kalıtım ve lyonizasyon
F = Fig('x', 364, 'Fabry hastalığında X’e bağlı kalıtım: hasta babanın ve heterozigot annenin çocukları; kadında rastgele X inaktivasyonu', w=1080)
serit(F, 6, 6, 620, 'X’e bağlı kalıtım', BRANDD); zemin(F, 6, 42, 620, 316)


def birey(x, y, erkek, dur):          # dur: 0 sağlıklı · 1 heterozigot (yarım) · 2 hasta (dolu)
    c = RED
    if erkek:
        F.r(x - 15, y - 15, 30, 30, c if dur == 2 else '#fff', INK, 1.8, 2)
    else:
        F.el(x, y, 15, 15, c if dur == 2 else '#fff', INK, 1.8)
        if dur == 1: F.a(f'<path d="M{x},{y - 15} A15,15 0 0 1 {x},{y + 15} Z" fill="{c}"/>'); F.el(x, y, 15, 15, 'none', INK, 1.8)


def aile(ox, baba, anne, cocuk, bas, alt):
    F.t(ox + 140, 74, bas, 13, 800, INK, 'middle')
    birey(ox + 90, 110, True, baba); birey(ox + 190, 110, False, anne); F.ln(ox + 105, 110, ox + 175, 110, INK, 1.8)
    F.ln(ox + 140, 110, ox + 140, 146, INK, 1.8); F.ln(ox + 50, 146, ox + 230, 146, INK, 1.8)
    for i, (e, d) in enumerate(cocuk):
        x = ox + 50 + i * 60; F.ln(x, 146, x, 166, INK, 1.8); birey(x, 182, e, d)
    F.tl(ox + 140, 228, alt, 12, 17, fill=INK, a='middle')


aile(20, 2, 0, [(False, 1), (True, 0), (False, 1), (True, 0)], 'Hasta baba', ['Tüm kızlar heterozigot', '(çoğu zaman hasta);', 'oğullara geçmez'])
aile(320, 0, 1, [(True, 2), (False, 1), (True, 0), (False, 0)], 'Heterozigot anne', ['Her çocuğa %50:', 'oğul hasta, kız', 'heterozigot'])
for i, (e, d, t) in enumerate(((True, 2, 'hasta erkek'), (False, 1, 'heterozigot kadın'), (True, 0, 'sağlıklı'))):
    x = 48 + i * 170; birey(x, 320, e, d); F.t(x + 24, 325, t, 11.8, None, INK)
serit(F, 636, 6, 438, 'Kadında rastgele X inaktivasyonu', PUR); zemin(F, 636, 42, 438, 316)
for j, (oy, n, t1, t2) in enumerate(((60, 8, 'Çoğu hücrede sağlam X aktif', 'hafif klinik'), (190, 28, 'Çoğu hücrede mutant X aktif', 'erkek kadar ağır'))):
    mut = set(random.Random(7 + j).sample(range(36), n))
    for r in range(4):
        for c in range(9):
            x, y = 656 + c * 24, oy + 10 + r * 24
            F.r(x, y, 21, 21, '#f4b4ac' if r * 9 + c in mut else '#bfe6cf', '#8a9aa8', 1, 4)
    F.t(888, oy + 44, t1, 12.6, 800, INK); F.t(888, oy + 62, t2, 12, None, INK2)
F.r(656, 312, 12, 12, '#bfe6cf', '#8a9aa8', 1, 3); F.t(674, 322, 'sağlam X aktif', 11.4, None, INK)
F.r(790, 312, 12, 12, '#f4b4ac', '#8a9aa8', 1, 3); F.t(808, 322, 'mutant X aktif', 11.4, None, INK)
F.t(656, 346, 'Kadında enzim aktivitesi normal olabilir: tanı genetik testle.', 11.6, 800, PUR)
D.yeni('s17_x', 'x17_9', 'Temel · Şekil', 'Fabry — X’e Bağlı Kalıtım ve Kadında Mozaiklik', F,
       '<b>Okuma:</b> Hasta erkek mutant X’i tüm kızlarına verir, oğullarına vermez; heterozigot kadın her çocuğuna yüzde elli olasılıkla geçirir. '
       'Kadında her hücrede X’lerden biri rastgele susturulur: mutant X’in aktif kaldığı hücre oranı klinik ağırlığı belirler. Enzim aktivitesi normal görünebileceğinden kadında tanı genetik testle konur.',
       'Şekil: solda iki soy ağacı. Hasta babanın dört çocuğundan iki kız heterozigot, iki oğul sağlıklı. Heterozigot annenin çocuklarında bir oğul hasta, bir kız heterozigot, bir oğul ve bir kız sağlıklı. '
       'Sağda iki kadın dokusunun hücre mozaiği: üstte çoğu hücrede sağlam X aktif, klinik hafif; altta çoğu hücrede mutant X aktif, klinik erkek kadar ağır.')

# ============================================================================================== 2 · sarkoidozda kalsitriol
F = Fig('d', 392, 'Sarkoidozda granülom makrofajının düzensiz 1α-hidroksilazı ve hiperkalsiüri ile hiperkalsemiye giden zincir', w=1080)
serit(F, 6, 6, 1068, 'İki 1α-hidroksilaz: biri denetimli, biri değil', BRANDD); zemin(F, 6, 42, 1068, 344)


def kutu(x, y, w, t1, t2=None, c=INK2, fill='#fff', h=48):
    F.r(x, y, w, h, fill, c, 1.6, 10); F.t(x + w / 2, y + (20 if t2 else 29), t1, 13, 800, INK, 'middle')
    if t2: F.t(x + w / 2, y + 38, t2, 11.6, None, INK2, 'middle')


kutu(24, 66, 196, 'Güneş (UVB) + diyet', 'yazın substrat artar', GOLD, '#fff6e0')
kutu(24, 150, 196, '25(OH)D', 'karaciğer · 25-hidroksilaz')
F.ok(122, 115, 122, 146, INK2, 2.2)
kutu(300, 66, 300, 'Böbrek 1α-hidroksilaz (CYP27B1)', 'PTH uyarır · FGF23 ve 1,25(OH)₂D baskılar', BRAND, '#e8f6ff')
kutu(300, 196, 300, 'Granülom makrofajı 1α-hidroksilaz', 'PTH’den bağımsız · IFN-γ uyarır', RED, '#fdeaea')
F.ok(222, 166, 296, 96, BRAND, 2.2); F.ok(222, 180, 296, 216, RED, 2.2)
kutu(680, 132, 250, '1,25(OH)₂D ↑', 'kalsitriol fazlası', RED, '#fdeaea')
F.ok(602, 96, 676, 150, BRAND, 1.8, '5 4'); F.ok(602, 220, 676, 170, RED, 3)
kutu(680, 222, 250, 'Bağırsak Ca emilimi ↑', 'kemik rezorpsiyonu ↑')
F.ok(805, 182, 805, 218, INK2, 2.2)
kutu(680, 306, 120, 'Hiperkalsiüri', 'önce', GOLD, '#fff6e0'); kutu(816, 306, 114, 'Hiperkalsemi', 'sonra', RED, '#fdeaea')
F.ok(760, 272, 740, 302, INK2, 2); F.ok(850, 272, 870, 302, INK2, 2)
kutu(952, 222, 110, 'PTH ↓', 'baskılanır', BRAND, '#e8f6ff')
F.ok(932, 318, 984, 274, INK2, 2)
F.yol('M1006,220 C1006,40 700,40 604,72', BRAND, 2, ok=True, dash='6 4')
F.t(756, 102, 'Geri bildirim yalnız böbrek enzimini frenler', 12, 700, BRAND, 'middle')
F.engel(450, 298, 450, 250, GREEN, 3); F.t(462, 284, 'Glukokortikoid granülom enzimini baskılar', 12, 800, GREEN)
F.tl(24, 240, ['Laboratuvar imzası', '• Ca yüksek, PTH baskılı', '• 1,25(OH)₂D yüksek ya da'], 12, 18, fill=INK); F.t(35, 294, 'uygunsuz normal', 12, None, INK)
F.tl(24, 312, ['• 25(OH)D normal ya da düşük', '• İdrar Ca yüksek'], 12, 18, fill=INK)
D.yeni('s17_d', 'x17_18', 'Mekanizma · Şekil', 'Granülomdaki 1α-Hidroksilaz — Zincir', F,
       '<b>Okuma:</b> Böbrekteki 1α-hidroksilaz PTH, FGF23 ve kalsitriolle denetlenir; granülom makrofajındaki enzim bu geri bildirimden bağımsızdır ve IFN-γ ile uyarılır. '
       'Kalsitriol fazlası bağırsak emilimini ve kemik rezorpsiyonunu artırır: önce hiperkalsiüri, sonra hiperkalsemi; PTH baskılanır. Yazın artan 25(OH)D substratı tabloyu belirginleştirir.',
       'Şekil: solda güneş ve diyetten gelen D vitamini, karaciğerde 25 hidroksi D vitaminine dönüşür. Buradan iki yol: üstte PTH ile uyarılan, FGF23 ve kalsitriolle baskılanan böbrek enzimi; '
       'altta PTH’den bağımsız, interferon gama ile uyarılan granülom makrofajı enzimi. İkisi kalsitriolü artırır; bağırsak kalsiyum emilimi ve kemik rezorpsiyonu artar, önce hiperkalsiüri, sonra hiperkalsemi gelişir, PTH baskılanır. '
       'Geri bildirim yalnız böbrek enzimini frenler; glukokortikoid granülom enzimini baskılar.')

# ============================================================================================== 3 · orak hücre: neden medulla?
F = Fig('orak', 384, 'Renal medullada düşük oksijen, yüksek ozmolalite ve düşük pH’ın vasa rektada orak hücreleşmeye yol açması; medüller ve glomerüler yollar', w=1080)
serit(F, 6, 6, 440, 'Vasa rekta: üç koşulun kesişimi', RED); zemin(F, 6, 42, 440, 336)
F.a('<defs><linearGradient id="g17m" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbeee9"/><stop offset="1" stop-color="#e39d93"/></linearGradient></defs>')
F.r(30, 60, 150, 306, 'url(#g17m)', '#c98b82', 1.4, 8)
F.t(105, 80, 'korteks', 11.4, 700, INK2, 'middle'); F.t(105, 356, 'papilla', 11.4, 700, '#7a2f27', 'middle')
F.yol('M80,92 L80,300 Q80,336 105,336 Q130,336 130,300 L130,92', '#a2564e', 16, op=.25)
F.yol('M80,92 L80,300 Q80,336 105,336 Q130,336 130,300 L130,92', '#c0392b', 2)
for y in (110, 150, 190):
    F.el(80, y, 6, 3.6, '#c0392b', '#8e2b26', 1); F.el(130, y + 18, 6, 3.6, '#c0392b', '#8e2b26', 1)
for (x, y, a) in ((80, 238, 20), (82, 268, -30), (78, 296, 60), (98, 330, 10), (112, 332, -50), (128, 302, 30), (104, 322, 80)):
    F.a(f'<path transform="rotate({a} {x} {y})" d="M{x - 8},{y} Q{x},{y - 9} {x + 8},{y} Q{x},{y - 3.5} {x - 8},{y} Z" fill="#c0392b" stroke="#8e2b26" stroke-width="1"/>')
F.ok(200, 92, 200, 316, INK2, 2)
F.tl(214, 112, ['pO₂ ↓', 'karşı akım O₂ şantı,', 'kalın çıkan kol O₂ tüketir'], 12.4, 17, fill=INK, fw=800)
F.tl(214, 196, ['Ozmolalite ↑', '300 → 1200 mOsm/kg:', 'hücre büzüşür, HbS ↑'], 12.4, 17, fill=INK, fw=800)
F.tl(214, 286, ['pH ↓', 'Bohr etkisi: O₂', 'afinitesi azalır'], 12.4, 17, fill=INK, fw=800)
etk(F, (104, 330), 330, 340, ['HbS polimerleşir;', 'vasa rekta tıkanır'], fs=12)
for j, (y, bas, c, sat) in enumerate(((6, 'Medüller yol', RED, ['Hipostenüri: en erken ve en yaygın', 'Papiller nekroz → hematüri, kolik', 'Ağrısız hematüri (çoğu kez sol)', 'Tip 4 RTA benzeri: hiperkalemi', 'Renal medüller karsinom (nadir; çoğu kez taşıyıcıda)']),
                                       (196, 'Glomerüler yol', PUR, ['Anemi + NO → hiperfiltrasyon', 'Hemoliz ürünleri → endotel hasarı, albüminüri', 'FSGS, orak hücre glomerülopatisi', 'İlerleyici eGFR kaybı; APOL1 ağırlaştırır']))):
    F.r(456, y, 618, 182, TINT[c], c, 1.6, 10); F.t(474, y + 28, bas, 14, 800, c)
    F.tl(474, y + 56, ['• ' + t for t in sat], 12.4, 23, fill=INK)
D.yeni('s17_orak', 'x17_26', 'Patofizyoloji · Şekil', 'Orak Hücre — Neden Medulla?', F,
       '<b>Okuma:</b> Vasa rekta papillaya indikçe oksijen azalır, ozmolalite 1200 mOsm/kg’a çıkar ve pH düşer; üçü birlikte HbS polimerleşmesini kolaylaştırır ve damarı tıkar. '
       'Medüller yol hipostenüri, papiller nekroz, hematüri ve asidifikasyon defekti yapar; glomerüler yolda hiperfiltrasyon albüminüriye ve FSGS’ye ilerler.',
       'Şekil: solda korteksten papillaya inen bir vasa rekta kıvrımı. Korteks düzeyinde yuvarlak eritrositler, papilla düzeyinde orak biçimli ve kümelenmiş eritrositler damarı tıkıyor. '
       'Yanında aşağı doğru artan üç koşul: oksijen basıncı düşer, ozmolalite 300’den 1200’e çıkar, pH düşer. Sağda iki kutu: medüller yol ve glomerüler yol bulguları.')
