# drsavasozturk.com

Prof. Dr. Savaş Öztürk'ün kişisel akademik sitesi: özgeçmiş, yayınlar, hekimler için Dahiliye İlaç Atlası ve Nefroloji Yeni İlaçlar Çalışma Atlası.

İçerik [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr) lisanslıdır. Yazı tipleri SIL Open Font License 1.1 (`yazi_tipleri/`).

## Yayın notu (hasta videolarının yazılı sayfaları)

`bobrek-sagligi/` ve `araclar/` klasörleri site kurulum betiğinin (site_kur.py) çıktısında yoktur; yayın sırasında **silinmemelidir**. Kurulum çıktısı depoya kopyalandıktan sonra, commit'ten önce şu komut çalıştırılır (tekrar çalıştırmak güvenlidir):

```bash
python3 -I araclar/video_sayfalari.py .
```

Komut; YouTube kimliği ve `araclar/metin/NN.md` metni olan her bölüm için `bobrek-sagligi/<adres>/` sayfasını üretir, `hasta.html` kartlarına bağlantı, `index.html`'e kişi işaretlemesi ekler, `sitemap.xml`, `robots.txt` ve `sw.js` sürüm etiketini günceller. Yeni bölüm metni PDF'ten eklemek için: `python3 -I araclar/pdf_metin.py "NN. Başlık.pdf"`. `araclar/sluglar.json` kalıcı adresleri tutar; elle değiştirilmez.
