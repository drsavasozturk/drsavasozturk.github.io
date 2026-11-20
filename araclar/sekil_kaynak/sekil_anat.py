#!/usr/bin/env python3
"""Anatomik çizim seti (pilot, 20 Kasım 2026): gölgeli, gradyanlı böbrek, üreter, mesane, damar ve taş.
Kimlikler şekil kimliğiyle öneklenir (tüm şekiller aynı sayfada satır içi durur)."""
import math, random
from sekil_kit import *

IDR_A, IDR_K, IDR_C = '#fbe08a', '#e2aa22', '#a8780f'      # idrar: açık, koyu, çizgi


def tanim(F):
    """Şekle bir kez gradyan ve filtre tanımları ekler; önek döndürür."""
    p = 'an_' + F.fid
    if getattr(F, '_an', None): return p
    F._an = True
    F.a(f'''<defs>
<radialGradient id="{p}_kor" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#e6a197"/><stop offset=".55" stop-color="#cc7468"/><stop offset="1" stop-color="#a24d45"/></radialGradient>
<linearGradient id="{p}_pir" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9c3f38"/><stop offset="1" stop-color="#c8665c"/></linearGradient>
<linearGradient id="{p}_idr" gradientUnits="userSpaceOnUse" x1="-30" y1="-40" x2="25" y2="40"><stop offset="0" stop-color="{IDR_A}"/><stop offset="1" stop-color="{IDR_K}"/></linearGradient>
<radialGradient id="{p}_mes" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#fdeba6"/><stop offset=".7" stop-color="#f2c544"/><stop offset="1" stop-color="#d9a21c"/></radialGradient>
<radialGradient id="{p}_kas" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#e2aaa0"/><stop offset="1" stop-color="#b9736a"/></radialGradient>
<radialGradient id="{p}_tas" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#d8c7a8"/><stop offset=".45" stop-color="#8a6a44"/><stop offset="1" stop-color="#3f2c16"/></radialGradient>
<filter id="{p}_gol" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur in="SourceAlpha" stdDeviation="3.2"/><feOffset dx="2.5" dy="4" result="o"/>
<feComponentTransfer><feFuncA type="linear" slope=".28"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="{p}_gol2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur in="SourceAlpha" stdDeviation="1.4"/><feOffset dx="1" dy="1.6"/>
<feComponentTransfer><feFuncA type="linear" slope=".35"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>''')
    return p


BOB = 'M-4,-56 C-34,-56 -45,-28 -45,0 C-45,28 -34,56 -4,56 C14,56 25,44 23,29 C21,18 11,13 9,0 C11,-13 21,-18 23,-29 C25,-44 14,-56 -4,-56 Z'
S0 = (6, 0)                                         # sinüs merkezi (yerel)
ACI = (100, 124, 148, 170, 190, 212, 236, 260)      # piramit doğrultuları (derece)
MAJ = ((-6, -30), (-15, 0), (-6, 30))               # majör kaliksler


def _sinir(t):
    """Sinüs merkezinden t açısıyla giden ışının böbrek dış sınırına uzaklığı (elips yaklaşımı)."""
    c, s = math.cos(math.radians(t)), math.sin(math.radians(t))
    cx, rx, ry = -11, 34, 56
    a = (c / rx) ** 2 + (s / ry) ** 2; b = 2 * c * (S0[0] - cx) / rx ** 2; cc = ((S0[0] - cx) / rx) ** 2 - 1
    return (-b + math.sqrt(b * b - 4 * a * cc)) / (2 * a)


