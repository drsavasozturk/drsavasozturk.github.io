#!/usr/bin/env python3
"""drsavasozturk.com · Nefroloji Ders Serisi'ne şekil paketi ekler (Kasım 2026, kullanıcı isteği).

Kullanım:  python3 -I araclar/sekil_ekle.py dersler/nefroloji-ders-serisi/index.html [araclar/sekiller.json]
Tekrar çalıştırmak güvenlidir: önce daha önce eklenmiş bütün şekilleri söker, sonra paketi baştan ekler.
Seri başka bir ortamda yeniden üretilip depoya kopyalandığında bu komut şekilleri geri getirir.

Paket (sekiller.json) ögeleri:
  mod "yeni": hedef slaydın hemen ardına yeni bir şekil slaydı ekler (id, ders, kicker, baslik, svg, alt, not).
  mod "ic"  : hedef slaydın gövdesinin sonuna (dipnottan önce) şekli yerleştirir; slaydın metnine dokunmaz.
Ana sayfadaki ders slayt sayıları ve toplamlar yeniden hesaplanır.
"""
import re, sys, json, os, html

IMZA = '<i class="soimza" aria-hidden="true"></i>'
STIL = ('<style id="sekil-stil">.skf{margin:0;text-align:center}.skf svg,.skic svg{display:block;margin:0 auto}'
        '.skic{margin:8px 0 0}.skn{font-size:13.6px;line-height:1.36;color:#4a5b6b;margin-top:6px;text-align:left}'
        '.skn b{color:#084f6e}.skn i{font-style:italic}</style>')


def sok(h):
    h = re.sub(r'<section id="[^"]*" data-ders="\d+" class="slide sk" data-sekil="[^"]*".*?</section>\n?', '', h, flags=re.S)
    h = re.sub(r'<div class="skic" data-sekil="[^"]*">.*?</div><!--/skic-->\n?', '', h, flags=re.S)
    return re.sub(r'<style id="sekil-stil">.*?</style>', '', h, flags=re.S)


def slayt_bul(h, sid):
    m = re.search(r'<section\b[^>]*\bid="%s"[^>]*>' % re.escape(sid), h)
    assert m, 'hedef slayt yok: ' + sid
    b = h.index('</section>', m.end())
    return m.start(), m.end(), b


def ekle(h, paket):
    son = {}                                    # aynı hedefe birden çok yeni slayt: sırayı koru
    for o in paket:
        if o['mod'] == 'yeni':
            hedef = son.get(o['hedef'], o['hedef'])
            _, _, b = slayt_bul(h, hedef); b += len('</section>')
            if h[b:b + 1] == '\n': b += 1
            yeni = ('<section id="%s" data-ders="%s" class="slide sk" data-sekil="%s" data-notes="%s">\n'
                    '  <div class="kicker">%s</div>\n  <h2>%s</h2>\n  <div class="body xs">\n    <figure class="skf">%s</figure>\n%s  </div>\n%s</section>\n'
                    % (o['id'], o['ders'], o['id'], html.escape(o.get('not', ''), quote=True), o['kicker'], o['baslik'], o['svg'],
                       ('    <div class="skn">%s</div>\n' % o['alt']) if o.get('alt') else '', IMZA))
            h = h[:b] + yeni + h[b:]; son[o['hedef']] = o['id']
        else:
            a, ae, b = slayt_bul(h, o['hedef']); s = h[a:b]
            blok = '<div class="skic" data-sekil="%s">%s%s</div><!--/skic-->\n' % (o['id'], o['svg'], ('<div class="skn">%s</div>' % o['alt']) if o.get('alt') else '')
            if o.get('konum') == 'bas':
                m = re.search(r'<div class="body[^"]*">\s*', s); assert m, o['hedef']; k = m.end()
            else:
                fn = s.rfind('<div class="fn">')
                if fn >= 0: k = fn
                else:
                    k = s.rfind('</div>'); assert k >= 0, o['hedef']       # gövdenin kapanışı
            s = s[:k] + blok + s[k:]; h = h[:a] + s + h[b:]
    return h


def say(h):
    """Ana sayfadaki slayt sayılarını güncelle."""
    n = {}
    for d in re.findall(r'<section\b[^>]*\bdata-ders="(\d+)"', h): n[d] = n.get(d, 0) + 1
    def lc(m): return m.group(1) + str(n[m.group(2)]) + m.group(4)
    h, k = re.subn(r'(<a class="li navto" data-go="L(\d+)"[^>]*>.{0,400}?<span class="lc"[^>]*>)(\d+)(</span>)', lc, h, flags=re.S)
    assert k == len(n), (k, len(n))
    # içindekiler katmanındaki "NN slayt" satırları
    def ds(m): return m.group(1) + str(n[m.group(2)]) + m.group(4)
    h, k2 = re.subn(r'(data-go="L(\d+)">[^<]*</div><div class="ds">)(\d+)( slayt)', ds, h)
    assert k2 == len(n), (k2, len(n))
    top = sum(n.values())
    m = re.search(r'(\d+) ders slaytı</b> \+ (\d+) ek sayfa = (\d+)', h); assert m
    fark = int(m.group(3)) - int(m.group(1)) - int(m.group(2))
    h = h[:m.start()] + '%d ders slaytı</b> + %s ek sayfa = %d' % (top, m.group(2), top + int(m.group(2)) + fark) + h[m.end():]
    return h, top


def isle(h, paket):
    h = sok(h)
    h = ekle(h, paket)
    i = h.index('</head>'); h = h[:i] + STIL + h[i:]
    return say(h)


if __name__ == '__main__':
    p = sys.argv[1]
    pk = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sekiller.json')
    paket = json.load(open(pk, encoding='utf-8'))
    t = open(p, encoding='utf-8').read(); y, top = isle(t, paket)
    if y != t: open(p, 'w', encoding='utf-8').write(y)
    print(p, 'değişti' if y != t else 'aynı', '| şekil:', len(paket), '(yeni slayt %d, slayt içi %d)' % (sum(o['mod'] == 'yeni' for o in paket), sum(o['mod'] != 'yeni' for o in paket)), '| ders slaytı:', top)
