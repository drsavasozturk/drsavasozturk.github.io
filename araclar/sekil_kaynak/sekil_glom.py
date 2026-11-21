#!/usr/bin/env python3
"""Glomerül çizim kiti (Kasım 2026, kullanıcının verdiği örnek tarzında; özgün çizim).

Üç bileşen:
  Lobul      : üç kapiller ilmek + ortada mezangiyal hücre; pencereli endotel, GBM, podosit ayaksı çıkıntıları ve
               podosit gövdeleri (ışık-elektron mikroskobu arası şematik görünüm). Lezyon seçenekleriyle.
  Glomerul   : tüm glomerül: Bowman kapsülü, paryetal epitel, vasküler kutup (afferent/efferent arteriyol),
               üriner kutup (proksimal tübül başlangıcı), kapiller yumak. Hilal, skleroz, çökme vb. seçenekleri.
  bariyer    : filtrasyon bariyerinin yakın görünümü (lümen → glikokaliks → pencereli endotel → GBM üç katman →
               ayaksı çıkıntılar ve yarık diyaframı → Bowman boşluğu).
"""
import math, random
from sekil_kit import *

POD = '#f0dcae'; POD_K = '#a98447'; POD_N = '#ecbcc6'; POD_NK = '#a35c72'
GBM = '#cfe3eb'; GBM_K = '#5b8b9b'; GBM_D = '#7fa9b7'
END_K = '#cf3f3f'; END_C = '#f3a6a6'; END_N = '#8f1f4d'
MESC = '#bba3e4'; MESC_K = '#5b4594'; MESM = '#ece5f8'; MESN = '#3a2777'
LUM = '#fffafa'; RBC = '#e0605b'; RBC_I = '#f19a95'
BOW = '#fbf6ea'; DEP = '#23303d'
LEUK = '#dcefd6'; LEUK_K = '#5f8f57'; LEUK_N = '#2e5b35'
FIB = '#f08a4b'; FIB_K = '#c25a1f'
SKL = '#f3d2d9'; SKL_K = '#c48f9b'; HYAL = '#f4a3b8'
TUB = '#f3d2b4'; TUB_K = '#b98a5f'; TUB_N = '#9b6a8a'


def P(c, r, a):
    return c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a))


def _pd(pts, kapali=True):
    return 'M' + ' L'.join('%.1f,%.1f' % p for p in pts) + (' Z' if kapali else '')


