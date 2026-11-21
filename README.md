# drsavasozturk.com

Prof. Dr. Savaş Öztürk'ün kişisel akademik sitesi: özgeçmiş, yayınlar, hekimler için Dahiliye İlaç Atlası ve Nefroloji Yeni İlaçlar Çalışma Atlası.

İçerik [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr) lisanslıdır. Yazı tipleri SIL Open Font License 1.1 (`yazi_tipleri/`).

## Yayın notu (hasta videolarının yazılı sayfaları)

`bobrek-sagligi/` ve `araclar/` klasörleri site kurulum betiğinin (site_kur.py) çıktısında yoktur; yayın sırasında **silinmemelidir**. Kurulum çıktısı depoya kopyalandıktan sonra, commit'ten önce şu komut çalıştırılır (tekrar çalıştırmak güvenlidir):

```bash
python3 -I araclar/video_sayfalari.py .
```

Komut; YouTube kimliği ve `araclar/metin/NN.md` metni olan her bölüm için `bobrek-sagligi/<adres>/` sayfasını üretir, `hasta.html` kartlarına bağlantı, `index.html`'e kişi işaretlemesi ekler, `sitemap.xml`, `robots.txt` ve `sw.js` sürüm etiketini günceller. Yeni bölüm metni PDF'ten eklemek için: `python3 -I araclar/pdf_metin.py "NN. Başlık.pdf"`. `araclar/sluglar.json` kalıcı adresleri tutar; elle değiştirilmez.

## Yayın notu (sunumlarda sahiplik ibaresi, 19 Kasım 2026)

`dersler/*/index.html` ve `literatur/*/index.html` sunumlarında giriş kapısının üçüncü onay kutusu (`dk3`: izinsiz kullanılamaz) ve her slayttaki "Prof. Dr. Savaş Öztürk tarafından hazırlanmıştır" ibaresi (`i.soimza`; yalnız bu cümle, kullanıcı isteği) `araclar/imza_ekle.py` ile eklenir. Atlaslarda (`dahiliye-ilac-atlasi/`, `nefroloji-yeni-ilaclar/`) aynı araç yalnız giriş kapısına üçüncü kutuyu (`yzc3`) ekler; sayfa içine ibare koymaz. Yeni ya da yeniden üretilmiş bir sunum ya da atlas depoya kopyalandıktan sonra, commit'ten önce (tekrar çalıştırmak güvenlidir):

```bash
python3 -I araclar/imza_ekle.py dersler/*/index.html literatur/*/index.html dahiliye-ilac-atlasi/index.html nefroloji-yeni-ilaclar/index.html
```

## Nefroloji Ders Serisi şekil paketi (Kasım 2026)

Seriye eklenen özgün şematik şekiller sunumun içine elle yazılmaz; `araclar/sekiller.json` paketinden `araclar/sekil_ekle.py` ile eklenir.
Seri başka bir ortamda yeniden üretilip depoya kopyalandığında şekilleri geri getirmek için (tekrar çalıştırmak güvenlidir):

```
python3 -I araclar/sekil_ekle.py dersler/nefroloji-ders-serisi/index.html
python3 -I araclar/metin_duzelt.py dersler/nefroloji-ders-serisi/index.html
python3 -I araclar/imza_ekle.py dersler/nefroloji-ders-serisi/index.html
```

- "yeni" ögeler hedef slaydın ardına şekil slaydı ekler; "ic" ögeler mevcut slaydın gövdesinin sonuna yerleşir (metne dokunmaz).
- Araç ana sayfadaki ders slayt sayılarını ve toplamı yeniden hesaplar. `index.html` ve `atlaslar.html` içindeki toplam slayt sayısı elle güncellenir (şu an 2770).
- Şekillerin kaynağı `araclar/sekil_kaynak/` içindedir: `sekil_kit.py` (çizim kiti: tübül hücresi, kapiller ilmek, çubuk grafik, idrar yolu), `sekil_glom.py` (glomerül kiti: üç kapiller ilmekli lobül, vasküler ve tübüler kutuplu glomerül, filtrasyon bariyeri, immünfloresan paterni), `sekil_ortak.py` (ortak yardımcılar), ders başına tanım dosyası (`sekil_07.py` … `sekil_15.py`, `sekil_21.py`), `sekil_paket.py` (paketi üretir), `sekil_olc.py` (slayttaki boş alanı ölçer, görüntü alır).
- Glomerül kalıbı (20 Kasım 2026): glomerüler şekillerde glomerül vektörle çizilmez. Taban, Prof. Öztürk’ün verdiği normal glomerül görselidir (`dersler/nefroloji-ders-serisi/gorsel/glom_yumak.webp`: bütün glomerül; `glom_lobul.webp`: üç kapillerli lobül). Lezyonlar `araclar/sekil_kaynak/sekil_gk.py` (`GK` sınıfı) ile tabanın üzerine bindirilir; duvar, mezangiyum ve kapsül konumları `araclar/sekil_kaynak/kalip/kalip.json` ölçümünden gelir, elle koordinat verilmez. Kullanım kılavuzu claude.ai projesindeki `claude/glomerul_kalibi.md` belgesindedir. `sekil_glom.py` içindeki `Glomerul`, `Lobul` ve `mini_glomerul` yeni şekilde kullanılmaz. Filtrasyon bariyeri şeridi (Ders 08 ve 09) vektör çizim olarak kalmıştır.
- `araclar/metin_duzelt.py`: hakem denetiminde bulunan slayt metni düzeltmeleri; slayt kimliğiyle sınırlı ve tekrar çalıştırmak güvenlidir. Seri kaynağından yeniden üretilirse bu aracı da çalıştırın.
- Kural: şekil mümkünse mevcut slayda, metin küçülmeden sığıyorsa oraya; sığmıyorsa yeni slayda konur. Her şekil yayından önce bağımsız bir hakemce denetlenir.

## Tek dosyalık derslerin yeni sürümü (21 Kasım 2026)

Parenteral / İstatistik / Makale motoruyla üretilmiş bir dersin yeni tek dosyası yayındaki sayfaya şöyle aktarılır (site kabuğu, ortak kapı ve servis çalışanı kaydı korunur; iç ikinci onay kutusu ve "2026–2027" ibaresi çıkarılır; slayt ibaresi yinelenmez):

```bash
python3 -I araclar/ders_guncelle.py <yeni_tek_dosya.html> dersler/<ad>/index.html
```

Ardından `sw.js` sürüm etiketi artırılır, `sitemap.xml` tarihi ve `surum-notlari.html` güncellenir, `araclar/test_site.py` çalıştırılır.


**İndirme kuralına istisna (21.11.2026):** İstatistik dersindeki beş sentetik uygulama veri seti (.sav, .csv) sayfaya gömülüdür (`window.VERISET`) ve `.vsbtn` düğmeleriyle indirilir. Sitede başka indirme yoktur; `test_site.py` bunu denetler.