def bobrek(F, cx, cy, k=1.0, ayna=False, gen=1, damar=True):
    """Kesitli böbrek: korteks, medüller piramitler, kaliksler, pelvis, hilus damarları.
    gen: 0 normal · 1 hafif · 2 orta · 3 ağır toplayıcı sistem genişlemesi. Üreter çıkış noktasını döndürür."""
    p = tanim(F); sx = -k if ayna else k
    g = f'<g transform="translate({cx:g},{cy:g}) scale({sx:g},{k:g})">'
    if damar:   # hilus damarları (ven önde)
        g += (f'<path d="M14,-12 C26,-14 34,-16 46,-16" stroke="#7d1f1a" stroke-width="8" fill="none" stroke-linecap="round"/>'
              f'<path d="M14,-12 C26,-14 34,-16 46,-16" stroke="#cf4a3f" stroke-width="5.6" fill="none" stroke-linecap="round"/>'
              f'<path d="M14,-5 C26,-4 34,-5 46,-4" stroke="#27457a" stroke-width="10" fill="none" stroke-linecap="round"/>'
              f'<path d="M14,-5 C26,-4 34,-5 46,-4" stroke="#5c80c4" stroke-width="7.4" fill="none" stroke-linecap="round"/>'
              f'<path d="M16,-7 C26,-6 34,-7 44,-6" stroke="#a9c1ea" stroke-width="1.6" fill="none" stroke-linecap="round" opacity=".8"/>')
    g += f'<path d="{BOB}" fill="url(#{p}_kor)" stroke="#7a3530" stroke-width="1.8" filter="url(#{p}_gol)"/>'
    g += '<path d="M-30,-40 C-40,-22 -41,4 -36,22" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" opacity=".18"/>'
    papil = []
    for t in ACI:
        d = _sinir(t); c, s = math.cos(math.radians(t)), math.sin(math.radians(t))
        tb = d * .80; ta = d * (.40 + .04 * gen); w = math.radians(10.5)
        b1 = (S0[0] + tb * math.cos(math.radians(t) - w), S0[1] + tb * math.sin(math.radians(t) - w))
        b2 = (S0[0] + tb * math.cos(math.radians(t) + w), S0[1] + tb * math.sin(math.radians(t) + w))
        ap = (S0[0] + ta * c, S0[1] + ta * s); papil.append(ap)
        g += (f'<path d="M{b1[0]:.1f},{b1[1]:.1f} Q{S0[0] + tb * 1.04 * c:.1f},{S0[1] + tb * 1.04 * s:.1f} {b2[0]:.1f},{b2[1]:.1f} L{ap[0]:.1f},{ap[1]:.1f} Z" '
              f'fill="url(#{p}_pir)" stroke="#86322c" stroke-width=".6" opacity=".92"/>')
        for f_ in (.3, .6):   # piramit çizgileri
            q = (b1[0] + (b2[0] - b1[0]) * f_, b1[1] + (b2[1] - b1[1]) * f_)
            g += f'<line x1="{q[0]:.1f}" y1="{q[1]:.1f}" x2="{ap[0]:.1f}" y2="{ap[1]:.1f}" stroke="#e7a59c" stroke-width=".45" opacity=".7"/>'
    w_inf, r_cal = (3.2, 4.6, 6.6, 8.4)[gen], (3.6, 4.6, 6.0, 7.6)[gen]
    pw, ph = (8, 11, 15, 19)[gen], (10, 14, 19, 24)[gen]
    ic = ''
    for ap in papil:   # minör kaliks (papillayı saran çanak) → en yakın majör kaliks
        m = min(MAJ, key=lambda q: (q[0] - ap[0]) ** 2 + (q[1] - ap[1]) ** 2)
        ux_, uy_ = ap[0] - S0[0], ap[1] - S0[1]; L = math.hypot(ux_, uy_); ux_, uy_ = ux_ / L, uy_ / L
        dip = (ap[0] - ux_ * r_cal * .9, ap[1] - uy_ * r_cal * .9)
        ic += f'<line x1="{dip[0]:.1f}" y1="{dip[1]:.1f}" x2="{m[0]}" y2="{m[1]}" stroke-width="{w_inf}" stroke-linecap="round"/>'
        b0 = math.atan2(-uy_, -ux_); pts = []
        for q in range(11):
            f_ = b0 + math.radians(-105 + 21 * q); pts.append(f'{ap[0] + r_cal * 1.15 * math.cos(f_):.1f},{ap[1] + r_cal * 1.15 * math.sin(f_):.1f}')
        ic += f'<polyline points="{" ".join(pts)}" fill="none" stroke-width="{w_inf * .9 + 1:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
    for m in MAJ: ic += f'<line x1="{m[0]}" y1="{m[1]}" x2="10" y2="0" stroke-width="{w_inf + 2.4}" stroke-linecap="round"/>'
    ic += f'<ellipse cx="10" cy="2" rx="{pw}" ry="{ph}"/>'
    g += f'<g stroke="{IDR_C}" fill="{IDR_C}">{ic}</g>'
    g += f'<g stroke="url(#{p}_idr)" fill="url(#{p}_idr)">{_daralt(ic)}</g>'
    g += '</g>'
    F.a(g)
    ex, ey = 10 + pw * .55, 2 + ph * .72
    return (cx + (-ex if ayna else ex) * k, cy + ey * k)


def _daralt(ic):
    """Dış çizgi katmanının biraz incesi: idrar dolgusu."""
    import re
    ic = re.sub(r'stroke-width="([\d.]+)"', lambda m: f'stroke-width="{max(float(m.group(1)) - 1.6, .8):g}"', ic)
    ic = re.sub(r' r="([\d.]+)"', lambda m: f' r="{max(float(m.group(1)) - .8, .8):g}"', ic)
    ic = re.sub(r'rx="([\d.]+)" ry="([\d.]+)"', lambda m: f'rx="{float(m.group(1)) - .8:g}" ry="{float(m.group(2)) - .8:g}"', ic)
    return ic


def yol_d(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)


def ureter(F, pts, w=5):
    """pts: üreter boyunca noktalar. Koyu kenar, gradyan dolgu, ince parlama."""
    d = yol_d(pts)
    F.yol(d, IDR_C, w + 3); F.yol(d, IDR_K, w + .6); F.yol(d, IDR_A, w * .55)
    F.a(f'<path d="{d}" transform="translate(-.9,-.6)" stroke="#fffbe8" stroke-width="{w * .18:g}" fill="none" stroke-linecap="round" opacity=".85"/>')