def elips(F, x, y, rx, ry, aci=0, fill='#fff', st=None, sw=1.2, op=None):
    at = f' stroke="{st}" stroke-width="{sw:g}"' if st else ''
    if op: at += f' opacity="{op}"'
    F.a(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" transform="rotate({aci:.1f} {x:.1f} {y:.1f})" fill="{fill}"{at}/>')


def eritrosit(F, x, y, r, aci=0):
    elips(F, x, y, r, r * .86, aci, RBC, '#b8433f', 1)
    elips(F, x, y, r * .46, r * .36, aci, RBC_I)


def notrofil(F, x, y, r):
    F.el(x, y, r, r, LEUK, LEUK_K, 1.3)
    for (dx, dy, q) in ((-.38, -.18, .3), (.06, -.4, .27), (.38, .06, .29), (-.04, .34, .27)):
        F.el(x + dx * r, y + dy * r, q * r, q * r * .82, LEUK_N)


def monosit(F, x, y, r):
    F.el(x, y, r, r, '#e6e0f0', '#7b6c99', 1.3)
    elips(F, x + r * .1, y, r * .55, r * .42, 20, '#4b3f6b')


def yumusat(pts, k=3, n=1):
    for _ in range(n):
        m = len(pts); q = []
        for i in range(m):
            sx = sy = 0
            for j in range(-k, k + 1):
                sx += pts[(i + j) % m][0]; sy += pts[(i + j) % m][1]
            q.append((sx / (2 * k + 1), sy / (2 * k + 1)))
        pts = q
    return pts


def normaller(pts):
    m = len(pts); ns = []
    for i in range(m):
        tx = pts[(i + 1) % m][0] - pts[i - 1][0]; ty = pts[(i + 1) % m][1] - pts[i - 1][1]
        L = math.hypot(tx, ty) or 1
        ns.append((ty / L, -tx / L))
    return ns


def kaydir(pts, ns, d):
    return [(p[0] + n[0] * d, p[1] + n[1] * d) for p, n in zip(pts, ns)]


def yay_uzunluk(pts):
    L = [0.0]
    for i in range(1, len(pts)): L.append(L[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    return L


def etk(F, p, tx, ty, lines, sag=True, c=INK, fs=12, kalin=True, lc=INK2):
    """Etiket: p noktasından metne çizgi. Çizgi metnin en yakın kenarına bağlanır, yazının içinden geçmez."""
    ls = lines if isinstance(lines, list) else [lines]
    w_ = max(gen(l, fs, i == 0 and kalin) for i, l in enumerate(ls)); lh = fs + 2.5
    x0, x1 = (tx, tx + w_) if sag else (tx - w_, tx)
    ust, alt = ty - fs * .82, ty + (len(ls) - 1) * lh + fs * .3
    if p[0] < x0 - 4: q = (x0 - 5, ty - 4)
    elif p[0] > x1 + 4: q = (x1 + 5, ty - 4)
    elif p[1] < ust: q = (min(max(p[0], x0 + 6), x1 - 6), ust - 3)
    elif p[1] > alt: q = (min(max(p[0], x0 + 6), x1 - 6), alt + 3)
    else:
        q = (tx + (-5 if sag else 5), ty - 4); UYARI.append('%s: nokta yazının üstünde: %s' % (getattr(F, 'fid', '?'), ls[0]))
    F.el(p[0], p[1], 2.3, 2.3, lc)
    F.ln(p[0], p[1], q[0], q[1], lc, 1.15)
    for i, l in enumerate(ls):
        F.t(tx, ty + i * lh, l, fs, 800 if (kalin and i == 0) else None, c if i == 0 else INK2, 'start' if sag else 'end')


# =================================================================================================== LOBÜL
class Lobul:
    """Üç kapiller ilmek ve ortada mezangiyum. aci0: ilk kapillerin yönü (derece; -90 = yukarı)."""

    def __init__(s, F, cx, cy, k=1.0, aci0=-90, **o):
        s.F, s.cx, s.cy, s.k, s.o = F, cx, cy, k, o
        s.r = o.get('lumen', 44) * k; s.d = 62 * k * o.get('acik', 1.0)
        s.g = o.get('gbm', 7.5) * k
        s.fh = 7 * k; s.bw = 10 * k
        s.mm = o.get('mez_m', 41) * k; s.mc = o.get('mez_c', 17) * k
        s.ac = [aci0, aci0 + 120, aci0 + 240]
        s.cap = [P((cx, cy), s.d, a) for a in s.ac]
        s.centik = [a + 60 for a in s.ac]
        s.dep = {}
        s.ciz()

    # ---- geometri
    def _rho(s, f, R, mm):
        ux, uy = math.cos(f), math.sin(f)
        w = ((1 + math.cos(3 * (f - math.radians(s.ac[0] + 60)))) / 2) ** 2
        best = s.mc + (mm - s.mc) * w
        for (px, py) in s.cap:
            qx, qy = px - s.cx, py - s.cy
            b = qx * ux + qy * uy; disc = R * R - (qx * qx + qy * qy) + b * b
            if disc >= 0: best = max(best, b + math.sqrt(disc))
        return best

    def kontur(s, R, mm, n=360, yk=3, yn=2):
        pts = []
        for i in range(n):
            f = 2 * math.pi * i / n; rr = s._rho(f, R, mm)
            pts.append((s.cx + rr * math.cos(f), s.cy + rr * math.sin(f)))
        return yumusat(pts, yk, yn)

    def _idx(s, a):
        return int(round((a % 360) / 360 * 360)) % 360

    # ---- etiket noktaları
    def p_gbm(s, a): return s.mid[s._idx(a)]
    def p_fp(s, a):
        i = s._idx(a); n = s.ns[i]; p = s.mid[i]; d = s.g / 2 + s.fh * .5
        return (p[0] + n[0] * d, p[1] + n[1] * d)
    def p_pod(s, i=0): return s.podc[i]
    def p_podc(s, a):
        i = s._idx(a); return s.dis[i]
    def p_endo(s, i=0): return s.endc[i]
    def p_lumen(s, i=0): return s.cap[i]
    def p_mez(s): return (s.cx, s.cy)
    def yakin(s, tur, x, y):
        return min(s.dep[tur], key=lambda q: math.hypot(q[0] - x, q[1] - y))
    def p_mezm(s, j=0):
        a = s.centik[j]; return P((s.cx, s.cy), s.mm * .72, a)
    def p_ic(s, i, a, ek=0):
        """i. kapillerin merkezine göre a açısında, GBM iç yüzünde (ek: içe doğru px)."""
        return P(s.cap[i], s.r + 1 - ek, a)

    # ---- çizim
    def ciz(s):
        F, o, k = s.F, s.o, s.k
        R_in = s.r + 1
        s.mid = s.kontur(R_in + s.g / 2, s.mm + s.g / 2)
        s.ns = normaller(s.mid)
        ic_ = kaydir(s.mid, s.ns, -s.g / 2)
        s.dis = s.kontur(R_in + s.g + s.fh + s.bw, s.mm + s.g + s.fh + s.bw * .4, yk=5, yn=3)
        yar = s.kontur(R_in + s.g + s.fh, s.mm + s.g + s.fh * .6, yk=4, yn=2)
        efase = o.get('efase')
        def efase_mi(a):
            if efase is True: return True
            if not efase: return False
            for (a0, a1) in efase:
                if (a - a0) % 360 <= (a1 - a0) % 360: return True
            return False
        # podosit gövdeleri (önce gövdenin dış çizgisi, sonra bant ile birleşir)
        pod_ac = o.get('podosit', s.centik)
        s.podc = []
        for a in pod_ac:
            i = s._idx(a); p = s.dis[i]; n = s.ns[i]
            # dış konturun radyal yönü
            ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
            c = (p[0] + ux * 9 * k, p[1] + uy * 9 * k); s.podc.append(c)
        F.yol(_pd(s.dis), POD_K, 2.2, POD)
        for c, a in zip(s.podc, pod_ac):
            elips(F, c[0], c[1], 27 * k, 17 * k, a + 90, POD, POD_K, 1.8)
        F.yol(_pd(s.dis), None, 0, POD)
        for c, a in zip(s.podc, pod_ac):
            elips(F, c[0], c[1], 10.5 * k, 7 * k, a + 90, POD_N, POD_NK, 1.2)
        if o.get('vakuol'):
            for c, a in zip(s.podc, pod_ac):
                for (dx, dy) in ((-15, -3), (14, 2), (-6, 8)):
                    F.el(c[0] + dx * k * math.cos(math.radians(a + 90)) - dy * k * math.sin(math.radians(a + 90)), c[1] + dx * k * math.sin(math.radians(a + 90)) + dy * k * math.cos(math.radians(a + 90)), 3.4 * k, 3.4 * k, '#fffdf4', POD_K, .8)
        if o.get('mikrovillus'):
            for (a0, a1) in o['mikrovillus']:
                for a in range(int(a0), int(a1), 5):
                    i = s._idx(a); p = s.dis[i]; ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
                    F.ln(p[0] - ux * 2, p[1] - uy * 2, p[0] + ux * 9 * k, p[1] + uy * 9 * k, POD_K, 3.6 * k)
                    F.ln(p[0] - ux * 2, p[1] - uy * 2, p[0] + ux * 8.5 * k, p[1] + uy * 8.5 * k, POD, 2.2 * k)
        # yarık boşluğu (Bowman rengi) + ayaksı çıkıntılar
        F.yol(_pd(yar), None, 0, BOW)
        L = yay_uzunluk(s.mid); adim = o.get('fp_adim', 8) * k; hedef = 0
        s.fp = []
        for i in range(len(s.mid)):
            a = i * 360 / len(s.mid)
            if efase_mi(a): continue
            if L[i] >= hedef:
                hedef = L[i] + adim
                p, n = s.mid[i], s.ns[i]
                b0 = (p[0] + n[0] * (s.g / 2 - 1), p[1] + n[1] * (s.g / 2 - 1)); b1 = (p[0] + n[0] * (s.g / 2 + s.fh + 3 * k), p[1] + n[1] * (s.g / 2 + s.fh + 3 * k))
                s.fp.append((b0, b1))
        for (b0, b1) in s.fp: F.ln(b0[0], b0[1], b1[0], b1[1], POD_K, 6 * k)
        for (b0, b1) in s.fp: F.ln(b0[0], b0[1], b1[0], b1[1], POD, 4.2 * k)
        if efase:
            seg = []; segs = []
            for i in range(len(s.mid)):
                a = i * 360 / len(s.mid)
                if efase_mi(a):
                    p, n = s.mid[i], s.ns[i]; d = s.g / 2 + s.fh / 2 + 1
                    seg.append((p[0] + n[0] * d, p[1] + n[1] * d))
                elif seg: segs.append(seg); seg = []
            if seg: segs.append(seg)
            if efase is True and segs: segs = [segs[0] + segs[-1]] if len(segs) > 1 else segs
            for sg in segs:
                F.yol(_pd(sg, efase is True and len(segs) == 1), POD_K, s.fh + 4.4 * k)
                F.yol(_pd(sg, efase is True and len(segs) == 1), POD, s.fh + 2.6 * k)
        if o.get('ayrilma'):
            for (a0, a1) in o['ayrilma']:
                ii = [s._idx(a0 + t) for t in range(int((a1 - a0) % 360) + 1)]
                ic0 = [(s.mid[i][0] + s.ns[i][0] * (s.g / 2 - .5), s.mid[i][1] + s.ns[i][1] * (s.g / 2 - .5)) for i in ii]
                dis0 = [(s.dis[i][0] + s.ns[i][0] * 16, s.dis[i][1] + s.ns[i][1] * 16) for i in ii][::-1]
                F.yol(_pd(ic0 + dis0), None, 0, BOW)
            s.ayr_p = s.p_gbm((o['ayrilma'][0][0] + o['ayrilma'][0][1]) / 2)
        # mezangiyal matriks (GBM içi)
        mez_renk = o.get('mez_renk', MESM)
        F.yol(_pd(ic_), None, 0, mez_renk)
        # GBM
        gr = GBM; gk = GBM_K
        if o.get('yogun'): gr, gk = '#33414f', '#1d2731'
        if o.get('amiloid'): gr, gk = '#f6cdb8', '#c98a6a'
        F.yol(_pd(s.mid), gk, s.g + 2.4 * k); F.yol(_pd(s.mid), gr, s.g)
        if o.get('lamel'):
            for d_, c_ in ((-s.g * .28, '#3f6f80'), (0, '#ffffff'), (s.g * .28, '#3f6f80')):
                pts = [(p[0] + n[0] * (d_ + 1.2 * math.sin(i / 2.3)), p[1] + n[1] * (d_ + 1.2 * math.sin(i / 2.3))) for i, (p, n) in enumerate(zip(s.mid, s.ns))]
                F.yol(_pd(pts), c_, 1.1 if c_ != '#ffffff' else 1.6, op=.9)
        # lümenler
        for i, c in enumerate(s.cap):
            F.el(c[0], c[1], R_in, R_in, LUM)
        if o.get('lipo'):
            for i, c in enumerate(s.cap):
                F.el(c[0], c[1], R_in - 1, R_in - 1, '#fdf1c2')
                for f_ in (.82, .62, .42, .24): F.el(c[0] + 2 * k, c[1] - 1 * k, (R_in - 1) * f_, (R_in - 1) * f_ * .94, 'none', '#d9be6a', 1.1)
        if o.get('kriyo'):
            for i in o['kriyo']:
                c = s.cap[i]; F.yol(f'M{c[0] - 20 * k:.1f},{c[1] - 6 * k:.1f} q{8 * k:.1f},{-18 * k:.1f} {26 * k:.1f},{-12 * k:.1f} q{14 * k:.1f},{10 * k:.1f} {4 * k:.1f},{26 * k:.1f} q{-16 * k:.1f},{10 * k:.1f} {-30 * k:.1f},{-14 * k:.1f} z', '#c46a7e', 1.2, '#f2b8c6')
        # çift kontur (MPGN): içte yeni bazal membran, arada mezangiyal interpozisyon
        if o.get('cift'):
            for i, c in enumerate(s.cap):
                a_m = math.degrees(math.atan2(s.cy - c[1], s.cx - c[0]))
                a0, a1 = a_m + 62, a_m + 298
                def arc(rr):
                    return [P(c, rr, a0 + (a1 - a0) * t / 60) for t in range(61)]
                F.yol(_pd(arc(R_in - 4.5 * k), False), mez_renk, 7 * k)
                for t in (.2, .5, .8):
                    q = P(c, R_in - 4.5 * k, a0 + (a1 - a0) * t); elips(F, q[0], q[1], 5 * k, 2.6 * k, a0 + (a1 - a0) * t + 90, MESC, MESC_K, 1)
                F.yol(_pd(arc(R_in - 9 * k), False), GBM_K, 3.6 * k); F.yol(_pd(arc(R_in - 9 * k), False), GBM, 2 * k)
        if o.get('nodul'):
            rn = s.d - R_in - 1.5 * k
            F.el(s.cx, s.cy, rn, rn, '#f6dde3', '#c98d9b', 1.4)
            for f_ in (.78, .55, .32): F.el(s.cx, s.cy, rn * f_, rn * f_ * .95, 'none', '#e2b3c0', 1)
            for t in range(0, 360, 60): q = P((s.cx, s.cy), rn * .9, t + 30); elips(F, q[0], q[1], 3.6 * k, 2.2 * k, t + 120, MESN)
            s.nodul_p = (s.cx, s.cy)
        # mezangiyal hücre
        w5 = lambda f: ((1 + math.cos(3 * (f - math.radians(s.ac[0] + 60)))) / 2) ** 5
        cr0, cr1 = o.get('mez_hucre', (12, 23))
        pts = [(s.cx + (cr0 + cr1 * w5(2 * math.pi * i / 180)) * k * math.cos(2 * math.pi * i / 180),
                s.cy + (cr0 + cr1 * w5(2 * math.pi * i / 180)) * k * math.sin(2 * math.pi * i / 180)) for i in range(180)]
        if not o.get('nodul'):
            F.yol(_pd(yumusat(pts, 2, 1)), MESC_K, 1.6, MESC)
            elips(F, s.cx, s.cy, 8.5 * k, 10 * k, s.ac[0] + 90, MESN)
            elips(F, s.cx - 2 * k, s.cy - 2.5 * k, 2.2 * k, 1.6 * k, 0, '#7e6bb8')
        ek = o.get('mez_hiper', 0)
        if ek:
            yer = []
            for j in range(3):
                for f_ in (.5, .78):
                    yer.append(P((s.cx, s.cy), s.mm * f_, s.centik[j] + (9 if f_ > .6 else -6)))
            for q in yer[:ek]:
                elips(F, q[0], q[1], 6.5 * k, 4.6 * k, 0, MESC, MESC_K, 1.2); elips(F, q[0], q[1], 3.8 * k, 3 * k, 0, MESN)
        # endotel
        s.endc = []
        for i, c in enumerate(s.cap):
            kalin = o.get('endokap')
            re_ = (12 if o.get('cift') else 2.3) * k
            F.el(c[0], c[1], R_in - re_, R_in - re_, 'none', END_K, (3.2 if not kalin else 5) * k, dash=f'{8 * k:.1f} {3.2 * k:.1f}')
            a_m = math.degrees(math.atan2(s.cy - c[1], s.cx - c[0]))
            a_e = a_m + o.get('endo_ac', 52)
            q = P(c, R_in - re_ - 4.7 * k, a_e); s.endc.append(q)
            elips(F, q[0], q[1], (14 if not kalin else 17) * k, (6.4 if not kalin else 8) * k, a_e + 90, END_C, END_K, 1.3)
            elips(F, q[0], q[1], 8.4 * k, 4 * k, a_e + 90, END_N)
            if o.get('tri') and i == o.get('tri_i', 0):
                tq = (q[0] + 8 * k * math.cos(math.radians(a_e + 90)), q[1] + 8 * k * math.sin(math.radians(a_e + 90)))
                F.el(tq[0], tq[1], 4.4 * k, 4.4 * k, '#fff4f4', '#7a1f3d', 1.2)
                for t in range(0, 180, 45): F.ln(tq[0] - 3 * k * math.cos(math.radians(t)), tq[1] - 3 * k * math.sin(math.radians(t)), tq[0] + 3 * k * math.cos(math.radians(t)), tq[1] + 3 * k * math.sin(math.radians(t)), '#7a1f3d', .8)
                s.tri_p = tq
            if o.get('eritrosit', True) and not kalin:
                eritrosit(F, c[0] - 6 * k, c[1] + 4 * k, 12 * k, 25 + i * 50)
            if kalin and o.get('endokap_n'):
                n_ = o['endokap_n']; rr_ = (R_in - re_) * .52
                for t in range(n_):
                    q2 = c if t == 0 else P(c, rr_, 360 / (n_ - 1) * (t - 1) + 25 + i * 40)
                    (notrofil if t % 2 == 0 else monosit)(F, q2[0], q2[1], (10.5 if t % 2 == 0 else 8.2) * k)
            elif kalin:
                notrofil(F, c[0] + 4 * k, c[1] - 3 * k, 13 * k)
                if i != 1: monosit(F, c[0] - 15 * k, c[1] + 14 * k, 9.5 * k)
        # ---- birikimler
        se = o.get('subepi')
        if se:
            adim_ = se.get('adim', 3); boy = se.get('boy', 5.2) * k; evre = se.get('evre', 2)
            noktalar = []
            for j, (b0, b1) in enumerate(s.fp):
                pass
            L = yay_uzunluk(s.mid); hedef = 4 * k; aralik = se.get('aralik', 15) * k
            for i in range(len(s.mid)):
                if L[i] >= hedef:
                    hedef = L[i] + aralik; noktalar.append(i)
            s.dep['subepi'] = []
            for j, i in enumerate(noktalar):
                p, n = s.mid[i], s.ns[i]
                q = (p[0] + n[0] * (s.g / 2 + boy * .55), p[1] + n[1] * (s.g / 2 + boy * .55)); s.dep['subepi'].append(q)
                ang = math.degrees(math.atan2(n[1], n[0]))
                if evre >= 2 and se.get('diken', True):
                    # dikenler: birikimler arasında GBM uzantıları
                    i2 = noktalar[j + 1] if j + 1 < len(noktalar) else None
                    if i2 is not None:
                        im = (i + i2) // 2; pm, nm = s.mid[im], s.ns[im]
                        a0 = (pm[0] + nm[0] * (s.g / 2 - .5), pm[1] + nm[1] * (s.g / 2 - .5)); a1 = (pm[0] + nm[0] * (s.g / 2 + boy * 1.15), pm[1] + nm[1] * (s.g / 2 + boy * 1.15))
                        F.ln(a0[0], a0[1], a1[0], a1[1], GBM_K, 3.6 * k); F.ln(a0[0], a0[1], a1[0], a1[1], GBM, 2 * k)
                if evre >= 3:
                    elips(F, q[0], q[1], boy * 1.05, boy * .8, ang, GBM, GBM_K, 1)
                    elips(F, q[0], q[1], boy * .62, boy * .44, ang, '#56606b' if evre == 3 else '#f4f8fa')
                else:
                    elips(F, q[0], q[1], boy * .8, boy * .58, ang, DEP, '#fff', .8)
        if o.get('hump'):
            s.dep['hump'] = []
            for a in o['hump']:
                i = s._idx(a); p, n = s.mid[i], s.ns[i]; ang = math.degrees(math.atan2(n[1], n[0]))
                q = (p[0] + n[0] * (s.g / 2 + 6 * k), p[1] + n[1] * (s.g / 2 + 6 * k)); s.dep['hump'].append(q)
                elips(F, q[0], q[1], 9.5 * k, 7.5 * k, ang + 90, DEP, '#fff', 1)
        if o.get('subendo'):
            s.dep['subendo'] = []
            for (i, a, yay, kal) in o['subendo']:
                c = s.cap[i]
                pts = [P(c, R_in - kal * k / 2 - .3, a - yay / 2 + yay * t / 30) for t in range(31)]
                F.yol(_pd(pts, False), '#ffffff', kal * k + 1.6); F.yol(_pd(pts, False), o.get('subendo_renk', DEP), kal * k)
                s.dep['subendo'].append(P(c, R_in - kal * k / 2, a))
        if o.get('mez'):
            s.dep['mez'] = []
            rng = random.Random(7)
            for j in range(3):
                for (f_, da) in ((.62, -14), (.8, 8), (.45, 18))[:o['mez']]:
                    q = P((s.cx, s.cy), s.mm * f_, s.centik[j] + da); s.dep['mez'].append(q)
                    elips(F, q[0], q[1], o.get('mez_boy', 4.6) * k, o.get('mez_boy', 4.6) * .78 * k, rng.random() * 180, o.get('mez_dep_renk', DEP), '#fff', .8)
        if o.get('intra'):
            for a in range(0, 360, 4):
                i = s._idx(a); p = s.mid[i]
                if (a // 4) % 3 == 0: F.el(p[0], p[1], s.g * .28, s.g * .28, DEP)
        if o.get('nekroz') is not None:
            a = o['nekroz']; i0 = s._idx(a - 7); i1 = s._idx(a + 7)
            seg = [s.mid[j % 360] for j in range(i0, i0 + ((i1 - i0) % 360) + 1)]
            F.yol(_pd(seg, False), BOW, s.g + 3 * k)
            p, n = s.mid[s._idx(a)], s.ns[s._idx(a)]
            q = (p[0] + n[0] * 16 * k, p[1] + n[1] * 16 * k)
            F.yol(f'M{p[0] - n[1] * 10 * k:.1f},{p[1] + n[0] * 10 * k:.1f} Q{q[0] + n[1] * 22 * k:.1f},{q[1] - n[0] * 22 * k:.1f} {q[0] + n[0] * 14 * k:.1f},{q[1] + n[1] * 14 * k:.1f} '
                  f'Q{q[0] - n[1] * 22 * k:.1f},{q[1] + n[0] * 22 * k:.1f} {p[0] + n[1] * 10 * k:.1f},{p[1] - n[0] * 10 * k:.1f} Z', FIB_K, 1.2, FIB, op=.92)
            rng = random.Random(3)
            for _ in range(9):
                F.el(q[0] + rng.uniform(-11, 11) * k, q[1] + rng.uniform(-11, 11) * k, 1.4 * k, 1.4 * k, '#3a2a2a')
            s.dep['nekroz'] = q
        if o.get('amiloid'):
            rng = random.Random(5)
            for _ in range(70):
                j = rng.randrange(3); q = P((s.cx, s.cy), s.mm * rng.uniform(.25, .95), s.centik[j] + rng.uniform(-16, 16))
                a = rng.uniform(0, 180); F.ln(q[0], q[1], q[0] + 4 * k * math.cos(math.radians(a)), q[1] + 4 * k * math.sin(math.radians(a)), '#c46a4a', .9)
            for a in range(0, 360, 6):
                i = s._idx(a); p, n = s.mid[i], s.ns[i]
                F.ln(p[0] + n[0] * s.g / 2, p[1] + n[1] * s.g / 2, p[0] + n[0] * (s.g / 2 + 5 * k), p[1] + n[1] * (s.g / 2 + 5 * k), '#c46a4a', 1.1)


# =================================================================================================== TÜM GLOMERÜL
def _yumak_noktalar():
    import random as _r
    g = _r.Random(12); q = []
    for (yy, xs) in ((-.73, (-.42, 0, .42)), (-.364, (-.63, -.21, .21, .63)), (0, (-.84, -.42, 0, .42, .84)), (.364, (-.63, -.21, .21, .63)), (.73, (-.42, 0, .42))):
        for xx in xs:
            q.append((xx + g.uniform(-.035, .035), yy + g.uniform(-.035, .035), g.uniform(.165, .2)))
    return q


_YUMAK = _yumak_noktalar()


class Glomerul:
    """Tüm glomerül. vp: vasküler kutup açısı, up: üriner kutup açısı (derece). R: Bowman kapsülü yarıçapı."""

    def __init__(s, F, cx, cy, R=120, vp=-90, up=90, **o):
        s.F, s.cx, s.cy, s.R, s.vp, s.up, s.o = F, cx, cy, R, vp, up, o
        s.ciz()

    def p_kapsul(s, a): return P((s.cx, s.cy), s.R, a)
    def p_bow(s, a): return P((s.cx, s.cy), (s.R + s.Rt * 1.08 + s.kay) / 2, a)
    def p_yumak(s, a, f=.6): return P(s.tc, s.Rt * f, a)
    def p_af(s): return s.af
    def p_ef(s): return s.ef
    def p_tub(s): return s.tub
    def p_par(s, a): return P((s.cx, s.cy), s.R - 3.5, a)

    def ciz(s):
        F, o, R = s.F, s.o, s.R
        c0 = (s.cx, s.cy)
        # proksimal tübül
        if o.get('tubul', True):
            tw = R * .34; L = R * o.get('tubul_boy', .95)
            ux, uy = math.cos(math.radians(s.up)), math.sin(math.radians(s.up)); nx, ny = -uy, ux
            b = P(c0, R * .86, s.up); e_ = (b[0] + ux * (L + R * .14), b[1] + uy * (L + R * .14))
            for sg in (-1, 1):
                x0, y0 = b[0] + nx * sg * tw, b[1] + ny * sg * tw
                F.a(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x0 + ux * (L + R * .14):.1f}" y2="{y0 + uy * (L + R * .14):.1f}" stroke="{TUB_K}" stroke-width="{R * .2 + 2:.1f}"/>')
                F.a(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x0 + ux * (L + R * .14):.1f}" y2="{y0 + uy * (L + R * .14):.1f}" stroke="{TUB}" stroke-width="{R * .2:.1f}"/>')
            F.a(f'<line x1="{b[0]:.1f}" y1="{b[1]:.1f}" x2="{e_[0]:.1f}" y2="{e_[1]:.1f}" stroke="{BOW}" stroke-width="{2 * tw - R * .2 - 2:.1f}"/>')
            t = R * .2
            while t < L + R * .1:
                for sg in (-1, 1):
                    q = (b[0] + ux * t + nx * sg * tw, b[1] + uy * t + ny * sg * tw)
                    F.el(q[0] + nx * sg * R * .03, q[1] + ny * sg * R * .03, R * .035, R * .035, TUB_N)
                    m0 = (b[0] + ux * (t - R * .09) + nx * sg * (tw - R * .1), b[1] + uy * (t - R * .09) + ny * sg * (tw - R * .1))
                    m1 = (b[0] + ux * (t - R * .09) + nx * sg * (tw + R * .1), b[1] + uy * (t - R * .09) + ny * sg * (tw + R * .1))
                    F.ln(m0[0], m0[1], m1[0], m1[1], TUB_K, .8)
                    for j in range(5):
                        z0 = (b[0] + ux * (t - R * .07 + j * R * .03) + nx * sg * (tw - R * .1), b[1] + uy * (t - R * .07 + j * R * .03) + ny * sg * (tw - R * .1))
                        F.ln(z0[0], z0[1], z0[0] - nx * sg * R * .035, z0[1] - ny * sg * R * .035, TUB_K, .7)
                t += R * .18
            s.tub = (b[0] + ux * L * .6 + nx * tw, b[1] + uy * L * .6 + ny * tw)
        else:
            s.tub = P(c0, R, s.up)
        # Bowman kapsülü
        kal = o.get('kapsul_kal', 2.8)
        F.el(s.cx, s.cy, R, R, BOW)
        acik = math.degrees(math.asin(min(.95, (R * .34) / R))) if o.get('tubul', True) else 0
        yirtik = o.get('kapsul_yirtik')
        def yay(a0, a1, rr):
            n = max(8, int(abs(a1 - a0) / 3)); return [P(c0, rr, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
        aralar = [(s.up + acik, s.up + 360 - acik)]
        if yirtik:
            ya, yw = yirtik
            aralar = [(s.up + acik, ya - yw / 2 + (360 if ya - yw / 2 < s.up + acik else 0)), (ya + yw / 2 + (360 if ya + yw / 2 < s.up + acik else 0), s.up + 360 - acik)]
        for (a0, a1) in aralar:
            F.yol(_pd(yay(a0, a1, R), False), GBM_K, kal + 1.2); F.yol(_pd(yay(a0, a1, R - .6), False), '#a9c7d2', kal - .6)
            F.yol(_pd(yay(a0, a1, R - kal / 2 - 2.2), False), POD_K, 3.6); F.yol(_pd(yay(a0, a1, R - kal / 2 - 2.2), False), POD, 2.2)
            a = a0 + 12
            while a < a1 - 6:
                q = P(c0, R - kal / 2 - 2.6, a); elips(F, q[0], q[1], 4.4, 1.9, a + 90, POD_N, POD_NK, .8); a += 34
        # hilal
        hil = o.get('hilal')
        s.kay = 0; s.tc = c0; s.Rt = R * .7
        if hil:
            a0, a1, tur = hil[0], hil[1], hil[2] if len(hil) > 2 else 'hucresel'
            am = (a0 + a1) / 2; gen_ = ((a1 - a0) % 360) / 360
            s.kay = R * (.06 + .18 * gen_); s.tc = P(c0, s.kay, am + 180); s.Rt = R * (.72 - .22 * gen_)
        if o.get('cokme'): s.Rt *= .82
        if o.get('global'): s.Rt *= .66
        # arteriyoller
        vu, vv = math.cos(math.radians(s.vp)), math.sin(math.radians(s.vp)); vn = (-vv, vu)
        hil_p = P(c0, R * .98, s.vp)
        s.af = s.ef = hil_p
        for (sg, gw, ad) in ((1, R * .2, 'af'), (-1, R * .15, 'ef')):
            st = (hil_p[0] + vn[0] * sg * R * .16, hil_p[1] + vn[1] * sg * R * .16)
            ab = o.get('arteriyol_boy', .45); en = (st[0] + vu * R * ab + vn[0] * sg * R * .26, st[1] + vv * R * ab + vn[1] * sg * R * .26)
            ic0 = P(s.tc, s.Rt * .55, s.vp)
            d = f'M{ic0[0]:.1f},{ic0[1]:.1f} Q{st[0]:.1f},{st[1]:.1f} {en[0]:.1f},{en[1]:.1f}'
            hy = o.get('hiyalinoz') and ad == 'af'
            F.yol(d, '#9e2b25', gw + 2); F.yol(d, HYAL if hy else '#d9534f', gw); F.yol(d, '#f7c4c0', gw * .42)
            q = (en[0] - vu * R * .1, en[1] - vv * R * .1)
            if ad == 'af': s.af = q
            else: s.ef = q
        # yumak
        rot = s.vp + 90
        ld = []
        for (x, y, r) in _YUMAK:
            cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
            X, Y = x * cr - y * sr, x * sr + y * cr
            ld.append((s.tc[0] + X * s.Rt, s.tc[1] + Y * s.Rt, r * s.Rt * (o.get('ilmek_k', 1.0))))
        s.ilmekler = ld
        # segmental lezyon açıları
        def acida(x, y, rng_):
            if not rng_: return False
            a = math.degrees(math.atan2(y - s.tc[1], x - s.tc[0])); a0, a1 = rng_
            return (a - a0) % 360 <= (a1 - a0) % 360 and math.hypot(x - s.tc[0], y - s.tc[1]) > s.Rt * .22
        skl = o.get('skleroz'); nek = o.get('nekroz'); nod = o.get('nodul', ())
        mk = o.get('mez_genis', 1.0)
        hp = P(s.tc, s.Rt * .98, s.vp)
        s.skl_n = []
        if not o.get('global'):
            # 1) birleşik podosit örtüsü (dış çizgisiyle)
            for (x, y, r) in ld: F.el(x, y, r * 1.36, r * 1.36, POD, POD_K, 2.2)
            for (x, y, r) in ld: F.el(x, y, r * 1.36 - 1.1, r * 1.36 - 1.1, POD)
            # 2) mezangiyal sap: hilustan ilmeklerin arasına uzanan dallar
            ic_ = [(x, y, r) for (x, y, r) in ld]
            for (x, y, r) in ic_:
                F.ln(hp[0], hp[1], x, y, '#d9ccef', (5.5 + 3 * (mk - 1)) * s.R / 120)
            for i in range(len(ld)):
                for j in range(i + 1, len(ld)):
                    (x1, y1, r1), (x2, y2, r2) = ld[i], ld[j]
                    if math.hypot(x1 - x2, y1 - y2) < s.Rt * .5:
                        F.el((x1 + x2) / 2, (y1 + y2) / 2, s.Rt * .07 * mk, s.Rt * .07 * mk, '#e3d8f4')
            for (x, y, r) in ld:
                q = P((x, y), r * 1.12, math.degrees(math.atan2(hp[1] - y, hp[0] - x)))
                elips(F, q[0], q[1], r * .32 * mk, r * .22 * mk, 0, MESC, MESC_K, .7); F.el(q[0], q[1], r * .12, r * .12, MESN)
        for i, (x, y, r) in enumerate(ld):
            if o.get('global'):
                continue
            if acida(x, y, skl):
                s.skl_n.append((x, y, r)); continue
            if acida(x, y, o.get('endokap_seg')):
                F.el(x, y, r * 1.07, r * 1.07, GBM, GBM_K, 1.1)
                F.el(x, y, r, r, '#fbefd6')
                for (dx, dy) in ((-.38, -.3), (.35, -.25), (0, .4)):
                    F.el(x + dx * r, y + dy * r, r * .36, r * .36, '#fff8e6', '#c9a77a', .8)
                    for t in range(3): F.el(x + dx * r + r * .14 * math.cos(t * 2.1), y + dy * r + r * .14 * math.sin(t * 2.1), r * .07, r * .07, '#e5d3ad')
                s.endseg_p = (x, y); continue
            if o.get('cokme'):
                pts = [P((x, y), r * (.5 + .12 * math.sin(7 * t * math.pi / 18)), t * 10) for t in range(36)]
                F.yol(_pd(pts), GBM_K, 2.2, GBM)
                continue
            if i in nod:
                F.el(x, y, r * 1.12, r * 1.12, '#f6dde3', SKL_K, 1.4)
                for f_ in (.78, .52, .28): F.el(x, y, r * f_, r * f_, 'none', '#e3b6c2', 1)
                for t in range(0, 360, 90): q = P((x, y), r * .9, t + 20); elips(F, q[0], q[1], 2.6, 1.6, t + 110, MESN)
                continue
            if not o.get('efase'):
                F.el(x, y, r * 1.17, r * 1.17, 'none', POD_K, 2.6, dash='1.2 1.8')
            F.el(x, y, r * 1.07, r * 1.07, GBM, GBM_K, 1.1 if not o.get('gbm_kalin') else 2.8)
            dar = .74 if o.get('endokap') else 1.0
            if o.get('endokap'):
                F.el(x, y, r * .98, r * .98, '#f4c0c0')
            F.el(x, y, r * dar, r * dar, LUM)
            F.el(x, y, r * .9 * dar, r * .9 * dar, 'none', END_K, 1.5, dash='3.2 1.5')
            if o.get('endokap') and i % 2 == 0: notrofil(F, x, y, r * .5)
            elif o.get('endokap'): monosit(F, x, y, r * .45)
            elif i % 3 == 0: eritrosit(F, x, y, r * .42, i * 30)
        if o.get('mez_cekirdek'):
            rng = random.Random(14)
            for i in range(len(ld)):
                for j in range(i + 1, len(ld)):
                    (x1, y1, r1), (x2, y2, r2) = ld[i], ld[j]
                    if math.hypot(x1 - x2, y1 - y2) < s.Rt * .5 and rng.random() < o['mez_cekirdek']:
                        elips(F, (x1 + x2) / 2, (y1 + y2) / 2, s.Rt * .045, s.Rt * .035, rng.uniform(0, 180), MESN)
        if o.get('podosit_n'):
            n = o['podosit_n']
            for t in range(n):
                a = s.vp + 90 + 360 * (t + .5) / n
                q = P(s.tc, s.Rt * 1.08, a); elips(F, q[0], q[1], s.Rt * .13, s.Rt * .085, a + 90, POD, POD_K, 1.2); elips(F, q[0], q[1], s.Rt * .06, s.Rt * .045, a + 90, POD_N, POD_NK, .8)
        if o.get('global'):
            F.el(s.tc[0], s.tc[1], s.Rt * 1.05, s.Rt * 1.05, SKL, SKL_K, 1.6)
            rng = random.Random(4)
            for _ in range(10):
                q = P(s.tc, s.Rt * rng.uniform(.1, .9), rng.uniform(0, 360)); F.yol(f'M{q[0] - 6:.1f},{q[1]:.1f} q6,-4 12,0', '#d7a6b2', 1.1)
            for _ in range(4):
                q = P(s.tc, s.Rt * rng.uniform(.2, .8), rng.uniform(0, 360)); elips(F, q[0], q[1], 3, 1.6, rng.uniform(0, 180), MESN)
        # segmental skleroz bloğu + yapışıklık (sineşi) + hiyalinoz
        if skl:
            a0, a1 = skl; span = (a1 - a0) % 360; am = a0 + span / 2
            for (x, y, r) in s.skl_n: F.el(x, y, r * 1.3, r * 1.3, SKL, SKL_K, 1.2)
            for (x, y, r) in s.skl_n: F.el(x, y, r * 1.3 - 1, r * 1.3 - 1, SKL)
            for (x, y, r) in s.skl_n:
                F.yol(f'M{x - r * .7:.1f},{y:.1f} q{r * .7:.1f},{-r * .5:.1f} {r * 1.4:.1f},0', '#d9a8b4', 1)
                elips(F, x + r * .3, y + r * .4, 2.6, 1.5, 30, MESN)
            s.skl_p = P(s.tc, s.Rt * .7, am)
            if o.get('yapisiklik', True):
                p0 = P(s.tc, s.Rt * 1.0, am - 9); p1 = P(s.tc, s.Rt * 1.0, am + 9)
                q1 = P((s.cx, s.cy), s.R - 3, am + 12); q0 = P((s.cx, s.cy), s.R - 3, am - 12)
                m0 = P((s.cx, s.cy), (s.R + s.Rt + s.kay) / 2, am - 5); m1 = P((s.cx, s.cy), (s.R + s.Rt + s.kay) / 2, am + 5)
                F.yol(f'M{p0[0]:.1f},{p0[1]:.1f} Q{m0[0]:.1f},{m0[1]:.1f} {q0[0]:.1f},{q0[1]:.1f} L{q1[0]:.1f},{q1[1]:.1f} Q{m1[0]:.1f},{m1[1]:.1f} {p1[0]:.1f},{p1[1]:.1f} Z', SKL_K, 1.2, SKL)
                s.sinesi = P((s.cx, s.cy), (s.R + s.Rt * .95 + s.kay) / 2, am)
            rng = random.Random(8)
            if o.get('hiyalin', True):
                for j in range(3):
                    q = P(s.tc, s.Rt * rng.uniform(.45, .8), am + rng.uniform(-.28, .28) * span); F.el(q[0], q[1], 5.2, 4, HYAL, '#d36d8a', 1)
            if o.get('kopuk'):
                for j in range(4):
                    q = P(s.tc, s.Rt * rng.uniform(.5, .85), am + rng.uniform(-.3, .3) * span)
                    F.el(q[0], q[1], 6, 6, '#fff8e8', '#c9a77a', 1)
                    for t in range(4): F.el(q[0] + 2.4 * math.cos(t * 1.6), q[1] + 2.4 * math.sin(t * 1.6), 1.4, 1.4, '#e8d8b8')
        # çökme: hiperplastik podositler (yalancı hilal)
        if o.get('cokme'):
            rng = random.Random(2)
            for a in range(0, 360, 26):
                q = P(s.tc, s.Rt * 1.12, a + rng.uniform(-6, 6)); elips(F, q[0], q[1], 11, 8, a + 90, POD, POD_K, 1.3); elips(F, q[0], q[1], 5.2, 4.2, a, POD_NK)
            s.cokme_p = P(s.tc, s.Rt * 1.12, 26 * 3)
        # hilal
        if hil:
            a0, a1, tur = hil[0], hil[1], hil[2] if len(hil) > 2 else 'hucresel'
            span = (a1 - a0) % 360
            ic_r = lambda a: math.hypot(*(lambda p: (p[0] - s.cx, p[1] - s.cy))(P(s.tc, s.Rt * 1.12, a)))
            dis_ = [P(c0, R - 5.5, a0 + span * t / 40) for t in range(41)]
            ic_ = [P(s.tc, s.Rt * 1.14, a1 - span * t / 40) for t in range(41)]
            dolgu = {'hucresel': '#f6e2cf', 'fibroselular': '#ece4df', 'fibroz': '#dfe7eb'}[tur]
            F.yol(_pd(dis_ + ic_), '#c9a98d' if tur != 'fibroz' else '#9fb3bd', 1.4, dolgu)
            rng = random.Random(11)
            am = a0 + span / 2
            for j in range(int(span * 1.25)):
                a = a0 + 4 + rng.random() * (span - 8)
                rin = math.hypot(P(s.tc, s.Rt * 1.14, a)[0] - s.cx, P(s.tc, s.Rt * 1.14, a)[1] - s.cy)
                rr = rng.uniform(rin + 5, R - 10)
                if rr < rin + 4: continue
                q = P(c0, rr, a)
                if tur == 'hucresel' or (tur == 'fibroselular' and rng.random() < .5):
                    elips(F, q[0], q[1], 5.2, 3.8, rng.uniform(0, 180), '#efc9a8', '#b98a63', .7); F.el(q[0], q[1], 1.9, 1.9, '#7d4a62')
                else:
                    elips(F, q[0], q[1], 4.2, 1.1, a + 90, '#6c7f8c')
            if tur != 'hucresel':
                for j in range(5):
                    rr = (R - 6 + s.Rt * 1.14 + s.kay) / 2 + (j - 2) * 4
                    F.yol(_pd([P(c0, rr + 1.6 * math.sin(t), a0 + 5 + (span - 10) * t / 30) for t in range(31)], False), '#a8bcc6', .9)
            if o.get('fibrin_hilal', tur == 'hucresel'):
                q = P(c0, (R + s.Rt * 1.14 + s.kay) / 2, am - span * .18); elips(F, q[0], q[1], 9, 4.5, am + 70, FIB, FIB_K, .8)
            s.hilal_p = P(c0, (R - 5 + s.Rt * 1.14 + s.kay) / 2, am)
        if yirtik:
            ya, yw = yirtik; rng = random.Random(6)
            for j in range(16):
                q = P(c0, R + rng.uniform(4, 22), ya + rng.uniform(-yw, yw)); F.el(q[0], q[1], 2.6, 2.6, '#6c5a8c')
        if nek:
            a0, a1 = nek; am = a0 + ((a1 - a0) % 360) / 2
            q = P(s.tc, s.Rt * .82, am)
            F.yol(f'M{q[0] - 14:.1f},{q[1] - 6:.1f} q10,-14 24,-2 q8,12 -2,20 q-14,8 -22,-4 z', FIB_K, 1.2, FIB, op=.95)
            rng = random.Random(9)
            for _ in range(10): F.el(q[0] + rng.uniform(-12, 12), q[1] + rng.uniform(-10, 10), 1.5, 1.5, '#3a2a2a')
            s.nekroz_p = q


# =================================================================================================== FİLTRASYON BARİYERİ
def bariyer(F, x, y, w, h=170, **o):
    """Yatay filtrasyon bariyeri: üstte kapiller lümen, altta Bowman boşluğu. Dönüş: katmanların y değerleri."""
    yl = y + h * .26                     # endotel üst
    ye = yl + 9                          # endotel alt / GBM üst
    gk = o.get('gbm_k', 1.0); hg = 20 * gk
    yg = ye + hg                         # GBM alt
    hf = 15; yf = yg + hf               # ayaksı çıkıntı alt (birincil uzantı)
    F.r(x, y, w, yl - y, LUM, None, rx=0)
    F.r(x, yg, w, y + h - yg, BOW, None, rx=0)
    # glikokaliks
    for i in range(int(w / 5)):
        xx = x + 2 + i * 5; F.ln(xx, yl - 1, xx + 1.2, yl - 5.5, '#9bc59b', 1)
    # endotel (pencereli)
    fen = o.get('pencere', 26)
    xx = x
    while xx < x + w:
        x1 = min(x + w, xx + fen - 6)
        F.r(xx, yl, x1 - xx, 9, END_C, END_K, 1, 4)
        xx += fen
    # GBM
    lam = o.get('lamel')
    F.r(x, ye, w, hg, '#e4f0f4', None, rx=0)
    if not lam:
        F.r(x, ye + hg * .3, w, hg * .4, GBM_D, None, rx=0)
    else:
        rng = random.Random(1)
        for j in range(5):
            yy = ye + hg * (.15 + .17 * j)
            F.yol('M' + ' L'.join('%.1f,%.1f' % (x + t * w / 60, yy + 2.2 * math.sin(t * .9 + j)) for t in range(61)), GBM_D, 2.2)
        for j in range(12):
            F.el(x + rng.uniform(8, w - 8), ye + rng.uniform(3, hg - 3), 1.6, 1.6, '#41606b')
    F.ln(x, ye, x + w, ye, GBM_K, 1); F.ln(x, yg, x + w, yg, GBM_K, 1)
    # ayaksı çıkıntılar
    ef = o.get('efase')                   # (x0 oranı, x1 oranı)
    ayr = o.get('ayrilma')                # çıplak GBM aralığı
    fw, gap = 13, 6
    xx = x + 3; j = 0
    s_ = {'yl': yl, 'ye': ye, 'yg': yg, 'yf': yf, 'fp': [], 'yarik': []}
    def icinde(xv, rng_):
        return rng_ and x + rng_[0] * w <= xv <= x + rng_[1] * w
    while xx < x + w - fw:
        if icinde(xx + fw / 2, ef) or icinde(xx + fw / 2, ayr):
            xx += fw + gap; j += 1; continue
        c = POD if j % 2 == 0 else '#e9d09a'
        F.r(xx, yg, fw, hf + 4, c, POD_K, 1.1, 5)
        s_['fp'].append(xx + fw / 2)
        if not icinde(xx + fw + gap / 2, ef) and xx + fw + gap < x + w - fw:
            F.ln(xx + fw, yg + 3.5, xx + fw + gap, yg + 3.5, '#4a7d4a', 1.6, '1.6 1')
            s_['yarik'].append((xx + fw + gap / 2, yg + 3.5))
        xx += fw + gap; j += 1
    if ef:
        x0, x1 = x + ef[0] * w, x + ef[1] * w
        F.r(x0, yg, x1 - x0, hf - 2, POD, POD_K, 1.1, 4)
        if o.get('mikrovillus'):
            for xv in range(int(x0 + 6), int(x1 - 4), 10): F.r(xv, yf - 2, 4, 12, POD, POD_K, .9, 2)
    # birincil uzantı ve podosit gövdesi
    F.r(x, yf, w, 12, POD, POD_K, 1.2, 6)
    if ef:
        F.r(x + ef[0] * w, yg + hf - 3, (ef[1] - ef[0]) * w, 6, POD, None, rx=0)
    py = yf + 12 + 16
    pc = o.get('podosit_x', .5)
    elips(F, x + w * pc, py, 46, 20, 0, POD, POD_K, 1.4)
    F.r(x + w * pc - 46, yf + 4, 92, 12, POD, None, rx=0)
    elips(F, x + w * pc, py + 2, 20, 11, 0, POD_N, POD_NK, 1)
    if o.get('vakuol'):
        for (dx, dy, r_) in ((-30, -4, 5), (28, 2, 4.2), (-14, 8, 3.4), (34, -8, 3)):
            F.el(x + w * pc + dx, py + dy, r_, r_, '#fffdf6', POD_K, .8)
    s_['pod'] = (x + w * pc, py)
    # birikimler
    for (tur, xs) in o.get('birikim', ()):
        for xv in xs:
            X = x + xv * w
            if tur == 'subepi': elips(F, X, yg + 4, 8, 5.5, 0, DEP, '#fff', .8)
            elif tur == 'subendo': elips(F, X, ye + 4, 9, 4.5, 0, DEP, '#fff', .8)
            elif tur == 'intra': elips(F, X, ye + hg / 2, 10, hg * .32, 0, DEP)
    # sızıntı
    if o.get('protein'):
        rng = random.Random(3)
        for j in range(18): F.el(x + rng.uniform(5, w - 5), y + rng.uniform(5, yl - y - 8), 2, 2, '#3c7dbf')
        for xv in o['protein']:
            X = x + xv * w
            for (dy, dx) in ((6, 0), (hg * .5 + 9, 3), (yf - ye + 12, -2), (yf - ye + 40, 4)): F.el(X + dx, ye + dy - 6, 2.2, 2.2, '#3c7dbf')
    if o.get('rbc_gecis') is not None:
        X = x + o['rbc_gecis'] * w
        F.r(X - 6, ye - 1, 12, hg + 2, BOW, None, rx=0)
        eritrosit(F, X, ye + hg / 2, 11, 90)
    s_['x'] = x; s_['w'] = w
    return s_


# =================================================================================================== KÜÇÜK GLOMERÜL + BÜYÜTME
def mini_glomerul(F, cx, cy, R=32, vp=-135, up=45, etiket=True, fs=10.5):
    """Kaba tüm glomerül: Bowman kapsülü, yumak, vasküler kutupta afferent/efferent arteriyol, tübüler kutupta proksimal tübül."""
    c0 = (cx, cy)
    # proksimal tübül (tübüler kutup)
    ux, uy = math.cos(math.radians(up)), math.sin(math.radians(up)); nx, ny = -uy, ux
    b = P(c0, R * .92, up); L = R * 1.15; tw = R * .3
    for sg in (-1, 1):
        x0, y0 = b[0] + nx * sg * tw, b[1] + ny * sg * tw
        F.ln(x0, y0, x0 + ux * L, y0 + uy * L, TUB_K, R * .22 + 1.6, cap='butt'); F.ln(x0, y0, x0 + ux * L, y0 + uy * L, TUB, R * .22, cap='butt')
    F.ln(b[0], b[1], b[0] + ux * L, b[1] + uy * L, BOW, 2 * tw - R * .22 - 1.6, cap='butt')
    for t in (.35, .7, 1.0):
        for sg in (-1, 1):
            q = (b[0] + ux * L * t + nx * sg * tw, b[1] + uy * L * t + ny * sg * tw); F.el(q[0], q[1], R * .045, R * .045, TUB_N)
    # kapsül
    F.el(cx, cy, R, R, BOW)
    acik = 21
    pts = [P(c0, R, up + acik + (360 - 2 * acik) * i / 60) for i in range(61)]
    F.yol(_pd(pts, False), GBM_K, 2.2); F.yol(_pd([P(c0, R - 1.8, up + acik + (360 - 2 * acik) * i / 60) for i in range(61)], False), POD, 1.6)
    # arteriyoller (vasküler kutup)
    vu, vv = math.cos(math.radians(vp)), math.sin(math.radians(vp)); vn = (-vv, vu)
    h = P(c0, R * .9, vp); ic0 = P(c0, R * .35, vp)
    uc = {}
    for (sg, gw, ad) in ((1, R * .19, 'af'), (-1, R * .14, 'ef')):
        st = (h[0] + vn[0] * sg * R * .16, h[1] + vn[1] * sg * R * .16)
        en = (st[0] + vu * R * .55 + vn[0] * sg * R * .3, st[1] + vv * R * .55 + vn[1] * sg * R * .3)
        d = f'M{ic0[0]:.1f},{ic0[1]:.1f} Q{st[0]:.1f},{st[1]:.1f} {en[0]:.1f},{en[1]:.1f}'
        F.yol(d, '#9e2b25', gw + 1.6); F.yol(d, '#d9534f', gw); F.yol(d, '#f7c4c0', gw * .4)
        uc[ad] = (en, sg)
    # yumak
    rng = random.Random(21)
    for (x, y, r) in _YUMAK:
        cr, sr = math.cos(math.radians(vp + 90)), math.sin(math.radians(vp + 90))
        X, Y = (x * cr - y * sr) * R * .66, (x * sr + y * cr) * R * .66
        F.el(cx + X, cy + Y, r * R * .66 * 1.32, r * R * .66 * 1.32, POD, POD_K, .7)
    for (x, y, r) in _YUMAK:
        cr, sr = math.cos(math.radians(vp + 90)), math.sin(math.radians(vp + 90))
        X, Y = (x * cr - y * sr) * R * .66, (x * sr + y * cr) * R * .66
        F.el(cx + X, cy + Y, r * R * .66 * 1.05, r * R * .66 * 1.05, '#f3b9b6', '#c95c58', .7)
    if etiket:
        for ad, ytxt in (('af', 'afferent'), ('ef', 'efferent')):
            en, sg = uc[ad]
            # metni arteriyolün dış yanına koy
            q = (en[0] + vn[0] * sg * 6, en[1] + vn[1] * sg * 6)
            anc = 'end' if q[0] < cx - 2 else ('start' if q[0] > cx + 2 else 'middle')
            F.t(q[0], q[1] + 4, ytxt, fs, 700, '#9e2b25', anc)
        te = (b[0] + ux * L, b[1] + uy * L)
        if ux < -.3: F.t(te[0] - 18, te[1] + 19, 'proksimal tübül', fs, 700, TUB_K)
        else: F.t(te[0] + ux * 6, te[1] + uy * 6 + 10, 'proksimal tübül', fs, 700, TUB_K, 'start' if ux > .3 else 'middle')
    return dict(c=c0, R=R, vp=P(c0, R, vp), up=P(c0, R, up))


def yakinlastir(F, mg, hedef, hr, kutu_a=0, kutu_f=.42, kutu_s=None):
    """Küçük glomerül üzerindeki kareden büyütülmüş lobüle iki kılavuz çizgisi. hedef: lobül merkezi, hr: lobül yarıçapı."""
    c0, R = mg['c'], mg['R']
    k = P(c0, R * kutu_f, kutu_a); s = kutu_s or R * .36
    a = math.degrees(math.atan2(k[1] - hedef[1], k[0] - hedef[0]))
    sagda = hedef[0] > k[0]
    kx = k[0] + (s / 2 if sagda else -s / 2)
    for sg in (-1, 1):
        q = P(hedef, hr, a - sg * 13 * (1 if sagda else -1))
        F.ln(kx, k[1] + sg * s / 2, q[0], q[1], '#1d7a7a', 1.1, '4 3')
    F.r(k[0] - s / 2, k[1] - s / 2, s, s, 'none', '#1d7a7a', 1.8, 2)


# =================================================================================================== İMMÜNFLORESAN PATERNİ
IF_Y = '#79f08b'


def if_patern(F, cx, cy, R, tip, renk=IF_Y, baslik=None, alt=None, fs=12, resim=None):
    """Karanlık zeminde floresan glomerül paterni. tip: mez · ince · lineer · kaba · yildiz · mez_kap · negatif.
    resim: gorsel/an_<resim>.webp (ChatGPT ile çizilmiş floresan glomerül, kare) — verilirse vektör desen yerine çizilir."""
    fid = f'{F.fid}g{len(F.p)}'
    if resim:
        x0, s_ = cx - R * 1.14, R * 2.28
        F.a(f'<clipPath id="{fid}k"><rect x="{x0:.1f}" y="{cy - R * 1.14:.1f}" width="{s_:.1f}" height="{s_:.1f}" rx="10"/></clipPath>'
            f'<rect x="{x0:.1f}" y="{cy - R * 1.14:.1f}" width="{s_:.1f}" height="{s_:.1f}" rx="10" fill="#000"/>'
            f'<image href="/dersler/nefroloji-ders-serisi/gorsel/an_{resim}.webp" x="{x0:.1f}" y="{cy - R * 1.14:.1f}" width="{s_:.1f}" height="{s_:.1f}" clip-path="url(#{fid}k)"/>')
        if baslik: F.t(cx, cy + R * 1.14 + 17, baslik, fs + .5, 800, INK, 'middle')
        for i, l in enumerate((alt if isinstance(alt, list) else [alt]) if alt else []):
            F.t(cx, cy + R * 1.14 + 17 + (i + 1) * (fs + 3), l, fs - .5, None, INK2, 'middle')
        return
    F.a(f'<defs><filter id="{fid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="1.1"/></filter></defs>')
    F.r(cx - R * 1.14, cy - R * 1.14, R * 2.28, R * 2.28, '#08110b', None, rx=10)
    F.el(cx, cy, R * 1.02, R * 1.02, 'none', '#1d3324', 1.4)
    ld = [(cx + x * R * .82, cy + y * R * .82, r * R * .82) for (x, y, r) in _YUMAK]
    for (x, y, r) in ld: F.el(x, y, r * 1.08, r * 1.08, 'none', '#16281b', 1)
    rng = random.Random(len(F.p) + 3)
    g = []
    def nokta(x, y, rr, op=.95): g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.2f}" fill="{renk}" opacity="{op}"/>')
    if tip in ('mez', 'mez_kap', 'yildiz'):
        for i in range(len(ld)):
            for j in range(i + 1, len(ld)):
                (x1, y1, r1), (x2, y2, r2) = ld[i], ld[j]
                if math.hypot(x1 - x2, y1 - y2) < R * .5:
                    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                    n_ = 4 if tip != 'yildiz' else 1
                    for _ in range(n_): nokta(mx + rng.uniform(-R * .05, R * .05), my + rng.uniform(-R * .05, R * .05), rng.uniform(R * .018, R * .035) * (1.2 if tip == 'mez' else 1))
    if tip in ('ince', 'lineer', 'kaba', 'yildiz', 'mez_kap'):
        for (x, y, r) in ld:
            rr = r * 1.06
            if tip == 'lineer':
                g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="none" stroke="{renk}" stroke-width="{max(1.4, R * .022):.2f}" opacity=".95"/>')
                continue
            n = {'ince': 26, 'kaba': 9, 'yildiz': 5, 'mez_kap': 8}[tip]
            for t in range(n):
                a = 360 * t / n + rng.uniform(-6, 6)
                q = P((x, y), rr, a)
                if tip == 'ince': nokta(q[0], q[1], max(.8, R * .011))
                elif tip == 'kaba': elips(F, 0, 0, 0, 0); g.append(f'<ellipse cx="{q[0]:.1f}" cy="{q[1]:.1f}" rx="{R * .042:.1f}" ry="{R * .026:.1f}" transform="rotate({a + 90:.0f} {q[0]:.1f} {q[1]:.1f})" fill="{renk}" opacity=".95"/>')
                else:
                    if rng.random() < .7: nokta(q[0], q[1], rng.uniform(R * .014, R * .03))
    F.a(f'<g filter="url(#{fid})">' + ''.join(g) + '</g>')
    F.a('<g>' + ''.join(g) + '</g>')
    if baslik: F.t(cx, cy + R * 1.14 + 17, baslik, fs + .5, 800, INK, 'middle')
    if alt:
        for i, l in enumerate(alt if isinstance(alt, list) else [alt]):
            F.t(cx, cy + R * 1.14 + 17 + (i + 1) * (fs + 3), l, fs - .5, None, INK2, 'middle')


# =================================================================================================== TÜBÜL KESİTİ
def tubul_kesit(F, cx, cy, r=26, atrofik=False):
    if not atrofik:
        F.el(cx, cy, r + 2, r + 2, 'none', '#7fa9b7', 1.4)
        for t in range(12):
            a0, a1 = t * 30, t * 30 + 30
            p0, p1, p2, p3 = P((cx, cy), r, a0), P((cx, cy), r, a1), P((cx, cy), r * .45, a1), P((cx, cy), r * .45, a0)
            F.a(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} L{p3[0]:.1f},{p3[1]:.1f} Z" fill="{TUB}" stroke="{TUB_K}" stroke-width=".8"/>')
            q = P((cx, cy), r * .76, a0 + 15); F.el(q[0], q[1], r * .09, r * .09, TUB_N)
        F.el(cx, cy, r * .42, r * .42, BOW)
    else:
        rr = r * .72
        pts = [P((cx, cy), rr * (1 + .07 * math.sin(5 * t * math.pi / 18)), t * 10) for t in range(36)]
        F.yol(_pd(pts), '#6f97a6', 4.2, '#eef3f5')
        for t in range(8):
            q = P((cx, cy), rr * .72, t * 45 + 10); elips(F, q[0], q[1], r * .13, r * .06, t * 45 + 100, TUB_N)
        F.el(cx, cy, rr * .35, rr * .35, '#fbfbf6', '#c9d6dc', .8)
