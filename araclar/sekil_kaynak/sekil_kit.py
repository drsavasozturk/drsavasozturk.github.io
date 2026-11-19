#!/usr/bin/env python3
"""Nefroloji Ders Serisi · özgün vektör şekil kiti (Kasım 2026).

Tüm şekiller 1140 birim genişliğinde bir SVG tuvaline çizilir (slayttaki mevcut şekillerle aynı ölçü).
Bileşenler:  Fig (temel çizim) · epitel (tübül hücresi: lümen | hücre | kan) · mini (küçük hücre paneli)
             ilmek (glomerül kapiller ilmek kesiti, birikim yerleri) · cubuk (gruplu çubuk grafik)
             bobrek / ureter / mesane (idrar yolu şemaları)
Renkler sunumun paletidir. Yazı tipi sayfadan devralınır.
"""
import math, html as H

INK = '#16222f'; INK2 = '#4a5b6b'; MUT = '#6b7b8a'; LINE = '#c9d6e0'
BRAND = '#0b6e99'; BRANDD = '#084f6e'; ACC = '#008b8b'; GOLD = '#b97a00'; RED = '#c0392b'; GREEN = '#1f8a4c'; PUR = '#6a4c93'
TINT = {BRAND: '#e8f6ff', BRANDD: '#e8f6ff', ACC: '#e3f7f7', GOLD: '#fff6e0', RED: '#fdeaea', GREEN: '#eaf7ef', PUR: '#f1ecf8', INK2: '#f2f5f8', MUT: '#f2f5f8'}
LUMEN = '#fffbea'; KAN = '#fdf1f0'; HUCRE = '#eef7fc'; IDRAR = '#f5c518'


def e(s): return H.escape(str(s), quote=True)


def duz(txt):
    return ''.join((p[0] if isinstance(p, tuple) else p) for p in txt) if isinstance(txt, (list, tuple)) else str(txt)


def gen(txt, fs, kalin=False):
    """Kaba metin genişliği tahmini (px)."""
    w = 0
    for ch in duz(txt):
        if ch in " .,;:·'’ilıİIjt()|/⁺⁻": w += .31
        elif ch in 'mwMW': w += .88
        elif ch in '₂₃²³': w += .36
        elif ch.isupper() or ch.isdigit(): w += .64
        else: w += .55
    return w * fs * (1.07 if kalin else 1)


UYARI = []


