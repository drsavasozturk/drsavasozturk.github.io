#!/usr/bin/env python3
"""Anatomik çizim seti (20 Kasım 2026; kullanıcı kararı: anatomik çizimler yeniden, "kalite hissedilsin").
Gölgeli ve gradyanlı böbrek (korteks, piramitler, sinüs yağı, damarlar, toplayıcı sistem), üreter, mesane, prostat,
damar, taş, nefrostomi kateteri ve double-J stent, aksiyel kesit ögeleri (vertebra, psoas, aort, vena kava, lenf nodu, fibroz).
Kimlikler şekil kimliğiyle öneklenir (tüm şekiller aynı sayfada satır içi durur): an_<fid>_…
Gradyanlar: tek eksenli (yatay ya da düşey) çizgilerde objectBoundingBox görünmez; bu yüzden userSpaceOnUse."""
import math, random
from sekil_kit import *

IDR_A, IDR_K, IDR_C = '#fbe08a', '#e2aa22', '#a8780f'      # idrar: açık, koyu, çizgi
KAT = '#1f5f9e'                                            # kateter ve stent


def tanim(F):
    """Şekle bir kez gradyan, filtre ve doku tanımları ekler; önek döndürür."""
    p = 'an_' + F.fid
    if getattr(F, '_an', None): return p
    F._an = True
    F.a(f'''<defs>
<radialGradient id="{p}_kor" cx="36%" cy="30%" r="78%"><stop offset="0" stop-color="#eab0a6"/><stop offset=".5" stop-color="#cf7a6d"/><stop offset="1" stop-color="#9f4a42"/></radialGradient>
<radialGradient id="{p}_pir" gradientUnits="userSpaceOnUse" cx="6" cy="0" r="52"><stop offset=".3" stop-color="#c76a5f"/><stop offset=".62" stop-color="#9e3f37"/><stop offset="1" stop-color="#7f2f29"/></radialGradient>
<radialGradient id="{p}_yag" gradientUnits="userSpaceOnUse" cx="14" cy="0" r="34"><stop offset="0" stop-color="#f7ebc9"/><stop offset="1" stop-color="#e3c98f"/></radialGradient>
<linearGradient id="{p}_idr" gradientUnits="userSpaceOnUse" x1="-30" y1="-40" x2="25" y2="40"><stop offset="0" stop-color="{IDR_A}"/><stop offset="1" stop-color="{IDR_K}"/></linearGradient>
<radialGradient id="{p}_mes" cx="40%" cy="32%" r="72%"><stop offset="0" stop-color="#fdedb0"/><stop offset=".7" stop-color="#f2c544"/><stop offset="1" stop-color="#d9a21c"/></radialGradient>
<radialGradient id="{p}_kas" cx="40%" cy="28%" r="78%"><stop offset="0" stop-color="#e8b5ab"/><stop offset=".6" stop-color="#cf8d83"/><stop offset="1" stop-color="#ad6359"/></radialGradient>
<radialGradient id="{p}_pro" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#e9c6dc"/><stop offset="1" stop-color="#b9799f"/></radialGradient>
<radialGradient id="{p}_tas" cx="34%" cy="28%" r="78%"><stop offset="0" stop-color="#e2d3b4"/><stop offset=".45" stop-color="#9a7a50"/><stop offset="1" stop-color="#4a3319"/></radialGradient>
<linearGradient id="{p}_tas2" gradientUnits="userSpaceOnUse" x1="-24" y1="-40" x2="30" y2="36"><stop offset="0" stop-color="#e6d7b8"/><stop offset=".5" stop-color="#b89466"/><stop offset="1" stop-color="#7a5932"/></linearGradient>
<pattern id="{p}_tdok" patternUnits="userSpaceOnUse" width="7" height="7"><circle cx="1.6" cy="2" r=".7" fill="#4a3319" opacity=".55"/><circle cx="5" cy="5.4" r=".5" fill="#4a3319" opacity=".45"/><circle cx="5.6" cy="1.2" r=".35" fill="#fff" opacity=".5"/></pattern>
<pattern id="{p}_lif" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(-62)"><line x1="0" y1="3" x2="6" y2="3" stroke="#a6584f" stroke-width=".55" opacity=".5"/></pattern>
<pattern id="{p}_fib" patternUnits="userSpaceOnUse" width="14" height="9"><path d="M0,3 C3.5,0.6 7,5.4 10.5,3 S14,1.8 14,3 M0,7.5 C3.5,5.1 7,9.9 10.5,7.5" stroke="#857a69" stroke-width=".7" fill="none" opacity=".55"/></pattern>
<pattern id="{p}_kem" patternUnits="userSpaceOnUse" width="9" height="8"><ellipse cx="2.6" cy="2.4" rx="1.6" ry="1.1" fill="#d7c39b" opacity=".75"/><ellipse cx="6.8" cy="6" rx="1.3" ry="1.5" fill="#d7c39b" opacity=".7"/><ellipse cx="7.4" cy="1.6" rx=".8" ry=".7" fill="#d7c39b" opacity=".6"/></pattern>
<radialGradient id="{p}_ao" cx="38%" cy="32%" r="72%"><stop offset="0" stop-color="#f08a7e"/><stop offset=".6" stop-color="#d4483d"/><stop offset="1" stop-color="#9c2a22"/></radialGradient>
<radialGradient id="{p}_ven" cx="38%" cy="32%" r="72%"><stop offset="0" stop-color="#a9c0ea"/><stop offset=".6" stop-color="#6286c6"/><stop offset="1" stop-color="#3d5f99"/></radialGradient>
<radialGradient id="{p}_lnf" cx="36%" cy="30%" r="76%"><stop offset="0" stop-color="#e4ebf4"/><stop offset=".6" stop-color="#b7c6da"/><stop offset="1" stop-color="#8197b4"/></radialGradient>
<radialGradient id="{p}_psoas" cx="40%" cy="34%" r="74%"><stop offset="0" stop-color="#e7b2a8"/><stop offset="1" stop-color="#bf7a70"/></radialGradient>
<filter id="{p}_gol" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur in="SourceAlpha" stdDeviation="3.2"/><feOffset dx="2.5" dy="4" result="o"/>
<feComponentTransfer><feFuncA type="linear" slope=".26"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="{p}_gol2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur in="SourceAlpha" stdDeviation="1.4"/><feOffset dx="1" dy="1.6"/>
<feComponentTransfer><feFuncA type="linear" slope=".35"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>''')
    return p


