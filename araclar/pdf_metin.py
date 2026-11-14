#!/usr/bin/env python3
"""Bölüm metni PDF'ini (Claude belgesinden dışa aktarılmış) araclar/metin/NN.md dosyasına çevirir.

Kullanım:  python3 -I araclar/pdf_metin.py "32. Diyalize girmezsem ne olur.pdf" [...]
Bölüm numarası dosya adındaki ilk "NN." kalıbından alınır. Biçim dışı satır görürse uyarır.
"""
import re, sys
from pathlib import Path
import pdfplumber

HEDEF = Path(__file__).resolve().parent / "metin"


def satirlar(pdf):
    for si, sayfa in enumerate(pdf.pages):
        kel = sayfa.extract_words(extra_attrs=["fontname", "size"], keep_blank_chars=False, x_tolerance=1.5)
        grup = {}
        for k in kel:
            grup.setdefault(round(k["top"] / 3), []).append(k)
        # aynı satırda farklı punto (kalın/normal) birkaç piksel kayabilir: komşu kümeleri birleştir
        anahtar = sorted(grup)
        birles, son = [], None
        for a in anahtar:
            if son is not None and a - son <= 1 and abs(min(k["top"] for k in grup[a]) - min(k["top"] for k in birles[-1])) < 4:
                birles[-1].extend(grup[a])
            else:
                birles.append(list(grup[a]))
            son = a
        for g in birles:
            g.sort(key=lambda k: k["x0"])
            yield si, g


def cevir(yol):
    cik, uyari = [], []
    durum = None            # None | "p" | "ol" | "ul"
    onceki_alt, onceki_sayfa, tampon = None, None, []

    def bosalt():
        nonlocal tampon, durum
        if tampon:
            metin = re.sub(r"\s+", " ", " ".join(tampon)).strip()
            metin = re.sub(r"\*\*\s*\*\*", " ", metin)
            cik.append(metin)
            tampon = []

    def bicim(kelimeler):
        par, kalin = [], False
        for k in kelimeler:
            b = "Semibold" in k["fontname"] or "Bold" in k["fontname"]
            if b and not kalin: par.append("**" + k["text"]); kalin = True
            elif not b and kalin: par[-1] += "**"; par.append(k["text"]); kalin = False
            else: par.append(k["text"])
        if kalin: par[-1] += "**"
        return " ".join(par)

    with pdfplumber.open(yol) as pdf:
        for si, g in satirlar(pdf):
            font, punto, x0, ust = g[0]["fontname"], g[0]["size"], g[0]["x0"], min(k["top"] for k in g)
            if "DejaVu" in font and punto < 8: continue                      # sayfa üst/alt bilgisi
            if "Serif" in font and punto > 20: continue                       # belge başlığı
            if punto < 10 and "Serif" not in font: continue                   # tarih · yazar satırı
            bosluk = (ust - onceki_alt) if (onceki_alt is not None and si == onceki_sayfa) else None
            yeni_sayfa = onceki_sayfa is not None and si != onceki_sayfa
            onceki_alt, onceki_sayfa = ust, si
            bitti = bool(tampon) and re.search(r"[.!?:…”\"]\*{0,2}$", tampon[-1]) is not None
            if "Serif" in font:                                               # ara başlık
                bosalt(); cik.append(""); cik.append("## " + " ".join(k["text"] for k in g)); cik.append(""); durum = None
                continue
            numara = re.fullmatch(r"(\d+)\.", g[0]["text"]) and 50 < x0 < 62
            if numara:
                bosalt(); durum = "ol"
                tampon = [f"{g[0]['text']} " + bicim(g[1:])]
            elif 62 <= x0 < 80:                                               # liste girintisi
                if durum == "ol" and tampon:
                    tampon.append(bicim(g))
                elif durum == "ul" and tampon and not ((bosluk is not None and bosluk >= 20) or (yeni_sayfa and bitti)):
                    tampon.append(bicim(g))
                else:
                    bosalt()
                    if durum not in ("ul",): cik.append("")
                    durum = "ul"; tampon = ["- " + bicim(g)]
            elif x0 < 50:                                                     # gövde paragrafı
                if durum == "p" and tampon and not ((bosluk is not None and bosluk >= 22) or (yeni_sayfa and bitti)):
                    tampon.append(bicim(g))
                else:
                    bosalt(); cik.append(""); durum = "p"; tampon = [bicim(g)]
            else:
                uyari.append(f"beklenmeyen girinti x={x0:.0f}: {' '.join(k['text'] for k in g)[:60]}")
                bosalt(); cik.append(""); durum = "p"; tampon = [bicim(g)]
        bosalt()
    # ol maddeleri arasında boş satır olmasın; fazla boş satırları toparla
    metin = "\n".join(cik)
    metin = re.sub(r"\n{3,}", "\n\n", metin).strip() + "\n"
    metin = re.sub(r"(?m)^(\d+\. .*)\n\n(?=\d+\. )", r"\1\n", metin)
    metin = re.sub(r"(?m)^(- .*)\n\n(?=- )", r"\1\n", metin)
    metin = re.sub(r"(?m)^(.*[^\n])\n(?=1\. )", r"\1\n\n", metin)
    return metin, uyari


if __name__ == "__main__":
    HEDEF.mkdir(exist_ok=True)
    for a in sys.argv[1:]:
        m = re.search(r"(?:^|[-_ /])(\d{1,2})\.[_ ]", Path(a).name)
        if not m: print("numara bulunamadı:", a); continue
        no = int(m.group(1))
        metin, uyari = cevir(a)
        (HEDEF / f"{no:02d}.md").write_text(metin, encoding="utf-8")
        print(f"{no:02d}.md  {len(metin.split())} kelime  {metin.count('## ')} başlık" + ("  UYARI: " + "; ".join(uyari) if uyari else ""))
