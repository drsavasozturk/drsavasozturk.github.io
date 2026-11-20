#!/usr/bin/env python3
"""Nefroloji Ders Serisi — doğrulanmış slayt metni düzeltmeleri (idempotent).
Kullanım: python3 metin_duzelt.py dersler/nefroloji-ders-serisi/index.html"""
import sys
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
]
p = sys.argv[1]; s = open(p, encoding='utf-8').read(); n = 0
for sid, a, b in D:
    i = s.find('<section id="%s"' % sid); j = s.find('</section>', i)
    assert i >= 0, sid
    blok = s[i:j]
    if b in blok: continue
    assert blok.count(a) == 1, (sid, blok.count(a))
    s = s[:i] + blok.replace(a, b) + s[j:]; n += 1
open(p, 'w', encoding='utf-8').write(s)
print(f'{p}: {n} düzeltme uygulandı ({len(D) - n} zaten uygulanmış)')