# ------------------------------------------------------------------------------------------------ yardımcılar
def yuvarla(pts, kapali=True):
    """Noktalardan geçen düzgün eğri (Catmull-Rom → kübik Bezier)."""
    n = len(pts); d = f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    rng = range(n) if kapali else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (kapali or i > 0) else pts[0]; p1 = pts[i]; p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (kapali or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6); c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d + (' Z' if kapali else '')


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def egri(P, n=60):
    return [bez(*P, i / n) for i in range(n + 1)]


def yol_d(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)


def _dir(t): return math.cos(math.radians(t)), math.sin(math.radians(t))


# ------------------------------------------------------------------------------------------------ böbrek
BOB = 'M-4,-56 C-34,-56 -45,-28 -45,0 C-45,28 -34,56 -4,56 C14,56 25,44 23,29 C21,18 11,13 9,0 C11,-13 21,-18 23,-29 C25,-44 14,-56 -4,-56 Z'
S0 = (6, 0)                                         # sinüs merkezi (yerel)
ACI = (100, 124, 148, 170, 190, 212, 236, 260)      # piramit doğrultuları (derece; 100 alt kutup, 260 üst kutup)
MAJ = ((-6, -30), (-15, 0), (-6, 30))               # majör kaliksler: üst, orta, alt


def _sinir(t):
    """Sinüs merkezinden t açısıyla giden ışının böbrek dış sınırına uzaklığı (elips yaklaşımı)."""
    c, s = _dir(t)
    cx, rx, ry = -11, 34, 56
    a = (c / rx) ** 2 + (s / ry) ** 2; b = 2 * c * (S0[0] - cx) / rx ** 2; cc = ((S0[0] - cx) / rx) ** 2 - 1
    return (-b + math.sqrt(b * b - 4 * a * cc)) / (2 * a)


def _pel(pel): return (6, 10, 13, 16, 19)[pel], (8, 13, 17, 21, 25)[pel]


def cikis(cx, cy, k=1.0, ayna=False, pel=1):
    """Üreteropelvik bileşke (üreter çıkışı), çizmeden önce üreter yolunu kurmak için."""
    pw, ph = _pel(pel); ex, ey = 10 + pw * .5, 2 + ph * .8
    return (cx + (-ex if ayna else ex) * k, cy + ey * k)


