#!/usr/bin/env python3
"""drsavasozturk.com · hasta videoları için yazılı sayfalar ve arama motoru işaretlemesi.

Kullanım (depo kökünde):   python3 -I araclar/video_sayfalari.py .

Ne yapar (tekrar çalıştırmak güvenlidir; site_kur.py çıktısı depoya kopyalandıktan SONRA çalıştırılır):
  1. hasta.html içindeki bölümleri okur; YouTube kimliği VE araclar/metin/NN.md dosyası olan her bölüm için
     bobrek-sagligi/<slug>/index.html üretir (video + yazılı anlatım + VideoObject/MedicalWebPage JSON-LD).
  2. bobrek-sagligi/index.html (yazılı anlatımların listesi) üretir.
  3. hasta.html kartlarına yazılı sayfa bağlantısı, index.html'e kişi/site JSON-LD ekler.
  4. sitemap.xml, robots.txt ve sw.js sürüm etiketini günceller.

Veri: araclar/metin/NN.md (bölüm metni), araclar/sluglar.json (kalıcı adresler; elle değiştirmeyin),
      araclar/yayin.json (YouTube yayın tarihleri), araclar/durum.json (metin değişim tarihleri).
"""
import hashlib, html, json, re, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

KOK = "https://drsavasozturk.com"
KLASOR = "bobrek-sagligi"
ARAC = Path(__file__).resolve().parent
BUGUN = datetime.now(timezone(timedelta(hours=3))).date().isoformat()
AYLAR = "Ocak Şubat Mart Nisan Mayıs Haziran Temmuz Ağustos Eylül Ekim Kasım Aralık".split()
KISI = {
    "@type": "Person", "@id": KOK + "/#kisi", "name": "Savaş Öztürk", "honorificPrefix": "Prof. Dr.",
    "jobTitle": "İç Hastalıkları ve Nefroloji Profesörü", "url": KOK + "/",
    "affiliation": {"@type": "CollegeOrUniversity",
                    "name": "İstanbul Üniversitesi, İstanbul Tıp Fakültesi, İç Hastalıkları Anabilim Dalı, Nefroloji Bilim Dalı"},
    "knowsAbout": ["Nefroloji", "İç hastalıkları", "Kronik böbrek hastalığı", "Hemodiyaliz", "Periton diyalizi",
                   "Glomerüler hastalıklar", "Böbrek nakli"],
    "sameAs": ["https://orcid.org/0000-0002-0961-3810", "https://avesis.istanbul.edu.tr/savas.ozturk",
               "https://www.youtube.com/@drsavasozturk", "https://www.instagram.com/prof.dr.savasozturk/"],
}
KISI_KISA = {k: KISI[k] for k in ("@type", "@id", "name", "honorificPrefix", "jobTitle", "url", "sameAs")}


def oku(p): return Path(p).read_text(encoding="utf-8")
def yaz(p, s):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists() or p.read_text(encoding="utf-8") != s:
        p.write_text(s, encoding="utf-8"); return True
    return False
def jyukle(ad):
    p = ARAC / ad
    return json.loads(oku(p)) if p.exists() else {}