class Fig:
    def __init__(s, fid, h, label, w=1140, mh=None):
        s.fid, s.w, s.h, s.label, s.mh = fid, w, h, label, (mh or h)
        s.p, s.mk = [], {}

    def a(s, *x): s.p.extend(x); return s

    # ---- yazı: txt düz metin ya da [(metin, 'b' | 'i' | 'bi' | renk | ''), ...] parçaları
    def t(s, x, y, txt, fs=13, fw=None, fill=INK, a='start', it=False, ls=None, op=None):
        at = ''
        if fw: at += f' font-weight="{fw}"'
        if it: at += ' font-style="italic"'
        if a != 'start': at += f' text-anchor="{a}"'
        if ls: at += f' letter-spacing="{ls}"'
        if op: at += f' opacity="{op}"'
        if isinstance(txt, (list, tuple)):
            ic = ''
            for par in txt:
                m, st = (par if isinstance(par, tuple) else (par, ''))
                q = ''
                for k in ([st] if isinstance(st, str) else st):
                    if k.startswith('#'): q += f' fill="{k}"'
                    else:
                        if 'b' in k: q += ' font-weight="800"'
                        if 'i' in k: q += ' font-style="italic"'
                ic += f'<tspan{q}>{e(m)}</tspan>'
        else:
            ic = e(txt)
        s.p.append(f'<text x="{x:g}" y="{y:g}" font-size="{fs:g}" fill="{fill}"{at}>{ic}</text>')

    def tl(s, x, y, lines, fs=13, lh=None, **k):
        lh = lh or fs * 1.3
        for i, l in enumerate(lines): s.t(x, y + i * lh, l, fs, **k)

    def r(s, x, y, w, h, fill='#fff', st=None, sw=1.6, rx=10, dash=None, op=None):
        at = f' stroke="{st}" stroke-width="{sw:g}"' if st else ''
        if dash: at += f' stroke-dasharray="{dash}"'
        if op: at += f' opacity="{op}"'
        s.p.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx:g}" fill="{fill}"{at}/>')

    def el(s, cx, cy, rx, ry=None, fill='#fff', st=None, sw=1.6, op=None, dash=None):
        ry = rx if ry is None else ry
        at = f' stroke="{st}" stroke-width="{sw:g}"' if st else ''
        if op: at += f' opacity="{op}"'
        if dash: at += f' stroke-dasharray="{dash}"'
        s.p.append(f'<ellipse cx="{cx:g}" cy="{cy:g}" rx="{rx:g}" ry="{ry:g}" fill="{fill}"{at}/>')

    def ln(s, x1, y1, x2, y2, c=INK2, sw=2, dash=None, cap='round'):
        at = f' stroke-dasharray="{dash}"' if dash else ''
        s.p.append(f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{c}" stroke-width="{sw:g}" stroke-linecap="{cap}"{at}/>')

    def _m(s, c):
        if c not in s.mk: s.mk[c] = f'm{s.fid}{len(s.mk)}'
        return s.mk[c]

    def ok(s, x1, y1, x2, y2, c=INK2, sw=2.4, dash=None, cift=False):
        at = f' stroke-dasharray="{dash}"' if dash else ''
        if cift: at += f' marker-start="url(#{s._m(c)}s)"'
        s.p.append(f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{c}" stroke-width="{sw:g}" marker-end="url(#{s._m(c)})"{at}/>')

    def yol(s, d, c=INK2, sw=2.4, fill='none', ok=False, dash=None, op=None, join='round'):
        at = f' marker-end="url(#{s._m(c)})"' if ok else ''
        if dash: at += f' stroke-dasharray="{dash}"'
        if op: at += f' opacity="{op}"'
        st = f' stroke="{c}" stroke-width="{sw:g}" stroke-linejoin="{join}" stroke-linecap="round"' if c else ''
        s.p.append(f'<path d="{d}" fill="{fill}"{st}{at}/>')

    def engel(s, x1, y1, x2, y2, c=RED, sw=2.6, T=9):
        """İnhibisyon çizgisi: uçta dik kısa çizgi (⊣)."""
        s.ln(x1, y1, x2, y2, c, sw)
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L, dx / L
        s.ln(x2 + nx * T, y2 + ny * T, x2 - nx * T, y2 - ny * T, c, sw + .6)

    def etiket(s, x, y, w, lines, c=BRAND, fs=13, lh=None, pad=8, a='start', fill=None, dash=None):
        """Renkli çerçeveli not kutusu; y kutunun düşey ORTASIDIR. İlk satır kalın ve renkli."""
        lh = lh or fs * 1.28; h = pad * 2 + lh * len(lines) - (lh - fs) * .6
        s.r(x, y - h / 2, w, h, fill or TINT.get(c, '#fff'), c, 1.5, 8, dash)
        for i, l in enumerate(lines):
            g_ = gen(l, fs if i == 0 else fs - .8, i == 0)
            if g_ > w - 2 * pad + 2: UYARI.append('%s: etiket taşıyor (%d > %d): %s' % (s.fid, g_, w - 2 * pad, duz(l)))
        tx = x + pad + 1 if a == 'start' else x + w / 2
        for i, l in enumerate(lines):
            s.t(tx, y - h / 2 + pad + fs * .84 + i * lh, l, fs if i == 0 else fs - .8, 800 if i == 0 else None, c if i == 0 else INK, a)
        return h

    def isaret(s, x, y, tur='x', r=9.5):
        c = RED if tur == 'x' else GREEN
        s.el(x, y, r, r, c, '#fff', 1.6)
        if tur == 'x':
            s.ln(x - 4, y - 4, x + 4, y + 4, '#fff', 2.3); s.ln(x - 4, y + 4, x + 4, y - 4, '#fff', 2.3)
        else:
            s.yol(f'M{x:g},{y - 5:g} L{x + 4.6:g},{y + 3.6:g} L{x - 4.6:g},{y + 3.6:g} Z', None, 0, '#fff')

    def svg(s):
        d = ''
        for c, i in s.mk.items():
            d += (f'<marker id="{i}" markerWidth="11" markerHeight="11" refX="8.5" refY="5.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0.6 L10,5.5 L0,10.4 z" fill="{c}"/></marker>'
                  f'<marker id="{i}s" markerWidth="11" markerHeight="11" refX="2.5" refY="5.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M11,0.6 L1,5.5 L11,10.4 z" fill="{c}"/></marker>')
        return (f'<svg viewBox="0 0 {s.w:g} {s.h:g}" style="width:100%;height:auto;max-height:{s.mh:g}px" role="img" aria-label="{e(s.label)}">'
                + (f'<defs>{d}</defs>' if d else '') + ''.join(s.p) + '</svg>')


# ------------------------------------------------------------------------------------------------ tübül hücresi
def _sekil(F, x, y, tip, renk):
    if tip == 'kanal':
        F.r(x - 14, y - 22, 11, 44, renk, '#fff', 1.6, 5); F.r(x + 3, y - 22, 11, 44, renk, '#fff', 1.6, 5)
    elif tip == 'pompa':
        F.el(x, y, 21, 21, renk, '#fff', 2); F.t(x, y + 4, 'ATP', 10.5, 800, '#fff', 'middle')
    elif tip == 'res':   # reseptör: zarı geçen Y biçimi yerine yuvarlak başlı gövde
        F.r(x - 6, y - 20, 12, 40, renk, '#fff', 1.6, 6)
    else:
        F.r(x - 13, y - 22, 26, 44, renk, '#fff', 2, 13)


def epitel(F, ad, apikal, bazal, y0=8, h=None, mx=340, bx=740, lx=6, rx=1074, sat=76, ust=50, firca=False,
           hucre_renk=HUCRE, tw=196, lumen_ad='LÜMEN · idrar', kan_ad='İNTERSTİSYUM · kan', para=None):
    """Lümen | hücre | kan düzeninde tek hücre. apikal / bazal: sözlük listeleri
       ad, iyon, yon ('gir' | 'cik'), ters (karşı yönde taşınan), tip ('tas' | 'kanal' | 'pompa' | 'res'), renk,
       tag (satırlar), tagc (renk), isaret ('x' kayıp | 'a' kazanım), alt (hücre içi küçük not), y (satır ortası; yoksa sırayla)
       para: (etiket, tag satırları, renk) -> hücrenin altında paraselüler yol."""
    n = max(len(apikal), len(bazal)); h = h or (ust + n * sat)
    ph = 66 if para else 0
    F.r(lx, y0, mx - lx, h + ph, LUMEN, None, rx=8); F.r(bx, y0, rx - bx, h + ph, KAN, None, rx=8)
    F.r(mx, y0, bx - mx, h, hucre_renk, None, rx=0)
    if para:
        F.r(mx, y0 + h + 48, bx - mx, ph - 48, hucre_renk, None, rx=0, op=.75)
        F.ln(mx, y0 + h + 48, mx, y0 + h + ph, BRANDD, 4, cap='butt'); F.ln(bx, y0 + h + 48, bx, y0 + h + ph, BRANDD, 4, cap='butt')
        F.ln(mx, y0 + h + 48, bx, y0 + h + 48, BRANDD, 2); F.ln(mx, y0 + h, bx, y0 + h, BRANDD, 2)
    if firca:
        yy = y0 + 6
        while yy < y0 + h - 4:
            F.ln(mx - 11, yy, mx, yy, BRANDD, 2.2); yy += 7
    F.ln(mx, y0, mx, y0 + h, BRANDD, 4.5, cap='butt'); F.ln(bx, y0, bx, y0 + h, BRANDD, 4.5, cap='butt')
    F.t(lx + 12, y0 + 22, lumen_ad, 12.5, 800, GOLD, ls='.06em')
    F.t((mx + bx) / 2, y0 + 24, ad, 15, 800, BRANDD, 'middle')
    F.t(rx - 12, y0 + 22, kan_ad, 12.5, 800, RED, 'end', ls='.06em')
    ys = []
    for liste, zx, sol in ((apikal, mx, True), (bazal, bx, False)):
        for i, o in enumerate(liste):
            y = o.get('y', y0 + ust + i * sat + sat / 2); ys.append(y)
            c = o.get('renk', BRAND); d = 1 if sol else -1          # d: hücreye doğru yön
            dis, ic = zx - d * 98, zx + d * 80
            gir = o.get('yon', 'gir') == 'gir'
            ters = o.get('ters')
            ya = y - 7 if ters else y
            if o.get('iyon'):
                if gir: F.ok(dis, ya, ic, ya, c)
                else: F.ok(ic, ya, dis, ya, c)
                F.t(zx - d * 26, ya - 9, o['iyon'], 13, 700, c, 'end' if sol else 'start')
                if gen(o['iyon'], 13, True) > 104: UYARI.append('%s: iyon yazısı uzun: %s' % (F.fid, duz(o['iyon'])))
            if ters:
                if gir: F.ok(ic, y + 10, dis, y + 10, MUT)
                else: F.ok(dis, y + 10, ic, y + 10, MUT)
                F.t(zx - d * 26, y + 27, ters, 12.5, 700, MUT, 'end' if sol else 'start')
            _sekil(F, zx, y, o.get('tip', 'tas'), c)
            F.t(zx + d * 24, ya - 9, o['ad'], 13.5, 800, INK, 'start' if sol else 'end')
            if o.get('alt'):
                alt = o['alt'] if isinstance(o['alt'], list) else [o['alt']]
                for k, sat_ in enumerate(alt): F.t(zx + d * 24, y + 26 + k * 14.5, sat_, 11.8, None, INK2, 'start' if sol else 'end')
            if o.get('isaret'): F.isaret(zx + d * 15, y - 27, o['isaret'])
            if o.get('tag'):
                tc = o.get('tagc', RED); tx = lx + 8 if sol else rx - 8 - tw
                F.etiket(tx, y, tw, o['tag'], tc, o.get('tagfs', 12.8))
                if sol: F.ln(tx + tw + 3, y, dis - 5, y, tc, 1.4, '2 4')
                else: F.ln(dis + 5, y, tx - 3, y, tc, 1.4, '2 4')
    if para:
        et, tag, pc = para; yp = y0 + h + 34
        F.ok(mx - 98, yp, bx + 98, yp, pc, 2.4, '7 5')
        F.r(mx - 5, yp - 9, 10, 18, pc, '#fff', 1.4, 3); F.r(bx - 5, yp - 9, 10, 18, pc, '#fff', 1.4, 3)
        F.t((mx + bx) / 2, yp - 14, et, 12.8, 700, pc, 'middle')
        if tag: F.etiket(lx + 8, yp - 2, tw, tag, RED, 12.4, pad=6)
    return dict(mx=mx, bx=bx, y0=y0, h=h, lx=lx, rx=rx, ys=ys)


def mini(F, x, w, y, h, ad, apikal=(), bazal=(), cw=None, renk=HUCRE, lumen_w=None):
    """Küçük hücre paneli (üçlü karşılaştırmalar için). apikal/bazal: (y, ad, iyon, yon, tip, renk, isaret)."""
    cw = cw or w * .46; lw = lumen_w or (w - cw) / 2; mx = x + lw; bx = mx + cw
    F.r(x, y, lw, h, LUMEN, None, rx=8); F.r(bx, y, x + w - bx, h, KAN, None, rx=8); F.r(mx, y, cw, h, renk, None, rx=0)
    F.ln(mx, y, mx, y + h, BRANDD, 4, cap='butt'); F.ln(bx, y, bx, y + h, BRANDD, 4, cap='butt')
    F.t(x + 8, y + 17, 'LÜMEN', 11, 800, GOLD, ls='.06em'); F.t(x + w - 8, y + 17, 'KAN', 11, 800, RED, 'end', ls='.06em')
    F.t((mx + bx) / 2, y + 19, ad, 13, 800, BRANDD, 'middle')
    for liste, zx, sol in ((apikal, mx, True), (bazal, bx, False)):
        for (yy, nm, iyon, yon, tip, c, isr) in liste:
            d = 1 if sol else -1; dis, ic = zx - d * 62, zx + d * 46
            if iyon:
                if yon == 'gir': F.ok(dis, yy, ic, yy, c, 2.2)
                else: F.ok(ic, yy, dis, yy, c, 2.2)
                F.t(zx - d * 22, yy - 8, iyon, 12, 700, c, 'end' if sol else 'start')
            _sekil(F, zx, yy, tip, c)
            F.t(zx + d * 20, yy - 8, nm, 12.2, 800, INK, 'start' if sol else 'end')
            if isr: F.isaret(zx + d * 13, yy - 26, isr, 8.5)
    return dict(mx=mx, bx=bx)


# ------------------------------------------------------------------------------------------------ glomerül kapiller ilmek
def ilmek(F, cx, cy, R=62, birikim=(), efase=False, mez_hiper=False, diken=False, tri=False, gbm_c='#7d8fa3', etiketler=True, se=((200, 13), (262, 13), (330, 13)), se_k=7):
    """Tek kapiller ilmeğin enine kesiti: lümen · endotel (pencereli) · GBM · podosit ayaksı çıkıntıları · altta mezangiyum.
       birikim: 'subepi' | 'subendo' | 'mez' | 'intra' ögeleri. efase: ayaksı çıkıntı silinmesi. diken: GBM dikenleri (spike).
       tri: endotelde tübüloretiküler inklüzyon."""
    a0, a1 = 125, 415          # GBM yayı (derece; saat yönü, 0 = sağ); altta 55-125 arası mezangiyum açıklığı
    def P(r, a): return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
    # mezangiyum
    F.yol(f'M{cx - R * .78:g},{cy + R * .62:g} Q{cx:g},{cy + R * .15:g} {cx + R * .78:g},{cy + R * .62:g} L{cx + R * .55:g},{cy + R * 1.45:g} L{cx - R * .55:g},{cy + R * 1.45:g} Z', '#b9a7d6', 1.5, '#ece4f7')
    F.el(cx, cy + R * 1.02, R * .2, R * .15, PUR if not mez_hiper else PUR, None)
    if mez_hiper:
        F.el(cx - R * .34, cy + R * 1.2, R * .17, R * .13, PUR); F.el(cx + R * .34, cy + R * 1.2, R * .17, R * .13, PUR)
    # lümen + eritrosit
    F.el(cx, cy, R, R, '#fff5f4', None)
    F.el(cx - R * .2, cy - R * .12, R * .22, R * .17, '#e98b80', None, op=.75); F.el(cx + R * .26, cy + R * .16, R * .2, R * .15, '#e98b80', None, op=.75)
    # GBM
    x0, y0 = P(R + 9, a0); x1, y1 = P(R + 9, a1)
    F.yol(f'M{x0:.1f},{y0:.1f} A{R + 9:g},{R + 9:g} 0 1 1 {x1:.1f},{y1:.1f}', gbm_c, 9)
    # endotel (pencereli: kesikli)
    x0, y0 = P(R + 1.5, a0 + 2); x1, y1 = P(R + 1.5, a1 - 2)
    F.yol(f'M{x0:.1f},{y0:.1f} A{R + 1.5:g},{R + 1.5:g} 0 1 1 {x1:.1f},{y1:.1f}', '#d9534f', 3.4, dash='9 4')
    # podosit ayaksı çıkıntıları
    if efase:
        x0, y0 = P(R + 19, a0 + 3); x1, y1 = P(R + 19, a1 - 3)
        F.yol(f'M{x0:.1f},{y0:.1f} A{R + 19:g},{R + 19:g} 0 1 1 {x1:.1f},{y1:.1f}', BRAND, 8.5)
    else:
        a = a0 + 5
        while a < a1 - 3:
            x, y = P(R + 19.5, a); F.el(x, y, 5.2, 5.2, BRAND, None); a += 11.5
    # birikimler
    if 'subepi' in birikim:
        for a in range(a0 + 18, a1 - 8, 27):
            x, y = P(R + 16.5, a); F.el(x, y, 6.6, 5.2, INK, '#fff', 1)
            if diken:
                for da in (-7, 7):
                    xa, ya = P(R + 13, a + da); xb, yb = P(R + 22, a + da); F.ln(xa, ya, xb, yb, gbm_c, 3)
    if 'subendo' in birikim:
        for (a, ya) in se:
            x0, y0 = P(R + 3.5, a - ya); x1, y1 = P(R + 3.5, a + ya)
            F.yol(f'M{x0:.1f},{y0:.1f} A{R + 3.5:g},{R + 3.5:g} 0 0 1 {x1:.1f},{y1:.1f}', INK, se_k)
    if 'intra' in birikim:
        x0, y0 = P(R + 9, 205); x1, y1 = P(R + 9, 335)
        F.yol(f'M{x0:.1f},{y0:.1f} A{R + 9:g},{R + 9:g} 0 0 1 {x1:.1f},{y1:.1f}', INK, 5.5, dash='16 9')
    if 'mez' in birikim:
        for dx, dy in ((-.3, .78), (.28, .8), (0, 1.26), (-.2, 1.1), (.3, 1.12)):
            F.el(cx + R * dx, cy + R * dy, 5.4, 4.4, INK, '#fff', 1)
    if tri:
        x, y = P(R - 9, 300); F.el(x, y, 6.5, 6.5, '#fff', RED, 1.6); F.ln(x - 3.4, y - 2, x + 3.4, y + 2, RED, 1.4); F.ln(x - 3.4, y + 2, x + 3.4, y - 2, RED, 1.4)
    return P


# ------------------------------------------------------------------------------------------------ çubuk grafik
def cubuk(F, x, y, w, h, gruplar, seriler, ymax=100, adim=20, birim='%', fs=13, bw=None, baslik=None, deger=None, lejant=True, lejx=None):
    """gruplar: [(etiket ya da [satırlar], [değerler...], (isteğe bağlı) [değer yazıları])] · seriler: [(ad, renk)]
       (x, y) çizim alanının SOL ÜST köşesi; h eksen yüksekliği (taban y + h)."""
    if baslik: F.t(x, y - 12, baslik, fs + .5, 800, BRANDD)
    t = 0
    while t <= ymax + 1e-9:
        yy = y + h - h * t / ymax
        F.ln(x, yy, x + w, yy, LINE if t else INK2, 1 if t else 1.8, None if not t else '3 4')
        F.t(x - 8, yy + 4, f'{t:g}', fs - 1.5, None, MUT, 'end'); t += adim
    F.t(x - 8, y - 12, birim, fs - 1.5, 700, MUT, 'end')
    ng, ns = len(gruplar), len(seriler); gw = w / ng
    bw = bw or min(46, gw * .72 / ns)
    for g, gr in enumerate(gruplar):
        et, vals = gr[0], gr[1]; yaz = gr[2] if len(gr) > 2 else None
        gx = x + gw * g + gw / 2; bx0 = gx - bw * ns / 2 - (ns - 1) * 2
        for k, v in enumerate(vals):
            if v is None: continue
            bh = h * v / ymax; bx = bx0 + k * (bw + 4)
            F.r(bx, y + h - bh, bw, bh, seriler[k][1], None, rx=3)
            F.t(bx + bw / 2, y + h - bh - 6, (yaz[k] if yaz else (deger(v) if deger else f'{v:g}'.replace('.', ','))), fs - .5, 800, seriler[k][1], 'middle')
        for k, l in enumerate(et if isinstance(et, list) else [et]):
            F.t(gx, y + h + 18 + k * (fs + 2), l, fs - .5, 700 if k == 0 else None, INK if k == 0 else INK2, 'middle')
    if lejant:
        lx = x + 6 if lejx is None else lejx
        for k, (ad, c) in enumerate(seriler):
            F.r(lx, y - 26 + 0, 13, 13, c, None, rx=3); F.t(lx + 18, y - 15, ad, fs - .5, 700, INK2); lx += 30 + len(ad) * (fs * .56)


# ------------------------------------------------------------------------------------------------ idrar yolu şemaları
def bobrek(F, cx, cy, k=1.0, pelvis=0, ayna=False, renk='#c9736b', skar=False, kucuk=False, idrar=IDRAR):
    """Böbrek (hilus içe bakar). pelvis: 0 normal · 1 hafif · 2 orta · 3 ağır genişleme (kaliksler küntleşir)."""
    if kucuk: k *= .72
    sx = -k if ayna else k
    g = f'<g transform="translate({cx:g},{cy:g}) scale({sx:g},{k:g})">'
    g += f'<path d="M-6,-50 C-36,-50 -38,50 -6,50 C16,50 22,28 12,12 C6,4 6,-4 12,-12 C22,-28 16,-50 -6,-50 Z" fill="{renk}" stroke="#8e4a44" stroke-width="2"/>'
    pw = (7, 10, 15, 21)[pelvis]; ph = (9, 13, 19, 27)[pelvis]; kr = (3.2, 4.6, 6.6, 8.6)[pelvis]; kc = idrar
    for (tx, ty) in ((-8, -26), (-14, 0), (-8, 26)):
        g += f'<line x1="6" y1="0" x2="{tx}" y2="{ty}" stroke="{kc}" stroke-width="{2.6 + pelvis * 2.2:g}" stroke-linecap="round"/>'
        g += f'<circle cx="{tx}" cy="{ty}" r="{kr}" fill="{kc}"/>'
    g += f'<ellipse cx="8" cy="0" rx="{pw}" ry="{ph}" fill="{kc}"/>'
    if skar: g += '<path d="M-27,-22 L-17,-16 L-28,-8" fill="none" stroke="#fff" stroke-width="3"/><path d="M-29,14 L-19,20 L-27,30" fill="none" stroke="#fff" stroke-width="3"/>'
    g += '</g>'
    F.a(g)
    return (cx + (-(8 + pw * .6) if ayna else (8 + pw * .6)) * k, cy + ph * .7 * k)     # üreter çıkış noktası


def ureter(F, x1, y1, x2, y2, gen=4, kivrim=0, renk=IDRAR, kenar='#a07a00'):
    """Üreter: gen kalınlık; kivrim 0-3 (kıvrımlılık)."""
    dx = 13 * kivrim; n = 3 if kivrim else 1
    if kivrim:
        ys = [y1 + (y2 - y1) * i / (2 * n) for i in range(2 * n + 1)]; xs = [x1 + (x2 - x1) * i / (2 * n) for i in range(2 * n + 1)]
        d = f'M{x1:g},{y1:g}'
        for i in range(1, 2 * n + 1, 2):
            sgn = 1 if (i // 2) % 2 == 0 else -1
            d += f' Q{xs[i] + sgn * dx:g},{ys[i]:g} {xs[i + 1]:g},{ys[i + 1]:g}'
    else:
        d = f'M{x1:g},{y1:g} C{x1:g},{(y1 + y2) / 2:g} {x2:g},{(y1 + y2) / 2:g} {x2:g},{y2:g}'
    F.yol(d, kenar, gen + 2.4); F.yol(d, renk, gen)


def mesane(F, cx, cy, rx=34, ry=28, duvar=3, renk=IDRAR, uretra=18, valv=False, arka=False):
    F.el(cx, cy, rx + duvar, ry + duvar, '#b98a80', '#8e4a44', 1.6); F.el(cx, cy, rx, ry, renk)
    uy = cy + ry + duvar
    if arka:   # genişlemiş posterior üretra ("anahtar deliği")
        F.yol(f'M{cx - 7:g},{uy - 3:g} Q{cx - 15:g},{uy + 12:g} {cx - 4:g},{uy + 22:g} L{cx + 4:g},{uy + 22:g} Q{cx + 15:g},{uy + 12:g} {cx + 7:g},{uy - 3:g} Z', '#8e4a44', 1.6, renk)
        F.ln(cx, uy + 22, cx, uy + 22 + uretra, '#8e4a44', 5); F.ln(cx, uy + 22, cx, uy + 22 + uretra, renk, 2)
        if valv: F.ln(cx - 8, uy + 21, cx + 8, uy + 21, RED, 3.4)
    else:
        F.ln(cx, uy - 1, cx, uy + uretra, '#8e4a44', 5.5); F.ln(cx, uy - 1, cx, uy + uretra, renk, 2.4)