def bobrek(F, cx, cy, k=1.0, ayna=False, pel=1, kal=0, maj=None, ince=0.0, damar=True, doku=True, sinus=True,
           ureter=None, uw=5.0, tas_dolgu=False, grup=None, gizli=False, gen=None):
    """Koronal kesitli böbrek: kapsül, korteks, medüller piramitler, sinüs yağı, segmental/arkuat damarlar, toplayıcı sistem.
    pel 0–4 pelvis genişliği · kal 0–4 minör kaliks genişlemesi (≥2: kalikslerde küntleşme) · maj 0–4 infundibulum ve majör kaliks
    ince 0–1 parankim incelmesi · ureter: global noktalar ya da f(ux, uy) → noktalar (toplayıcı sistemle tek gövde çizilir)
    tas_dolgu: toplayıcı sistemi dolduran (staghorn) taş · grup: dış <g> özniteliği (ör. 'data-etk="x"').
    Döndürür: ux, uy (bileşke), pel (pelvis merkezi), kal (8 minör kaliks merkezi; 0 alt kutup → 7 üst kutup), maj, pap."""
    if gen is not None: pel, kal = gen, 0
    if maj is None: maj = min(4, max(pel - 1, kal))
    p = tanim(F); sx = -k if ayna else k
    def G(q): return (cx + sx * q[0], cy + k * q[1])
    def L(q): return ((q[0] - cx) / sx, (q[1] - cy) / k)
    pw, ph = _pel(pel)
    PC = (10 + pel * .6, 2)
    E = (10 + pw * .5, 2 + ph * .8)
    gu = '' if not grup else ' ' + grup
    g = f'<g{gu} transform="translate({cx:g},{cy:g}) scale({sx:g},{k:g})"{" opacity=\"0\"" if gizli else ""}>'
    dmr = ''
    if damar:   # hilus damarları: önden bakışta ven en önde, sonra arter, pelvis en arkada (grubun sonunda çizilir)
        for d_, kn, gv, w in (('M15,-14 C26,-17 36,-19 48,-20', '#7d1f1a', '#cf4a3f', 5.4), ('M15,-6 C26,-6 36,-7 50,-7', '#27457a', '#5c80c4', 7.2)):
            dmr += (f'<path d="{d_}" stroke="{kn}" stroke-width="{w + 2.2:g}" fill="none" stroke-linecap="round"/>'
                    f'<path d="{d_}" stroke="{gv}" stroke-width="{w:g}" fill="none" stroke-linecap="round"/>'
                    f'<path d="{d_}" transform="translate(0,-1.3)" stroke="#fff" stroke-width="{w * .22:g}" fill="none" stroke-linecap="round" opacity=".45"/>')
    g += f'<path d="{BOB}" fill="url(#{p}_kor)" stroke="#7a3530" stroke-width="{1.8 / max(k, .6) * 1.2:.2f}" filter="url(#{p}_gol)"/>'
    g += f'<path d="{BOB}" transform="translate(1.2,1) scale(.955)" fill="none" stroke="#f5cfc7" stroke-width=".7" opacity=".55"/>'   # kapsül altı ince çizgi
    g += '<path d="M-30,-42 C-41,-24 -42,4 -37,24" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" opacity=".16"/>'
    # piramit geometrisi (kal: tek değer ya da 8 kaliks için liste; 0 alt kutup → 7 üst kutup)
    KL = list(kal) if isinstance(kal, (list, tuple)) else [kal] * len(ACI)
    km = max(KL)
    tb_f = .80 + .07 * ince
    PY = []
    for t, kk in zip(ACI, KL):
        d = _sinir(t); PY.append((t, d, d * tb_f, d * (.42 + .035 * kk + .2 * ince), kk))
    ta_o = sum(q[3] / q[1] for q in PY) / len(PY)        # ortalama papilla derinliği (sinüs ve damarlar için)
    if doku:   # korteks: glomerül noktacıkları
        rg = random.Random(7)
        for _ in range(int(120 * min(1, k / 2.2))):
            t = rg.uniform(96, 264); d = _sinir(t); r = rg.uniform(d * (tb_f + .03), d * .96); c, s_ = _dir(t)
            g += f'<circle cx="{S0[0] + r * c:.1f}" cy="{S0[1] + r * s_:.1f}" r=".42" fill="#8e3b34" opacity=".32"/>'
    if sinus:   # sinüs yağı
        sp = [(15, 21)]
        for t in range(100, 264, 8):
            d = _sinir(t); sp.append((S0[0] + d * ta_o * .84 * _dir(t)[0], S0[1] + d * ta_o * .84 * _dir(t)[1]))
        sp += [(15, -21), (12, -9), (11, 0), (12, 9)]
        g += f'<path d="{yuvarla(sp)}" fill="url(#{p}_yag)" stroke="#d3b67a" stroke-width=".5"/>'
    if doku:   # segmental ve interlobar arterler, arkuat ve interlobüler arterler
        art = ''
        for i in range(len(ACI) - 1):
            tm = (ACI[i] + ACI[i + 1]) / 2; d = _sinir(tm); c, s_ = _dir(tm)
            r0, r1 = d * ta_o * .9, d * tb_f
            art += f'<path d="M17,-8 Q{S0[0] + r0 * .6 * c:.1f},{S0[1] + r0 * .6 * s_ - 3:.1f} {S0[0] + r0 * c:.1f},{S0[1] + r0 * s_:.1f} L{S0[0] + r1 * c:.1f},{S0[1] + r1 * s_:.1f}"/>'
        for (t, d, tb, ta, kk) in PY:
            r = tb * 1.02; a0, a1 = math.radians(t - 13.5), math.radians(t + 13.5)
            art += f'<path d="M{S0[0] + r * math.cos(a0):.1f},{S0[1] + r * math.sin(a0):.1f} A{r:.1f},{r:.1f} 0 0 1 {S0[0] + r * math.cos(a1):.1f},{S0[1] + r * math.sin(a1):.1f}"/>'
            for dt in (-7, 0, 7):
                c, s_ = _dir(t + dt); r2 = r + (d - r) * .6
                art += f'<line x1="{S0[0] + r * c:.1f}" y1="{S0[1] + r * s_:.1f}" x2="{S0[0] + r2 * c:.1f}" y2="{S0[1] + r2 * s_:.1f}" stroke-width=".3"/>'
        g += f'<g stroke="#b3241d" stroke-width=".6" fill="none" opacity=".55" stroke-linecap="round">{art}</g>'
    # piramitler (yuvarlak papilla ucu; genişlemiş kalikste küt)
    pir = ''; PAP = []
    for (t, d, tb, ta, kk) in PY:
        w = 10.5; w2 = 3.6 + 2.5 * ince + (.6 * kk if kk >= 3 else 0)
        b1 = (S0[0] + tb * _dir(t - w)[0], S0[1] + tb * _dir(t - w)[1]); b2 = (S0[0] + tb * _dir(t + w)[0], S0[1] + tb * _dir(t + w)[1])
        n1 = (S0[0] + (ta + 2.4) * _dir(t - w2)[0], S0[1] + (ta + 2.4) * _dir(t - w2)[1]); n2 = (S0[0] + (ta + 2.4) * _dir(t + w2)[0], S0[1] + (ta + 2.4) * _dir(t + w2)[1])
        ap = (S0[0] + ta * _dir(t)[0], S0[1] + ta * _dir(t)[1]); PAP.append(ap)
        qb = (S0[0] + tb * 1.045 * _dir(t)[0], S0[1] + tb * 1.045 * _dir(t)[1])
        dd = 1.4 if kk < 3 else -1.2
        apc = (S0[0] + (ta - dd) * _dir(t)[0], S0[1] + (ta - dd) * _dir(t)[1])
        pir += (f'<path d="M{b1[0]:.1f},{b1[1]:.1f} Q{qb[0]:.1f},{qb[1]:.1f} {b2[0]:.1f},{b2[1]:.1f} L{n2[0]:.1f},{n2[1]:.1f} Q{apc[0]:.1f},{apc[1]:.1f} {n1[0]:.1f},{n1[1]:.1f} Z" '
                f'fill="url(#{p}_pir)" stroke="#7c2c26" stroke-width=".55"/>')
        for f_ in (.18, .38, .62, .82):
            q = (b1[0] + (b2[0] - b1[0]) * f_, b1[1] + (b2[1] - b1[1]) * f_)
            pir += f'<line x1="{q[0]:.1f}" y1="{q[1]:.1f}" x2="{ap[0] + (q[0] - ap[0]) * .12:.1f}" y2="{ap[1] + (q[1] - ap[1]) * .12:.1f}" stroke="#eaaaa0" stroke-width=".38" opacity=".55"/>'
    # toplayıcı sistem: tek gövde (dış çizgi + dolgu). Genişlemiş kaliksler (≥2) piramitlerin üstünde çizilir.
    w_maj = (3.0, 3.6, 5.6, 7.4, 9.0)[maj]
    T, TG = [], []   # ('c', [noktalar], w) | ('e', cx, cy, rx, ry, açı); TG: piramit üstü
    KAL, RC = [], []
    for (t, d, tb, ta, kk), ap in zip(PY, PAP):
        u = _dir(t); rc = (3.5, 3.8, 5.0, 6.6, 8.0 + 1.6 * ince)[kk]; wi = (2.4, 2.6, 3.8, 5.0, 6.2)[kk]
        of = .12 if kk < 2 else -.05
        c = (ap[0] + u[0] * rc * of, ap[1] + u[1] * rc * of); KAL.append(c); RC.append(rc)
        m = min(MAJ, key=lambda q: (q[0] - ap[0]) ** 2 + (q[1] - ap[1]) ** 2)
        x_ = [('c', [c, m], wi), ('e', c[0], c[1], rc * .95, rc * 1.22, t)]
        T += x_
        if kk >= 2: TG += x_
    TM = [('c', [m, PC], w_maj) for m in MAJ] + [('e', PC[0], PC[1], pw, ph, 0), ('c', [PC, E], min(pw, ph) * .55)]
    T += TM
    UP = None; TU = []
    if ureter is not None:
        up = ureter(*G(E)) if callable(ureter) else ureter
        UP = [L(q) for q in up]; TU = [('c', [E] + UP[1:], uw / k), ('c', [PC, E, UP[min(3, len(UP) - 1)]], max(uw / k, 2.6))]
        if not tas_dolgu: T += TU

    def ciz(o, renk, ek=0.0, sk=1.0, T=T):
        s_ = ''
        for x in T:
            if x[0] == 'c':
                s_ += f'<path d="{yol_d(x[1])}" stroke-width="{max(x[2] * sk + ek, .5):.2f}" fill="none"/>'
            else:
                _, ex_, ey_, rx, ry, a_ = x
                s_ += f'<ellipse cx="{ex_:.1f}" cy="{ey_:.1f}" rx="{max(rx * sk + ek / 2, .4):.2f}" ry="{max(ry * sk + ek / 2, .4):.2f}" transform="rotate({a_:.0f} {ex_:.1f} {ey_:.1f})"/>'
        return f'<g stroke="{renk}" fill="{renk}" stroke-linecap="round" stroke-linejoin="round"{o}>{s_}</g>'
    if tas_dolgu:
        ts = (ciz('', IDR_C, 1.6, T=TU) + ciz('', f'url(#{p}_idr)', T=TU) if UP else '') + \
             ciz('', '#3b2810', 1.7) + ciz('', f'url(#{p}_tas2)') + ciz(' opacity=".9"', f'url(#{p}_tdok)', -.4)
        ust = ''
    else:
        ts = ciz('', IDR_C, 1.6) + ciz('', f'url(#{p}_idr)')
        ust = (ciz('', IDR_C, 1.6, T=TG) + ciz('', f'url(#{p}_idr)', T=TG + TM + TU)) if TG and km < 3 else ''
    par = f'<ellipse cx="{PC[0] - pw * .3:.1f}" cy="{PC[1] - ph * .38:.1f}" rx="{pw * .32:.1f}" ry="{ph * .2:.1f}" fill="#fff" opacity="{.28 if tas_dolgu else .42}" transform="rotate(-20 {PC[0] - pw * .3:.1f} {PC[1] - ph * .38:.1f})"/>'
    if not tas_dolgu:
        for c, rc, kk in zip(KAL, RC, KL):
            if kk >= 2: par += f'<circle cx="{c[0] - rc * .3:.1f}" cy="{c[1] - rc * .34:.1f}" r="{rc * .26:.1f}" fill="#fff" opacity=".35"/>'
    if km >= 3 and min(KL) >= 2: g += pir + ts + par        # hepsi genişlemiş: tümü piramitlerin üstünde
    else: g += ts + pir + ust + par
    g += dmr + '</g>'
    F.a(g)
    R = dict(ux=G(E)[0], uy=G(E)[1], pel=G(PC), kal=[G(c) for c in KAL], maj=[G(m) for m in MAJ], pap=[G(a) for a in PAP], k=k,
             ureter=[G(q) for q in UP] if UP else None)
    return R