def jyaz(ad, d): yaz(ARAC / ad, json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
def e(s): return html.escape(s, quote=True)
def tarih_tr(iso):
    y, a, g = iso.split("-"); return f"{int(g)} {AYLAR[int(a) - 1]} {y}"
def ld(veri): return '<script type="application/ld+json">' + json.dumps(veri, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def slug_yap(baslik):
    s = baslik.lower().translate(str.maketrans("çğıöşüâîû", "cgiosuaiu")).replace("i̇", "i")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    if len(s) > 60: s = s[:60].rsplit("-", 1)[0]
    return s


def kok_yol(parca):
    """Göreli href/src değerlerini kökten başlatır (alt klasördeki sayfalar için)."""
    def d(m):
        y = m.group(2)
        return f'{m.group(1)}="/{"" if y in ("./", ".") else y}"'
    return re.sub(r'(href|src)="(?!https?:|mailto:|#|/|&#|data:)([^"]*)"', d, parca)


# ---------- hasta.html: önceki yamaları geri al, bölümleri oku ----------
def yama_sok(h):
    h = re.sub(r'<style id="yz-css">.*?</style>', "", h, flags=re.S)
    h = re.sub(r'<a class="yz" href="[^"]*">(.*?)</a>', r"\1", h, flags=re.S)
    h = re.sub(r' · <a class="yz2" href="[^"]*">[^<]*</a>', "", h)
    return h


def bolumler(h):
    cik = []
    par = re.split(r'<section id="([a-z0-9-]+)"><h2>(.*?)</h2>', h)
    for i in range(1, len(par) - 2, 3):
        sid, sbas, govde = par[i], html.unescape(par[i + 1]), par[i + 2]
        for m in re.finditer(r'<article class="vid" id="b(\d+)">(.*?)</article>', govde, re.S):
            a = m.group(2)
            yt = re.search(r'data-yt="([^"]+)"', a)
            h3 = html.unescape(re.sub(r"<[^>]+>", "", re.search(r"<h3>(.*?)</h3>", a, re.S).group(1)))
            acik = html.unescape(re.sub(r"<[^>]+>", "", re.search(r"</h3><p>(.*?)</p>", a, re.S).group(1)))
            sure = re.search(r'class="sure">([^<]*)<', a).group(1)
            kisa = html.unescape(re.search(r'class="vbas">([^<]*)<', a).group(1))
            cik.append(dict(no=int(m.group(1)), sec=sid, sect=sbas, yt=yt.group(1) if yt else None,
                            baslik=re.sub(r"^\d+\.\s*", "", h3), acik=acik, sure=sure, kisa=kisa))
    return cik


# ---------- metin (markdown alt kümesi) -> HTML ----------
def satir_ici(s):
    s = e(s).replace("&quot;", '"').replace("&#x27;", "’")
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r'"([^"]+)"', r"“\1”", s)


def metin_html(md):
    satirlar, cik, liste, atla = md.splitlines(), [], None, False
    def kapat():
        nonlocal liste
        if liste: cik.append(f"</{liste}>"); liste = None
    for s in satirlar:
        s = s.rstrip()
        if s.startswith("# "): continue
        if s.startswith("### "):
            kapat()
            if not atla: cik.append(f"<h3>{satir_ici(s[4:].strip())}</h3>")
            continue
        if s.startswith("## "):
            kapat(); atla = s[3:].strip().lower().startswith("kapanış kartı")
            if not atla: cik.append(f"<h2>{satir_ici(s[3:].strip())}</h2>")
            continue
        if atla or not s.strip():
            if not s.strip() and liste is None: pass
            continue
        m = re.match(r"(\d+)\.\s+(.*)", s); b = re.match(r"[-•]\s+(.*)", s)
        if m or b:
            tur = "ol" if m else "ul"
            if liste != tur: kapat(); cik.append(f"<{tur}>"); liste = tur
            cik.append(f"<li>{satir_ici((m.group(2) if m else b.group(1)))}</li>")
            continue
        kapat()
        if re.match(r"(Bir sonraki konu|Sıradaki konu)\s*:", s): continue
        cik.append(f"<p>{satir_ici(s)}</p>")
    kapat()
    return "\n".join(cik)


def sure_iso(sure):
    p = [int(x) for x in sure.split(":")]
    if len(p) == 3: return f"PT{p[0]}H{p[1]}M{p[2]}S"
    return f"PT{p[0]}M{p[1]}S"


STIL = """<style>
.kir{font-size:.9rem;color:var(--mut);margin:0 0 12px}.kir a{font-weight:600}
.oynk{max-width:760px;margin:16px 0 4px}.oynk .oyn{border-radius:14px;overflow:hidden}
.oynk .oy{padding:22px 24px}.oynk .oy .vno{font-size:3rem}.oynk .oy .vbas{font-size:1.5rem;margin-top:10px}
.vmeta{margin:8px 0 0;color:var(--mut);font-size:.95rem}
.metin{max-width:46em;margin-top:22px}.metin h2{margin-top:1.5em;font-size:1.4rem}.metin h3{margin-top:1.2em;font-size:1.15rem}.metin li{margin:.4em 0}
.metin ol,.metin ul{padding-left:1.4em}
.imza{max-width:46em;color:var(--mut);border-top:1px solid var(--line);padding-top:12px;margin-top:26px;font-size:.95rem}
.onson{display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;max-width:46em;margin:18px 0 0}
.onson a{flex:1 1 15em;padding:10px 14px;border:1px solid var(--line);border-radius:12px;background:var(--card);text-decoration:none;font-weight:600}
.onson small{display:block;color:var(--mut);font-weight:400}
.ilgili{max-width:46em;margin-top:26px}.ilgili li{margin:.35em 0}
.yliste h2{margin-top:1.4em}.yliste li{margin:.5em 0;max-width:48em}.yliste span{color:var(--mut)}
@media print{.oynk,.onson,.ilgili{display:none}}
</style>"""
OYNAT_JS = ("<script>document.querySelectorAll('.oyn[data-yt]').forEach(function(d){var b=d.querySelector('button');"
            "b.addEventListener('click',function(){var f=document.createElement('iframe');"
            "f.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(d.getAttribute('data-yt'))+'?autoplay=1&rel=0';"
            "f.title=b.getAttribute('aria-label').replace(/ oynat:/,':');"
            "f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';f.allowFullscreen=true;"
            "f.referrerPolicy='strict-origin-when-cross-origin';d.replaceChildren(f);f.focus();});});</script>")


def main(site):
    site = Path(site)
    hasta = yama_sok(oku(site / "hasta.html"))
    bol = bolumler(hasta)
    if not bol: sys.exit("hasta.html içinde bölüm bulunamadı; betik güncellenmeli.")

    # ortak parçalar hasta.html'den alınır; menü ve alt bilgi siteyle aynı kalır
    ust = kok_yol(re.search(r'<header class="ust">.*?</header>', hasta, re.S).group(0))
    alt_m = re.search(r'<footer class="alt">.*?</footer>(<script>.*?</script>)?', hasta, re.S)
    alt = kok_yol(alt_m.group(0)).replace("register('./sw.js',{scope:'./'})", "register('/sw.js',{scope:'/'})")
    uyari = re.search(r'<div class="uyari">.*?</div>', hasta, re.S).group(0)
    bas_ek = kok_yol("".join(re.findall(r'<link rel="(?:manifest|icon|apple-touch-icon|stylesheet)"[^>]*>|<meta name="theme-color"[^>]*>|<script defer src=[^>]*></script>',
                                         hasta[:hasta.find("</head>")])))

    sluglar, yayin, durum = jyukle("sluglar.json"), jyukle("yayin.json"), jyukle("durum.json")
    sayfalar = []
    for b in sorted(bol, key=lambda x: x["no"]):
        mp = ARAC / "metin" / f"{b['no']:02d}.md"
        if not b["yt"] or not mp.exists(): continue
        k = str(b["no"])
        if k not in sluglar:
            s = slug_yap(b["baslik"])
            if s in sluglar.values(): s += f"-{b['no']}"
            sluglar[k] = s
        b["slug"] = sluglar[k]
        b["govde"] = metin_html(oku(mp))
        if b["yt"] not in yayin: yayin[b["yt"]] = BUGUN
        b["yayin"] = yayin[b["yt"]]
        ozet = hashlib.sha256((b["govde"] + b["baslik"] + b["acik"] + b["yt"]).encode()).hexdigest()[:16]
        if durum.get(k, {}).get("ozet") != ozet: durum[k] = {"ozet": ozet, "degisim": BUGUN}
        b["degisim"] = max(durum[k]["degisim"], b["yayin"])
        b["url"] = f"{KOK}/{KLASOR}/{b['slug']}/"
        sayfalar.append(b)
    jyaz("sluglar.json", sluglar); jyaz("yayin.json", yayin); jyaz("durum.json", durum)

    def bas(baslik, acik, url, tur="article", ek=""):
        t = f"{baslik} · Prof. Dr. Savaş Öztürk"
        return (f'<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>{e(t)}</title><meta name="description" content="{e(acik)}"><link rel="canonical" href="{url}">'
                f'<meta name="robots" content="max-snippet:-1,max-image-preview:large,max-video-preview:-1">'
                f'<meta property="og:type" content="{tur}"><meta property="og:site_name" content="Prof. Dr. Savaş Öztürk"><meta property="og:locale" content="tr_TR">'
                f'<meta property="og:title" content="{e(baslik)}"><meta property="og:description" content="{e(acik)}"><meta property="og:url" content="{url}">'
                f'<meta property="og:image" content="{KOK}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
                f'<meta name="twitter:card" content="summary_large_image">{bas_ek}{STIL}{ek}</head><body>{ust}')

    uretilen = {}
    for i, b in enumerate(sayfalar):
        once = sayfalar[i - 1] if i else None
        sonra = sayfalar[i + 1] if i + 1 < len(sayfalar) else None
        ilgili = [x for x in sayfalar if x["sec"] == b["sec"] and x is not b]
        video = {"@type": "VideoObject", "@id": b["url"] + "#video", "name": b["baslik"], "description": b["acik"],
                 "thumbnailUrl": [f"https://i.ytimg.com/vi/{b['yt']}/hqdefault.jpg"], "uploadDate": b["yayin"] + "T09:00:00+03:00",
                 "duration": sure_iso(b["sure"]), "embedUrl": f"https://www.youtube-nocookie.com/embed/{b['yt']}",
                 "url": f"https://www.youtube.com/watch?v={b['yt']}", "inLanguage": "tr", "author": {"@id": KISI["@id"]}}
        graf = {"@context": "https://schema.org", "@graph": [
            {"@type": "MedicalWebPage", "@id": b["url"], "url": b["url"], "name": b["baslik"], "headline": b["baslik"],
             "description": b["acik"], "inLanguage": "tr", "datePublished": b["yayin"], "dateModified": b["degisim"],
             "lastReviewed": b["degisim"], "author": {"@id": KISI["@id"]}, "reviewedBy": {"@id": KISI["@id"]},
             "audience": {"@type": "Patient"}, "isPartOf": {"@type": "WebSite", "@id": KOK + "/#site", "url": KOK + "/", "name": "Prof. Dr. Savaş Öztürk"},
             "image": KOK + "/og.png", "video": {"@id": video["@id"]}},
            video, KISI_KISA,
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": KOK + "/"},
                {"@type": "ListItem", "position": 2, "name": "Hasta ve yakınları için", "item": KOK + "/hasta.html"},
                {"@type": "ListItem", "position": 3, "name": b["baslik"], "item": b["url"]}]}]}
        etiket = e(f"{b['no']}. bölümü oynat: {b['baslik']} ({b['sure']})")
        s = bas(b["baslik"], b["acik"], b["url"], ek=ld(graf))
        s += (f'<main class="ic"><p class="kir"><a href="/">Ana sayfa</a> › <a href="/hasta.html#{b["sec"]}">Hasta ve yakınları için</a> › {e(b["kisa"])}</p>'
              f'<p class="ust-et">Böbrek sağlığı videoları · {b["no"]}. bölüm</p><h1>{e(b["baslik"])}</h1><p class="giris">{e(b["acik"])}</p>'
              f'<div class="oynk"><div class="oyn" data-yt="{b["yt"]}"><button type="button" class="oy" aria-label="{etiket}"><span class="vno">{b["no"]}</span>'
              f'<span class="vbas">{e(b["kisa"])}</span><span class="uc" aria-hidden="true"></span><span class="sure">{b["sure"]}</span></button></div>'
              f'<p class="vmeta">Video · {b["sure"]} · <a href="https://www.youtube.com/watch?v={b["yt"]}" rel="noopener noreferrer" target="_blank">YouTube’da izle</a></p></div>'
              f'{uyari}<article class="metin"><p class="ust-et">Bu bölümün yazılı anlatımı</p>\n{b["govde"]}\n</article>'
              f'<p class="imza">Hazırlayan: <a href="/ozgecmis.html">Prof. Dr. Savaş Öztürk</a>, İç Hastalıkları ve Nefroloji · Yayın: {tarih_tr(b["yayin"])}'
              + (f' · Güncelleme: {tarih_tr(b["degisim"])}' if b["degisim"] != b["yayin"] else "") + "</p>")
        s += '<div class="onson">'
        if once: s += f'<a href="/{KLASOR}/{once["slug"]}/"><small>← Önceki bölüm</small>{e(once["baslik"])}</a>'
        if sonra: s += f'<a href="/{KLASOR}/{sonra["slug"]}/"><small>Sonraki bölüm →</small>{e(sonra["baslik"])}</a>'
        s += "</div>"
        if ilgili:
            s += (f'<section class="ilgili"><h2>{e(b["sect"])}</h2><ul>'
                  + "".join(f'<li><a href="/{KLASOR}/{x["slug"]}/">{e(x["baslik"])}</a></li>' for x in ilgili) + "</ul></section>")
        s += f'<p class="vmeta"><a href="/hasta.html">Tüm videolar</a> · <a href="/{KLASOR}/">Tüm yazılı anlatımlar</a></p>{OYNAT_JS}</main>{alt}</body></html>\n'
        uretilen[f"{KLASOR}/{b['slug']}/index.html"] = s

    # liste sayfası
    l_acik = "Böbrek sağlığı üzerine hasta ve yakınlarının sık sorduğu sorular: her videonun yazılı anlatımı, konu başlıklarına göre."
    l_url = f"{KOK}/{KLASOR}/"
    s = bas("Böbrek sağlığı: yazılı anlatımlar", l_acik, l_url, tur="website")
    s += ('<main class="ic yliste"><p class="kir"><a href="/">Ana sayfa</a> › <a href="/hasta.html">Hasta ve yakınları için</a> › Yazılı anlatımlar</p>'
          f'<h1>Böbrek sağlığı: yazılı anlatımlar</h1><p class="giris">Hasta ve yakınları için hazırlanan videoların yazılı anlatımları. Her sayfada video ve metni birlikte bulunur. Videoların tümü için <a href="/hasta.html">Hasta ve yakınları için</a> sayfasına bakın.</p>{uyari}')
    gorulen = []
    for b in sayfalar:
        if b["sec"] not in gorulen: gorulen.append(b["sec"])
    for sec in gorulen:
        grup = [b for b in sayfalar if b["sec"] == sec]
        s += f'<section><h2>{e(grup[0]["sect"])}</h2><ul>' + "".join(
            f'<li><a href="/{KLASOR}/{b["slug"]}/">{e(b["baslik"])}</a><br><span>{e(b["acik"])}</span></li>' for b in grup) + "</ul></section>"
    s += f"</main>{alt}</body></html>\n"
    uretilen[f"{KLASOR}/index.html"] = s

    # artık üretilmeyen eski sayfaları sil, yenileri yaz
    kl = site / KLASOR
    if kl.exists():
        for p in kl.rglob("index.html"):
            if p.relative_to(site).as_posix() not in uretilen: p.unlink()
        for d in sorted([d for d in kl.rglob("*") if d.is_dir()], reverse=True):
            if not any(d.iterdir()): d.rmdir()
    for yol, icerik in uretilen.items(): yaz(site / yol, icerik)

    # hasta.html kartlarına bağlantı
    def kart(m):
        a = m.group(0); no = int(m.group(1))
        b = next((x for x in sayfalar if x["no"] == no), None)
        if not b: return a
        hedef = f'{KLASOR}/{b["slug"]}/'
        a = re.sub(r"<h3>(.*?)</h3>", lambda h: f'<h3><a class="yz" href="{hedef}">{h.group(1)}</a></h3>', a, count=1, flags=re.S)
        return re.sub(r'(<p class="yl">.*?</a>)(</p>)', lambda y: f'{y.group(1)} · <a class="yz2" href="{hedef}">Yazısını oku</a>{y.group(2)}', a, count=1, flags=re.S)
    hasta2 = re.sub(r'<article class="vid" id="b(\d+)">.*?</article>', kart, hasta, flags=re.S)
    hasta2 = hasta2.replace("</head>", '<style id="yz-css">.vid h3 a{color:inherit;text-decoration:none}.vid h3 a:hover{text-decoration:underline}</style></head>', 1)
    yaz(site / "hasta.html", hasta2)

    # ana sayfa: kişi ve site işaretlemesi
    ana = re.sub(r'<script type="application/ld\+json" id="ld-kisi">.*?</script>', "", oku(site / "index.html"), flags=re.S)
    kisi_ld = ld({"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": KOK + "/#site", "url": KOK + "/", "name": "Prof. Dr. Savaş Öztürk", "inLanguage": "tr", "publisher": {"@id": KISI["@id"]}},
        {"@type": "ProfilePage", "@id": KOK + "/#sayfa", "url": KOK + "/", "inLanguage": "tr", "mainEntity": {"@id": KISI["@id"]}},
        dict(KISI, description="İstanbul Üniversitesi İstanbul Tıp Fakültesi İç Hastalıkları Anabilim Dalı, Nefroloji Bilim Dalı öğretim üyesi.")]}
    ).replace('<script type="application/ld+json">', '<script type="application/ld+json" id="ld-kisi">')
    yaz(site / "index.html", ana.replace("</head>", kisi_ld + "</head>", 1))

    # sitemap
    sm = re.sub(rf"<url><loc>{re.escape(KOK)}/{KLASOR}/[^<]*</loc>.*?</url>", "", oku(site / "sitemap.xml"), flags=re.S)
    son = max([b["degisim"] for b in sayfalar] or [BUGUN])
    ek = f"<url><loc>{l_url}</loc><lastmod>{son}</lastmod></url>" + "".join(
        f'<url><loc>{b["url"]}</loc><lastmod>{b["degisim"]}</lastmod></url>' for b in sayfalar)
    yaz(site / "sitemap.xml", sm.replace("</urlset>", ek + "</urlset>"))

    # robots: araç klasörü taranmasın
    rb = oku(site / "robots.txt")
    if "Disallow: /araclar/" not in rb:
        yaz(site / "robots.txt", rb.replace("Allow: /\n", "Allow: /\nDisallow: /araclar/\n", 1) if "Allow: /\n" in rb else rb.rstrip("\n") + "\nDisallow: /araclar/\n")

    # service worker: sürüm etiketi içerik değişince değişsin (ziyaretçi eski önbellekte kalmasın)
    sw = oku(site / "sw.js")
    iz = hashlib.sha256(("".join(uretilen[k] for k in sorted(uretilen)) + hasta2).encode()).hexdigest()[:8]
    sw2 = re.sub(r"const V = '([^'.]+)(?:\.y[0-9a-f]+)?';", lambda m: f"const V = '{m.group(1)}.y{iz}';", sw, count=1)
    if sw2 == sw and f".y{iz}'" not in sw: sys.exit("sw.js içinde sürüm satırı bulunamadı; betik güncellenmeli.")
    yaz(site / "sw.js", sw2)

    eksik = [b["no"] for b in bol if b["yt"] and not (ARAC / "metin" / f"{b['no']:02d}.md").exists()]
    print(f"{len(sayfalar)} yazılı sayfa üretildi." + (f" Metni olmayan yayındaki bölümler: {eksik}" if eksik else ""))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
