#!/usr/bin/env python3
"""Nefroloji Ders Serisi — doğrulanmış slayt metni düzeltmeleri (idempotent).
Kullanım: python3 metin_duzelt.py dersler/nefroloji-ders-serisi/index.html"""
import re, sys
D = [  # (slayt, eski, yeni)
    ('x21_15', '• Glikojen depo hastalığı tip 1 (Fanconi-Bickel)',
     '• Fanconi-Bickel sendromu (glikojen depo hastalığı tip XI; <i>SLC2A2</i>)'),
    ('x21_13', 'WNK4 normalde NCC\'yi baskılar; işlev kaybı NCC\'yi <span class="hl-r">aşırı etkin</span> kılar. KLHL3 ve CUL3, WNK proteinlerinin yıkımını düzenleyen ubikitin-ligaz kompleksini oluşturur',
     'WNK1 ve WNK4, SPAK/OSR1 üzerinden NCC\'yi etkinleştirir; mutasyonlar bu kinazların KLHL3–CUL3 aracılı yıkımını engeller ya da ekspresyonunu artırır, NCC <span class="hl-r">aşırı etkin</span> kalır'),
    ('x21_12', 'ubikitin ligaz <b>NEDD4</b> tarafından', 'ubikitin ligaz <b>NEDD4-2</b> tarafından'),
    ('x07_18', "bunlar steroide yanıtsızdı ve tekrar biyopside FSGS saptandı",
     "bunlar steroide daha az yanıt verdi ve tekrar biyopside daha sık FSGS saptandı"),
    ('x07_22', "<b>2020 Cochrane güncellemesi:", "<b>Cochrane güncellemeleri (2020, 2024):"),
    ('x07_22', "daha uzun steroid = daha fazla yan etki, aynı nüks oranı.",
     "daha uzun steroid nüksü azaltmaz; ek steroid maruziyeti yarar getirmez."),
    ('x07_21', 'Hahn D, Hodson EM, Willis NS, Craig JC. Corticosteroid therapy for nephrotic syndrome in children. <i>Cochrane Database Syst Rev</i> 2015;3:CD001533.',
     'Hahn D, Samuel SM, Willis NS, Craig JC, Hodson EM. Corticosteroid therapy for nephrotic syndrome in children. <i>Cochrane Database Syst Rev</i> 2024;8:CD001533.'),
    ('x07_22', 'Hahn D, Hodson EM, Willis NS, Craig JC. Corticosteroid therapy for nephrotic syndrome in children. <i>Cochrane Database Syst Rev</i> 2015;3:CD001533.',
     'Hahn D, Samuel SM, Willis NS, Craig JC, Hodson EM. Corticosteroid therapy for nephrotic syndrome in children. <i>Cochrane Database Syst Rev</i> 2024;8:CD001533.'),
    ('x07_49', 'Hahn D, Hodson EM, Willis NS, Craig JC. Corticosteroid therapy for nephrotic syndrome in children. <i>Cochrane Database Syst Rev</i> 2015;3:CD001533.',
     'Hahn D, Samuel SM, Willis NS, Craig JC, Hodson EM. Corticosteroid therapy for nephrotic syndrome in children. <i>Cochrane Database Syst Rev</i> 2024;8:CD001533.'),
    ('x14_8', 'hipokomplementemi <b>1 aydan</b> uzun sürüyorsa', 'hipokomplementemi <b>6–8 haftadan</b> uzun sürüyorsa'),
    ('x27_11', 'Vazodilatasyon tükenir; preglomerüler direnç artmaya başlar.',
     'Afferent dilatasyon azalır; efferent (postglomerüler) vazokonstriksiyon basıncı yüksek tutar.'),
    ('x18_9', '<b>antiparalel beta-tabaka</b> yapısına', '<b>çapraz-β (cross-β)</b> yapısına'),
    ('x26_36', '<span class="hl-r">pH &gt;7,0\'ı aşmayın</span> — kalsiyum fosfat çökelmesi riski',
     '<span class="hl-r">Korunmada pH 7,0\'ı aşmayın</span> — kalsiyum fosfat çökelmesi riski; taşı eritmede kısa süre 7,0–7,2 (EAU)'),
    ('x17_26', '(vasa rektada oksijen ekstraksiyonu yüksek)', '(vasa rektada karşı akım O₂ şantı ve kalın çıkan kolun O₂ tüketimi)'),
    # 21 Kasım 2026 · ChatGPT kararları (kullanıcı yetkisiyle) ve hakem uyumu
    ('x27_13', '• Drenaj sonrası post-obstrüktif diürez <b>beklenmez</b>',
     '• Drenaj sonrası belirgin post-obstrüktif diürez (POD) gelişme olasılığı daha düşüktür; ancak <b>tamamen dışlanamaz</b>'),
    ('x27_13', '• Drenaj sonrası <b>belirgin post-obstrüktif diürez</b> beklenir',
     '• Drenaj sonrası <b>post-obstrüktif diürez (POD)</b> gelişebilir; idrar çıkışı ve elektrolitler izlenmelidir'),
    ('x27_13', 'drenajdan sonra çok daha belirgin bir post-obstrüktif diürez olur; tek taraflıda pratikte olmaz. Bunu ezberletin.',
     'drenajdan sonra post-obstrüktif diürez gelişebilir; idrar çıkışı ve elektrolitler izlenmelidir. Tek taraflıda belirgin diürez olasılığı daha düşüktür, ancak tamamen dışlanamaz.'),
    ('x26_37', '<b>Proteus mirabilis</b> (klasik), Klebsiella, Providencia, Morganella, Serratia, <b>Ureaplasma urealyticum</b>, Corynebacterium urealyticum, Staphylococcus saprophyticus, bazı Pseudomonas suşları.',
     '<b><i>Proteus mirabilis</i></b> (klasik), <i>Klebsiella</i>, <i>Providencia</i>, <i>Morganella</i>, <i>Serratia</i>, <b><i>Ureaplasma urealyticum</i></b>, <i>Corynebacterium urealyticum</i>, <i>Staphylococcus saprophyticus</i>, bazı <i>Pseudomonas</i> suşları.'),
    ('x26_37', '<span class="hl-r">Escherichia coli üreaz ÜRETMEZ</span>', '<span class="hl-r"><i>Escherichia coli</i> üreaz ÜRETMEZ</span>'),
    ('x44_5', 'kalan nefronlar hipertrofiye olur.', 'kalan nefronlarda kompansatuvar hipertrofi görülebilir.'),
]
p = sys.argv[1]; s = open(p, encoding='utf-8').read(); n = 0
for sid, a, b in D:
    i = s.find('<section id="%s"' % sid); j = s.find('</section>', i)
    assert i >= 0, sid
    blok = s[i:j]
    if b in blok: continue
    assert blok.count(a) == 1, (sid, blok.count(a))
    s = s[:i] + blok.replace(a, b) + s[j:]; n += 1
# yazım birliği (21 Kasım 2026): Türkçe anatomik terimde "iliyak" (Latince "iliaka" ve "sakroiliyak" etkilenmez)
s, ng = re.subn(r'\b([İi])liak\b', lambda m: m.group(1) + 'liyak', s)
open(p, 'w', encoding='utf-8').write(s)
print(f'{p}: {n} düzeltme uygulandı ({len(D) - n} zaten uygulanmış); iliak→iliyak {ng}')