def mesane(F, cx, cy, rx=46, ry=34, girisler=(), uretra=16):
    """Kesitli mesane: kas duvarı, idrar, trigon ve üreter ağızları."""
    p = tanim(F)
    d = (f'M{cx - rx},{cy - ry * .1} C{cx - rx},{cy - ry * 1.05} {cx + rx},{cy - ry * 1.05} {cx + rx},{cy - ry * .1} '
         f'C{cx + rx},{cy + ry * .62} {cx + rx * .32},{cy + ry} {cx},{cy + ry} C{cx - rx * .32},{cy + ry} {cx - rx},{cy + ry * .62} {cx - rx},{cy - ry * .1} Z')
    F.yol(f'M{cx - 5},{cy + ry - 2} L{cx - 5},{cy + ry + uretra} M{cx + 5},{cy + ry - 2} L{cx + 5},{cy + ry + uretra}', '#9a5a52', 3)
    F.r(cx - 4, cy + ry - 4, 8, uretra + 3, IDR_K, None, rx=3)
    F.a(f'<path d="{d}" fill="url(#{p}_kas)" stroke="#8e4a44" stroke-width="1.6" filter="url(#{p}_gol)"/>')
    ic = (f'M{cx - rx + 7},{cy - ry * .08} C{cx - rx + 7},{cy - ry * .86} {cx + rx - 7},{cy - ry * .86} {cx + rx - 7},{cy - ry * .08} '
          f'C{cx + rx - 7},{cy + ry * .5} {cx + rx * .26},{cy + ry - 7} {cx},{cy + ry - 7} C{cx - rx * .26},{cy + ry - 7} {cx - rx + 7},{cy + ry * .5} {cx - rx + 7},{cy - ry * .08} Z')
    F.a(f'<path d="{ic}" fill="url(#{p}_mes)" stroke="{IDR_C}" stroke-width="1"/>')
    F.a(f'<path d="M{cx - rx * .55},{cy - ry * .42} Q{cx - rx * .2},{cy - ry * .72} {cx + rx * .2},{cy - ry * .66}" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".45"/>')
    tg = [(cx - rx * .42, cy + ry * .12), (cx + rx * .42, cy + ry * .12), (cx, cy + ry - 9)]
    F.a(f'<path d="M{tg[0][0]:.1f},{tg[0][1]:.1f} L{tg[1][0]:.1f},{tg[1][1]:.1f} L{tg[2][0]:.1f},{tg[2][1]:.1f} Z" fill="#e9b94a" opacity=".55"/>')
    for (x, y) in tg[:2]: F.el(x, y, 3.4, 2.2, '#8a5a10', None)
    return tg


def damar(F, pts, tur='a', w=7):
    """Arter (a) ya da ven (v): koyu kenar, gradyanlı gövde, parlama."""
    d = yol_d(pts)
    kenar, govde, par = (('#7d1f1a', '#cf4a3f', '#f2a59b') if tur == 'a' else ('#27457a', '#5c80c4', '#bcd0f0'))
    F.yol(d, kenar, w + 2.6); F.yol(d, govde, w)
    F.a(f'<path d="{d}" transform="translate(-.8,-1.2)" stroke="{par}" stroke-width="{w * .22:g}" fill="none" stroke-linecap="round" opacity=".8"/>')


def tas(F, x, y, r, tohum=1):
    p = tanim(F); rg = random.Random(tohum); n = 11; pts = []
    for i in range(n):
        a = 2 * math.pi * i / n; rr = r * rg.uniform(.74, 1.06)
        pts.append(f'{x + rr * math.cos(a):.1f},{y + rr * math.sin(a):.1f}')
    F.a(f'<polygon points="{" ".join(pts)}" fill="url(#{p}_tas)" stroke="#2e1f0d" stroke-width="1.2" stroke-linejoin="round" filter="url(#{p}_gol2)"/>')
    for i in range(5):
        a = rg.uniform(0, 6.28); q = rg.uniform(.15, .55) * r
        F.el(x + q * math.cos(a), y + q * math.sin(a), r * .09, r * .09, '#2a1c0c', None, op=.6)
    F.el(x - r * .32, y - r * .36, r * .24, r * .15, '#fff', None, op=.8)
    return (x + r * .95, y)


def rozet(F, x, y, n, c=BRANDD, r=9):
    F.el(x, y, r, r, c, '#fff', 1.8); F.t(x, y + 4.2, str(n), 11.5, 800, '#fff', 'middle')


def cagri(F, p, tx, ty, lines, fs=12, c=INK, renk='#56677a'):
    """İnce çağrı çizgisi: noktada beyaz halkalı uç, metnin sol kenarına yatay bağlanır."""
    ls = lines if isinstance(lines, list) else [lines]
    qx = tx - 6; qy = ty - fs * .35
    mx = qx - 18
    F.a(f'<path d="M{p[0]:.1f},{p[1]:.1f} L{mx:.1f},{qy:.1f} L{qx:.1f},{qy:.1f}" stroke="{renk}" stroke-width="1.1" fill="none"/>')
    F.el(p[0], p[1], 3.2, 3.2, '#fff', renk, 1.3)
    F.t(tx, ty, ls[0], fs, 800, c)
    for i, l in enumerate(ls[1:]): F.t(tx, ty + (i + 1) * (fs + 3), l, fs - .6, None, INK2)
