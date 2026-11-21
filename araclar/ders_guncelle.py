#!/usr/bin/env python3
"""drsavasozturk.com · tek dosyalık ders sunumunun yeni sürümünü yayındaki sayfaya aktarır (21.11.2026).

Kullanım:  python3 -I araclar/ders_guncelle.py <yeni_tek_dosya.html> dersler/<ad>/index.html

Parenteral / İstatistik / Makale motoruyla (fw_css + fw_js) üretilmiş sunumlar içindir. Yayındaki sayfanın
site kabuğu korunur; yalnız sunumun kendisi değişir:
  - <head>: başlık, açıklama, canonical, og etiketleri, ortak kapı stili AYNEN kalır; motorun <style> bloğu yenisiyle değişir.
  - <body>: ortak giriş kapısı (dkapi: dk1, dk2, dk3) ve ana sayfa düğmesi AYNEN kalır; slaytlar, sözlük ve motor betiği yenisiyle değişir.
  - Sondaki kapı betiği ve servis çalışanı kaydı AYNEN kalır.
  - Tek dosyadaki ikinci iç onay kutusu (onayCb2: izinsiz kullanılamaz) çıkarılır; sitede aynı beyan ortak kapıdaki dk3 kutusudur.
  - Kapaktaki "2026–2027 Eğitim-Öğretim Yılı" ibaresi çıkarılır (kullanıcı isteği, 8.11.2026).
  - Slayt ibaresi (i.soimza) imza_ekle.py ile aynı ögedir; araç sonunda imza_ekle.isle çağrılır (yinelemez).
Denetim: sunum gövdesinde dış adres (http/https), indirme özniteliği ve tarayıcı depolaması olmamalı; varsa yazmayı reddeder.
İstisna (kullanıcı onayı, 21.11.2026): İstatistik dersinin sentetik uygulama veri setleri gömülü veriden (window.VERISET) .vsbtn düğmesiyle indirilir;
bu, betik içinde üretilen bir indirmedir ve gövdede indirme özniteliği taşımaz.
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import imza_ekle

GOVDE = "<script>document.body.classList.add('js');</script>"
KAPI_JS = "<script>(function(){var o=document.getElementById('dkapi')"
STIL = re.compile(r'<style>.*?</style>', re.S)          # motorun kimliksiz ilk stil bloğu


def aktar(yeni, eski):
    for h, ad in ((yeni, 'yeni dosya'), (eski, 'yayındaki sayfa')):
        assert h.count(GOVDE) == 1, f'{ad}: gövde başlangıcı bulunamadı'
    assert eski.count(KAPI_JS) == 1 and 'id="dk3"' in eski, 'yayındaki sayfada ortak kapı (dk3) yok'
    bas_e, bas_y = eski[:eski.index(GOVDE)], yeni[:yeni.index(GOVDE)]
    ms, my = STIL.search(bas_e), STIL.search(bas_y)
    assert ms and my, 'motor stil bloğu bulunamadı'
    bas = bas_e[:ms.start()] + my.group(0) + bas_e[ms.end():]
    orta = yeni[yeni.index(GOVDE):yeni.rindex('</body>')].rstrip() + '\n'
    # iç ikinci onay kutusu sitede yok (ortak kapıdaki dk3 aynı beyandır)
    orta, n = re.subn(r'\s*<label class="onay-tik" id="onayTik2">.*?</label>', '', orta, flags=re.S)
    assert n <= 1
    orta = orta.replace('2026–2027 Eğitim-Öğretim Yılı · ', '').replace(' · 2026–2027 Eğitim-Öğretim Yılı', '')
    son = eski[eski.index(KAPI_JS):]
    # denetim: sunum gövdesi (betikler hariç) dışarıya bağlanmamalı, indirme ve depolama olmamalı
    govde_html = re.sub(r'<script>.*?</script>', '', orta, flags=re.S)
    assert 'id="onayCb2"' not in govde_html
    dis = re.findall(r'(?:href|src)="(https?:[^"]+)"', govde_html)
    assert not dis, f'sunum gövdesinde dış adres: {dis[:3]}'
    assert ' download' not in govde_html, 'sunum gövdesinde indirme özniteliği'
    for yasak in ('localStorage', 'sessionStorage', 'indexedDB', 'document.cookie'):
        assert yasak not in orta, f'tarayıcı depolaması: {yasak}'
    h = imza_ekle.isle(bas + orta + son)
    n_sl = len(re.findall(r'<section\b[^>]*\bclass="slide[ "]', h))
    assert h.count(imza_ekle.IMZA) == n_sl, (h.count(imza_ekle.IMZA), n_sl)
    assert h.count('id="dk3"') == 1 and 'noindex' not in bas
    return h, n_sl


if __name__ == '__main__':
    if len(sys.argv) != 3: sys.exit(__doc__)
    yeni = open(sys.argv[1], encoding='utf-8').read(); eski = open(sys.argv[2], encoding='utf-8').read()
    h, n = aktar(yeni, eski)
    open(sys.argv[2], 'w', encoding='utf-8').write(h)
    print(sys.argv[2], '| slayt:', n, '| kaynak satırı:', h.count('<div class="fn">'), '| sarı işaret:', h.count('<mark class="mk">'),
          '| bayt:', len(h.encode('utf-8')))
