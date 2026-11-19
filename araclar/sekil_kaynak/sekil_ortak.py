"""Ders şekil dosyaları için ortak yardımcılar."""
from sekil_kit import *
from sekil_glom import *

OZGUN = ' <i>Özgün şematik çizim; ölçekli değildir.</i>'
OZGUN_G = ' <i>Özgün çizim.</i>'


class Ders:
    def __init__(s, no):
        s.no = no; s.L = []

    def yeni(s, sid, hedef, kicker, baslik, F, alt, notu, oz=OZGUN):
        s.L.append(dict(id=sid, ders=s.no, mod='yeni', hedef=hedef, kicker=kicker, baslik=baslik, svg=F.svg(), alt=alt + oz, **{'not': notu}))

    def ic(s, sid, hedef, F, alt=None, konum='son'):
        s.L.append(dict(id=sid, ders=s.no, mod='ic', hedef=hedef, svg=F.svg(), alt=alt, konum=konum))


def serit(F, x, y, w, txt, c, h=28, fs=13.5):
    F.r(x, y, w, h, TINT.get(c, '#f2f5f8'), None, rx=8); F.t(x + w / 2, y + h * .68, txt, fs, 800, c, 'middle')


def hap(F, x, y, txt, c=BRAND, fs=12.2, fill=None, kalin=True):
    w = gen(txt, fs, kalin) + 22
    F.r(x, y - 13, w, 26, fill or TINT.get(c, '#fff'), c, 1.3, 13); F.t(x + w / 2, y + 4.4, txt, fs, 700 if kalin else None, INK, 'middle'); return w


def haplar(F, x, y, w, liste, c=BRAND, fs=12.2, ara=8, satir=32):
    xx, yy = x, y
    for h_ in liste:
        ww = gen(h_, fs, True) + 22
        if xx + ww > x + w: xx, yy = x, yy + satir
        hap(F, xx, yy, h_, c, fs); xx += ww + ara
    return yy


def rozet(F, x, y, txt, c=RED, fs=11.5):
    w = gen(txt, fs, True) + 16
    F.r(x - w / 2, y - 11, w, 22, c, None, rx=11); F.t(x, y + 4.2, txt, fs, 800, '#fff', 'middle')


def zemin(F, x, y, w, h):
    F.r(x, y, w, h, BOW, None, rx=10)


def ikonlar(F, x, y, n, tutulan, r=7.5, ara=19, c=RED):
    """Biyopsideki glomerülleri temsil eden küçük daireler; ilk 'tutulan' kadarı lezyonlu."""
    for i in range(n):
        cx = x + i * ara
        F.el(cx, y, r, r, BOW, GBM_K, 1.1); F.el(cx, y, r * .7, r * .7, '#f4b7b4' if i >= tutulan else c, None)