# ------------------------------------------------------------------------------------------------ üreter, mesane, prostat
def ureter(F, pts, w=5, grup=None):
    """pts: üreter boyunca noktalar. Koyu kenar, gradyan dolgu, ince parlama."""
    d = yol_d(pts); s = ''
    s += f'<path d="{d}" stroke="{IDR_C}" stroke-width="{w + 3:g}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{d}" stroke="{IDR_K}" stroke-width="{w + .6:g}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{d}" stroke="{IDR_A}" stroke-width="{w * .55:g}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{d}" transform="translate(-.9,-.6)" stroke="#fffbe8" stroke-width="{w * .18:g}" fill="none" stroke-linecap="round" opacity=".85"/>'
    F.a(f'<g {grup}>{s}</g>' if grup else s)


def _mes_d(cx, cy, rx, ry):
    return (f'M{cx - rx:.1f},{cy - ry * .1:.1f} C{cx - rx:.1f},{cy - ry * 1.05:.1f} {cx + rx:.1f},{cy - ry * 1.05:.1f} {cx + rx:.1f},{cy - ry * .1:.1f} '
            f'C{cx + rx:.1f},{cy + ry * .62:.1f} {cx + rx * .3:.1f},{cy + ry:.1f} {cx:.1f},{cy + ry:.1f} C{cx - rx * .3:.1f},{cy + ry:.1f} {cx - rx:.1f},{cy + ry * .62:.1f} {cx - rx:.1f},{cy - ry * .1:.1f} Z')


