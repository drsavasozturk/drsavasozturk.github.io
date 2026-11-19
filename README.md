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
- `araclar/metin_duzelt.py`: hakem denetiminde bulunan slayt metni düzeltmeleri; slayt kimliğiyle sınırlı ve tekrar çalıştırmak güvenlidir. Seri kaynağından yeniden üretilirse bu aracı da çalıştırın.
- Kural: şekil mümkünse mevcut slayda, metin küçülmeden sığıyorsa oraya; sığmıyorsa yeni slayda konur. Her şekil yayından önce bağımsız bir hakemce denetlenir.