def _mes_pts(cx, cy, rx, ry, n=40):
    """_mes_d ile aynı kontur, nokta listesi."""
    S = [((cx - rx, cy - ry * .1), (cx - rx, cy - ry * 1.05), (cx + rx, cy - ry * 1.05), (cx + rx, cy - ry * .1)),
         ((cx + rx, cy - ry * .1), (cx + rx, cy + ry * .62), (cx + rx * .3, cy + ry), (cx, cy + ry)),
         ((cx, cy + ry), (cx - rx * .3, cy + ry), (cx - rx, cy + ry * .62), (cx - rx, cy - ry * .1))]
    return [bez(*q, i / n) for q in S for i in range(n)]


def _isin(pts, cx, cy, aci):
    """Konturun (cx, cy) merkezinden 'aci' doğrultusundaki ışınla kesiştiği nokta (yaklaşık)."""
    return min(pts, key=lambda q: abs(math.atan2(q[1] - cy, q[0] - cx) - math.radians(aci)) if q != (cx, cy) else 9)


def giris(cx, cy, rx, ry, taraf=-1, duvar=7):
    """Üreterin mesane duvarına girdiği nokta (dış yüz, alt-yan taban). taraf: -1 sol (şekilde), +1 sağ."""
    return _isin(_mes_pts(cx, cy, rx, ry), cx, cy, 90 - taraf * 58)


def mesane(F, cx, cy, rx=46, ry=34, taraflar=(-1,), duvar=7, uretra=16, prostat=0, trabekul=False, grup=None, gizli=False, idrar=True):
    """Kesitli mesane: kas duvarı, mukoza, idrar, trigon, intramural üreter tüneli ve ağızları, mesane boynu, üretra; isteğe bağlı prostat.
    taraflar: üreter giren taraflar (-1 sol, +1 sağ). prostat: 0 yok · 1 normal · 2 büyümüş (BPH). Döndürür: dict(giris, agiz, tunel, boyun)."""
    p = tanim(F); o = []
    a = o.append
    if prostat:
        pr = (16, 30)[prostat - 1]; pry = (11, 21)[prostat - 1]; py_ = cy + ry + pry * (.5 if prostat == 1 else .3)
    # üretra
    a(f'<path d="M{cx - 5:.1f},{cy + ry - 3:.1f} L{cx - 4:.1f},{cy + ry + uretra:.1f} M{cx + 5:.1f},{cy + ry - 3:.1f} L{cx + 4:.1f},{cy + ry + uretra:.1f}" stroke="#9a5a52" stroke-width="3" fill="none" stroke-linecap="round"/>')
    a(f'<rect x="{cx - 4:.1f}" y="{cy + ry - 4:.1f}" width="8" height="{uretra + 3:.1f}" rx="3" fill="{IDR_K}"/>')
    if prostat:
        a(f'<ellipse cx="{cx:.1f}" cy="{py_:.1f}" rx="{pr}" ry="{pry}" fill="url(#{p}_pro)" stroke="#86486c" stroke-width="1.4" filter="url(#{p}_gol2)"/>')
        for i in range(6):
            aa = math.radians(195 + i * 30); a(f'<path d="M{cx:.1f},{py_:.1f} L{cx + pr * .82 * math.cos(aa):.1f},{py_ + pry * .82 * math.sin(aa):.1f}" stroke="#a3628a" stroke-width=".6" opacity=".5"/>')
            aa = math.radians(15 + i * 30); a(f'<path d="M{cx:.1f},{py_:.1f} L{cx + pr * .82 * math.cos(aa):.1f},{py_ + pry * .82 * math.sin(aa):.1f}" stroke="#a3628a" stroke-width=".6" opacity=".5"/>')
        a(f'<path d="M{cx:.1f},{py_ - pry:.1f} L{cx:.1f},{py_ + pry + 4:.1f}" stroke="#8a5a1a" stroke-width="{(3.8, 2.6)[prostat - 1]}" stroke-linecap="round"/>')
        a(f'<path d="M{cx:.1f},{py_ - pry:.1f} L{cx:.1f},{py_ + pry + 4:.1f}" stroke="{IDR_K}" stroke-width="{(2.4, 1.1)[prostat - 1]}" stroke-linecap="round"/>')
    d = _mes_d(cx, cy, rx, ry)
    a(f'<path d="{d}" fill="url(#{p}_kas)" stroke="#8e4a44" stroke-width="1.6" filter="url(#{p}_gol)"/>')
    a(f'<path d="{d}" fill="url(#{p}_lif)" opacity=".7"/>')
    irx, iry = rx - duvar, ry - duvar; icy = cy + duvar * .12
    ic = _mes_d(cx, icy, irx, iry)
    if trabekul:   # kalın, trabeküle duvar: düzensiz mukoza, kas demetleri, küçük sellüller
        rg = random.Random(5); P0 = _mes_pts(cx, icy, irx, iry, 10); pts = []
        for i, q in enumerate(P0):
            f_ = 1 + rg.uniform(-.035, .03); pts.append((cx + (q[0] - cx) * f_, icy + (q[1] - icy) * f_))
        ic = yuvarla(pts)
        for i in range(0, len(P0), 2):
            q = P0[i]; v = (q[0] - cx, q[1] - icy); L_ = math.hypot(*v) or 1
            a(f'<path d="M{q[0]:.1f},{q[1]:.1f} L{q[0] + v[0] / L_ * duvar * .55:.1f},{q[1] + v[1] / L_ * duvar * .55:.1f}" stroke="#9c544b" stroke-width="2.2" opacity=".45" stroke-linecap="round"/>')
        for aa in (210, 330):
            q = _isin(_mes_pts(cx, icy, irx, iry), cx, icy, aa); a(f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="{duvar * .42:.1f}" fill="#f3c9c1" stroke="#b97069" stroke-width=".9"/>')
    a(f'<path d="{ic}" fill="#f3c9c1" stroke="#b97069" stroke-width="1"/>')       # mukoza
    lum = ic if trabekul else _mes_d(cx, icy + .4, irx - 1.6, iry - 1.6)
    a(f'<path d="{lum}" fill="{"url(#" + p + "_mes)" if idrar else "#f6dcd6"}" stroke="{IDR_C}" stroke-width=".9"/>')
    a(f'<path d="M{cx - irx * .58:.1f},{icy - iry * .38:.1f} Q{cx - irx * .2:.1f},{icy - iry * .7:.1f} {cx + irx * .24:.1f},{icy - iry * .64:.1f}" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".42"/>')
    boyun = (cx, cy + ry - duvar * .55)
    IP = _mes_pts(cx, icy, irx - 1.6, iry - 1.6)
    ag = {t: _isin(IP, cx, icy, 90 - t * 50) for t in (-1, 1)}
    ag = {t: (q[0] - t * 2.5, q[1] - 2.5) for t, q in ag.items()}
    a(f'<path d="M{ag[-1][0]:.1f},{ag[-1][1]:.1f} Q{cx:.1f},{ag[-1][1] - 4:.1f} {ag[1][0]:.1f},{ag[1][1]:.1f} L{boyun[0]:.1f},{boyun[1] - 2:.1f} Z" fill="#e9b34e" opacity=".45"/>')
    R = dict(giris={}, agiz={}, tunel={}, boyun=boyun)
    for tf in taraflar:   # intramural tünel: dış duvardan içe-aşağı, ağıza
        E = giris(cx, cy, rx, ry, tf); O = ag[tf]
        tn = [bez(E, (E[0] - tf * duvar * .2, E[1] + duvar * .5), (O[0] + tf * duvar * .5, O[1] + 1), O, i / 12) for i in range(13)]
        dd = yol_d(tn)
        a(f'<path d="{dd}" stroke="{IDR_C}" stroke-width="5" fill="none" stroke-linecap="round"/><path d="{dd}" stroke="{IDR_K}" stroke-width="3.2" fill="none" stroke-linecap="round"/>')
        a(f'<ellipse cx="{O[0]:.1f}" cy="{O[1]:.1f}" rx="3.4" ry="2.2" fill="#7a4e0c"/>')
        R['giris'][tf] = E; R['agiz'][tf] = O; R['tunel'][tf] = tn
    s = ''.join(o)
    if grup or gizli: s = f'<g {grup or ""}{" opacity=\"0\"" if gizli else ""}>{s}</g>'
    F.a(s)
    return R


# ------------------------------------------------------------------------------------------------ damar, taş
def damar(F, pts, tur='a', w=7, d=None):
    """Arter (a) ya da ven (v): koyu kenar, gövde, parlama. pts ya da hazır yol (d)."""
    d = d or yolu(pts)
    kenar, govde, par = (('#7d1f1a', '#cf4a3f', '#f4aaa0') if tur == 'a' else ('#27457a', '#5c80c4', '#c3d4f2'))
    F.yol(d, kenar, w + 2.6); F.yol(d, govde, w)
    F.a(f'<path d="{d}" transform="translate(-.6,-1.3)" stroke="{par}" stroke-width="{w * .24:g}" fill="none" stroke-linecap="round" opacity=".8"/>')


def yolu(pts):
    return yuvarla(pts, False) if len(pts) > 2 else yol_d(pts)


def tas(F, x, y, r, tohum=1, grup=None):
    """Dokulu, gölgeli taş. Sağ kenar noktasını döndürür."""
    p = tanim(F); rg = random.Random(tohum); n = 10; pts = []
    for i in range(n):
        a = 2 * math.pi * i / n + rg.uniform(-.15, .15); rr = r * rg.uniform(.78, 1.05)
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    d = yuvarla(pts)
    s = f'<path d="{d}" fill="url(#{p}_tas)" stroke="#2e1f0d" stroke-width="1.1" stroke-linejoin="round" filter="url(#{p}_gol2)"/>'
    s += f'<path d="{d}" fill="url(#{p}_tdok)" opacity=".8"/>'
    for i in range(4):
        a = rg.uniform(0, 6.28); q = rg.uniform(.2, .55) * r
        s += f'<ellipse cx="{x + q * math.cos(a):.1f}" cy="{y + q * math.sin(a):.1f}" rx="{r * .1:.1f}" ry="{r * .08:.1f}" fill="#2a1c0c" opacity=".45"/>'
    s += f'<ellipse cx="{x - r * .3:.1f}" cy="{y - r * .36:.1f}" rx="{r * .26:.1f}" ry="{r * .15:.1f}" fill="#fff" opacity=".75" transform="rotate(-25 {x - r * .3:.1f} {y - r * .36:.1f})"/>'
    F.a(f'<g {grup}>{s}</g>' if grup else s)
    return (x + r * .95, y)


def rozet(F, x, y, n, c=BRANDD, r=9):
    F.el(x, y, r, r, c, '#fff', 1.8); F.t(x, y + 4.2, str(n), 11.5, 800, '#fff', 'middle')


def cagri(F, p, tx, ty, lines, fs=12, c=INK, renk='#56677a', grup=None):
    """İnce çağrı çizgisi: noktada beyaz halkalı uç, metnin sol kenarına yatay bağlanır."""
    ls = lines if isinstance(lines, list) else [lines]
    qx = tx - 6; qy = ty - fs * .35; mx = qx - 18
    if grup: F.a(f'<g {grup}>')
    F.a(f'<path d="M{p[0]:.1f},{p[1]:.1f} L{mx:.1f},{qy:.1f} L{qx:.1f},{qy:.1f}" stroke="{renk}" stroke-width="1.1" fill="none"/>')
    F.el(p[0], p[1], 3.2, 3.2, '#fff', renk, 1.3)
    F.t(tx, ty, ls[0], fs, 800, c)
    for i, l in enumerate(ls[1:]): F.t(tx, ty + (i + 1) * (fs + 3), l, fs - .6, None, INK2)
    if grup: F.a('</g>')


# ------------------------------------------------------------------------------------------------ kateter ve stent
def pigtail(cx, cy, r, a0=90, tur=1.0, yon=1):
    """a0 açısından başlayan, tur kadar dönen kıvrık uç (yol parçası, M ile başlar)."""
    n = 36; pts = []
    for i in range(n + 1):
        a = math.radians(a0 + yon * 360 * tur * i / n); rr = r * (1 - .18 * i / n)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def kateter(F, pts, w=3.4, renk=KAT, delik=0, grup=None, d=None):
    """Radyoopak kateter: koyu kenar, açık gövde, orta çizgi; delik: yan delik sayısı."""
    d = d or yolu(pts)
    s = (f'<path d="{d}" stroke="#0d2f52" stroke-width="{w + 1.8:g}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{d}" stroke="{renk}" stroke-width="{w:g}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{d}" stroke="#cfe3f6" stroke-width="{w * .3:g}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>')
    if delik and pts:
        for i in range(1, delik + 1):
            q = pts[int(len(pts) * i / (delik + 1))]; s += f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="{w * .28:.1f}" fill="#0d2f52"/>'
    F.a(f'<g {grup}>{s}</g>' if grup else s)


# ------------------------------------------------------------------------------------------------ aksiyel kesit ögeleri (ön yukarıda, hastanın sağı solda)
def vertebra(F, cx, cy, s=1.0):
    """Lomber vertebra: gövde (kortikal kabuk + trabeküler kemik), pedikül, lamina, transvers ve spinöz çıkıntı, spinal kanal."""
    p = tanim(F)
    def P(x, y): return (cx + x * s, cy + y * s)
    gov = [P(-46, -4), P(-40, -28), P(-20, -38), P(0, -40), P(20, -38), P(40, -28), P(46, -4), P(38, 22), P(16, 30), P(0, 26), P(-16, 30), P(-38, 22)]
    arka = [P(-14, 30), P(-24, 40), P(-62, 46), P(-66, 54), P(-30, 56), P(-16, 70), P(-6, 100), P(6, 100), P(16, 70), P(30, 56), P(66, 54), P(62, 46), P(24, 40), P(14, 30)]
    F.a(f'<path d="{yuvarla(arka)}" fill="#efe3c8" stroke="#a88f60" stroke-width="1.6"/>')
    F.a(f'<path d="{yuvarla(arka)}" fill="url(#{p}_kem)"/>')
    kan = [P(-14, 36), P(0, 32), P(14, 36), P(18, 50), P(0, 62), P(-18, 50)]
    F.a(f'<path d="{yuvarla(kan)}" fill="#f8f3ea" stroke="#a88f60" stroke-width="1.3"/>')
    F.el(*P(0, 47), 7.5 * s, 7 * s, '#f2e1a8', '#c9a95e', .8)     # dural kese
    F.a(f'<path d="{yuvarla(gov)}" fill="#f1e6cd" stroke="#9c8250" stroke-width="2.4"/>')
    F.a(f'<path d="{yuvarla(gov)}" fill="url(#{p}_kem)"/>')
    F.a(f'<path d="{yuvarla([P(-36, -6), P(-30, -24), P(0, -32), P(30, -24), P(36, -6), P(28, 14), P(0, 18), P(-28, 14)])}" fill="none" stroke="#fff" stroke-width="1.2" opacity=".45"/>')
    return dict(on=P(0, -40), gov=gov)


def kas(F, pts, ad='psoas'):
    """Kas kesiti (psoas, paraspinal): gradyan, lif dokusu, fasya."""
    p = tanim(F); d = yuvarla(pts)
    F.a(f'<path d="{d}" fill="url(#{p}_psoas)" stroke="#9b544b" stroke-width="1.4"/>')
    F.a(f'<path d="{d}" fill="url(#{p}_lif)" opacity=".9"/>')
    return d


def arter_kesit(F, x, y, r, kalsifik=True):
    p = tanim(F)
    F.el(x, y, r + 2.6, r + 2.6, '#f3d6cf', '#8e2b26', 1.6)
    F.el(x, y, r, r, f'url(#{p}_ao)', '#9c2a22', 1)
    F.el(x - r * .32, y - r * .36, r * .3, r * .18, '#fff', None, op=.55)
    if kalsifik:
        F.a(f'<path d="M{x + (r + 1.4) * math.cos(math.radians(130)):.1f},{y + (r + 1.4) * math.sin(math.radians(130)):.1f} A{r + 1.4:.1f},{r + 1.4:.1f} 0 0 1 {x + (r + 1.4) * math.cos(math.radians(160)):.1f},{y + (r + 1.4) * math.sin(math.radians(160)):.1f}" stroke="#fffdf4" stroke-width="2.4" fill="none" stroke-linecap="round"/>')


def ven_kesit(F, x, y, rx, ry):
    p = tanim(F)
    F.el(x, y, rx, ry, f'url(#{p}_ven)', '#2f4f86', 1.4)
    F.el(x - rx * .3, y - ry * .35, rx * .3, ry * .18, '#fff', None, op=.5)


def ureter_kesit(F, x, y, r=6, gen=1.0):
    F.el(x, y, r + 1.6, r + 1.6, '#efd9a0', IDR_C, 1.3)
    F.el(x, y, r * .55 * gen, r * .55 * gen, IDR_K, None)
    F.el(x - r * .2, y - r * .25, r * .18, r * .12, '#fff', None, op=.7)


def lenf(F, x, y, rx, ry, a=0, tohum=1):
    """Büyümüş lenf nodu: hafif lobüllü, gölgeli."""
    p = tanim(F); rg = random.Random(tohum); pts = []
    for i in range(12):
        t = 2 * math.pi * i / 12; rr = rg.uniform(.93, 1.04)
        u, v = rx * rr * math.cos(t), ry * rr * math.sin(t); ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        pts.append((x + u * ca - v * sa, y + u * sa + v * ca))
    F.a(f'<path d="{yuvarla(pts)}" fill="url(#{p}_lnf)" stroke="#5f7796" stroke-width="1.3" filter="url(#{p}_gol2)"/>')


def fibroz(F, pts):
    """Retroperitoneal fibroz dokusu: gri-bej, kolajen dalgaları, düzensiz sınır."""
    p = tanim(F); d = yuvarla(pts)
    F.a(f'<path d="{d}" fill="#d9d0c0" stroke="#8c816d" stroke-width="1.5" opacity=".96"/>')
    F.a(f'<path d="{d}" fill="url(#{p}_fib)"/>')
    return d
